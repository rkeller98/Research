"""Standalone torque-referenced dq-flux regularization experiment.

Default: analyze, save JSON/CSV/PDF, print a research summary, and show plots.
Use ``--save-only`` for the identical headless CI workflow.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import sys

import numpy as np

PAPER = Path(__file__).resolve().parents[1]
ROOT = PAPER.parents[1]
DATA = PAPER / "figures" / "data"
DATA.mkdir(parents=True, exist_ok=True)
MPL_CONFIG = ROOT / "tmp" / "matplotlib"
MPL_CONFIG.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CONFIG))
os.environ.setdefault("XDG_CACHE_HOME", str(ROOT / "tmp" / "cache"))
sys.path.insert(0, str(ROOT / "shared/python"))

from canonical_dataset import load_dataset
from magnetic_model import flux as normalized_truth_flux
from potential_splines import design, roughness

spec = importlib.util.spec_from_file_location(
    "torque_poc", ROOT / "docs/torque_flux_consistency/proof_of_concept.py"
)
poc = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(poc)

SEED = 20261007
SYNTHETIC_LAMBDA = 0.1
REAL_LAMBDA = 10.0
LAMBDA_GRID = np.array([0.01, 0.1, 1.0, 10.0, 100.0])


def torque(current, flux, kt):
    return kt * (current[:, 1] * flux[:, 0] - current[:, 0] * flux[:, 1])


def directions(current):
    magnitude = np.linalg.norm(current, axis=1)
    radial = np.divide(current, magnitude[:, None], out=np.zeros_like(current),
                       where=magnitude[:, None] > 0)
    return magnitude, radial, np.column_stack([radial[:, 1], -radial[:, 0]])


def potential_operators(points, scales, flux_base=0.1):
    """Gauge-fixed B-spline potential operators; no parity is imposed."""
    gauge = design(np.zeros((1, 2)))
    z = np.linalg.svd(gauge, full_matrices=True)[2][1:].T
    energy_base = flux_base * float(np.max(scales))
    derivative = lambda dx, dy: design(points, dx, dy) @ z * energy_base / (
        scales[0] ** dx * scales[1] ** dy
    )
    return dict(gd=derivative(1, 0), gq=derivative(0, 1),
                dd=derivative(2, 0), dq=derivative(1, 1), qq=derivative(0, 2),
                roughness=roughness(None, 3) @ z)


def fit_correction(current, points, scales, residual, groups, kt, lam, flux_base=0.1):
    """Fit one global co-energy correction and one free offset per group."""
    op = potential_operators(points, scales, flux_base)
    tmat = kt * (current[:, 1, None] * op["gd"] - current[:, 0, None] * op["gq"])
    labels = np.unique(groups)
    offsets = np.column_stack([groups == label for label in labels]).astype(float)
    tscale = max(float(np.std(residual)), 1e-9)
    change = np.vstack([op["gd"], op["gq"]]) / flux_base
    nc = tmat.shape[1]
    matrix = np.block([
        [tmat / tscale, offsets / tscale],
        [np.sqrt(lam) * op["roughness"], np.zeros((len(op["roughness"]), len(labels)))],
        [np.sqrt(0.05 * lam) * change, np.zeros((len(change), len(labels)))],
    ])
    target = np.r_[residual / tscale, np.zeros(len(op["roughness"]) + len(change))]
    solution = np.linalg.lstsq(matrix, target, rcond=None)[0]
    coefficients = solution[:nc]
    delta_flux = np.column_stack([op["gd"] @ coefficients, op["gq"] @ coefficients])
    delta_torque = tmat @ coefficients
    corrected_residual = residual - delta_torque
    hessian = np.stack([
        np.column_stack([op["dd"] @ coefficients, op["dq"] @ coefficients]),
        np.column_stack([op["dq"] @ coefficients, op["qq"] @ coefficients]),
    ], axis=1)
    return dict(coefficients=coefficients, delta_flux=delta_flux,
                delta_torque=delta_torque, corrected_residual=corrected_residual,
                group_labels=labels,
                offsets=np.array([corrected_residual[groups == x].mean() for x in labels]),
                hessian=hessian,
                change_rms_Wb=float(np.sqrt(np.mean(delta_flux ** 2))),
                roughness_norm=float(np.linalg.norm(op["roughness"] @ coefficients)),
                reciprocity_max_H=float(np.max(abs(hessian[:, 0, 1] - hessian[:, 1, 0]))))


def centered_rms(values, groups):
    centered = values.copy()
    for label in np.unique(groups):
        selected = groups == label
        centered[selected] -= centered[selected].mean()
    return float(np.sqrt(np.mean(centered ** 2)))


def grid_metrics(field, size, spacing):
    shaped = field.reshape(size, size, 2)
    curl = (np.gradient(shaped[:, :, 1], spacing[0], axis=0)
            - np.gradient(shaped[:, :, 0], spacing[1], axis=1))
    second = []
    for component in range(2):
        second += [np.diff(shaped[:, :, component], n=2, axis=axis).ravel()
                   for axis in (0, 1)]
    return dict(curl_rms_mH=float(1000 * np.sqrt(np.mean(curl ** 2))),
                second_difference_rms_mWb=float(
                    1000 * np.sqrt(np.mean(np.concatenate(second) ** 2))))


def write_csv(name, header, values):
    np.savetxt(DATA / name, values, delimiter=",", fmt="%.17g", comments="", header=header)


def synthetic_experiment():
    rng = np.random.default_rng(SEED)
    size, ibase, psibase, pole_pairs = 17, 100.0, 0.1, 3
    points = np.array([(x, y) for x in np.linspace(-.9, .9, size)
                       for y in np.linspace(-.9, .9, size)])
    current, kt = ibase * points, 1.5 * pole_pairs
    truth = psibase * normalized_truth_flux(points)
    x, y = points.T
    magnitude, radial, normal = directions(current)
    conservative = psibase * np.column_stack([
        .06 * y**2 + .06 * x, .12 * x * y - .06 * y])
    wave = (.0015 * np.sin(2.5 * np.pi * x) * np.cos(1.5 * np.pi * y))[:, None] * normal
    radial_null = psibase * .012 * points
    noise = rng.normal(0, .0005, (len(current), 2))
    raw_without_radial = truth + conservative + wave + noise
    raw = raw_without_radial + radial_null
    true_offset, torque_noise_sd = 1.2, .12
    measured = torque(current, truth, kt) + true_offset + rng.normal(0, torque_noise_sd, len(current))
    raw_torque = torque(current, raw, kt)
    residual = measured - raw_torque
    groups = np.zeros(len(current), dtype=int)
    fits, sensitivity = {}, []
    for lam in LAMBDA_GRID:
        fit = fit_correction(current, points, np.array([ibase, ibase]), residual,
                             groups, kt, float(lam), psibase)
        corrected = raw + fit["delta_flux"]
        fits[float(lam)] = fit
        sensitivity.append([lam, 1000 * np.sqrt(np.mean((corrected - truth) ** 2)),
                            centered_rms(fit["corrected_residual"], groups),
                            1000 * fit["change_rms_Wb"], fit["roughness_norm"]])
    fit = fits[SYNTHETIC_LAMBDA]
    corrected = raw + fit["delta_flux"]
    corrected_without_radial = raw_without_radial + fit["delta_flux"]
    raw_error, corrected_error = raw - truth, corrected - truth
    valid = magnitude > 0
    component_rms = lambda error, direction: float(
        1000 * np.sqrt(np.mean(np.sum(error[valid] * direction[valid], axis=1) ** 2)))
    spacing = (2 * .9 * ibase / (size - 1),) * 2
    report = dict(
        experiment="known-truth global co-energy correction", seed=SEED,
        grid=dict(size=size, points=len(current), current_limit_A=90.0),
        machine=dict(configuration="one amplitude-invariant three-phase PMSM",
                     pole_pairs=pole_pairs, k_T=kt),
        measurement=dict(true_group_offset_Nm=true_offset,
                         torque_noise_sd_Nm=torque_noise_sd),
        corruption=dict(components=["smooth conservative distortion", "spatial normal wave",
                                    "radial torque-null potential", "point noise"]),
        regularization=dict(
            parameterization="gauge-fixed degree-four tensor B-spline co-energy correction",
            selected_lambda=SYNTHETIC_LAMBDA,
            selection="fixed demonstration value; ground truth is used only for evaluation",
            lambda_grid=LAMBDA_GRID.tolist(), change_weight_relative_to_lambda=.05),
        metrics=dict(
            flux_rmse_raw_mWb=float(1000 * np.sqrt(np.mean(raw_error ** 2))),
            flux_rmse_corrected_mWb=float(1000 * np.sqrt(np.mean(corrected_error ** 2))),
            torque_residual_bias_raw_Nm=float(residual.mean()),
            torque_residual_rms_raw_Nm=float(np.sqrt(np.mean(residual ** 2))),
            estimated_group_offset_Nm=float(fit["offsets"][0]),
            centered_residual_rms_raw_Nm=centered_rms(residual, groups),
            centered_residual_rms_corrected_Nm=centered_rms(fit["corrected_residual"], groups),
            radial_error_rms_raw_mWb=component_rms(raw_error, radial),
            radial_error_rms_corrected_mWb=component_rms(corrected_error, radial),
            normal_error_rms_raw_mWb=component_rms(raw_error, normal),
            normal_error_rms_corrected_mWb=component_rms(corrected_error, normal),
            radial_null_preservation_max_mWb=float(1000 * np.max(abs(
                (corrected - corrected_without_radial) - radial_null))),
            correction_reciprocity_max_H=fit["reciprocity_max_H"],
            correction_roughness_norm=fit["roughness_norm"],
            raw_structure=grid_metrics(raw, size, spacing),
            corrected_structure=grid_metrics(corrected, size, spacing),
            truth_structure=grid_metrics(truth, size, spacing)),
        interpretation=("The global conservative prior recovers most torque-visible structure and the offset. "
                        "The radial potential remains torque-invisible; a conservative addition cannot remove "
                        "curl introduced by nonconservative corruption."))
    m = report["metrics"]
    assert m["flux_rmse_corrected_mWb"] < m["flux_rmse_raw_mWb"]
    assert m["centered_residual_rms_corrected_Nm"] < .25 * m["centered_residual_rms_raw_Nm"]
    assert abs(m["estimated_group_offset_Nm"] - true_offset) < .05
    assert m["radial_null_preservation_max_mWb"] < 1e-10
    assert m["correction_reciprocity_max_H"] < 1e-14
    write_csv("synthetic_recovery.csv",
              "id_A,iq_A,psi_d_truth_Wb,psi_q_truth_Wb,psi_d_raw_Wb,psi_q_raw_Wb,"
              "psi_d_corrected_Wb,psi_q_corrected_Wb,torque_measured_Nm,torque_raw_Nm,"
              "residual_raw_Nm,residual_corrected_Nm,radial_null_d_Wb,radial_null_q_Wb",
              np.column_stack([current, truth, raw, corrected, measured, raw_torque,
                               residual, fit["corrected_residual"], radial_null]))
    write_csv("lambda_sensitivity.csv",
              "lambda,flux_rmse_corrected_mWb,centered_residual_rms_Nm,change_rms_mWb,roughness_norm",
              np.asarray(sensitivity))
    arrays = dict(current=current, truth_flux=truth, raw_flux=raw,
                  corrected_flux=corrected, raw_residual=residual,
                  corrected_residual=fit["corrected_residual"],
                  lambda_rows=np.asarray(sensitivity), size=np.array([size]))
    return report, arrays


def low_complexity_residual(points, residual):
    x, y = points.T
    matrix = np.column_stack([np.ones(len(x)), x, y, x**2, x*y, y**2])
    prediction = matrix @ np.linalg.lstsq(matrix, residual, rcond=None)[0]
    bins = (np.floor((x + 1) * 5) + 3 * np.floor((y + 1) * 5)).astype(int) % 5
    errors = []
    for fold in range(5):
        train, test = bins != fold, bins == fold
        coefficients = np.linalg.lstsq(matrix[train], residual[train], rcond=None)[0]
        errors.extend(residual[test] - matrix[test] @ coefficients)
    return dict(in_sample_rms_Nm=float(np.sqrt(np.mean((residual - prediction) ** 2))),
                spatial_five_fold_rms_Nm=float(np.sqrt(np.mean(np.asarray(errors) ** 2))))


def real_experiment():
    data, manifest = load_dataset("psm_dual_system_multirpm")
    current = np.column_stack([data["id"], data["iq"]])
    raw_flux = np.column_stack([data["psi_d"], data["psi_q"]])
    measured, raw_torque = data["torque"], data["torque_map"]
    residual, groups = measured - raw_torque, data["rpm_req"].astype(int)
    center, scales = .5 * (current.min(0) + current.max(0)), .505 * np.ptp(current, axis=0)
    points = (current - center) / scales
    assert np.all(data["kt"] == 12) and set(np.unique(groups)) == {1000, 3000}
    fits, sensitivity = {}, []
    for lam in LAMBDA_GRID:
        fit = fit_correction(current, points, scales, residual, groups, 12., float(lam))
        fits[float(lam)] = fit
        sensitivity.append([lam, *[np.std(fit["corrected_residual"][groups == rpm])
                                    for rpm in (1000, 3000)],
                            1000 * fit["change_rms_Wb"], fit["roughness_norm"]])
    fit = fits[REAL_LAMBDA]
    corrected_flux = raw_flux + fit["delta_flux"]
    corrected_residual = fit["corrected_residual"]
    transfer = []
    for training_rpm in (1000, 3000):
        train = groups == training_rpm
        trained = fit_correction(current[train], points[train], scales, residual[train],
                                 groups[train], 12., REAL_LAMBDA)
        op = potential_operators(points, scales)
        delta = np.column_stack([op["gd"] @ trained["coefficients"],
                                 op["gq"] @ trained["coefficients"]])
        transferred = residual - (torque(current, raw_flux + delta, 12.) - raw_torque)
        for evaluated_rpm in (1000, 3000):
            selected = groups == evaluated_rpm
            transfer.append(dict(trained_rpm=training_rpm, evaluated_rpm=evaluated_rpm,
                                 raw_centered_rms_Nm=float(np.std(residual[selected])),
                                 corrected_centered_rms_Nm=float(np.std(transferred[selected]))))
    slices = []
    for rpm in (1000, 3000):
        selected = groups == rpm
        magnitude = np.linalg.norm(current[selected], axis=1)
        qualified = magnitude >= .1 * magnitude.max()
        raw, corrected = residual[selected], corrected_residual[selected]
        slices.append(dict(
            rpm=rpm, temperature_reference_C=70, points=int(selected.sum()),
            normalized_points=int(qualified.sum()), raw_residual_bias_Nm=float(raw.mean()),
            raw_residual_rms_Nm=float(np.sqrt(np.mean(raw ** 2))),
            raw_centered_rms_Nm=float(np.std(raw)),
            estimated_group_offset_Nm=float(corrected.mean()),
            corrected_residual_rms_Nm=float(np.sqrt(np.mean(corrected ** 2))),
            corrected_centered_rms_Nm=float(np.std(corrected)),
            median_torque_std_Nm=float(np.median(data["torque_std"][selected])),
            constant_offset_hypothesis=dict(model_rms_Nm=float(np.std(raw)),
                quadratic_residual_model=low_complexity_residual(points[selected], raw))))
    report = dict(
        experiment="portable Multi-RPM stationary residual regularization",
        source=dict(dataset="psm_dual_system_multirpm", csv_sha256=manifest["csv_sha256"],
                    requested_speed_slices_rpm=[1000, 3000], temperature_reference_C=70),
        machine=dict(phase_selector=1, represented_three_phase_systems=2,
                     pole_pairs=4, k_T=12,
                     torque_factor_basis="3p for two equally represented amplitude-invariant systems"),
        hypothesis="M_meas-M_theo,corr is approximately constant within each qualified group",
        regularization=dict(parameterization="one shared gauge-fixed co-energy correction plus one offset per speed",
            selected_lambda=REAL_LAMBDA,
            selection="fixed conservative demonstration value; lambda path reported, not optimized on unknown truth",
            lambda_grid=LAMBDA_GRID.tolist(), change_weight_relative_to_lambda=.05,
            change_rms_mWb=1000 * fit["change_rms_Wb"],
            correction_roughness_norm=fit["roughness_norm"],
            correction_reciprocity_max_H=fit["reciprocity_max_H"]),
        slices=slices, leave_one_speed_out_transfer=transfer,
        interpretation=("Offsets dominate the uncentered discrepancy. A shared conservative correction reduces "
                        "in-sample centered spread, but each single-speed correction worsens the other slice; "
                        "these data do not validate a speed-invariant physical flux correction."),
        limit=("CAN torque is not calibrated electromagnetic ground truth; losses, sensor offset, terminal-versus-"
               "magnetic current, and speed-dependent voltage reconstruction remain unresolved."))
    assert fit["reciprocity_max_H"] < 1e-14
    assert all(x["corrected_centered_rms_Nm"] < x["raw_centered_rms_Nm"] for x in slices)
    write_csv("real_residuals.csv",
              "rpm_req,id_A,iq_A,psi_d_raw_Wb,psi_q_raw_Wb,psi_d_corrected_Wb,psi_q_corrected_Wb,"
              "torque_measured_Nm,torque_theoretical_raw_Nm,residual_raw_Nm,residual_corrected_Nm,"
              "delta_psi_d_Wb,delta_psi_q_Wb",
              np.column_stack([groups, current, raw_flux, corrected_flux, measured, raw_torque,
                               residual, corrected_residual, fit["delta_flux"]]))
    write_csv("real_lambda_sensitivity.csv",
              "lambda,centered_rms_1000rpm_Nm,centered_rms_3000rpm_Nm,change_rms_mWb,roughness_norm",
              np.asarray(sensitivity))
    arrays = dict(groups=groups, current=current, raw_flux=raw_flux,
                  corrected_flux=corrected_flux, raw_residual=residual,
                  corrected_residual=corrected_residual,
                  lambda_rows=np.asarray(sensitivity))
    return report, arrays


def observability_checks():
    """Preserve original local observability tests and add boundary cases."""
    report, extra = poc.run_checks(), {}
    def check(name, condition):
        assert condition, name
        extra[name] = {"passed": True}
    current = np.array([[0., 100.], [0., -100.], [100., 0.], [-100., 0.],
                        [60., 80.], [-60., 80.], [-60., -80.], [60., -80.]])
    magnitude, radial, normal = poc.directions(current)
    flux = poc.flux(current)
    check("axis_id_zero", np.allclose(poc.torque(current[:2], flux[:2]),
                                      poc.KT * current[:2, 1] * flux[:2, 0]))
    check("axis_iq_zero", np.allclose(poc.torque(current[2:4], flux[2:4]),
                                      -poc.KT * current[2:4, 0] * flux[2:4, 1]))
    visible = poc.torque(current, flux + .005 * normal) - poc.torque(current, flux)
    invisible = poc.torque(current, flux + .008 * radial) - poc.torque(current, flux)
    mixed = poc.torque(current, flux + .008 * radial + .005 * normal) - poc.torque(current, flux)
    check("four_quadrants_normal_observable", np.allclose(visible, poc.KT * magnitude * .005))
    check("four_quadrants_radial_invisible", np.allclose(invisible, 0, atol=1e-12))
    check("four_quadrants_mixed_projection", np.allclose(mixed, visible))
    check("positive_negative_torque", np.any(poc.torque(current, flux) > 0)
          and np.any(poc.torque(current, flux) < 0))
    tiny = np.array([[1e-9, 0.], [0., 1e-9]])
    check("small_current_torque_continuous", np.max(abs(poc.torque(tiny, poc.flux(tiny)))) < 1e-8)
    check("origin_torque_zero", float(poc.torque(np.zeros(2), poc.flux(np.zeros(2)))) == 0)
    check("reciprocal_isotropic_radial_null",
          np.allclose(poc.torque(current, flux + .0001 * current), poc.torque(current, flux)))
    check("radial_even_potential_and_positive_curvature",
          np.all(np.linalg.eigvalsh(np.diag([.0001, .0001])) > 0))
    def normal_projection(point):
        row = np.array([point[1], -point[0]])
        return row * point[1] / np.dot(point, point)
    point, step = np.array([.6, .8]), 1e-5
    dq = (normal_projection(point + [0, step]) - normal_projection(point - [0, step])) / (2 * step)
    dd = (normal_projection(point + [step, 0]) - normal_projection(point - [step, 0])) / (2 * step)
    check("pointwise_minimum_change_need_not_preserve_curl", abs(dd[1] - dq[0]) > .1)
    xd, xq, excitation = .6, .8, 2.
    hessian = np.array([[excitation, 0., xd], [0., excitation, xq], [xd, xq, 0.]])
    check("three_current_reciprocity_radial_excitation_family",
          np.allclose(hessian, hessian.T) and np.isclose(xq * excitation * xd - xd * excitation * xq, 0))
    grid = np.array([(x, y) for x in np.linspace(-1, 1, 13) for y in np.linspace(-1, 1, 13)])
    hm, gu, gauge = poc.potential_operators(grid)
    columns = [0, 1, 3, 4, 6]
    ranks = {"torque": poc.spectrum(hm[:, columns]),
             "joint": poc.spectrum(np.vstack([hm[:, columns], gu[:, columns]])),
             "gauge": poc.spectrum(np.vstack([hm[:, columns], gu[:, columns], gauge[:, columns]]))}
    check("even_reciprocal_torque_rank_two_of_five", ranks["torque"]["rank"] == 2)
    check("even_reciprocal_joint_rank_four_gauge_five",
          ranks["joint"]["rank"] == 4 and ranks["gauge"]["rank"] == 5)
    for omega in (-100., 100.):
        xd, xq = current[-1]
        matrix = np.array([[0., -omega, xd], [omega, 0., xq],
                           [poc.KT * xq, -poc.KT * xd, 0.]])
        check(f"joint_local_rank_signed_speed_{omega:g}",
              np.isclose(np.linalg.det(matrix), -poc.KT * omega * (xd**2 + xq**2))
              and np.linalg.matrix_rank(matrix) == 3)
    for excitation in (0., 2.):
        eesm_flux = flux + np.column_stack([np.full(len(current), .01 * excitation),
                                             np.zeros(len(current))])
        check(f"excitation_slice_radial_null_{excitation:g}",
              np.allclose(poc.torque(current, eesm_flux + .0001 * current),
                          poc.torque(current, eesm_flux)))
    report["even_potential_operators"] = ranks
    report["additional_checks"] = extra
    report["total_passed"] = len(report["checks"]) + len(extra)
    return report


def plot_results(synthetic, real, show):
    import matplotlib.pyplot as plt
    import matplotlib.tri as mtri
    from publication_plotting import configure
    colors, outputs = configure(), []
    def save(fig, name):
        path = PAPER / "figures" / f"{name}.pdf"
        fig.savefig(path, bbox_inches="tight", metadata={"CreationDate": None, "ModDate": None})
        preview = ROOT / "tmp" / "torque_paper_figures"
        preview.mkdir(parents=True, exist_ok=True)
        fig.savefig(preview / f"{name}.png", bbox_inches="tight", dpi=180)
        outputs.append(path)
    # Local geometry retained as the limitation figure.
    fig, axes = plt.subplots(1, 2, figsize=(7, 3.2), layout="constrained")
    radial, normal = np.array([.6, .8]), np.array([.8, -.6])
    for v, label, color in [(radial, r"$n_i$", colors["reference"]),
                            (normal, r"$n_\tau$", colors["torque"])]:
        axes[0].annotate("", xy=v, xytext=(0, 0),
                         arrowprops=dict(arrowstyle="->", color=color, lw=1.8))
        axes[0].text(*(1.1 * v), label)
    old, closest = .8 * radial + .5 * normal, .8 * radial + .2 * normal
    axes[0].plot([0, old[0]], [0, old[1]], color=colors["derived"])
    axes[0].plot([old[0], .5 * normal[0]], [old[1], .5 * normal[1]], "--", color=colors["guide"])
    axes[0].scatter(*old, color=colors["derived"], marker="s")
    axes[0].set(title="(a) Torque sees the normal projection",
                xlabel="d flux / chosen base", ylabel="q flux / chosen base")
    t = np.linspace(-.4, 1.3, 100)
    axes[1].plot(*(t[:, None] * radial + .2 * normal).T, "--", color=colors["reference"], label="Equal torque")
    axes[1].scatter(*old, marker="s", color=colors["estimated"], label="Raw flux")
    axes[1].scatter(*closest, marker="o", facecolors="none", edgecolors=colors["derived"], label="Minimum change")
    axes[1].scatter(*(closest + .3 * radial), marker="^", color=colors["highlight"], label="Radial alternative")
    axes[1].set(title="(b) One torque value defines a line",
                xlabel="d flux / chosen base", ylabel="q flux / chosen base")
    axes[1].legend(loc="upper left", bbox_to_anchor=(0, -.22), ncols=2, fontsize=7)
    for ax in axes: ax.set_aspect("equal", adjustable="box")
    save(fig, "06_torque_geometry")
    # Synthetic recovery.
    size, current = int(synthetic["size"][0]), synthetic["current"]
    truth, raw, corrected = synthetic["truth_flux"], synthetic["raw_flux"], synthetic["corrected_flux"]
    fig, axes = plt.subplots(2, 2, figsize=(7, 5.7), layout="constrained")
    sl = slice((size // 2) * size, (size // 2 + 1) * size)
    for value, style, role, label in [(truth, "-", "reference", "Ground truth"),
                                       (raw, "--", "estimated", "Raw"),
                                       (corrected, "-", "derived", "Corrected")]:
        axes[0, 0].plot(current[sl, 1], 1000 * value[sl, 0], style,
                        color=colors[role], label=label)
    axes[0, 0].set(title=r"(a) Synthetic $i_d=0$ flux slice",
                   xlabel=r"$i_q$ (A)", ylabel=r"$\psi_d$ (mWb)")
    axes[0, 0].legend()
    axes[0, 1].scatter(synthetic["raw_residual"], synthetic["corrected_residual"],
                       s=12, color=colors["derived"])
    axes[0, 1].axhline(0, color=colors["guide"], lw=.8)
    axes[0, 1].set(title="(b) Constant group offset may remain",
                   xlabel="Raw residual (Nm)", ylabel="Corrected residual (Nm)")
    rows = synthetic["lambda_rows"]
    axes[1, 0].semilogx(rows[:, 0], rows[:, 1], "o-", color=colors["estimated"])
    axes[1, 0].axvline(SYNTHETIC_LAMBDA, color=colors["guide"], linestyle="--")
    axes[1, 0].set(title="(c) Regularization sensitivity", xlabel=r"$\lambda$",
                   ylabel="Corrected flux RMSE (mWb)")
    eraw, ecorr = np.linalg.norm(raw - truth, axis=1) * 1000, np.linalg.norm(corrected - truth, axis=1) * 1000
    limit = max(eraw.max(), ecorr.max())
    axes[1, 1].scatter(eraw, ecorr, s=12, color=colors["torque"])
    axes[1, 1].plot([0, limit], [0, limit], "--", color=colors["guide"])
    axes[1, 1].set(title="(d) Pointwise known-truth error",
                   xlabel="Raw vector error (mWb)", ylabel="Corrected vector error (mWb)")
    save(fig, "08_torque_recovery")
    # Standalone real residual surfaces.
    fig, axes = plt.subplots(2, 2, figsize=(7, 5.8), layout="constrained")
    for column, rpm in enumerate((1000, 3000)):
        selected = real["groups"] == rpm
        tri = mtri.Triangulation(real["current"][selected, 0], real["current"][selected, 1])
        values = [real["raw_residual"][selected], real["corrected_residual"][selected]]
        limit = max(np.max(abs(v - v.mean())) for v in values)
        levels = np.linspace(-limit, limit, 13)
        for row, (value, label) in enumerate(zip(values, ("Raw centered", "Corrected centered"))):
            contour = axes[row, column].tricontourf(
                tri, value - value.mean(), levels=levels,
                cmap=colors["error_map"], vmin=-limit, vmax=limit)
            axes[row, column].set(title=f"{label} residual, {rpm} rpm",
                                  xlabel=r"$i_d$ (A)", ylabel=r"$i_q$ (A)")
            fig.colorbar(contour, ax=axes[row, column], label="Torque residual (Nm)")
    save(fig, "09_real_residual_surfaces")
    fig, axes = plt.subplots(1, 2, figsize=(7, 3), layout="constrained")
    for rpm, role in ((1000, "reference"), (3000, "estimated")):
        selected = real["groups"] == rpm
        axes[0].scatter(real["raw_residual"][selected], real["corrected_residual"][selected],
                        s=13, color=colors[role], label=f"{rpm} rpm")
    axes[0].axhline(0, color=colors["guide"], lw=.8)
    axes[0].set(title="(a) Portable two-speed residuals",
                xlabel="Raw residual (Nm)", ylabel="Corrected residual (Nm)")
    axes[0].legend()
    rows = real["lambda_rows"]
    axes[1].semilogx(rows[:, 0], rows[:, 1], "o-", color=colors["reference"], label="1000 rpm")
    axes[1].semilogx(rows[:, 0], rows[:, 2], "s--", color=colors["estimated"], label="3000 rpm")
    axes[1].axvline(REAL_LAMBDA, color=colors["guide"], linestyle="--", label="Reported fit")
    axes[1].set(title="(b) Real-data regularization path", xlabel=r"$\lambda$",
                ylabel="Centered residual RMS (Nm)")
    axes[1].legend()
    save(fig, "10_real_regularization")
    if show: plt.show()
    else: plt.close("all")
    return outputs


def print_summary(synthetic, real, outputs):
    m = synthetic["metrics"]
    print("\nTorque-referenced dq-flux research experiment\n" + "=" * 49)
    print("Synthetic: known co-energy, one three-phase PMSM, p=3, k_T=4.5")
    print(f"  Flux RMSE: {m['flux_rmse_raw_mWb']:.3f} -> {m['flux_rmse_corrected_mWb']:.3f} mWb")
    print(f"  Centered torque residual: {m['centered_residual_rms_raw_Nm']:.3f} -> {m['centered_residual_rms_corrected_Nm']:.3f} Nm")
    print(f"  Group offset: true {synthetic['measurement']['true_group_offset_Nm']:.3f}, estimated {m['estimated_group_offset_Nm']:.3f} Nm")
    print(f"  Normal error: {m['normal_error_rms_raw_mWb']:.3f} -> {m['normal_error_rms_corrected_mWb']:.3f} mWb")
    print(f"  Radial-null preservation error: {m['radial_null_preservation_max_mWb']:.2e} mWb")
    print(f"  Map second-difference RMS: {m['raw_structure']['second_difference_rms_mWb']:.3f} -> "
          f"{m['corrected_structure']['second_difference_rms_mWb']:.3f} mWb (unobserved structure remains)")
    print(f"  Correction roughness norm: {m['correction_roughness_norm']:.3e}")
    print(f"  Conservative correction reciprocity error: {m['correction_reciprocity_max_H']:.2e} H")
    print(f"  Local observability regression: {synthetic['observability_regression']['total_passed']} checks passed")
    print("\nReal: psm_dual_system_multirpm")
    print(f"  Provenance: {real['source']['csv_sha256']}")
    print("  Selector 1; two three-phase systems; p=4; k_T=3p=12; CAN is not EM ground truth.")
    for row in real["slices"]:
        cv = row["constant_offset_hypothesis"]["quadratic_residual_model"]["spatial_five_fold_rms_Nm"]
        print(f"  {row['rpm']} rpm / 70 C: {row['points']} OPs ({row['normalized_points']} qualified); "
              f"bias/RMS {row['raw_residual_bias_Nm']:.3f}/{row['raw_residual_rms_Nm']:.3f} Nm; "
              f"offset {row['estimated_group_offset_Nm']:.3f} Nm; centered "
              f"{row['raw_centered_rms_Nm']:.3f} -> {row['corrected_centered_rms_Nm']:.3f} Nm; "
              f"quadratic spatial-CV {cv:.3f} Nm")
    print("  Leave-one-speed-out: each single-speed correction worsens the other slice.")
    print(f"  Shared correction RMS: {real['regularization']['change_rms_mWb']:.3f} mWb")
    print(f"  Shared correction roughness/reciprocity: "
          f"{real['regularization']['correction_roughness_norm']:.3e} / "
          f"{real['regularization']['correction_reciprocity_max_H']:.2e} H")
    artifacts = [PAPER / "numerics/torque_synthetic.json", PAPER / "numerics/real_evaluation.json",
                 DATA / "synthetic_recovery.csv", DATA / "lambda_sensitivity.csv",
                 DATA / "real_residuals.csv", DATA / "real_lambda_sensitivity.csv", *outputs]
    print("\nArtifacts:")
    for path in artifacts: print(f"  {path.relative_to(ROOT)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save-only", action="store_true",
                        help="save all artifacts without GUI windows (CI/headless)")
    args = parser.parse_args()
    if args.save_only:
        import matplotlib
        matplotlib.use("Agg")
    checks = observability_checks()
    synthetic_report, synthetic_arrays = synthetic_experiment()
    synthetic_report["observability_regression"] = checks
    real_report, real_arrays = real_experiment()
    (PAPER / "numerics/torque_synthetic.json").write_text(
        json.dumps(synthetic_report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    (PAPER / "numerics/real_evaluation.json").write_text(
        json.dumps(real_report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    outputs = plot_results(synthetic_arrays, real_arrays, not args.save_only)
    print_summary(synthetic_report, real_report, outputs)


if __name__ == "__main__":
    main()
