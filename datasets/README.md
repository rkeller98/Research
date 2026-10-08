# Portable research measurements

The separate [historical DAT exports](historical_exports/README.md) preserve
former sandbox data whose source/fit recipes are incomplete. They are outside
the canonical v1 fixture contract and are not independent validation evidence.

The eight versionable fixtures contain operating-point means, not raw time
series. Derived-data publication was explicitly authorized by the repository
owner on 7 October 2026. This does not invent a third-party license. Full raw
MAT files remain local and ignored; no LFS is required. Each manifest binds its
CSV with SHA-256 and identifies relative raw sources, field meanings, aggregation,
conventions, uncertainties and limits.

## Catalog

| Dataset | Machine / configuration | OPs | CSV bytes | Purpose and torque qualification |
|---|---|---:|---:|---|
| `psm_dual_system_multirpm` | PSM, selector 1: two three-phase systems, p=4; 1000/3000 rpm; 70°C reference | 218 | 116834 | Primary torque/configuration demonstration and identifiability support. Total kT=3p=12 with equally represented systems; CAN calibration and losses remain unverified. |
| `psm_temperature_2500` | PSM, selector 0: three-phase, p=3; 2500 rpm; 30/70°C references | 680 | 368810 | Primary symmetry, co-energy consistency and reconstruction. CAN is often held across logger records; small repeat SD is not a calibration certificate. |
| `eesm_excitation_reduced` | EESM, p=4; 2250 rpm; excitation requests 3/6 A | 1856 | 988464 | Fixed-excitation stator demonstrations and multi-state regression. Phase selector and temperature references are absent, so torque factor is missing. Excitation flux is absent: full three-current reciprocity is not testable. |
| `asm_500rpm_set1` | ASM, selector 0, p=2; 500 rpm; 39.5°C reference | 152 | 84742 | Induction-machine import/state regression. Electrical speed includes slip; do not substitute mechanical rpm*p or apply a PSM current-only storage model. CAN uncalibrated. |
| `asm_500rpm_set2` | Same ASM configuration, second measurement block | 88 | 49382 | Companion coverage block; same campaign, not evidence of independent machine replication. |
| `psm_merge_4000_part1` | PSM, selector 1, p=3; 4000 rpm; 40°C reference | 328 | 186411 | Test2 merge/overlap regression and difficult torque comparison. Small typical repeat SD coexists with large map/CAN disagreement and some outliers. |
| `psm_merge_4000_part2` | Same two-system PSM campaign, second block | 208 | 119061 | Merge/state coverage; do not treat Test2 or Porsche aliases as independent measurements. |
| `psm_outlier_stress_60c` | PSM, selector 0, p=3; 2000 rpm; 60°C reference | 320 | 184881 | Stress case only: uniformly spaced sorted OP groups from the 60°C slice. No torque residual deletion. Reduced support is unsuitable as a primary precision or original full-map path benchmark. |

All figures are reproducible from these fixtures alone. Approximate or missing
units are qualified in the manifest: `Nm` for CAN follows MeasEval's signal
semantics, while the raw unit strings are often empty. No sensor certificate,
gear ratio, mechanical-loss map, or true magnetic flux was found.

## Raw inventory and verified lineage

`raw_inventory.json` records all 51 MAT files (290715194 bytes), 36 distinct
file hashes, actual channel names and selected numeric ranges/missingness.
The file-level counts are 40 PSM, 5 ASM, 3 EESM and 3 unknown; they include
aliases and are **not counts of independent measurements**. Machine code
`Machine_type` is interpreted through MeasEval's `eMachineType` enum: 1 PSM,
2 IM/ASM, 6 EESM. The three old torque/workspace exports lacking that channel
remain unknown rather than inheriting a filename or a product default.

`lineage.json` verifies exact duplicate groups and cross-format numeric
comparisons. `measeval_test_evidence.json` also checks the actual external
Test1–Test4 files against the local CI copies at the recorded MeasEval commit:

| Test | Evidence and aliases | Classification |
|---|---|---|
| Test1 | `EESM_Measdata_Reduced`; characterization asserts machine code 6, p=4, Rs=0.0366185 Ω; actual excitation varies | EESM |
| Test2 | Merge1=Matlab_031, Merge2=Matlab_032; characterization asserts machine code 1 and phase selector 1 | Two-system PSM |
| Test3 | `PSM_Measdata`, numeric code 1 and selector 0 | PSM |
| Test4 | ASM Set_01 Matlab_005/006, numeric code 2 and selector 0 | ASM |

The extractors call `ci_extract_measdata_model`, which summarizes root
description, X and Y metadata and numerical channels. The surrogate end-to-end
tests load each MAT, run `DataConversion`, `VariantHandling`, and missing-value
normalization; they do not independently certify physics. Availability checks
based on signal amplitude merely identify a nonzero channel.

`PSM_Measdata` and its 2500-rpm v5 copy have all 226 numeric channels equal.
The 1500-rpm variant has 220 equal channels and changes only six speed/angle
channels. Both aliases are excluded as independent speed experiments.
The Porsche multi-temperature variant changes only `Rotor_temp_ref` while
267 other channels stay identical. The two files named `WW_Dataset_neg_rpm_*`
are byte-identical to Mahle originals whose requested speed is **positive**
2000 rpm. The full Outlier source has an exact long-filename alias and a
separate filtered variant; neither is another campaign.

