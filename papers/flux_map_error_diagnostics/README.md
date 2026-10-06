# Symmetry-Based Identification and Correction of Stator-Resistance and Rotor-Angle Errors from dq Flux-Linkage Maps

Read [WRITING_GUIDE.md](../../WRITING_GUIDE.md) first. This English learning draft
owns reconstruction-error sensitivity, exact frame rotation, symmetry residuals,
resistance/angle fingerprints, speed separation, identifiability, nuisance
ambiguity, and correction proposals for MeasEval.

The document loads canonical `../../shared/`. It repeats a compact magnetic
foundation and cites the unpublished companion. Sections, concrete figures,
bibliography and experiments remain local. There is no private framework,
general `local.tex`, or dependency on the companion's source sections.

Build and reproduce from the repository root:

```powershell
./scripts/build.ps1 flux_map_error_diagnostics
python papers/flux_map_error_diagnostics/numerics/validate.py
```

The experiment requires Python 3, NumPy and SymPy. It writes
`numerics/validation.json` and `figures/data/`, including measurement-route
error injections, first-order estimates, finite-angle comparison and correction.
It checks reciprocity preservation under coherent rotation and exact
resistance/voltage-error confounding.

The exported draft is `output/pdf/flux_map_error_diagnostics.pdf`.
The local `magnetic_model.py` helper is identical to the reconstruction
experiment's copy; each experiment runs independently. MeasEval is described
as a proposal/Apply workflow, not as an implemented integration or measured
machine validation.

See [the companion](../physics_constrained_flux_maps/README.md),
[the split report](../../docs/flux_papers_split.md) and
[the architecture audit](../../docs/architecture_migration.md).
