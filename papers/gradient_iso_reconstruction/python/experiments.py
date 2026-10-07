"""Regenerate every numerical paper result; no inherited benchmark numbers.

Run from any cwd: python papers/gradient_iso_reconstruction/python/experiments.py
All randomness uses local seeded Generators. Tables are emitted from actual
results, while backend hashes and versions identify the geometry dependency.
"""
import csv
from dataclasses import asdict
import hashlib
import inspect
import json
from pathlib import Path
import platform
import subprocess
import sys

import numpy as np
import scipy
from scipy.spatial import cKDTree
from scipy.stats import spearmanr

from gradient_iso import Options, reconstruct, search_guidance, simplex_derivatives
from gradient_iso.backend import PointSet, SampledField, EdgeIntersector

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def save_csv(name, rows):
    with (DATA / name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def quadratic(x):
    d = x.shape[1]
    h = np.diag(np.arange(1., d + 1)) + .2 * np.ones((d, d))
    b = np.linspace(-.4, .4, d)
    return .5 * np.einsum("ni,ij,nj->n", x, h, x) + x @ b, x @ h + b, h


def himmelblau(x):
    a, b = x[:, 0], x[:, 1]
    u, v = a*a + b - 11, a + b*b - 7
    f = u*u + v*v
    g = np.column_stack((4*a*u + 2*v, 2*u + 4*b*v))
    return f, g


def local_quadratic(x, y, queries, *, exclude_self=False, neighbors=24):
    """Independent local polynomial comparator; centered and radius-scaled.

    For residual screening query==support and exclude_self=True; that sample
    is never used to predict its own value. This is not a robust regression.
    """
    d = x.shape[1]
    k = min(neighbors + int(exclude_self), len(x))
    indices = cKDTree(x).query(queries, k=k)[1]
    if exclude_self:
        indices = indices[:, 1:]
    values, gradients = [], []
    for q, ids in zip(queries, indices):
        delta = x[ids] - q
        radius = np.max(np.linalg.norm(delta, axis=1))
        u = delta / radius
        columns = [np.ones(len(u))] + [u[:, j] for j in range(d)]
        columns += [u[:, i] * u[:, j] for i in range(d) for j in range(i, d)]
        a = np.column_stack(columns)
        coefficients, _, rank, _ = np.linalg.lstsq(a, y[ids], rcond=None)
        if rank < a.shape[1]:
            values.append(np.nan)
            gradients.append(np.full(d, np.nan))
        else:
            values.append(coefficients[0])
            gradients.append(coefficients[1:d + 1] / radius)
    return np.asarray(values), np.asarray(gradients)


def classification_metrics(labels, anomaly, predicted):
    """Exact threshold sweep including tied ranks, ROC endpoints and AP.

    AP=sum(delta recall * precision at the attained rank); it is not the
    trapezoidal area under an interpolated PR curve.
    """
    labels, anomaly = np.asarray(labels, bool), np.asarray(anomaly, float)
    if not np.isfinite(anomaly).all() or not labels.any() or labels.all():
        raise ValueError("Ranking metrics require finite scores and both classes")
    order = np.argsort(-anomaly, kind="stable")
    y, score = labels[order], anomaly[order]
    ends = np.r_[np.flatnonzero(np.diff(score)), len(score) - 1]
    tp = np.cumsum(y)[ends]
    fp = (ends + 1) - tp
    recall, fpr = tp / labels.sum(), fp / (~labels).sum()
    precision = tp / (tp + fp)
    ap = np.sum(np.diff(np.r_[0., recall]) * precision)
    auc = np.trapezoid(np.r_[0., recall], np.r_[0., fpr])
    true_positive = np.sum(predicted & labels)
    p = true_positive / max(1, predicted.sum())
    r = true_positive / labels.sum()
    return {"prevalence": float(labels.mean()), "flag_rate": float(predicted.mean()),
            "precision": float(p), "recall": float(r), "f1": float(2*p*r/max(p+r, 1e-30)),
            "auc": float(auc), "ap": float(ap)}, (np.r_[0., fpr], np.r_[0., recall]), (recall, precision)


def derivative_experiments():
    rows = []
    for n in (80, 160, 320, 640):
        for seed in (11, 12, 13):
            x = np.random.default_rng(seed).uniform(-1, 1, (n, 2))
            f, _, h = quadratic(x)
            for noise in (0., .001, .01):
                y = f + noise * np.random.default_rng(seed + 100).normal(size=n)
                cloud = simplex_derivatives(x, y)
                _, truth, _ = quadratic(cloud.points)
                err = np.linalg.norm(cloud.values - truth, axis=1)
                _, quad_g = local_quadratic(x, y, cloud.points)
                quad_err = np.linalg.norm(quad_g - truth, axis=1)
                interior = np.max(np.abs(cloud.points), axis=1) < .8
                rows.append({"N": n, "seed": seed, "noise_std": noise,
                             "median_error": float(np.median(err)),
                             "p95_error": float(np.quantile(err, .95)),
                             "interior_median": float(np.median(err[interior])),
                             "quadratic_median": float(np.nanmedian(quad_err)),
                             "median_condition": float(np.median(cloud.condition)),
                             "max_inverse_norm": float(cloud.inverse_edge_norm.max())})
    save_csv("derivative_accuracy.csv", rows)
    # Recursive second order, reported separately from direct polynomial tests.
    hrows = []
    for seed in (11, 12, 13):
        x = np.random.default_rng(seed).uniform(-1, 1, (160, 2))
        f, _, h = quadratic(x)
        for noise in (0., .001):
            y = f + noise*np.random.default_rng(seed + 100).normal(size=len(x))
            c = reconstruct(x, y, Options(order=2, levels=15))[-1]
            interior = np.max(np.abs(c.points), axis=1) < .8
            error = np.linalg.norm(c.raw_hessian - h, axis=(1, 2))
            hrows.append({"seed": seed, "noise_std": noise, "representatives": len(c.points),
                          "interior_median_error": float(np.median(error[interior])),
                          "median_symmetry_defect": float(np.median(c.symmetry_defect[interior])),
                          "median_laplacian_error": float(np.median(np.abs(c.laplacian[interior] - np.trace(h))))})
    save_csv("recursive_hessian.csv", hrows)
    # Dimension feasibility is not a scalability claim.
    drows = []
    for d in (2, 3, 4):
        x = np.random.default_rng(21).uniform(-1, 1, (50, d))
        f, _, _ = quadratic(x)
        c = reconstruct(x, f, Options(levels=10))[0]
        _, truth, _ = quadratic(c.points)
        drows.append({"dimension": d, "N": len(x), "representatives": len(c.points),
                      "median_error": float(np.median(np.linalg.norm(c.values - truth, axis=1))),
                      "intersections": sum(len(i.coordinates) for i in c.iso if i is not None)})
    save_csv("dimensions.csv", drows)
    return rows, hrows, drows


def outlier_experiments():
    rows, sensitivity = [], []
    display = None
    for seed in (11, 12, 13):
        rng = np.random.default_rng(seed)
        x = rng.uniform(-6, 6, (240, 2))
        f, _ = himmelblau(x)
        scale = np.std(f)
        y = f + .01*scale*rng.normal(size=len(x))
        mask = np.zeros(len(x), bool)
        ids = rng.choice(len(x), 19, replace=False)
        mask[ids] = True
        y[ids] += 1.4*scale*rng.choice([-1, 1], len(ids))*(1+.5*rng.random(len(ids)))
        c = reconstruct(x, y, Options(levels=15))[0]
        labels = mask[c.source_simplices].any(axis=1)
        nearest_labels = mask[cKDTree(x).query(c.points)[1]]
        predicted = c.coverage < c.threshold
        metrics, roc, pr = classification_metrics(labels, -c.coverage, predicted)
        rows.append({"seed": seed, "method": "iso", **metrics})
        pred_values, _ = local_quadratic(x, y, x, exclude_self=True)
        residuals = np.abs(pred_values - y)
        baseline = residuals[c.source_simplices].max(axis=1)
        # Matched budget: compare exactly the same number of flagged cells.
        pred_baseline = np.zeros(len(baseline), bool)
        pred_baseline[np.argsort(-baseline, kind="stable")[:predicted.sum()]] = True
        base_metrics, _, _ = classification_metrics(labels, baseline, pred_baseline)
        rows.append({"seed": seed, "method": "quadratic_residual", **base_metrics})
        # Preserve exact samples and all intermediate quantities for inspection.
        np.savez(DATA / f"himmelblau_seed_{seed}.npz", points=x, clean=f, observed=y,
                 outlier=mask, representatives=c.points, gradient=c.values,
                 source_simplices=c.source_simplices, contamination=labels,
                 nearest_labels=nearest_labels, coverage=c.coverage, predicted=predicted,
                 baseline=baseline, condition=c.condition)
        if seed == 11:
            display = (x, y, mask, c, labels, roc, pr)
            for m in (8, 15, 30):
                for bandwidth_factor in (.5, 1., 2.):
                    opts = Options(levels=m, bandwidth=c.rms_edge_length*bandwidth_factor)
                    s = reconstruct(x, y, opts)[0]
                    mm, _, _ = classification_metrics(labels, -s.coverage, s.coverage < s.threshold)
                    sensitivity.append({"levels": m, "bandwidth_factor": bandwidth_factor,
                                        "mode": "uniform", **mm})
            q = reconstruct(x, y, Options(levels=15, level_mode="quantile"))[0]
            mm, _, _ = classification_metrics(labels, -q.coverage, q.coverage < q.threshold)
            sensitivity.append({"levels": 15, "bandwidth_factor": 1., "mode": "quantile", **mm})
            for sigma in (-1., 0., 1., 2.):
                threshold = c.coverage.mean() + sigma*c.coverage.std(ddof=1)
                mm, _, _ = classification_metrics(labels, -c.coverage, c.coverage < threshold)
                sensitivity.append({"levels": 15, "bandwidth_factor": 1., "mode": f"sigma={sigma:g}", **mm})
    save_csv("outlier_metrics.csv", rows)
    save_csv("sensitivity.csv", sensitivity)
    return rows, display


def guidance_experiments():
    rows = []
    for seed in (11, 12, 13):
        rng = np.random.default_rng(seed)
        x = rng.uniform(-1, 1, (240, 2))
        f, _, _ = quadratic(x)
        for noise in (0., .01):
            y = f + noise*np.random.default_rng(seed+100).normal(size=len(x))
            c = reconstruct(x, y, Options(levels=15))[0]
            _, true_g, _ = quadratic(c.points)
            error = np.linalg.norm(c.values - true_g, axis=1)
            guide = search_guidance([c], x, minimize=True)
            f0, _, _ = quadratic(guide["points"])
            f1, _, _ = quadratic(guide["proposed"])
            inside = guide["inside_hull"]
            improvement = f0 - f1
            cutoff = np.quantile(c.coverage, .75)
            high = inside & (c.coverage >= cutoff)
            rows.append({"seed": seed, "noise_std": noise, "inside_fraction": float(inside.mean()),
                         "improvement_fraction_inside": float(np.mean(improvement[inside] > 0)),
                         "improvement_fraction_high_coverage": float(np.mean(improvement[high] > 0)),
                         "coverage_error_spearman": float(spearmanr(c.coverage, error).statistic)})
            if seed == 11 and noise == .01:
                np.savez(DATA / "guidance.npz", points=c.points, gradient=c.values,
                         truth=true_g, proposed=guide["proposed"], inside=inside,
                         coverage=c.coverage, error=error, improvement=improvement)
    save_csv("guidance.csv", rows)
    return rows


def write_tables(derivatives, hessians, dimensions, outliers, guidance):
    lines = []
    for n in (80, 160, 320, 640):
        group = [r for r in derivatives if r["N"] == n and r["noise_std"] == 0]
        noisy = [r for r in derivatives if r["N"] == n and r["noise_std"] == .01]
        lines.append(f"{n} & {np.mean([r['median_error'] for r in group]):.3f} & "
                     f"{np.mean([r['p95_error'] for r in group]):.3f} & "
                     f"{np.mean([r['median_error'] for r in noisy]):.3f} & "
                     f"{np.mean([r['quadratic_median'] for r in noisy]):.3f} \\\\")
    (DATA / "derivative_rows.tex").write_text("\n".join(lines) + "\n\\bottomrule\n", encoding="utf-8")
    lines = []
    for method, name in (("iso", "Iso coverage"), ("quadratic_residual", "Local quadratic residual")):
        group = [r for r in outliers if r["method"] == method]
        columns = ["flag_rate", "precision", "recall", "auc", "ap"]
        vals = [f"{np.mean([r[k] for r in group]):.3f}" for k in columns]
        lines.append(name + " & " + " & ".join(vals) + r" \\")
    (DATA / "outlier_rows.tex").write_text("\n".join(lines) + "\n\\bottomrule\n", encoding="utf-8")
    summary = {"hessian": {}, "guidance": {}, "outliers": {}, "dimensions": dimensions}
    for noise in (0., .001):
        group = [r for r in hessians if r["noise_std"] == noise]
        summary["hessian"][str(noise)] = {k: float(np.mean([r[k] for r in group])) for k in
            ("interior_median_error", "median_symmetry_defect", "median_laplacian_error")}
    for noise in (0., .01):
        group = [r for r in guidance if r["noise_std"] == noise]
        summary["guidance"][str(noise)] = {k: float(np.mean([r[k] for r in group])) for k in
            ("improvement_fraction_inside", "improvement_fraction_high_coverage", "coverage_error_spearman")}
    for method in ("iso", "quadratic_residual"):
        group = [r for r in outliers if r["method"] == method]
        summary["outliers"][method] = {k: {"mean": float(np.mean([r[k] for r in group])),
                                               "std": float(np.std([r[k] for r in group], ddof=1))}
                                      for k in ("prevalence", "flag_rate", "precision", "recall", "auc", "ap")}
    (DATA / "summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False), encoding="utf-8")
    # Numeric macros belong to generated table content, not new commands.
    with (DATA / "hessian_rows.tex").open("w", encoding="utf-8") as stream:
        for noise, vals in summary["hessian"].items():
            stream.write(noise + " & " + " & ".join(f"{v:.3f}" for v in vals.values()) + r" \\" + "\n")
        stream.write("\\bottomrule\n")
    with (DATA / "guidance_rows.tex").open("w", encoding="utf-8") as stream:
        for noise, vals in summary["guidance"].items():
            stream.write(noise + " & " + " & ".join(f"{v:.3f}" for v in vals.values()) + r" \\" + "\n")
        stream.write("\\bottomrule\n")


def provenance():
    modules = {}
    for cls in (PointSet, SampledField, EdgeIntersector):
        path = Path(inspect.getfile(cls)).resolve()
        modules[cls.__name__] = {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    path = Path(inspect.getfile(EdgeIntersector)).resolve()
    repo = next((parent for parent in path.parents if (parent / ".git").exists()), None)
    snapshot = ROOT / "python" / "vendor" / "provenance.json"
    if (ROOT / "python" / "vendor") in path.parents:
        revision = json.loads(snapshot.read_text(encoding="utf-8"))["revision"]
    else:
        revision = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip() if repo else None
    result = {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
              "backend_revision": revision, "backend_modules": modules,
              "default_options": asdict(Options()), "seeds": [11, 12, 13]}
    (DATA / "provenance.json").write_text(json.dumps(result, indent=2), encoding="utf-8")


def main():
    DATA.mkdir(exist_ok=True)
    provenance()
    print("Derivative accuracy, recursive Hessian and dimensional checks", flush=True)
    derivatives, hessians, dimensions = derivative_experiments()
    print("Contamination screening and parameter sensitivity", flush=True)
    outliers, _ = outlier_experiments()
    print("Measured search proposals", flush=True)
    guidance = guidance_experiments()
    write_tables(derivatives, hessians, dimensions, outliers, guidance)
    from figures import make_figures
    make_figures()
    print(f"Results and figures written under {ROOT}", flush=True)


if __name__ == "__main__":
    main()
