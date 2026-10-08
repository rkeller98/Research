# Portfolio consolidation — 7 October 2026

The two composite flux manuscripts have been replaced in the active build by
five papers with separate questions. Their current scientific source and
results remain in `_archive/composite_papers/`: all 155 files in its source
snapshot pass SHA-256 preservation checks. The split includes the pending
torque extension present before migration. The ZIP was inspected as a proposal;
the current repository, writing guide, data and actual importer were authoritative.
The detailed section/figure/result mapping is in `paper_portfolio_migration.md`.

## Every active paper

Page counts include contents, glossary and references in the final all-paper build.

| Paper | Research question and central contribution | Pages | Changes and evidence |
|---|---|---:|---|
| `flux_correction_symmetry` | Which flux components does reflection observe and project? Complementary parity channels and the closest admissible pair, including unequal-weight interpretation. | 7 | Rewritten scope, independent projection derivation, measured-coordinate mirror support and explicit correction boundary. PSM original 2500-rpm lineage, 30/70°C references; 142/158 and 144/158 supported positive-q pairs. Raw, mirror, projected and removed values are exported separately. |
| `magnetic_coenergy_consistency` | Can measured flux be the gradient of one potential? Reciprocity and circulation, coordinate counterexamples and exact interpolant integration. | 9 | Retains potential/path/Hessian intuition; new P1 triangulation, independent clipped-area Green check and geometry sensitivity study on the same PSM lineage. Path disagreement RMS 1.064/0.933 J; independent integration discrepancies below 8.2e-15 J. This certifies the interpolant calculation, not true machine error. |
| `flux_correction_coenergy` | How can inconsistent samples be reconstructed in a common potential class? Gauge-fixed even B-spline gradient fitting with curvature regularization. | 9 | Original controlled synthetic regression retained with shared solver/model; new real spatial tuning fold: 267 training, 73 withheld, 61 inside training hull. Potential fit has zero parity/curl by construction but 2.713 mWb tuning RMS, versus 0.573 mWb independent fit. No true-flux superiority is inferred. Pointwise raw/fit/residual CSV retained. |
| `torque_flux_consistency` | Can independently measured stationary torque regularize spatially implausible dq-flux-map structure while allowing one nuisance offset per comparable operating condition? Global minimum-change regularization with a smooth scalar co-energy correction; local rank-one observability is retained as the identifiability limit. | 13 | Known-truth recovery, 58 observability checks and a qualified two-speed demonstration. Synthetic flux RMSE falls from 4.636 to 1.893 mWb and centered torque-residual RMS from 1.884 to 0.211 Nm; the injected radial null component remains unchanged. On the real Selector-1 fixture, total kT=3p=12 and shared correction reduces centered residual RMS from 0.386/0.515 to 0.317/0.458 Nm at 1000/3000 rpm. CAN calibration and the loss model remain open qualifications. |
| `flux_error_identifiability` | Which measurement-error directions can flux residuals distinguish? Exact and linear transformations, coordinate relabeling, rank/conditioning and nuisance confounding. | 17 | Original symbolic and numeric derivations retained. Multi-speed support is matched at 83 common current points. The pointwise inverse-speed resistance-equivalent fit leaves 0.352 mWb RMS and only 0.064 correlation; the physically scaled nuisance matrix has rank 5/6 and non-null condition number 2481. Resistance versus proportional voltage error is unidentifiable, offsets are weakly identifiable, and terminal versus magnetic current is unidentifiable without another channel. |
| `psm_voltage_geometry` | How does the stationary voltage limit shape the current plane? Affine/quadratic geometry, centers, principal directions and operating regions. | 14 | Existing scientific source retained; rebuilt with shared notation. Evidence remains its analytic linear-machine derivations and geometric examples, rather than the new measured fixtures. |
| `eesm_voltage_geometry` | How does excitation extend voltage geometry? Rank, nullspace, projected slices, torque surfaces and boundedness qualifications. | 12 | Existing source retained and rebuilt. Analytic linear EESM model and constructed geometry; no new experimental validation claim. |
| `gradient_iso_reconstruction` | What can sparse samples reveal about local directions and level sets? Simplex derivatives and iso reconstruction with a stated boundary between geometry and confidence. | 14 | Existing source retained and rebuilt. Existing synthetic/reference checks and documented Python/MATLAB comparison remain its evidence; this task does not turn confidence scores into calibration. |
| `n_dim_rootri` | How can isocontours be extracted in N dimensions from point clouds? Delaunay edge intersections and interpolation. | 5 | Existing derivation, examples and code retained; rebuilt. No new machine-data claim or new benchmark added. |
| `recursive_qp_within_simplex` | How can a quadratic objective be minimized within a simplex? Recursive interior/boundary minimization for local copper-loss optimization. | 3 | Existing algorithm and example retained; rebuilt. The new flux experiments do not validate production control performance. |
| `iemdc_digest_2024` | How can air-gap reluctance and concentrated winding distributions be constructed analytically? Node-specific overlap and an alternative winding construction. | 6 | Historical conference digest retained and rebuilt, with its original geometric derivations and illustrations. It has no connection to the new torque calibration question. |
| `temp_eesm_Mopt` | How can geometry organize constrained synchronous-machine torque optimization? Domain/model/conormal coordinates and constraints before multipliers. | 85 | Existing extended working draft retained and rebuilt. Its analytic/geometric models and existing numerical examples remain separate from the five flux papers; this consolidation is not a new experimental validation or shortening of that draft. |

