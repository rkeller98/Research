from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np
import pandas as pd
from scipy.interpolate import LinearNDInterpolator
from scipy.spatial import Delaunay

from raw_ww_data_importer import RawDataImporter
from flux_correction import (
    FluxMapSymmetryAnalyzer,
    build_ww_measurement_slice,
    get_breakpoints,
)

FILE_PATH = Path(__file__).resolve().parent / "WW_Dataset_Outlier.mat"

PAIRING_DECIMALS = 2
N_INTEGRATION_POINTS = 500

ID_THRESHOLD_REL = 0.10
IQ_THRESHOLD_REL = 0.10


def prepare_points(
    analyzer: FluxMapSymmetryAnalyzer,
) -> pd.DataFrame:
    points = analyzer.flux_points.copy()

    # Requested currents are used only to identify repeated operating points.
    points["id_key"] = points["id_req"].round(PAIRING_DECIMALS)
    points["iq_key"] = points["iq_req"].round(PAIRING_DECIMALS)

    # Repeated measurements -> one representative point.
    points = points.groupby(["id_key", "iq_key"], as_index=False).mean(
        numeric_only=True
    )

    return points


def build_flux_interpolators(
    points: pd.DataFrame,
) -> tuple[LinearNDInterpolator, LinearNDInterpolator]:
    # Magnetic field coordinates are the actually measured currents.
    coordinates = points[["id", "iq"]].to_numpy()

    triangulation = Delaunay(coordinates)

    psi_d_interp = LinearNDInterpolator(
        triangulation,
        points["psi_d"].to_numpy(),
    )

    psi_q_interp = LinearNDInterpolator(
        triangulation,
        points["psi_q"].to_numpy(),
    )

    return psi_d_interp, psi_q_interp


def integrate_segment(
    psi_d_interp: LinearNDInterpolator,
    psi_q_interp: LinearNDInterpolator,
    start: tuple[float, float],
    end: tuple[float, float],
) -> float:
    """
    Integrate

        dW' = psi_d di_d + psi_q di_q

    along one straight segment.
    """

    t = np.linspace(
        0.0,
        1.0,
        N_INTEGRATION_POINTS,
    )

    id_start, iq_start = start
    id_end, iq_end = end

    delta_id = id_end - id_start
    delta_iq = iq_end - iq_start

    id_path = id_start + t * delta_id
    iq_path = iq_start + t * delta_iq

    psi_d = psi_d_interp(id_path, iq_path)
    psi_q = psi_q_interp(id_path, iq_path)

    if np.any(np.isnan(psi_d)) or np.any(np.isnan(psi_q)):
        raise ValueError(
            f"Path segment {start} -> {end} leaves "
            "the measured interpolation domain."
        )

    integrand = psi_d * delta_id + psi_q * delta_iq

    return float(
        np.trapezoid(
            integrand,
            t,
        )
    )


def calculate_path_a(
    psi_d_interp: LinearNDInterpolator,
    psi_q_interp: LinearNDInterpolator,
    target_id: float,
    target_iq: float,
) -> float:
    W_1 = integrate_segment(
        psi_d_interp,
        psi_q_interp,
        start=(0.0, 0.0),
        end=(target_id, 0.0),
    )

    W_2 = integrate_segment(
        psi_d_interp,
        psi_q_interp,
        start=(target_id, 0.0),
        end=(target_id, target_iq),
    )

    return W_1 + W_2


def calculate_path_b(
    psi_d_interp: LinearNDInterpolator,
    psi_q_interp: LinearNDInterpolator,
    target_id: float,
    target_iq: float,
) -> float:
    W_1 = integrate_segment(
        psi_d_interp,
        psi_q_interp,
        start=(0.0, 0.0),
        end=(0.0, target_iq),
    )

    W_2 = integrate_segment(
        psi_d_interp,
        psi_q_interp,
        start=(0.0, target_iq),
        end=(target_id, target_iq),
    )

    return W_1 + W_2


