from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

import numpy as np
import pandas as pd
from scipy import stats

from raw_ww_data_importer import RawDataImporter

DEFAULT_PAIRING_DECIMALS = 2
DEFAULT_MIN_IQ_REL = 0.10
DEFAULT_HIGH_IQ_REL = 0.85


@dataclass(frozen=True)
class MeasurementSlice:
    """One speed/temperature slice reduced to one row per operating point."""

    operating_points: pd.DataFrame
    stator_resistance: float
    pole_pairs: int
    rpm: float
    rotor_temperature: float

    @property
    def omega_e(self) -> float:
        return 2 * np.pi * self.pole_pairs * self.rpm / 60


@dataclass(frozen=True)
class ResistanceEstimate:
    """Robust constant-resistance hypothesis over a selected high-|iq| region."""

    lower_relative_iq: float
    n_points: int
    delta_R_eq_median: float
    delta_R_eq_mean: float
    delta_R_eq_std: float
    delta_R_eq_mad: float
    resistance_equivalent: float


def _mode(values: np.ndarray) -> float:
    return float(stats.mode(values, keepdims=False).mode)


def get_breakpoints(
    raw: RawDataImporter,
) -> tuple[np.ndarray, np.ndarray]:
    """Return requested speed and rotor-temperature breakpoints."""
    rpm_breakpoints = np.unique(raw.get_signal("PE_Rpm_req"))
    rotor_temp_breakpoints = np.unique(raw.get_signal("Rotor_temp_ref"))
    return rpm_breakpoints, rotor_temp_breakpoints


def build_ww_measurement_slice(
    raw: RawDataImporter,
    rpm: float,
    rotor_temperature: float,
) -> MeasurementSlice:
    """
    Build one measurement slice from the WW raw format.

    Requested speed and rotor-temperature reference select the measurement block.
    Measured averaged currents and voltages are used for the electrical model.
    """
    rpm_req = raw.get_signal("PE_Rpm_req")
    rotor_temp_ref = raw.get_signal("Rotor_temp_ref")

    mask = np.isclose(rpm_req, rpm) & np.isclose(rotor_temp_ref, rotor_temperature)

    if not np.any(mask):
        raise ValueError(
            "No samples found for "
            f"rpm={rpm} and rotor_temperature={rotor_temperature}."
        )

    samples = pd.DataFrame(
        {
            "op_index": raw.get_signal("PE_Index_Flx_Char_StatorCurrent_OP_param_none")[
                mask
            ],
            "id_req": raw.get_signal("PE_Id_req_meas")[mask],
            "iq_req": raw.get_signal("PE_Iq_req_meas")[mask],
            "id": raw.get_signal("PE_Id_meas_avg")[mask],
            "iq": raw.get_signal("PE_Iq_meas_avg")[mask],
            "ud": raw.get_signal("PE_Ud_meas_avg")[mask],
            "uq": raw.get_signal("PE_Uq_meas_avg")[mask],
        }
    )

    stator_resistance = _mode(raw.get_signal("Const_Machine_R_s")[mask])

    pole_pairs = int(_mode(raw.get_signal("Const_Machine_pole_pairs")[mask]))

    operating_points = samples.groupby("op_index", as_index=False).mean()

    return MeasurementSlice(
        operating_points=operating_points,
        stator_resistance=stator_resistance,
        pole_pairs=pole_pairs,
        rpm=float(rpm),
        rotor_temperature=float(rotor_temperature),
    )


