"""Small configurable replacement for the MATLAB laboratory demos."""
import argparse
import os
from pathlib import Path

import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--function", choices=["quadratic", "himmelblau"], default="quadratic")
    parser.add_argument("--dimension", type=int, default=2)
    parser.add_argument("--samples", type=int, default=120)
    parser.add_argument("--order", type=int, default=1)
    parser.add_argument("--levels", type=int, default=15)
    parser.add_argument("--noise", type=float, default=0.)
    parser.add_argument("--outlier-fraction", type=float, default=0.)
    parser.add_argument("--representative", choices=["centroid", "circumcenter"], default="centroid")
    parser.add_argument("--seed", type=int, default=21)
    parser.add_argument("--vice-source", type=Path)
    parser.add_argument("--output", type=Path, default=Path("tmp/gradient_iso_demo"))
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args()
    if args.vice_source:
        os.environ["VICE_MEASEVAL_SOURCE"] = str(args.vice_source.resolve())
    from gradient_iso import Options, reconstruct, search_guidance
    from experiments import quadratic, himmelblau
    if args.dimension < 2 or args.samples < args.dimension + 1:
        parser.error("Need dimension >= 2 and at least dimension+1 samples")
    if args.function == "himmelblau" and args.dimension != 2:
        parser.error("Himmelblau is defined in two dimensions")
    if args.noise < 0 or not np.isfinite(args.noise) or not 0 <= args.outlier_fraction < 1:
        parser.error("Need finite noise >= 0 and 0 <= outlier-fraction < 1")
    rng = np.random.default_rng(args.seed)
    bound = 6 if args.function == "himmelblau" else 1
    x = rng.uniform(-bound, bound, (args.samples, args.dimension))
    evaluate = himmelblau if args.function == "himmelblau" else quadratic
    clean = evaluate(x)[0]
    y = clean + args.noise*np.std(clean)*rng.normal(size=len(x))
    contaminated = np.zeros(len(x), bool)
    ids = rng.choice(len(x), int(round(args.outlier_fraction*len(x))), replace=False)
    contaminated[ids] = True
    y[ids] += 1.4*np.std(clean)*rng.choice([-1, 1], len(ids))
    clouds = reconstruct(x, y, Options(order=args.order, levels=args.levels, representative=args.representative))
    guide = search_guidance(clouds, x, minimize=True)
    truth = evaluate(guide["points"])[1]
    improvement = evaluate(guide["points"])[0] - evaluate(guide["proposed"])[0]
    args.output.mkdir(parents=True, exist_ok=True)
    payload = {"input_points": x, "observations": y, "clean": clean, "outlier": contaminated,
               **{f"guidance_{key}": value for key, value in guide.items()},
               "gradient_truth": truth, "true_improvement": improvement}
    for c in clouds:
        for name in ("points", "values", "source_simplices", "condition", "coverage"):
            payload[f"order_{c.order}_{name}"] = getattr(c, name)
        print(f"Order {c.order}: {len(c.points)} representatives, {c.rejected_simplices} rejected; iso={c.iso_status}")
    np.savez(args.output / "demo.npz", **payload)
    inside = guide["inside_hull"]
    fraction = np.mean(improvement[inside] > 0) if inside.any() else np.nan
    print(f"Inside-hull trial fraction: {inside.mean():.3f}; actual improvement among inside: {fraction:.3f}")
    print(f"Results: {args.output.resolve()}")
    import matplotlib
    if not args.show:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "shared" / "python"))
    from publication_plotting import configure
    roles = configure()
    first = clouds[0]
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.6), layout="constrained")
    stride = max(1, len(first.points)//200)
    p, delta = first.points[::stride, :2], (guide["proposed"] - first.points)[::stride, :2]
    axes[0].scatter(*x[:, :2].T, s=8, color=roles["guide"])
    axes[0].quiver(*p.T, *delta.T, angles="xy", scale_units="xy", scale=1, color=roles["reference"])
    axes[0].set_title("Descent proposals" + (" (2-D projection)" if args.dimension > 2 else ""))
    finite = np.isfinite(first.coverage)
    if finite.any():
        plot = axes[1].scatter(*first.points[finite, :2].T, c=first.coverage[finite], cmap=roles["coverage_map"], s=10)
        fig.colorbar(plot, ax=axes[1], label="Iso coverage; not confidence")
    else:
        axes[1].text(.5, .5, "Iso coverage undefined", ha="center", transform=axes[1].transAxes)
    axes[1].set_title("First-order support")
    for axis in axes:
        axis.set(xlabel="$x_1$", ylabel="$x_2$", aspect="equal")
    fig.savefig(args.output / "demo.png", dpi=180)
    if args.show:
        plt.show()
    plt.close(fig)


if __name__ == "__main__":
    main()