def evaluate_target(
    psi_d_interp: LinearNDInterpolator,
    psi_q_interp: LinearNDInterpolator,
    omega_e: float,
    target_id: float,
    target_iq: float,
) -> dict[str, float]:
    W_A = calculate_path_a(
        psi_d_interp,
        psi_q_interp,
        target_id,
        target_iq,
    )

    W_B = calculate_path_b(
        psi_d_interp,
        psi_q_interp,
        target_id,
        target_iq,
    )

    delta_W = W_A - W_B

    reference_W = 0.5 * (abs(W_A) + abs(W_B))

    relative_difference = abs(delta_W) / max(reference_W, 1e-12)

    # Under the pure constant-resistance-error hypothesis:
    #
    #   Delta W = 2 * epsilon_R / omega_e * id * iq
    #
    # therefore
    #
    #   epsilon_R = omega_e * Delta W / (2 * id * iq)
    delta_R_eq_path = omega_e * delta_W / (2 * target_id * target_iq)

    return {
        "W_A": W_A,
        "W_B": W_B,
        "delta_W": delta_W,
        "relative_difference": relative_difference,
        "delta_R_eq_path": delta_R_eq_path,
    }


def calculate_path_resistance_field(
    analyzer: FluxMapSymmetryAnalyzer,
    id_threshold_rel: float = ID_THRESHOLD_REL,
    iq_threshold_rel: float = IQ_THRESHOLD_REL,
) -> pd.DataFrame:
    points = prepare_points(analyzer)

    psi_d_interp, psi_q_interp = build_flux_interpolators(points)

    id_threshold = id_threshold_rel * np.max(np.abs(points["id"]))

    iq_threshold = iq_threshold_rel * np.max(np.abs(points["iq"]))

    results = []
    skipped = 0

    for _, point in points.iterrows():
        target_id = float(point["id"])
        target_iq = float(point["iq"])

        # Avoid poorly conditioned regions near either axis.
        if abs(target_id) <= id_threshold:
            continue

        if abs(target_iq) <= iq_threshold:
            continue

        try:
            result = evaluate_target(
                psi_d_interp,
                psi_q_interp,
                analyzer.omega_e,
                target_id,
                target_iq,
            )

        except ValueError:
            # The target itself may lie inside the domain while one of the
            # rectangular integration paths leaves it.
            skipped += 1
            continue

        # Resistance value that would make this path residual vanish if a
        # scalar stator-resistance mismatch were the sole cause.
        R_eq_path = analyzer.stator_resistance - result["delta_R_eq_path"]

        results.append(
            {
                "id_key": point["id_key"],
                "iq_key": point["iq_key"],
                "id": target_id,
                "iq": target_iq,
                **result,
                "R_eq_path": R_eq_path,
            }
        )

    field = pd.DataFrame(results)

    if field.empty:
        raise ValueError(
            "No valid target points remained after axis exclusion "
            "and interpolation-domain checks."
        )

    print(
        f"Path field: {len(field)} valid targets, "
        f"{skipped} skipped because a rectangular path left the domain."
    )

    return field


def mad(
    values: pd.Series,
) -> float:
    median = values.median()

    return float(np.median(np.abs(values - median)))


def print_field_summary(
    name: str,
    analyzer: FluxMapSymmetryAnalyzer,
    field: pd.DataFrame,
) -> None:
    delta_R = field["delta_R_eq_path"]
    R_eq_path = field["R_eq_path"]
    relative = field["relative_difference"]

    print(f"\n--- {name} ---")

    print(f"Rs used:                  " f"{analyzer.stator_resistance * 1e3:.3f} mOhm")

    print(f"Valid path targets:        " f"{len(field)}")

    print(f"Median path difference:    " f"{100 * relative.median():.3f} %")

    print(f"Delta R_eq,path median:    " f"{1e3 * delta_R.median():.3f} mOhm")

    print(f"Delta R_eq,path MAD:       " f"{1e3 * mad(delta_R):.3f} mOhm")

    print(f"R_eq,path median:          " f"{1e3 * R_eq_path.median():.3f} mOhm")

    print(f"R_eq,path MAD:             " f"{1e3 * mad(R_eq_path):.3f} mOhm")


