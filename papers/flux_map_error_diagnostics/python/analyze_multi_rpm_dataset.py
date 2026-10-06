from pathlib import Path
import argparse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from raw_ww_data_importer import RawDataImporter
from flux_correction import (
    FluxMapSymmetryAnalyzer,
    build_ww_measurement_slice,
    get_breakpoints,
)

FILE_PATH = Path(__file__).resolve().parent / "WW_Dataset_Multi_RPM.mat"

PLOT = True


def print_summary(
    analyzer: FluxMapSymmetryAnalyzer,
) -> None:
    estimate = analyzer.estimate_high_current_resistance()
    metrics = analyzer.symmetry_metrics()

    print()
    print(f"RPM:                   {analyzer.measurement.rpm:.0f}")
    print("Rotor temperature:     " f"{analyzer.measurement.rotor_temperature:.1f} °C")
    print("Operating points:      " f"{len(analyzer.measurement.operating_points)}")
    print("Symmetric pairs:       " f"{len(analyzer.symmetric_pairs)}")
    print("Rs used:               " f"{analyzer.stator_resistance * 1e3:.3f} mOhm")
    print("Delta R_eq median:     " f"{estimate.delta_R_eq_median * 1e3:.3f} mOhm")
    print("Delta R_eq MAD:        " f"{estimate.delta_R_eq_mad * 1e3:.3f} mOhm")
    print("Resistance equivalent: " f"{estimate.resistance_equivalent * 1e3:.3f} mOhm")
    print("r_d RMS:               " f"{metrics['r_d_rms'] * 1e3:.3f} mWb")
    print("r_q RMS:               " f"{metrics['r_q_rms'] * 1e3:.3f} mWb")


def build_common_speed_comparison(
    analyzers: list[FluxMapSymmetryAnalyzer],
) -> pd.DataFrame:
    """
    Merge exactly matching symmetric current pairs across all speed slices.
    """
    common = None

    for analyzer in analyzers:
        rpm_label = int(round(analyzer.measurement.rpm))

        pairs = analyzer.symmetric_pairs[analyzer.symmetric_pairs["valid_delta_R_eq"]][
            [
                "id_key",
                "iq_key",
                "iq_mag",
                "r_d",
                "r_q",
                "delta_R_eq",
            ]
        ].copy()

        pairs = pairs.rename(
            columns={
                "iq_mag": f"iq_mag_{rpm_label}",
                "r_d": f"r_d_{rpm_label}",
                "r_q": f"r_q_{rpm_label}",
                "delta_R_eq": f"delta_R_eq_{rpm_label}",
            }
        )

        if common is None:
            common = pairs
        else:
            common = common.merge(
                pairs,
                on=["id_key", "iq_key"],
                validate="one_to_one",
            )

    if common is None:
        raise ValueError("No speed slices were supplied.")

    return common


def plot_multi_speed_comparison(
    analyzers: list[FluxMapSymmetryAnalyzer],
    common: pd.DataFrame,
) -> None:
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    for analyzer in analyzers:
        rpm_label = int(round(analyzer.measurement.rpm))
        pairs = analyzer.symmetric_pairs[analyzer.symmetric_pairs["valid_delta_R_eq"]]

        ax.scatter(
            pairs["id_key"],
            pairs["iq_mag"],
            1e3 * pairs["delta_R_eq"],
            s=5,
            label=f"{rpm_label} rpm",
        )

    ax.set_xlabel(r"$i_d$")
    ax.set_ylabel(r"$|i_q|$")
    ax.set_zlabel(r"$\Delta R_{\mathrm{eq}}$ / m$\Omega$")
    ax.legend()

    # If exactly two speed slices are present, also plot their pointwise
    # difference.  A pure constant resistance mismatch should give similar
    # delta_R_eq values at both speeds.
    if len(analyzers) == 2:
        rpm_a = int(round(analyzers[0].measurement.rpm))
        rpm_b = int(round(analyzers[1].measurement.rpm))

        col_a = f"delta_R_eq_{rpm_a}"
        col_b = f"delta_R_eq_{rpm_b}"

        difference = common[col_b] - common[col_a]

        print()
        print("Common symmetric pairs:", len(common))
        print(
            "Median pointwise Delta R_eq difference: "
            f"{1e3 * difference.median():.3f} mOhm"
        )
        print(
            "RMS pointwise Delta R_eq difference: "
            f"{1e3 * np.sqrt(np.mean(difference**2)):.3f} mOhm"
        )

        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")

        ax.scatter(
            common["id_key"],
            common["iq_key"],
            1e3 * difference,
            s=5,
        )

        ax.set_xlabel(r"$i_d$")
        ax.set_ylabel(r"$|i_q|$")
        ax.set_zlabel(
            rf"$\Delta R_{{\mathrm{{eq}},{rpm_b}}}"
            rf"-\Delta R_{{\mathrm{{eq}},{rpm_a}}}$ / m$\Omega$"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Constant rotor-reference speed comparison")
    parser.add_argument("--no-plots", action="store_true", help="Run without interactive figures")
    parser.add_argument("--export", action="store_true", help="Export manuscript data, tables and vector-figure sources")
    args = parser.parse_args()
    raw = RawDataImporter(FILE_PATH)

    rpm_breakpoints, temperature_breakpoints = get_breakpoints(raw)

    if len(temperature_breakpoints) != 1:
        raise ValueError(
            "Multi-RPM dataset was expected to contain exactly one rotor "
            f"temperature; found {temperature_breakpoints}."
        )

    rotor_temperature = float(temperature_breakpoints[0])

    analyzers = []

    for rpm in rpm_breakpoints:
        measurement = build_ww_measurement_slice(
            raw,
            rpm=float(rpm),
            rotor_temperature=rotor_temperature,
        )

        analyzer = FluxMapSymmetryAnalyzer(measurement)
        analyzers.append(analyzer)

        print_summary(analyzer)

    common = build_common_speed_comparison(analyzers)

    if args.export:
        from export_experiments import export_analysis
        export_analysis(raw, analyzers, "multi", FILE_PATH, common)

    if PLOT and not args.no_plots:
        plot_multi_speed_comparison(analyzers, common)
        plt.show()
