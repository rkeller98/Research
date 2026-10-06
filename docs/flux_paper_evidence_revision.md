# Flux-paper evidence revision: manuscript integration

Revision date: 2026-10-06. This report covers the latest incremental request.
The two existing papers and prior derivations, sources, experiments and figures
are retained. This is a repository report, not a third publication.

## Manuscript changes and audit mapping

The reconstruction paper is *Physics-Constrained Reconstruction of Saturated
dq Flux-Linkage Maps from Magnetic Co-Energy*. The diagnostics companion is
*On the Interpretation of Symmetry Residuals in Experimental dq Flux-Linkage Maps*.

| Reconstruction location | Integrated evidence and resulting interpretation |
|---|---|
| Abstract and Section 1, `01_introduction.tex` | Storage co-energy and terminal reconstruction are distinct. Terminal observations need coordinate/state/admissibility evidence before being interpreted as conjugate gradients. The main contribution remains an admissible storage model class. |
| Section 2, `02_measurement_to_flux.tex` | Voltage inversion recovers a terminal-current map and enforces neither symmetry nor conservation. Loss currents can prevent terminal current from being the magnetic state coordinate. |
| Section 3, `03_magnetic_coenergy.tex` | Co-energy differential, gauge, reciprocity and oriented integration are retained. Flux gives candidate slopes under a declared storage interpretation. Physical three-phase versus dq-normalized co-energy is explicit. |
| Section 4, `04_symmetry_and_reciprocity.tex` | Parity and integrability are independent; the even/odd counterexample has nonzero curl. A local chain-rule proof shows that coherent constant rotation preserves a potential and symmetric Hessian while rotating its reflection axis. |
| Sections 5 and 7 | Existing saturation/cross-saturation, differential-inductance and B-spline/RBF representation development remains valid and was not rederived. |
| Section 6, `06_physics_constrained_fitting.tex` | For inconsistent input, gradient fitting is a weighted, regularized projection into the chosen storage class. Explicit sample residuals must accompany predictions; structural zero curl is not a causal validation. |
| Section 8, `08_synthetic_evaluation.tex` | Existing known-ground-truth fitting, sparse/noisy/outlier and derivative-quality experiments remain unchanged and are rerun. They verify the method under their assumptions. |
| Section 9, `08b_real_data_admissibility.tex` | The real five-slice audit follows synthetic evaluation. It explains support/matching, oriented rectangle-average curl, resistance-shift invariance, exact P1/Green integration, raw-versus-hypothesis metrics, P1 derivative/geometry limits, conservative-reference interpolation tests and unverified measurement normalization. No real-data potential fit is claimed. |
| Section 10, `09_discussion.tex` | Conservative magnetizing storage can become nonconservative against terminal current after loss-branch reduction. The full Df-transpose pullback is required. Prediction/residual decomposition is not the unknown true magnetic law. Tilt is retained as possible loss/measurement information. Joint speeds, independently measured winding temperature and added observables form a research direction. |
| Section 11, `10_conclusion.tex` | The contribution and real-data evidence boundary are restated consistently; neither winding resistance, iron-loss causality nor a successful real-data co-energy reconstruction is identified. |

The evidence source remains
[papers/physics_constrained_flux_maps/docs/coenergy_analysis_audit.md](../papers/physics_constrained_flux_maps/docs/coenergy_analysis_audit.md),
together with its scripts and original JSON/CSV outputs. Its pre-existing user
edit is preserved byte-for-byte. The manuscript explains the findings itself;
reading the audit report is not required to understand the scientific argument.

## Reproducible tables and retained figures

Three audit table inputs are generated locally for both papers by
`papers/physics_constrained_flux_maps/numerics/export_audit_tables.py`, using
unchanged audit JSON and input/exporter SHA-256 manifests:

- `support.tex`: all five slices, operating-index groups and unique keys,
  accepted pairs/high-current pairs, valid rectangles and hull skips.
- `slice_comparison.tex`: all five symmetry equivalents, path medians/MADs,
  exact-P1 medians and path counts. Pair counts are exposed in the accompanying
  support table rather than hidden within an estimator description.
- `raw_adjusted_60.tex`: high-current and all-pair d/q/vector RMS and path
  metrics on exactly the same support before/after the resistance hypothesis.

The reconstruction paper includes all three; the compact companion cross-check
includes the comparison and raw-adjusted table. Tables are newly introduced by
this audit-integration work, and retained in the latest incremental revision.
No duplicate real-data section or additional decorative figure was created.
The existing measurement-to-model figure now explicitly states storage
coordinates/assumptions, model projection and diagnostic identifiability.
The existing synthetic, symmetry, landscape, path and derivative figures remain.