def compare_fields(
    raw_field: pd.DataFrame,
    corrected_field: pd.DataFrame,
) -> pd.DataFrame:
    comparison = raw_field.merge(
        corrected_field,
        on=["id_key", "iq_key"],
        suffixes=("_raw", "_corrected"),
        validate="one_to_one",
    )

    comparison["delta_R_eq_path_shift"] = (
        comparison["delta_R_eq_path_corrected"] - comparison["delta_R_eq_path_raw"]
    )

    comparison["R_eq_path_shift"] = (
        comparison["R_eq_path_corrected"] - comparison["R_eq_path_raw"]
    )

    comparison["path_difference_change"] = (
        comparison["relative_difference_corrected"]
        - comparison["relative_difference_raw"]
    )

    return comparison


def plot_resistance_fields(
    raw_field: pd.DataFrame,
    corrected_field: pd.DataFrame,
) -> None:
    fig = plt.figure(figsize=(12, 6))

    ax = fig.add_subplot(
        121,
        projection="3d",
    )

    ax.scatter(
        raw_field["id"],
        raw_field["iq"],
        1e3 * raw_field["delta_R_eq_path"],
        s=5,
    )

    ax.set_xlabel(r"$i_d$")
    ax.set_ylabel(r"$i_q$")
    ax.set_zlabel(r"$\Delta R_{\mathrm{eq,path}}$ / m$\Omega$")
    ax.set_title("Raw field")

    ax = fig.add_subplot(
        122,
        projection="3d",
    )

    ax.scatter(
        corrected_field["id"],
        corrected_field["iq"],
        1e3 * corrected_field["delta_R_eq_path"],
        s=5,
    )

    ax.set_xlabel(r"$i_d$")
    ax.set_ylabel(r"$i_q$")
    ax.set_zlabel(r"$\Delta R_{\mathrm{eq,path}}$ / m$\Omega$")
    ax.set_title("Symmetry-corrected field")


def plot_path_equivalent_resistance_fields(
    raw_field: pd.DataFrame,
    corrected_field: pd.DataFrame,
) -> None:
    comparison = compare_fields(
        raw_field,
        corrected_field,
    )

    fig = plt.figure(figsize=(18, 6))

    ax = fig.add_subplot(
        131,
        projection="3d",
    )

    ax.scatter(
        raw_field["id"],
        raw_field["iq"],
        1e3 * raw_field["R_eq_path"],
        s=5,
    )

    ax.set_xlabel(r"$i_d$")
    ax.set_ylabel(r"$i_q$")
    ax.set_zlabel(r"$R_{\mathrm{eq,path}}$ / m$\Omega$")
    ax.set_title("Raw reconstruction")

    ax = fig.add_subplot(
        132,
        projection="3d",
    )

    ax.scatter(
        corrected_field["id"],
        corrected_field["iq"],
        1e3 * corrected_field["R_eq_path"],
        s=5,
    )

    ax.set_xlabel(r"$i_d$")
    ax.set_ylabel(r"$i_q$")
    ax.set_zlabel(r"$R_{\mathrm{eq,path}}$ / m$\Omega$")
    ax.set_title("Symmetry-corrected reconstruction")

    ax = fig.add_subplot(
        133,
        projection="3d",
    )

    ax.scatter(
        comparison["id_raw"],
        comparison["iq_raw"],
        1e3 * comparison["R_eq_path_shift"],
        s=5,
    )

    ax.set_xlabel(r"$i_d$")
    ax.set_ylabel(r"$i_q$")
    ax.set_zlabel(
        r"$R_{\mathrm{eq,path,corr}}" r"-R_{\mathrm{eq,path,raw}}$ / m$\Omega$"
    )
    ax.set_title("Difference")


