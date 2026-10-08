# Research portfolio migration, 7 October 2026

Historical source locations were consolidated on 8 October in
[the final cleanup audit](final_cleanup.md). Both composite snapshots remain
unchanged; original geometry and Gradient-Iso sources now live under `_archive/`.

## Scientific ownership

| Active flux paper | Research question | Contribution | Origin | Main evidence |
|---|---|---|---|---|
| `flux_correction_symmetry` | Which flux components does reflection detect/project? | Complementary even/odd residuals, closest-pair projection, weighted interpretation and physical evidence boundary | Diagnostics structural/parity sections plus ZIP's projection framing | Algebra; portable PSM 2500-rpm measured-coordinate mirror interpolation |
| `magnetic_coenergy_consistency` | Can the measured field be one potential gradient? | Reciprocity/circulation tests, coordinate counterexamples, exact P1/independent Green audit and geometric sensitivity | Physics composite co-energy, Hessian and admissibility sections | Analytic affine checks; same original PSM lineage at 30/70°C references |
| `flux_correction_coenergy` | How can samples be projected into a common potential class? | Gauge-fixed gradient fit, even B-spline potential, curvature penalty and retained residuals | Physics composite fitting/numerical/synthetic sections | Original controlled synthetic regression; portable real spatial tuning experiment |
| `torque_flux_consistency` | Can stationary torque residual shape regularize a reconstructed flux map while group offsets remain free? | Global minimum-change/smooth correction, co-energy variant, offset nuisance model; rank-one/radial-null theory retained as its identifiability limit | Current physics composite torque theory plus new global recovery | Known-truth recovery and lambda path; portable two-speed residual/transfer study; 58 retained observability checks; six-phase kT=3p qualification |
| `flux_error_identifiability` | Which reconstruction-error directions are distinguishable? | Exact/linear transformations, scaled/whitened ranks and exact nuisance confounding | Diagnostics error-sensitivity, angle, identification and synthetic sections | Original symbolic/numeric regression; measured support nullspace check |

The independent-reference umbrella remains
`concepts/reference_quantity_flux_correction.md`: no separately qualified
electrical or magnetic reference supports another active correction paper.
Symmetry/path resistance equivalents are conditional normalizations, not an
independent measurement of winding resistance. Creating a sixth umbrella
paper would duplicate the mature claims above. Hessian-based parameter
derivation remains `concepts/coenergy_parameter_derivation.md`, with a future
question/validation gate rather than a thin paper.

The seven other existing active publications keep their own questions:
PSM/EESM voltage geometry; local simplex derivatives and iso reconstruction;
the IEMDC conference digest; N-dimensional contour/root extraction; recursive
QP within a simplex; and the extended constrained EESM torque-optimization
working draft. Their source was not changed by this scientific split; all
were rebuilt against the canonical glossary. Page counts and QA appear in
`portfolio_completion_report.md`.

## Research-issue completion map

| Research question | Owning paper | Reproducible evidence | Principal limitation | Issue |
|---|---|---|---|---|
| Which reflection-forbidden flux components and resistance-equivalent patterns are identifiable? | `flux_correction_symmetry` | Full-map/selected-region mirror metrics plus analytic resistance injection and exact voltage-drop confounder from `python scripts/evaluate_portfolio.py --save-only` | Symmetry identifies a forbidden subspace, not physical resistance or a cause | #2 |
| Is the reconstructed field compatible with one magnetic co-energy? | `magnetic_coenergy_consistency` | Affine zero-curl check, nonlinear conservative P1 artifact, analytic resistance curl, exact path/Green audit and conditioning subsets | Terminal-current coordinates, interpolation and loss branches prevent causal interpretation | #3 |
| Which multi-speed error directions are distinguishable? | `flux_error_identifiability` | Synthetic scaled rank plus 83-point inverse-speed test, physically scaled nuisance design and pointwise CSV | Resistance/proportional voltage are exactly confounded; magnetic current is unobserved | #4 |
| How do correction hypotheses, admissibility and identifiability fit together? | Five-paper flux portfolio; torque paper owns independent-reference regularization | Derivations, known-truth counterexamples, portable diagnostics, local/integrated tests and boundaries in `docs/research_epic_completion.md` | No portable fixture supplies calibrated true flux or certified electromagnetic torque | #1 |

## Source and result map

`P` below denotes archived `physics_constrained_flux_maps`, `D` archived
`flux_map_error_diagnostics`. Both are the current working-tree versions,
not the ZIP's substitutes. The archive's source snapshot verifies preservation.