The independent-reference umbrella and Hessian parameter-derivation ideas
remain in `concepts/`. Neither has enough separate reference evidence to
justify another active paper. The five new manuscripts have been read through
after the split; their titles, abstracts, transitions, figures, interpretations
and limitations now follow their own questions. Used bibliographies are trimmed,
and companion entries identify unpublished drafts rather than invented publications.
Necessary definitions remain locally readable; the polynomial model, spline
solver, exact mesh integration, plotting and dataset transport are shared.

The subsequent [structural cleanup](final_cleanup.md) records current historical
paths and fresh validation separately; the scientific evidence below is retained.

## Raw data, lineage and tests

The inventory contains 51 MAT files, 290,715,194 bytes, and 36 distinct raw
file hashes. File-level machine classifications are 40 PSM, 5 ASM, 3 EESM and
3 unknown. These counts include aliases and fixtures and are **not** counts
of independent machines or campaigns. `datasets/raw_inventory.json` records
channel presence, metadata, configuration, ranges and hashes for every file.
`datasets/lineage.json` records exact duplicate groups and signal comparisons.

Actual MeasEval fixtures, loaders, enum and assertions were inspected at
revision `2294be6ddbc3f85c5b7bfbb30cd76e2529adc9ce`. All six fixture files
match their local CI copies by SHA-256: Test1 is reduced EESM; Test2 is the
two-file Porsche/PSM merge; Test3 is PSM; Test4 is the two-file ASM set.
Test1/Test2 characterization assertions verify machine/configuration constants.
The CI extraction and surrogate pipeline also explain grouping, variant
handling and missing-value fallbacks. These tests support lineage and software
behavior; they do not certify sensor calibration or the magnetic model.

The PSM original and 2500-rpm variant have 226 equal numerical channels despite
different MAT formats. The 1500 variant changes only six speed/angle channels;
220 others, including currents and torque, are unchanged. They cannot be used
as independent speed experiments. Merge CI/root/Porsche copies are aliases.
The Porsche temperature variant edits its reference rather than measuring a
new thermal campaign. Files named negative-rpm can contain positive requested
speed. The artificial torque workspace duplicates a parent recording, includes
an identical workspace alias, and lacks machine type; it is excluded from
independent evidence. Persistent audit scripts reproduce these checks.