The central 2000-rpm/60-degree result is 8.274010 mOhm from selected high-current
symmetry versus 5.885553 mOhm path median (5.885512 with exact P1 integration).
The 500-point trapezoidal integration RMS error is 0.0000766 mOhm over all
2869 accepted rectangles. The discrepancy is therefore not explained by that
quadrature error. This does not bound interpolation or model-reduction error.
The high-current d RMS improves from 1.100092 to 0.219939 mWb, whereas all-pair
d RMS rises from 1.746480 to 1.954456 mWb and median relative path difference
rises from 3.488090 to 4.226703 percent. No data were selected to force agreement.

## Necessary companion changes

The existing `07c_conservation_cross_check.tex` remains the compact independent
cross-constraint test: area-average rather than local path equivalent, affine
invariance rather than resistance calibration, exact-integration gap, different
support, P1 limits and terminal/storage distinction. Full co-energy theory is
kept in the reconstruction paper. Introduction, metadata, companion bibliography,
and the experimental interpretation already reflect this scope.

The latest engineering-implications edit explicitly rejects automatic untilting
and preserves the possibility of loss-related information in the asymmetry.
The conclusion motivates joint identification with additional calibrated
observables and independently measured winding temperatures. A current-proportional
voltage error remains exactly confounded with resistance in flux reconstruction,
even across speeds. The conditional inverse transformation and its synthetic
sign validation are retained, without promoting them to a real-data correction.

## Claims narrowed and questions left open

The paper does not claim that a constrained fit repairs terminal data into the
true machine. It supplies a model class for conservative storage, with residuals
that can contain bias, losses, timing/angle, hysteresis, unmodeled dynamics,
actual asymmetry and interpolation/sampling error. Perfect parity does not
prove reciprocity, and perfect constructed curl does not validate causality.
A resistance-like tilt or invariant path equivalent does not calibrate actual
winding resistance. Iron loss is an illustrative possible mechanism, not the
confirmed explanation of the observed gap. Exact P1 integration validates the
integration of the interpolator, not its magnetic accuracy.

Open questions are the natural storage coordinates and fixed internal state,
voltage/transform/power normalization, true thermal winding state, loss-current
and inverter contributions, adequately matched magnetic states, causal
identifiability across speed and temperature, and robust derivative estimation
on sparse or poorly conditioned support. The real-data gap remains a result.
A real-data potential fit and a jointly identifiable loss/measurement model
require further evidence; neither is manufactured as part of draft completion.

## Validation and repository state

All five required runs passed their assertions:

| Command | Result |
|---|---|
| `python papers/physics_constrained_flux_maps/python/audit_coenergy.py` | All five real slices, conservative synthetic references, injected resistance and quadrature/Green checks passed. |
| `python papers/physics_constrained_flux_maps/python/audit_observables.py` | Quadrants, orientation, arbitrary resistance shifts, support/normalization and raw-adjusted observables passed. |
| `python papers/physics_constrained_flux_maps/python/audit_symbolic.py` | Independent exact symbolic identities passed, using bundled Python with SymPy 1.14.0. |
| `python papers/physics_constrained_flux_maps/numerics/evaluate.py` | Gauge/rank, B-spline analytic derivatives, noiseless recovery and seeded noisy/sparse/outlier/saturation checks passed. Existing generated results reproduced byte-for-byte. |
| `python papers/flux_map_error_diagnostics/numerics/validate.py` | Rotation sensitivity/reciprocity, correction signs, parameter rank, confounding and synthetic numerical checks passed. Existing generated results reproduced byte-for-byte. |

The numeric audit used Python 3.13.12, NumPy 2.4.4 and SciPy 1.17.1 with
headless Matplotlib from the existing ignored dependencies. The original audit
JSON records NumPy 2.5.3 and SciPy 1.18.1. Only `audit_results.json` and two
local-regression/triangle CSVs differed by version-sensitive roundoff; maximum
absolute difference was 7.275957614183426e-12. JSON checks used scaled tolerance
1e-10; CSVs passed absolute/relative 1e-12. Rerun copies and comparison evidence
are separately retained in ignored `tmp/flux_evidence_followup/`.
All original audit outputs, input MAT files, importer/reconstruction/audit
scripts, synthetic outputs and the user-edited audit document are byte-preserved.
Generated manuscript table provenance matches the original JSON/exporter hashes.