| Composite content | New ownership / treatment |
|---|---|
| P01 introduction; D01 introduction | Rewritten around five explicit questions; old framing archived |
| P02 / D02 stationary voltage inversion | Necessary short definitions in each relevant paper; portable measured electrical speed replaces old requested-speed experiment assumptions |
| P03 potential, gauge, paths, Green, PM example | Consistency paper owns full integrability argument; reconstruction has a short slope/gauge foundation |
| P04 / D03 magnetic symmetry and coordinate rotation | Symmetry owns reflection/projection; consistency retains counterexamples and chain rule; identifiability retains only required assumptions |
| P05 Hessian, saturation and differential cross-inductance | Consistency owns reciprocity/curvature explanation; reconstruction uses analytic derivatives as its method; further parameter extraction parked as concept |
| P05b torque observability | Torque paper, generic convention-qualified kT; real six-phase factor is explicit |
| P06/P07 gradient fitting, whitening, regularization, splines | Reconstruction paper; one shared benchmark and spline implementation |
| P08 synthetic reconstruction | Reconstruction paper; original seed/basis/noise/robust experiment retained |
| P08b real Outlier/Multi admissibility and audit tables | Preserved in archive; superseded active demonstration uses portable original PSM lineage, new exact P1/Green results |
| P08c conditional CAN factor-two results | Preserved in archive; replaced by newly computed two-system torque comparison |
| P09 loss branch / current pullback | Consistency discussion; not a claimed identified loss cause |
| D05 sensitivity, D06 coherent angle, D08 rank/confounding, D09 synthetic examples | Identifiability paper; original transformations and checks retained |
| D07 parity residuals | Symmetry projection paper; conditional error fingerprints referenced in identifiability |
| D07a/D07b requested-pair real temperature/speed experiments | Preserved as historical results; active symmetry now uses supported measured-coordinate mirror interpolation |
| D07c conservation cross-check | Consistency topic; old equivalent tables archived, new integrability evidence generated |
| D10 engineering workflow and P measurement pipeline | Removed from scientific narrative where not needed; technical import/export boundary documented separately |
| P10/D11/D12 conclusions/limits | Rewritten for each active claim; unsupported causal and old scale-ambiguity claims removed from active torque text |

## Figure and numerical ownership

P03 potential landscape / P04 integration paths are owned by the consistency
paper. Reconstruction keeps its synthetic fitted slope/curvature illustration
and adds one newly generated raw-versus-potential figure and pointwise CSV.
P06/P07 torque geometry/synthetic plots move to torque; previous real P08/P09
plots are archived and replaced by the new configuration-qualified figure.
D symmetry decomposition is owned by symmetry; D resistance/angle/error
fingerprint/speed illustrations remain in identifiability. Unused copied
figures and obsolete table dumps were removed from active folders.

The polynomial benchmark, exact P1 mesh integration, potential spline solver,
dataset I/O and publication plotting now live once under `shared/python`.
MATLAB canonical I/O lives under `shared/matlab`. Papers retain their local
experiments, result JSON, figure data, publication figures and bibliographies.
No active paper requires a local MeasEval installation or full raw MAT file.

The ZIP proposed five active papers and two concepts and warned that it lacked
the root writing guide/shared build. It was inspected and used as structural
material. Its copied raw data, stale real results, broad repeated foundations,
unverified build claim, and old scope metadata were not adopted as authority.
New definitions use canonical commands/glossary/styles. Bibliographies were
trimmed to actual citations and companion titles updated to active drafts.

## Dataset and importer decisions

See `datasets/README.md` for 51-file inventory, exact CI hashes, synthetic
speed/temperature lineage exclusions, machine-code evidence, eight exports,
candidate torque comparison, configuration diagnosis and remaining limits.
Data publication permission was explicitly supplied during this task.

Current MeasEval raw import is split between `adapter.matfile.MeasurementFiles`
and `DataConversion`. There is no current class/file named `RawDataImport`.
The former reads raw MATLAB measurement structs; the latter normalizes names,
aggregates by counter, optionally removes outliers, and retains numeric
signals while dropping channel metadata. No small canonical OP exchange
format existed there. Its downstream fallback/availability checks do not
constitute scientific calibration.

An opt-in `adapter.canonical` boundary was added in MeasEval with
`importCanonicalDataset` and `exportCanonicalDataset`, plus a three-row
transport fixture and round-trip/corruption test. This boundary receives an
explicit interpreted table/manifest instead of silently canonicalizing raw
physics inside `DataConversion`. The same version-1 MATLAB reference functions
are independently shipped in Research; there is no cross-repository runtime
dependency. The adapter is outside the production loading/calculation path.
Existing unrelated MeasEval documentation edits were preserved.

## Build and preservation

`build_all.ps1` already enumerates direct `papers/*/main.tex` files. The actual
migration therefore updates its active set without a hard-coded name list;
the archive is naturally excluded. `check_publication_content.py` validates
reachable inputs, graphics, duplicate labels, references and citation keys.
The architecture gate still rejects paper-local notation/styles/frameworks.
All twelve active documents build. Numerical and visual QA are recorded in
`portfolio_completion_report.md`; the archive remains a historical source
snapshot rather than another maintained omnibus manuscript.
