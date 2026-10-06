# Physics-Constrained Reconstruction of Saturated dq Flux-Linkage Maps from Magnetic Co-Energy

Read [WRITING_GUIDE.md](../../WRITING_GUIDE.md) first. This English learning draft
owns measurements to flux, latent co-energy, gauge/path integration, symmetry,
reciprocity, saturation, differential inductance, gradient fitting, numerical
representations, and its own fitting experiments.

The document loads canonical `../../shared/`. Sections, concrete figures,
bibliography and numerical content remain local. There is no private framework
or general `local.tex`; the paper depends on the repository.

Build and reproduce from the repository root:

```powershell
./scripts/build.ps1 physics_constrained_flux_maps
python papers/physics_constrained_flux_maps/numerics/evaluate.py
```

The experiment requires Python 3 and NumPy. It implements analytic degree-four
B-spline derivatives without SciPy and writes `numerics/evaluation.json` and
`figures/data/`. Checks include gauge/rank, exact recovery, two integration
paths and a parity-only counterexample. Seeded illustrations cover noise,
sparse samples, outliers and stronger saturation. RBF comparison is conceptual.

The exported draft is `output/pdf/physics_constrained_flux_maps.pdf`.
The numerical content helper `magnetic_model.py` is identical to the diagnostic
experiment's local copy; each experiment runs independently. This is model
content, separate from canonical notation/presentation infrastructure.

See [the companion](../flux_map_error_diagnostics/README.md),
[the split report](../../docs/flux_papers_split.md) and
[the architecture audit](../../docs/architecture_migration.md).