Architecture and its self-test, working-tree/staged whitespace checks, and
tracked-cache hygiene checks passed. The three pyc files and the inspected
empty `main.bbl-SAVE-ERROR` are removed in the existing staged hygiene change.
No original measurement or scientific audit artifact was deleted.
Final build and visual-review evidence is recorded below.
No automatic commit or push is authorized or performed.

### Final builds and complete visual review

Individual `scripts/build.ps1 physics_constrained_flux_maps` and
`scripts/build.ps1 flux_map_error_diagnostics` completed successfully, followed
by `scripts/build_all.ps1` for all eight registered papers. Every final paper
log is clean: no warnings, overfull/underfull boxes, missing characters or
unresolved references/citations. No TeX sources were changed during the builds.

Every page of both final PDFs was rendered and visually reviewed. Tables,
equations, orientation/sign conventions, units, chart axes/legends, captions,
glossaries and bibliographies are legible, with no overlap or clipping.
Extracted text contains no unresolved `??`. Reconstruction has five figures,
five tables and thirteen bibliography entries; diagnostics has twelve figures,
six tables and fourteen entries. All 22 reconstruction-page renders are
byte-identical after `build_all` to those already reviewed. Final PDF SHA-256
matches the reviewed artifact manifest.

- `output/pdf/physics_constrained_flux_maps.pdf`: 22 pages; SHA-256 `8cf46da4dda81c193b67d3e11e194d0bfdb4a4e969c88fec9f7c5d9dbe3852c1`.
- `output/pdf/flux_map_error_diagnostics.pdf`: 31 pages; SHA-256 `dfad224d07a3949b37d0d79f88121c18b15e897bac64a35bd88865818a988855`.

### Final Git status

The working tree retains the earlier incremental work. No reset, commit or
push was performed. The audit-document modification shown below is the
pre-existing user edit; this revision preserves its bytes. Four staged
removals are the requested build/cache hygiene. New audit sections, table
exports and this report remain untracked for review, and manuscript/common
infrastructure edits remain unstaged. No third combined paper is active.

```text
 M docs/flux_map_experimental_validation.md
 M docs/flux_papers_split.md
 M papers/flux_map_error_diagnostics/README.md
 M papers/flux_map_error_diagnostics/bibliography/references.bib
 M papers/flux_map_error_diagnostics/main.tex
 M papers/flux_map_error_diagnostics/metadata.tex
D  papers/flux_map_error_diagnostics/numerics/__pycache__/magnetic_model.cpython-312.pyc
 M papers/flux_map_error_diagnostics/sections/01_introduction.tex
 M papers/flux_map_error_diagnostics/sections/10_engineering_implications.tex
 M papers/flux_map_error_diagnostics/sections/12_conclusion.tex
 M papers/physics_constrained_flux_maps/README.md
 M papers/physics_constrained_flux_maps/bibliography/references.bib
 M papers/physics_constrained_flux_maps/docs/coenergy_analysis_audit.md
 M papers/physics_constrained_flux_maps/figures/01_measurement_pipeline.tex
 M papers/physics_constrained_flux_maps/main.tex
 M papers/physics_constrained_flux_maps/metadata.tex
D  papers/physics_constrained_flux_maps/numerics/__pycache__/magnetic_model.cpython-312.pyc
 M papers/physics_constrained_flux_maps/sections/01_introduction.tex
 M papers/physics_constrained_flux_maps/sections/02_measurement_to_flux.tex
 M papers/physics_constrained_flux_maps/sections/03_magnetic_coenergy.tex
 M papers/physics_constrained_flux_maps/sections/04_symmetry_and_reciprocity.tex
 M papers/physics_constrained_flux_maps/sections/06_physics_constrained_fitting.tex
 M papers/physics_constrained_flux_maps/sections/09_discussion.tex
 M papers/physics_constrained_flux_maps/sections/10_conclusion.tex
D  papers/temp_eesm_Mopt/main.bbl-SAVE-ERROR
D  sandbox/__pycache__/raw_ww_data_importer.cpython-313.pyc
 M shared/commands/machine_commands.tex
 M shared/glossary/symbols.tex
?? docs/flux_paper_evidence_revision.md
?? papers/flux_map_error_diagnostics/figures/data/audit/
?? papers/flux_map_error_diagnostics/sections/07c_conservation_cross_check.tex
?? papers/physics_constrained_flux_maps/figures/data/audit/
?? papers/physics_constrained_flux_maps/numerics/export_audit_tables.py
?? papers/physics_constrained_flux_maps/sections/08b_real_data_admissibility.tex
```