def plot_path_difference_fields(
    raw_field: pd.DataFrame,
    corrected_field: pd.DataFrame,
) -> None:
    fig = plt.figure(figsize=(12, 6))

    ax = fig.add_subplot(
        121,
        projection="3d",
    )

    ax.scatter(
        raw_field["id"],
        raw_field["iq"],
        100 * raw_field["relative_difference"],
        s=5,
    )

    ax.set_xlabel(r"$i_d$")
    ax.set_ylabel(r"$i_q$")
    ax.set_zlabel("Relative path difference / %")
    ax.set_title("Raw field")

    ax = fig.add_subplot(
        122,
        projection="3d",
    )

    ax.scatter(
        corrected_field["id"],
        corrected_field["iq"],
        100 * corrected_field["relative_difference"],
        s=5,
    )

    ax.set_xlabel(r"$i_d$")
    ax.set_ylabel(r"$i_q$")
    ax.set_zlabel("Relative path difference / %")
    ax.set_title("Symmetry-corrected field")


def plot_field_comparison(
    comparison: pd.DataFrame,
) -> None:
    fig = plt.figure()

    ax = fig.add_subplot(projection="3d")

    ax.scatter(
        comparison["id_raw"],
        comparison["iq_raw"],
        1e3 * comparison["delta_R_eq_path_shift"],
        s=5,
    )

    ax.set_xlabel(r"$i_d$")
    ax.set_ylabel(r"$i_q$")

    ax.set_zlabel(
        r"$\Delta R_{\mathrm{eq,path,corr}}"
        r"-\Delta R_{\mathrm{eq,path,raw}}$ / m$\Omega$"
    )

    ax.set_title("Effect of symmetry-based resistance correction")


def plot_flux_comparison(
    raw_analyzer: FluxMapSymmetryAnalyzer,
    corrected_analyzer: FluxMapSymmetryAnalyzer,
) -> None:
    """
    Plot raw, symmetry-corrected, and difference flux maps.

    One 1x3 figure is created for psi_d and another one for psi_q.
    """
    raw_points = prepare_points(raw_analyzer)
    corrected_points = prepare_points(corrected_analyzer)

    comparison = raw_points[["id_key", "iq_key", "id", "iq", "psi_d", "psi_q"]].merge(
        corrected_points[["id_key", "iq_key", "psi_d", "psi_q"]],
        on=["id_key", "iq_key"],
        suffixes=("_raw", "_corrected"),
        validate="one_to_one",
    )

    comparison["delta_psi_d"] = comparison["psi_d_corrected"] - comparison["psi_d_raw"]

    comparison["delta_psi_q"] = comparison["psi_q_corrected"] - comparison["psi_q_raw"]

    i_d = comparison["id"].to_numpy()
    i_q = comparison["iq"].to_numpy()

    tri = mtri.Triangulation(
        i_d,
        i_q,
    )

    for component, label, delta_label in [
        ("psi_d", r"$\psi_d$", r"$\Delta\psi_d$"),
        ("psi_q", r"$\psi_q$", r"$\Delta\psi_q$"),
    ]:
        raw_values = comparison[f"{component}_raw"].to_numpy()

        corrected_values = comparison[f"{component}_corrected"].to_numpy()

        difference = comparison[f"delta_{component}"].to_numpy()

        fig = plt.figure(figsize=(18, 6))

        fig.suptitle(f"{label}: effect of symmetry-based resistance correction")

        ax = fig.add_subplot(
            131,
            projection="3d",
        )

        ax.plot_trisurf(
            tri,
            raw_values,
            alpha=0.8,
        )

        ax.scatter(
            i_d,
            i_q,
            raw_values,
            s=0.5,
            c="black",
        )

        ax.set_xlabel(r"$i_d$")
        ax.set_ylabel(r"$i_q$")
        ax.set_zlabel(label)
        ax.set_title("Raw")

        ax = fig.add_subplot(
            132,
            projection="3d",
        )

        ax.plot_trisurf(
            tri,
            corrected_values,
            alpha=0.8,
        )

        ax.scatter(
            i_d,
            i_q,
            corrected_values,
            s=0.5,
            c="black",
        )

        ax.set_xlabel(r"$i_d$")
        ax.set_ylabel(r"$i_q$")
        ax.set_zlabel(label)
        ax.set_title("Symmetry corrected")

        ax = fig.add_subplot(
            133,
            projection="3d",
        )

        ax.plot_trisurf(
            tri,
            difference,
            alpha=0.8,
        )

        ax.scatter(
            i_d,
            i_q,
            difference,
            s=0.5,
            c="black",
        )

        ax.set_xlabel(r"$i_d$")
        ax.set_ylabel(r"$i_q$")
        ax.set_zlabel(delta_label)
        ax.set_title("Corrected - raw")


