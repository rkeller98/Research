# Physics-Constrained Reconstruction of Saturated dq Flux-Linkage Maps from Magnetic Co-Energy

Read [WRITING_GUIDE.md](../../WRITING_GUIDE.md) first. This English learning draft
owns measurements to flux, latent co-energy, gauge/path integration, symmetry,
reciprocity, saturation, differential inductance, gradient fitting, numerical
representations, and its own fitting experiments.
The real-data admissibility section tests the conservative/symmetric model
class against the completed audit. It is not a successful real-data co-energy
reconstruction: symmetry and path equivalents disagree, and a high-current
parity improvement accompanies worse all-pair d/vector and path metrics.

The document loads canonical `../../shared/`. Sections, concrete figures,
bibliography and numerical content remain local. There is no private framework
or general `local.tex`; the paper depends on the repository.

Build and reproduce from the repository root:

```powershell
python papers/physics_constrained_flux_maps/numerics/evaluate.py
python papers/physics_constrained_flux_maps/numerics/torque_consistency.py
python papers/physics_constrained_flux_maps/python/audit_coenergy.py
python papers/physics_constrained_flux_maps/python/audit_observables.py
python papers/physics_constrained_flux_maps/python/audit_symbolic.py
python papers/physics_constrained_flux_maps/numerics/export_audit_tables.py
./scripts/build.ps1 physics_constrained_flux_maps
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

The current real-data path experiment has a separate
[scientific audit](docs/coenergy_analysis_audit.md), with reproducible synthetic,
curl, quadrature and observable checks in `python/audit_*.py`. It distinguishes
parity from conservation and leaves physical resistance/loss attribution open.
Its findings now appear in the manuscript between synthetic evaluation and
discussion. The detailed audit remains the evidence/reproduction record,
including input/script hashes, exact P1/Green checks, geometry sensitivity,
normalization observables and retained raw artifacts. These calculations
require NumPy, pandas, SciPy, h5py and Matplotlib; the symbolic check additionally
requires SymPy. Set `MPLBACKEND=Agg` for headless execution.

The standard-library table exporter reads the existing audit JSON and writes
local TeX tables and hash manifests into both papers' `figures/data/audit/`.
It changes no evidence and performs no fit. Each paper builds with its own
generated table files. Exact P1 integration is exact for that interpolator;
the path equivalent averages curl over a rectangle, not local resistance.
Terminal/magnetizing coordinates, full dq normalization and cause attribution
remain open. A future potential fit is a model projection whose raw-to-model
residual must remain visible.

The storage/terminal distinction now governs the abstract, measurement and
potential interpretation, gradient-fit objective, and conclusions. A chain-rule
rotation proof is included locally. The discussion preserves apparent tilt as
potential loss/measurement information and motivates joint identification over
speed, independently measured winding temperature, and additional observables.
See [the evidence-integration report](../../docs/flux_paper_evidence_revision.md)
for the section-by-section mapping and final validation.

Torque observability now connects differential consistency to the fitting
formulation. It derives the current-normal projection, local solution line,
minimum-change representative, and reciprocal radial-potential null family.
The synthetic torque experiment preserves all 40 original research checks
and adds 18 axis/quadrant/rank/reciprocity/excitation checks. Its even-potential
example separates observation rank from gauge fixing and regularization.

The real torque section uses Multi_RPM, not Outlier, with the existing
electrical reconstruction and matching OP averages. CAN metadata do not
qualify a sensor, unit, electromagnetic torque or shaft torque. Real metrics
and plots therefore assume numeric CAN values are Nm with recorded sign and
unity gain explicitly. No measured-map correction or joint real-data fit is
performed. Current-threshold and speed/averaging sensitivities accompany the
unfiltered residual maps.

The reproducible pipeline requires the same NumPy/pandas/SciPy/h5py stack
and Matplotlib plus kpsewhich for the canonical palette. It reads the two
original files, writes JSON/CSV/generated TeX under numerics and figures/data,
and creates four vector PDF figures. The local paper's script calls the
unchanged research proof of concept for its original checks. Use
--checks-only to omit figure regeneration. Source/data hashes are recorded;
the vector PDFs omit creation/modification timestamps for repeatability.
See [the integration and evidence audit](docs/torque_consistency_integration.md)
for provenance, figure selection, limitations, and the decision against a split.