EESM has excitation slices but lacks excitation flux and an explicit phase
selector; full three-current reciprocity and a guessed torque coefficient are
not justified. ASM requires recorded electrical frequency including slip and
rotor-state qualifications. It cannot inherit a PSM current-only storage model.
Outlier is a reduced stress fixture; held CAN samples in quiet datasets do not
establish independent precision. See the catalog and candidate audit for the
complete source-by-source qualifications.

## Torque convention and quantitative status

Multi-RPM is the primary configuration diagnostic because it supplies current
direction coverage, both torque signs, complete voltage/current channels,
explicit phase configuration and two actual speed slices. The recorded
selector 1 is interpreted by MeasEval as two three-phase systems at 180°.
Its amplitude-invariant per-system dq representation is supported by the
phase-RMS/dq-magnitude ratio near 0.706. For equally represented systems:

\[
 M_{\rm total}=2\frac32p(\psi_di_q-\psi_qi_d),\qquad k_T=\frac62p=3p=12.
\]

The historical coefficient 6 omitted the second contribution. On the same
216 current-qualified OPs, torque RMS discrepancy changes from 19.7127 Nm
to 1.2122 Nm. At requested 1000/3000 rpm the respective torque RMS values are
0.9576/1.4271 Nm; normalized flux RMS is 1.5419/2.6696 mWb. Each slice contains
109 OPs, of which 108 meet the current threshold. These are newly computed
from unchanged CAN values and recorded mean electrical speed, with no gain fit.

The torque convention is now a prerequisite to, rather than the main result
of, the torque paper. The reader and CAN-source selection transport the numeric channel unchanged.
Raw CAN unit metadata is empty; software's Nm semantics are not a transducer
certificate. Voltage/power-analyzer zero channels cannot certify power or
line/phase scaling. Pole pairs alone cancel between kT and electrical speed
in requested-speed flux inversion, so changing p is not a factor-two remedy.
RMS/peak and power-invariant alternatives do not explain the recorded two-system
configuration. Sensor gain, shaft location, gear ratio, unequal system loading,
voltage errors and mechanical/magnetic losses remain unqualified contributors.
The leading scale disagreement is explained; quantitative signal comparison
is possible, but calibrated electromagnetic flux-error validation remains
conditional.

The revised experiment therefore fits a shared, smooth, gauge-fixed scalar
co-energy correction over both speed slices while estimating a separate
constant residual offset per speed. It is a regularized consistency
representative, not a claim of true flux. The centered residual RMS changes
from 0.386 to 0.317 Nm at 1000 rpm and from 0.515 to 0.458 Nm at 3000 rpm.
A speed-only correction worsens the held-out speed in both directions, so the
real result does not establish a speed-invariant physical correction. The
synthetic known-truth case establishes recoverability only for the
torque-visible component under the stated smoothness/change prior; its
torque-null radial component is deliberately preserved.

The issue-by-issue exit-criterion audit, evidence paths and ready-to-post
closure comments are recorded in `research_epic_completion.md`.

## Canonical data and import/export boundary

Version `research-operating-points-v1` uses UTF-8/LF CSV with 17-digit double
precision and empty missing values, plus an ordered-column JSON manifest bound
by SHA-256. The schema describes machine, relative source/hash, units, dq and
torque conventions, signs, scaling, grouping/filtering, known limitations and
rights. The repository owner's permission covers derived-data publication;
the manifest does not invent a third-party license. Raw data remains local.

| Dataset | OPs | CSV bytes | Manifest bytes | Role |
|---|---:|---:|---:|---|
| `psm_dual_system_multirpm` | 218 | 116,834 | 7,451 | Torque convention and measured support |
| `psm_temperature_2500` | 680 | 368,810 | 7,435 | Symmetry, consistency and reconstruction |
| `eesm_excitation_reduced` | 1,856 | 988,464 | 7,454 | Excitation-aware reference fixture |
| `asm_500rpm_set1` | 152 | 84,742 | 7,434 | Slip/state-aware reference fixture |
| `asm_500rpm_set2` | 88 | 49,382 | 7,431 | Second ASM measurement file |
| `psm_merge_4000_part1` | 328 | 186,411 | 7,441 | Merge lineage and diagnostic comparison |
| `psm_merge_4000_part2` | 208 | 119,061 | 7,441 | Second merge file |
| `psm_outlier_stress_60c` | 320 | 184,881 | 7,505 | Deterministically reduced stress case |