if __name__ == "__main__":
    raw = RawDataImporter(FILE_PATH)

    rpm_breakpoints, temperature_breakpoints = get_breakpoints(raw)

    measurement = build_ww_measurement_slice(
        raw,
        rpm=float(rpm_breakpoints[0]),
        rotor_temperature=float(temperature_breakpoints[1]),
    )

    raw_analyzer = FluxMapSymmetryAnalyzer(measurement)

    # Resistance-equivalent value inferred from the high-|iq| symmetry residual.
    symmetry_estimate = raw_analyzer.estimate_high_current_resistance()

    corrected_analyzer = raw_analyzer.with_stator_resistance(
        symmetry_estimate.resistance_equivalent
    )

    print("=== Symmetry-based resistance hypothesis ===")

    print(
        f"Rs used:                 " f"{raw_analyzer.stator_resistance * 1e3:.3f} mOhm"
    )

    print(
        f"Delta R_eq,sym median:   "
        f"{symmetry_estimate.delta_R_eq_median * 1e3:.3f} mOhm"
    )

    print(
        f"Rs symmetry estimate:    "
        f"{corrected_analyzer.stator_resistance * 1e3:.3f} mOhm"
    )

    print("\nCalculating raw path-resistance field ...")

    raw_field = calculate_path_resistance_field(raw_analyzer)

    print("\nCalculating symmetry-corrected " "path-resistance field ...")

    corrected_field = calculate_path_resistance_field(corrected_analyzer)

    print_field_summary(
        "Raw field",
        raw_analyzer,
        raw_field,
    )

    print_field_summary(
        "Symmetry-corrected field",
        corrected_analyzer,
        corrected_field,
    )

    comparison = compare_fields(
        raw_field,
        corrected_field,
    )

    print("\n--- Raw vs. symmetry-corrected comparison ---")

    print(f"Common path targets:       " f"{len(comparison)}")

    print(
        f"Median Delta R_eq shift:   "
        f"{1e3 * comparison['delta_R_eq_path_shift'].median():.3f} mOhm"
    )

    print(
        f"Median R_eq,path shift:    "
        f"{1e3 * comparison['R_eq_path_shift'].median():.6f} mOhm"
    )

    print(
        f"Median path-diff change:   "
        f"{100 * comparison['path_difference_change'].median():.3f} %-points"
    )

    plot_resistance_fields(
        raw_field,
        corrected_field,
    )

    plot_path_equivalent_resistance_fields(
        raw_field,
        corrected_field,
    )

    plot_path_difference_fields(
        raw_field,
        corrected_field,
    )

    plot_field_comparison(
        comparison,
    )

    # Flux maps: raw -> corrected -> difference.
    plot_flux_comparison(
        raw_analyzer,
        corrected_analyzer,
    )

    plt.show()
