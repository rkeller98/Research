import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from scipy import stats

from raw_ww_data_importer import RawDataImporter


FILE_PATH = r"C:\Git\Publications\sandbox\WW_Dataset_Outlier.mat"

PAIRING_DECIMALS = 2
IQ_THRESHOLD_REL = 0.1
PLOT = True


def build_operating_points(raw: RawDataImporter) -> tuple[pd.DataFrame, float, int, float]:
    # Select one speed / rotor-temperature slice
    rpm_req = raw.get_signal("PE_Rpm_req")
    rotor_temp_ref = raw.get_signal("Rotor_temp_ref")

    rpm_bp = np.unique(rpm_req)[0]
    rotor_temp_bp = np.unique(rotor_temp_ref)[1]

    mask = (
        np.isclose(rpm_req, rpm_bp)
        & np.isclose(rotor_temp_ref, rotor_temp_bp)
    )

    # Signals used for one operating point
    samples = pd.DataFrame({
        "op_index": raw.get_signal(
            "PE_Index_Flx_Char_StatorCurrent_OP_param_none"
        )[mask],
        "id_req": raw.get_signal("PE_Id_req_meas")[mask],
        "iq_req": raw.get_signal("PE_Iq_req_meas")[mask],
        "id": raw.get_signal("PE_Id_meas_avg")[mask],
        "iq": raw.get_signal("PE_Iq_meas_avg")[mask],
        "ud": raw.get_signal("PE_Ud_meas_avg")[mask],
        "uq": raw.get_signal("PE_Uq_meas_avg")[mask],
    })

    # Constants
    Rs = float(
        stats.mode(
            raw.get_signal("Const_Machine_R_s")[mask]
        ).mode
    )

    pole_pairs = int(
        stats.mode(
            raw.get_signal("Const_Machine_pole_pairs")[mask]
        ).mode
    )

    # Multiple samples -> one averaged operating point
    operating_points = (
        samples
        .groupby("op_index", as_index=False)
        .mean()
    )

    return operating_points, Rs, pole_pairs, rpm_bp


def calculate_flux(
    operating_points: pd.DataFrame,
    Rs: float,
    pole_pairs: int,
    rpm: float,
) -> tuple[np.ndarray, np.ndarray]:
    omega_e = 2 * np.pi * pole_pairs * rpm / 60

    i_d = operating_points["id"].to_numpy()
    i_q = operating_points["iq"].to_numpy()
    u_d = operating_points["ud"].to_numpy()
    u_q = operating_points["uq"].to_numpy()

    psi_d = (u_q - Rs * i_q) / omega_e
    psi_q = (Rs * i_d - u_d) / omega_e

    return psi_d, psi_q


def build_symmetric_pairs(
    operating_points: pd.DataFrame,
    omega_e: float,
) -> pd.DataFrame:
    points = operating_points.copy()

    # Pairing coordinates only.
    # Physical measured quantities are NOT rounded.
    points["id_key"] = points["id_req"].round(PAIRING_DECIMALS)
    points["iq_key"] = points["iq_req"].round(PAIRING_DECIMALS)

    # Some requested operating points were measured multiple times.
    # Collapse repetitions to one representative point.
    points = (
        points
        .groupby(["id_key", "iq_key"], as_index=False)
        .mean(numeric_only=True)
    )

    positive = points[points["iq_key"] > 0].copy()
    negative = points[points["iq_key"] < 0].copy()

    # (-iq) and (+iq) shall have the same pairing key.
    negative["iq_key"] = -negative["iq_key"]

    pairs = positive.merge(
        negative,
        on=["id_key", "iq_key"],
        suffixes=("_pos", "_neg"),
        validate="one_to_one",
    )

    # Forbidden symmetry components
    pairs["r_d"] = (
        pairs["psi_d_pos"] - pairs["psi_d_neg"]
    ) / 2

    pairs["r_q"] = (
        pairs["psi_q_pos"] + pairs["psi_q_neg"]
    ) / 2

    # Exclude small |iq| because division by iq becomes sensitive there.
    iq_threshold = IQ_THRESHOLD_REL * pairs["iq_key"].max()

    pairs["evaluate"] = pairs["iq_key"] > iq_threshold

    # Convention:
    # delta_R = R_used - R_true
    pairs.loc[pairs["evaluate"], "delta_R"] = (
        -omega_e
        * pairs.loc[pairs["evaluate"], "r_d"]
        / pairs.loc[pairs["evaluate"], "iq_key"]
    )

    return pairs


def plot_flux_maps(operating_points: pd.DataFrame) -> None:
    i_d = operating_points["id"].to_numpy()
    i_q = operating_points["iq"].to_numpy()
    psi_d = operating_points["psi_d"].to_numpy()
    psi_q = operating_points["psi_q"].to_numpy()

    tri = mtri.Triangulation(i_d, i_q)

    fig = plt.figure(figsize=(12, 10))

    ax = fig.add_subplot(121, projection="3d")
    ax.plot_trisurf(tri, psi_d, alpha=0.8)
    ax.scatter(i_d, i_q, psi_d, s=0.5, c="black")
    ax.set_xlabel(r"$i_d$")
    ax.set_ylabel(r"$i_q$")
    ax.set_zlabel(r"$\psi_d$")

    ax = fig.add_subplot(122, projection="3d")
    ax.plot_trisurf(tri, psi_q, alpha=0.8)
    ax.scatter(i_d, i_q, psi_q, s=0.5, c="black")
    ax.set_xlabel(r"$i_d$")
    ax.set_ylabel(r"$i_q$")
    ax.set_zlabel(r"$\psi_q$")


def plot_resistance_estimate(pairs: pd.DataFrame) -> None:
    evaluated = pairs[pairs["evaluate"]].copy()
    evaluated["delta_R_mOhm"] = 1e3 * evaluated["delta_R"]

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    ax.scatter(
        evaluated["id_key"],
        evaluated["iq_key"],
        evaluated["delta_R_mOhm"],
        s=4,
    )

    ax.set_xlabel(r"$i_d$")
    ax.set_ylabel(r"$|i_q|$")
    ax.set_zlabel(r"$\Delta R_s$ / m$\Omega$")


if __name__ == "__main__":
    raw = RawDataImporter(FILE_PATH)

    operating_points, Rs, pole_pairs, rpm = build_operating_points(raw)

    omega_e = 2 * np.pi * pole_pairs * rpm / 60

    psi_d, psi_q = calculate_flux(
        operating_points,
        Rs,
        pole_pairs,
        rpm,
    )

    operating_points["psi_d"] = psi_d
    operating_points["psi_q"] = psi_q

    pairs = build_symmetric_pairs(
        operating_points,
        omega_e,
    )

    evaluated = pairs[pairs["evaluate"]]

    delta_R_median = evaluated["delta_R"].median()
    Rs_estimated = Rs - delta_R_median

    print(f"RPM:              {rpm:.0f}")
    print(f"Pole pairs:       {pole_pairs}")
    print(f"Operating points: {len(operating_points)}")
    print(f"Symmetric pairs:  {len(pairs)}")
    print()
    print(f"Rs used:          {Rs * 1e3:.3f} mOhm")
    print(f"Delta Rs median:  {delta_R_median * 1e3:.3f} mOhm")
    print(f"Rs estimated:     {Rs_estimated * 1e3:.3f} mOhm")

    if PLOT:
        plot_flux_maps(operating_points)
        plot_resistance_estimate(pairs)
        plt.show()