class FluxMapSymmetryAnalyzer:
    """
    Academic analysis of symmetry residuals in reconstructed dq flux maps.

    The class deliberately does not decide whether a residual is truly caused by
    stator resistance.  delta_R_eq is a resistance-equivalent residual:
    if a constant stator-resistance mismatch were the only error source, it
    would be approximately constant over the operating region.
    """

    def __init__(
        self,
        measurement: MeasurementSlice,
        pairing_decimals: int = DEFAULT_PAIRING_DECIMALS,
        min_iq_rel: float = DEFAULT_MIN_IQ_REL,
    ):
        if not 0 <= min_iq_rel < 1:
            raise ValueError("min_iq_rel must satisfy 0 <= min_iq_rel < 1.")

        self.measurement = measurement
        self.pairing_decimals = pairing_decimals
        self.min_iq_rel = min_iq_rel

    @property
    def omega_e(self) -> float:
        return self.measurement.omega_e

    @property
    def stator_resistance(self) -> float:
        return self.measurement.stator_resistance

    @cached_property
    def flux_points(self) -> pd.DataFrame:
        """Operating points with reconstructed psi_d and psi_q."""
        points = self.measurement.operating_points.copy()

        i_d = points["id"].to_numpy()
        i_q = points["iq"].to_numpy()
        u_d = points["ud"].to_numpy()
        u_q = points["uq"].to_numpy()

        Rs = self.stator_resistance
        omega_e = self.omega_e

        points["psi_d"] = (u_q - Rs * i_q) / omega_e
        points["psi_q"] = (Rs * i_d - u_d) / omega_e

        return points

    @cached_property
    def symmetric_pairs(self) -> pd.DataFrame:
        """
        Pair measured +iq/-iq operating points and calculate forbidden symmetry
        components and the resistance-equivalent residual.
        """
        points = self.flux_points.copy()

        # Pairing coordinates only; measured physical values are not rounded.
        points["id_key"] = points["id_req"].round(self.pairing_decimals)
        points["iq_key"] = points["iq_req"].round(self.pairing_decimals)

        # Repeated requested operating points are repeated observations of the
        # same geometric point.  Collapse them before symmetry pairing.
        points = points.groupby(["id_key", "iq_key"], as_index=False).mean(
            numeric_only=True
        )

        positive = points[points["iq_key"] > 0].copy()
        negative = points[points["iq_key"] < 0].copy()

        # Give +iq and -iq the same positive pairing key.
        negative["iq_key"] = -negative["iq_key"]

        pairs = positive.merge(
            negative,
            on=["id_key", "iq_key"],
            suffixes=("_pos", "_neg"),
            validate="one_to_one",
        )

        # Forbidden symmetry components:
        # ideal symmetric map -> r_d = 0 and r_q = 0.
        pairs["r_d"] = (pairs["psi_d_pos"] - pairs["psi_d_neg"]) / 2

        pairs["r_q"] = (pairs["psi_q_pos"] + pairs["psi_q_neg"]) / 2

        # Physical current magnitude of the measured pair.
        pairs["iq_mag"] = (np.abs(pairs["iq_pos"]) + np.abs(pairs["iq_neg"])) / 2

        iq_threshold = self.min_iq_rel * pairs["iq_mag"].max()
        pairs["valid_delta_R_eq"] = pairs["iq_mag"] > iq_threshold

        valid = pairs["valid_delta_R_eq"]

        # Convention:
        # epsilon_R = R_used - R_true
        #
        # For a pure constant resistance mismatch:
        # r_d = -(epsilon_R / omega_e) * |iq|
        #
        # Therefore delta_R_eq equals epsilon_R only under that hypothesis.
        pairs.loc[valid, "delta_R_eq"] = (
            -self.omega_e * pairs.loc[valid, "r_d"] / pairs.loc[valid, "iq_mag"]
        )

        return pairs

    def estimate_high_current_resistance(
        self,
        lower_relative_iq: float = DEFAULT_HIGH_IQ_REL,
    ) -> ResistanceEstimate:
        """
        Robustly summarize delta_R_eq in a high-|iq| region.

        This is a hypothesis summary, not proof that the residual is caused by
        physical stator resistance.
        """
        if not 0 <= lower_relative_iq < 1:
            raise ValueError("lower_relative_iq must satisfy 0 <= value < 1.")

        pairs = self.symmetric_pairs[self.symmetric_pairs["valid_delta_R_eq"]].copy()

        iq_limit = lower_relative_iq * pairs["iq_mag"].max()
        high_current = pairs[pairs["iq_mag"] >= iq_limit]

        delta_R = high_current["delta_R_eq"].dropna()

        if delta_R.empty:
            raise ValueError(
                "No valid symmetric pairs in the requested high-current region."
            )

        median = float(delta_R.median())
        mean = float(delta_R.mean())
        std = float(delta_R.std())
        mad = float(np.median(np.abs(delta_R - median)))

        return ResistanceEstimate(
            lower_relative_iq=lower_relative_iq,
            n_points=len(delta_R),
            delta_R_eq_median=median,
            delta_R_eq_mean=mean,
            delta_R_eq_std=std,
            delta_R_eq_mad=mad,
            resistance_equivalent=self.stator_resistance - median,
        )

    def symmetry_metrics(self) -> dict[str, float]:
        pairs = self.symmetric_pairs
        return {
            "r_d_rms": float(np.sqrt(np.mean(pairs["r_d"] ** 2))),
            "r_q_rms": float(np.sqrt(np.mean(pairs["r_q"] ** 2))),
            "r_d_median_abs": float(np.median(np.abs(pairs["r_d"]))),
            "r_q_median_abs": float(np.median(np.abs(pairs["r_q"]))),
        }

    def with_stator_resistance(
        self,
        stator_resistance: float,
    ) -> "FluxMapSymmetryAnalyzer":
        """Return a fresh analysis using another resistance hypothesis."""
        measurement = MeasurementSlice(
            operating_points=self.measurement.operating_points.copy(),
            stator_resistance=float(stator_resistance),
            pole_pairs=self.measurement.pole_pairs,
            rpm=self.measurement.rpm,
            rotor_temperature=self.measurement.rotor_temperature,
        )

        return FluxMapSymmetryAnalyzer(
            measurement,
            pairing_decimals=self.pairing_decimals,
            min_iq_rel=self.min_iq_rel,
        )