`artificial_fixture_audit.json` inspects the old FakeForTesting MAT workspace:
its named measurement and `raw_data` alias are numerically identical, and
many channels repeat the parent twice. The artificially edited 604-record
fixture and negative-speed edits are excluded from independent experimental
evidence. The reader follows MeasEval's uniquely named `Matlab*` root rather
than accidentally selecting a saved workspace alias.

## Extraction and format

First inspect the importer/test semantics, then choose a portable OP boundary.
The existing format is a MATLAB measurement struct (`Info`, `Description`,
`X`, `Y`), not a small canonical interchange format. MeasEval's current
signal-only conversion loses raw channel metadata. We therefore use CSV plus
JSON, with a JSON Schema in `schema/operating_points_v1.schema.json`.

CSV is UTF-8/LF, comma-separated, numeric double values in 17 significant
digits, with empty missing values. Column order is explicit in the manifest.
JSON records IDs, raw hashes, exporter/schema versions, units/source fields,
phase/dq and torque qualifications, filter/grouping steps, limitations and
rights. Manifest schema validation is supplemented by matrix shape, column,
path and checksum validation in the Python/MATLAB readers.

The deterministic grouping keys are requested rpm, requested excitation,
rotor-temperature reference and positive measurement counter. This prevents
reused counters from mixing state slices. Required voltage/current/electrical
speed values must be finite. Each group retains means, selected medians, sample
SD (`ddof=1`) and finite-channel counts. It does not silently erase outliers,
zero torque, or infer a settling interval. Stored average channels and logger
records may be correlated. Zero-only rotor-temperature measurements are
disconnected placeholders and become missing; temperature **references** remain
distinct from measured temperatures.

Flux is inverted from group-mean voltage/current/Rs using mean
`PE_w_el_rad_avg`, not requested mechanical speed. It is a reconstructed
terminal field, not direct flux ground truth. Torque gain remains one. Selector
0 gives 3p/2, selector 1 gives 3p for the two-system total, selector 3 gives 5p/2;
missing or otherwise unresolved configuration leaves kT missing. Selector 2's
additional product pole correction is not generalized without a physical
convention audit.

With Python dependencies from `requirements-research.txt`, run from any working
directory using the repository scripts and an explicitly supplied raw root
that contains `Flux/` and `Trq/`:

```powershell
python scripts/inventory_measurements.py <raw-root>
python scripts/audit_data_lineage.py <raw-root>
python scripts/audit_fixture_evidence.py <raw-root> --measeval-root <measeval-repo>
python scripts/extract_research_datasets.py <raw-root>
python scripts/audit_torque_candidates.py <raw-root>
python scripts/evaluate_portfolio.py
python scripts/test_research_datasets.py
```

Only the first five commands require raw data. The optional fixture audit also
uses the explicitly supplied MeasEval checkout to compare CI copies. On the current machine the raw
root is the nested ignored `Test_Daten/Test_Daten`, but that path is a CLI input,
not an installed dependency. `load_dataset(id)` in
`shared/python/canonical_dataset.py` validates and loads the portable fixture.
MATLAB's independent `shared/matlab/importCanonicalDataset.m` and
`exportCanonicalDataset.m` transport the same contract. Run
`test_canonical_datasets(repoRoot)` after adding the repository `scripts` folder.
Unchanged MATLAB imports preserve original manifest bytes, including JSON nulls;
editing metadata requires deliberately rebuilding its manifest because MATLAB
structs do not preserve every null/empty-array distinction.

## Torque diagnosis

The previous Multi-RPM factor-two discrepancy omitted the second three-phase
system. Its stored selector 1, importer configuration and amplitude-invariant
RMS relation support total kT=3p=12 for p=4. The CAN/raw map ratio becomes near
one without fitting a gain. On the current-qualified support the discrepancy
RMS falls from 19.7127 Nm with kT=6 to 1.2122 Nm with kT=12.
See `torque_candidate_audit.json` for all compared candidates and exclusions.

This is a configuration explanation, not calibrated electromagnetic validation.
The field-level reader applies no factor or unit conversion, and MeasEval's
CAN torque source transports the numeric channel unchanged. Current RMS/dq
magnitude near 1/√2 supports per-system peak coordinates; voltage/power channels
that are identically zero cannot verify power or line/phase scaling. Pole pairs
alone cancel in kT/omega for requested-speed inversion. Offset, remaining
voltage errors, unequal represented systems, shaft losses and transducer
calibration remain open contributors to the smaller residual. They are not
corrected by choosing another arbitrary multiplier.

Multi-RPM is the primary configuration diagnostic because it combines explicit
phase configuration, two actual speed slices, current-direction coverage,
complete voltage/current signals, both torque signs and usable repeat scatter.
Quieter CAN records elsewhere can be held values; merge files have substantial
systematic discrepancies; EESM lacks phase configuration; ASM requires slip and
state qualifications. Outlier remains a stress case. No fixture is called a
calibrated electromagnetic torque reference.
