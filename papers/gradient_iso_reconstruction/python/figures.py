"""Scientific figures generated from saved experiment outputs."""
import csv
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1] / "shared" / "python"))
from publication_plotting import configure


def read(name):
    with (ROOT / "data" / name).open(encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def save(fig, name):
    output = ROOT / "figures" / "generated"
    output.mkdir(exist_ok=True)
    fig.savefig(output / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(output / f"{name}.png", bbox_inches="tight")
    plt.close(fig)


def make_figures():
    roles = configure()
    rows = read("derivative_accuracy.csv")
    fig, ax = plt.subplots(1, 2, figsize=(7.3, 2.7), layout="constrained")
    for noise, color, label in ((0., roles["reference"], "Clean"),
                                 (.001, roles["derived"], "Noise std 0.001"),
                                 (.01, roles["estimated"], "Noise std 0.01")):
        ns = [80, 160, 320, 640]
        means, spreads = [], []
        for n in ns:
            values = [float(r["median_error"]) for r in rows
                      if int(r["N"]) == n and float(r["noise_std"]) == noise]
            means.append(np.mean(values))
            spreads.append(np.std(values, ddof=1))
        ax[0].errorbar(ns, means, yerr=spreads, color=color, marker="o", label=label, capsize=3)
    for key, color, label in (("median_error", roles["estimated"], "Simplex interpolation"),
                              ("quadratic_median", roles["derived"], "Local quadratic (24 neighbors)")):
        values = [np.mean([float(r[key]) for r in rows if int(r["N"]) == n
                           and float(r["noise_std"]) == .01]) for n in ns]
        ax[1].plot(ns, values, color=color, marker="o", label=label)
    for axis in ax:
        axis.set(xlabel="Input samples N", ylabel="Median gradient error", xscale="log", yscale="log")
        axis.legend()
    ax[0].set_title("Refinement competes with noise amplification")
    ax[1].set_title("Same samples, different local estimators")
    save(fig, "accuracy")

    data = np.load(ROOT / "data" / "himmelblau_seed_11.npz")
    x, reps = data["points"], data["representatives"]
    fig, ax = plt.subplots(1, 3, figsize=(7.3, 2.7), layout="constrained")
    for axis, pts, labels, title in ((ax[0], x, data["outlier"], "Injected sample perturbations"),
                                    (ax[1], reps, data["contamination"], "Affected simplex centroids")):
        axis.scatter(*pts[~labels].T, s=5, color=roles["guide"])
        axis.scatter(*pts[labels].T, s=12, color=roles["estimated"])
        axis.set_title(title)
    cut = ax[2].scatter(*reps.T, s=8, c=data["coverage"], cmap=roles["coverage_map"])
    fig.colorbar(cut, ax=ax[2], label="Iso coverage S")
    ax[2].set_title("Geometric descriptor on derivative support")
    for axis in ax:
        axis.set(xlabel="$x_1$", ylabel="$x_2$", xlim=(-6, 6), ylim=(-6, 6), aspect="equal")
    save(fig, "contamination")

    from experiments import classification_metrics
    fig, ax = plt.subplots(1, 2, figsize=(7.3, 2.7), layout="constrained")
    for name, scores, color in (("Iso: low S is anomalous", -data["coverage"], roles["estimated"]),
                                 ("Quadratic residual", data["baseline"], roles["derived"])):
        _, roc, pr = classification_metrics(data["contamination"], scores, data["predicted"])
        ax[0].plot(*roc, color=color, label=name)
        ax[1].step(*pr, where="post", color=color, label=name)
    ax[0].plot([0, 1], [0, 1], color=roles["guide"], linestyle="--", label="Chance reference")
    ax[1].axhline(data["contamination"].mean(), color=roles["guide"], linestyle="--", label="Cell prevalence")
    ax[0].set(xlabel="False positive rate", ylabel="True positive rate", title="ROC, seed 11")
    ax[1].set(xlabel="Recall", ylabel="Precision", title="PR, seed 11")
    for axis in ax:
        axis.set(xlim=(0, 1), ylim=(0, 1.03))
        axis.legend(loc="lower right" if axis == ax[0] else "upper right")
    save(fig, "screening")

    guide = np.load(ROOT / "data" / "guidance.npz")
    fig, ax = plt.subplots(1, 2, figsize=(7.3, 2.8), layout="constrained")
    pts = guide["points"]
    delta = guide["proposed"] - pts
    index = np.arange(0, len(pts), 8)
    ax[0].scatter(*pts.T, s=4, color=roles["guide"], alpha=.5)
    ax[0].quiver(*pts[index].T, *delta[index].T, color=roles["reference"], angles="xy", scale_units="xy", scale=1)
    outside = ~guide["inside"]
    if outside.any():
        ax[0].scatter(*guide["proposed"][outside].T, marker="x", color=roles["estimated"], label="Outside sampled hull")
        ax[0].legend()
    ax[0].set(xlabel="$x_1$", ylabel="$x_2$", title="Descent proposals; true objective re-evaluated", aspect="equal")
    ax[1].scatter(guide["coverage"], guide["error"], s=8, color=roles["estimated"], alpha=.6)
    ax[1].set(xlabel="Iso coverage S", ylabel="Gradient error", yscale="log",
              title="Coverage alone does not calibrate error")
    save(fig, "guidance")

    from gradient_iso import Options, reconstruct
    from experiments import quadratic
    fig, ax = plt.subplots(1, 2, figsize=(7.3, 2.8), layout="constrained")
    for axis, values, title in ((ax[0], data["clean"], "Clean gradient-component cuts"),
                                (ax[1], data["observed"], "Perturbed gradient-component cuts")):
        cloud = reconstruct(data["points"], values, Options(levels=15))[0]
        cuts = cloud.iso[0]
        axis.scatter(*cloud.points.T, s=3, color=roles["guide"], alpha=.35)
        axis.scatter(*cuts.coordinates.T, s=6, color=roles["derived"])
        axis.set(xlabel="$x_1$", ylabel="$x_2$", xlim=(-6, 6), ylim=(-6, 6), aspect="equal", title=title)
        axis.text(.03, .03, f"{len(cuts.coordinates)} cuts; component 1\n15 levels spanning each field range",
                  transform=axis.transAxes, fontsize=8, bbox={"facecolor": "white", "alpha": .8, "edgecolor": "none"})
    save(fig, "iso_geometry")

    x = np.random.default_rng(11).uniform(-1, 1, (160, 2))
    f, _, h = quadratic(x)
    second = reconstruct(x, f, Options(order=2, levels=15))[1]
    interior = np.max(np.abs(second.points), axis=1) < .8
    fig, ax = plt.subplots(1, 2, figsize=(7.3, 2.7), layout="constrained")
    for i, (column, reference, title) in enumerate(((second.laplacian, np.trace(h), "Trace of recovered Hessian"),
                                                   (second.symmetry_defect, 0., "Mixed-partial disagreement"))):
        values = column[interior]
        lo, hi = np.quantile(values, [.01, .99])
        lo, hi = min(lo, reference), max(hi, reference)
        ax[i].hist(values, bins=np.linspace(lo, hi, 36), color=roles["estimated"], alpha=.75)
        ax[i].axvline(reference, color=roles["reference"], linestyle="--", label="Analytic quadratic")
        ax[i].set(xlabel="Value", ylabel="Interior cells", title=title)
        ax[i].legend()
        omitted = np.sum((values < lo) | (values > hi))
        ax[i].text(.97, .7, f"Central 98% range\n{omitted} cells beyond range",
                   ha="right", transform=ax[i].transAxes, fontsize=8)
    save(fig, "hessian")


if __name__ == "__main__":
    make_figures()
