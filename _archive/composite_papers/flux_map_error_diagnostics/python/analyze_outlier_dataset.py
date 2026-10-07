from pathlib import Path
import argparse

import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np
import pandas as pd

from raw_ww_data_importer import RawDataImporter
from flux_correction import (
    DEFAULT_HIGH_IQ_REL,
    FluxMapSymmetryAnalyzer,
    build_ww_measurement_slice,
    get_breakpoints,
)

FILE_PATH = Path(__file__).resolve().parent / "WW_Dataset_Outlier.mat"

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
    print("High-|iq| range:       " f"{100 * DEFAULT_HIGH_IQ_REL:.1f} ... 100 %")
    print("High-|iq| points:      " f"{estimate.n_points}")
    print("Delta R_eq median:     " f"{estimate.delta_R_eq_median * 1e3:.3f} mOhm")
    print("Delta R_eq MAD:        " f"{estimate.delta_R_eq_mad * 1e3:.3f} mOhm")
    print("Resistance equivalent: " f"{estimate.resistance_equivalent * 1e3:.3f} mOhm")
    print("r_d RMS:               " f"{metrics['r_d_rms'] * 1e3:.3f} mWb")
    print("r_q RMS:               " f"{metrics['r_q_rms'] * 1e3:.3f} mWb")


def plot_flux_maps(
    analyzers: list[FluxMapSymmetryAnalyzer],
) -> None:
    for analyzer in analyzers:
        points = analyzer.flux_points

        i_d = points["id"].to_numpy()
        i_q = points["iq"].to_numpy()
        psi_d = points["psi_d"].to_numpy()
        psi_q = points["psi_q"].to_numpy()

        tri = mtri.Triangulation(i_d, i_q)

        fig = plt.figure(figsize=(12, 8))
        fig.suptitle(
            f"{analyzer.measurement.rpm:.0f} rpm, "
            f"{analyzer.measurement.rotor_temperature:.0f} °C"
        )

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


def plot_temperature_comparison(
    analyzers: list[FluxMapSymmetryAnalyzer],
) -> None:
    summaries = []

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    for analyzer in analyzers:
        pairs = analyzer.symmetric_pairs[
            analyzer.symmetric_pairs["valid_delta_R_eq"]
        ].copy()

        ax.scatter(
            pairs["id_key"],
            pairs["iq_mag"],
            1e3 * pairs["delta_R_eq"],
            s=4,
            label=(f"{analyzer.measurement.rotor_temperature:.0f} °C"),
        )

        estimate = analyzer.estimate_high_current_resistance()
        summaries.append(
            {
                "temperature": analyzer.measurement.rotor_temperature,
                "delta_R_eq_median_mOhm": 1e3 * estimate.delta_R_eq_median,
                "delta_R_eq_mad_mOhm": 1e3 * estimate.delta_R_eq_mad,
            }
        )

    ax.set_xlabel(r"$i_d$")
    ax.set_ylabel(r"$|i_q|$")
    ax.set_zlabel(r"$\Delta R_{\mathrm{eq}}$ / m$\Omega$")
    ax.legend()

    summary = pd.DataFrame(summaries).sort_values("temperature")

    fig = plt.figure()
    plt.errorbar(
        summary["temperature"],
        summary["delta_R_eq_median_mOhm"],
        yerr=summary["delta_R_eq_mad_mOhm"],
        marker="o",
    )
    plt.xlabel("Rotor temperature / °C")
    plt.ylabel(r"High-$|i_q|$ $\Delta R_{\mathrm{eq}}$ / m$\Omega$")
    plt.grid(True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Constant-speed rotor-reference comparison")
    parser.add_argument("--no-plots", action="store_true", help="Run without interactive figures")
    parser.add_argument("--export", action="store_true", help="Export manuscript data, tables and vector-figure sources")
    args = parser.parse_args()
    raw = RawDataImporter(FILE_PATH)

    rpm_breakpoints, temperature_breakpoints = get_breakpoints(raw)

    if len(rpm_breakpoints) != 1:
        raise ValueError(
            "Outlier dataset was expected to contain exactly one speed; "
            f"found {rpm_breakpoints}."
        )

    rpm = float(rpm_breakpoints[0])

    analyzers = []

    for temperature in temperature_breakpoints:
        measurement = build_ww_measurement_slice(
            raw,
            rpm=rpm,
            rotor_temperature=float(temperature),
        )

        analyzer = FluxMapSymmetryAnalyzer(measurement)
        analyzers.append(analyzer)

        print_summary(analyzer)

    if args.export:
        from export_experiments import export_analysis
        export_analysis(raw, analyzers, "outlier", FILE_PATH)

    if PLOT and not args.no_plots:
        plot_flux_maps(analyzers)
        plot_temperature_comparison(analyzers)
        plt.show()