The eight CSVs total 2,098,585 bytes and their manifests 59,592 bytes. The
larger raw inventory is metadata only, below one MB. No new versionable file
exceeds two MB; no LFS or raw MAT payload was added. Grouping retains requested
labels, measured means, selected medians, deviations and finite counts. It
does not fit torque, delete residual outliers or infer settling windows.

The current MeasEval has no class/file named `RawDataImport`. Raw loading is
`adapter.matfile.MeasurementFiles`/`load_measurement`; signal-only aggregation
is `DataConversion`. Its metadata loss and fallback semantics are documented
in `technical/flux_dataset_boundary.md`. An opt-in
`SourceCode/+adapter/+canonical/` package was added in that checkout with
`importCanonicalDataset`, `exportCanonicalDataset`, a three-row transport
fixture and checksum/round-trip test. The production route is unchanged.
Unrelated existing documentation edits in MeasEval were preserved.

Research supplies independent reference MATLAB functions in `shared/matlab`
and Python functions in `shared/python/canonical_dataset.py`. Unchanged
MATLAB manifests preserve original JSON bytes so null and empty-array
distinctions survive; deliberate metadata changes require rebuilding the
manifest. Research evaluation needs the pinned Python dependencies and the
existing TeX `kpsewhich` used for the canonical palette, but no MATLAB runtime,
raw dataset or installed MeasEval checkout.

## Verification and remaining limits

| Check | Result |
|---|---|
| All-paper build | All 12 active papers build with the existing auto-discovery script; archive excluded |
| LaTeX logs | No unresolved citations/references, multiply-defined labels, overfull/underfull boxes or LaTeX/package warnings |
| Structure and shared architecture | All 12 pass input/figure/label/citation resolution and the canonical architecture gate |
| Visual QA | All pages of the five changed manuscripts reviewed; title/end/glossary pages of the seven retained documents checked after shared changes |
| Original fitting and identifiability regressions | Passed; original synthetic cases and formulas retained |
| Torque regression | All 58 checks passed, including the original 40 |
| Archived audits | Original symbolic, co-energy and observable assertions passed, with outputs isolated in ignored temporary directories |
| Python transport | All eight fixtures pass formal JSON schema, exact values and byte round-trip, checksum rejection and relative-provenance checks |
| MATLAB transport | All eight fixtures pass exact double, CSV-byte and manifest round-trips in R2025b |
| MeasEval opt-in adapter | Exact round-trip and corruption rejection passed; existing torque-source semantics test also passed |
| Raw re-extraction | All 16 CSV/manifest files byte-identical to the committed candidates |
| Portable scientific reproduction | 16 reports/figures/tables/pointwise outputs reproduce byte-for-byte |
| Source preservation | All 155 scientific source/result hashes match the archive snapshot |
| Git payload | No MAT, cache or temporary LaTeX files in the versionable payload; raw-directory ignore retained |

MATLAB startup emits warnings about pre-existing obsolete directories in the
local user path; the transport tests pass. Matplotlib/font tooling reports
old font timestamps; its generated publication figures are deterministic and
the final LaTeX logs are clean. Neither warning was hidden by changing user
configuration. Full MeasEval production tests were not rerun for this opt-in
transport adapter. Real calibration, uncertainty and storage-coordinate
qualification remain scientific limitations explicitly stated in the papers.

The repository remains on its existing branch. Changes were prepared locally;
no commit or push was performed by this task. Historical MAT blobs remain
recoverable in Git history and local ignored archival copies. Their active
tracked paths are removed rather than rewriting history. Historical archive
prose is preserved verbatim; active datasets and evaluation have no private
absolute-path dependency.
