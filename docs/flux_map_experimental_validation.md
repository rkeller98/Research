# Experimental flux-map diagnostics: completion report

## 1. Final title

**On the Interpretation of Symmetry Residuals in Experimental dq Flux-Linkage Maps**.

## 2. Research question

What information is contained in the forbidden symmetry components of experimentally
reconstructed dq flux-linkage maps, and to what extent can a simple
resistance-mismatch hypothesis explain their spatial, thermal, and speed-dependent structure?

## 3. Real datasets and provenance

Both supplied MATLAB v7.3/HDF5 files in the diagnostics paper's `python/` directory
were read through the supplied importer. Dataset hashes and software versions
are in `figures/data/experimental/outlier_results.json` and `multi_results.json`.
The original analyzers were executed before scientific content changes; their
working-tree versions were preserved in ignored `tmp/diagnostics_before/`.
The original importer and `flux_correction.py` remained byte-identical to those
snapshots. No physics bug was found. Changes to the two analyzers add only
`--no-plots` and `--export`; all calculations/defaults are retained.
The exporter adds requested comparisons, numeric tables and vector-figure sources.

Outlier: 2000 rpm, three pole pairs, used resistance 7.695 mOhm.
Multi-speed: 1000/3000 rpm, four pole pairs, used resistance 10 mOhm.
Different pole-pair constants mean these files are not pooled as one machine
calibration; machine identities and acquisition/calibration documentation remain open.
No companion-paper implementation was performed for this task. Concurrent working-tree
changes outside diagnostics are preserved.

## 4–6. Reproduced thermal/speed results and support

All resistance-equivalent values below are in mOhm. OP counts are operating-index
means, not raw samples or unique current geometries. High means measured pair
q-magnitude at least 85% of the slice maximum. Valid means strictly above 10%.
MAD is the raw, unscaled median absolute deviation and is not a confidence interval.

| Experiment | rpm | Rotor ref / C | Samples | OP groups | Keys | Pairs | Valid | High | High median | High MAD | Full valid range |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| outlier | 2000 | 40 | 12882 | 4220 | 4154 | 1172 | 1002 | 79 | 0.096 | 0.128 | [-1.595, 13.989] |
| outlier | 2000 | 60 | 12957 | 4220 | 4154 | 1172 | 1002 | 80 | -0.579 | 0.080 | [-3.370, 12.667] |
| outlier | 2000 | 80 | 12959 | 4220 | 4154 | 1172 | 1002 | 79 | -1.268 | 0.160 | [-3.389, 11.965] |
| multi | 1000 | 70 | 327 | 109 | 104 | 39 | 36 | 6 | -2.157 | 0.189 | [-2.431, 33.912] |
| multi | 3000 | 70 | 327 | 109 | 104 | 39 | 36 | 7 | -5.334 | 1.155 | [-7.541, 28.267] |

Outlier: 48 zero-q keys and 1762 unmatched nonzero-q keys per slice.
Multi-speed: eight zero-q keys and 18 unmatched nonzero-q keys per slice.
Repeated requested keys are averaged equally across OP-index groups. Measured
currents/voltages are never rounded; only requested-current keys use two decimals.
The denominator is `(abs(iq_pos)+abs(iq_neg))/2`, not requested current.
No missing counterpart is interpolated or extrapolated.

Outlier high medians shift 0.096 -> -0.579 -> -1.268 mOhm as rotor reference rises.
The conditional values `R_used - median(delta_R_eq)` are 7.599/8.274/8.963 mOhm;
these are not identified winding resistances. The stator-temperature reference
signal happens to match the rotor reference, but neither confirms conductor temperature.

Multi-speed high medians are -2.157/-5.334 mOhm, with MAD 0.189/1.155 mOhm;
only six/seven pairs contribute. Conditional equivalents are 12.157/15.334 mOhm.

## 7. Spatial structure

Full-valid-region median/MAD at rotor references 40/60/80 C is respectively
1.680/1.576, 0.967/1.531 and 0.250/1.553 mOhm. The high-current spread is much
smaller, but its threshold is empirical and slice membership differs.
The full range, spatial extrema and gaps remain visible without smoothing,
clipping or outlier removal. Both d-odd and q-even residuals are retained.
Outlier RMS `(r_d,r_q)` is (2.013,1.191), (1.746,1.309), (1.728,1.690) mWb.
Multi-speed RMS over all 39 pairs is (0.385,0.974)/(0.206,0.899) mWb.
Full valid median/MAD is 0.269/2.108 and -1.444/1.568 mOhm at 1000/3000 rpm.

## 8. Direct speed-scaling check

The valid common-key inner join contains 36 pairs. The RMS discrepancy of
`r_d_3000 - r_d_1000/3` is 0.157316 mWb; the median discrepancy is 0.103985 mWb.
Observed high-speed residual RMS on those points is 0.213497 mWb.
Measured pair magnitudes differ by at most 0.299551 A across speeds; accounting
for their ratio changes prediction-discrepancy RMS only to 0.157112 mWb.
Pointwise `delta_R_eq_3000 - delta_R_eq_1000`: median -2.621867 mOhm,
raw MAD 1.560261 mOhm, RMS 4.233837 mOhm, range [-15.178282, 2.697946] mOhm.
The scatter and spatial differences retain every common point. These are
model checks without a formal calibrated hypothesis test or fitted causal model.

## 9. Hypothesis interpretation

Spatial nonconstancy and pointwise speed differences weaken H0: one constant
used-minus-true stator-resistance mismatch alone explains the symmetry violation
under a correctly aligned symmetric quasi-static baseline and adequate matching.
A local constant equivalent summarizes part of the outlier data, but does not
prove a physical resistance contribution. Additional speed-dependent or
operating-point-dependent effects are required for a global explanation.
No unique physical decomposition or experimentally justified correction is claimed.

## 10. Causes explicitly not identified

Winding resistance, iron-loss current, angle/timing mismatch, current/voltage
sensor offsets or gains, inverter dead time/semiconductor drops, upstream voltage
reconstruction, frequency-dependent losses, pairing bias and real machine asymmetry
remain alternatives. Rotor/stator references do not establish winding equilibrium.
Measured-current mirror geometry need not mirror magnetizing-current geometry
when iron-loss currents are present. Classical skin depth is not an operating-current
law; effective AC resistance can depend on geometry and field distribution.

Correct prior derivations remain: coherent constant rotation preserves reciprocity
but rotates the reflection axis, angle sensitivity contains `L_diff J i - J psi`,
and a current-proportional voltage error exactly imitates resistance in reconstruction.
The existing known-model synthetic check still passes. Its recovery and correction
results are distinct from the experimental evidence.

## 11. Literature added and verified against primary sources

- [Sun and Xiao (2020)](https://doi.org/10.1049/iet-epa.2020.0137): nonlinear parity, differential cross-inductance reciprocity and saturation; not an implementation in this task.
- [Jebai et al. (2014), author preprint](https://arxiv.org/abs/1403.6641): energy/construction symmetry and reciprocity; baseline explanation only.
- [Richter, Dollinger and Doppelbauer (2014)](https://publikationen.bibliothek.kit.edu/1000045029): matching magnetic states in motoring/generating operation, loss versus magnetizing currents; IEEE DOI 10.1109/ICELMACH.2014.6960401.
- [Varvolik et al. (2022), author institution](https://nottingham-repository.worktribe.com/output/7655353): motor/generator averaging against ohmic and inverter voltage effects; DOI 10.3390/en15062207.
- [Brescia et al. (2023), author institution](https://iris.poliba.it/handle/11589/255520): resistance/flux/inductance/inverter-term estimation from operating conditions; DOI 10.1109/JESTPE.2023.3292526.
- [Krüner and Hackl (2019)](https://doi.org/10.3390/en12050862): measured versus magnetizing/loss current in a PMSM model.
- [Hackl, Kullick and Monzen (2021), author-laboratory record](https://lmres.ee.hm.edu/veranstaltungen/): nonlinear synchronous-machine copper/iron loss context; DOI 10.1109/ICIT46573.2021.9453497.

Existing Liu 2018 and Liu 2017 sources are retained and their titles, authors,
DOIs and publication metadata were checked. Deliberate position-offset injection
is distinguished from unknown-offset diagnosis. Resistance identification itself,
nonlinear parity and motoring/generating averaging are not claimed as new.
The prior companion citation appears only in the outlook.

## 12. Figures and numeric artifacts

Six added reproducible PGFPlots figures, using central styles/palette:

1. `08_experimental_flux.tex`: all flux OP means, both components at all three rotor references.
2. `09_experimental_residuals.tex`: all matched d-odd/q-even residuals and full extrema.
3. `10_experimental_equivalent.tex`: full valid spatial equivalent maps and median/raw-MAD thermal summary.
4. `11_high_current_structure.tex`: all valid equivalents versus relative measured q-current; empirical threshold shown.
5. `12_experimental_scaling.tex`: direct inverse-speed and equivalent-residual equality tests at 36 common keys.
6. `13_experimental_speed_structure.tex`: speed-dependent equivalent scatter and spatial pointwise differences.

The six existing analytical/synthetic figures remain. Python writes full CSV,
PGFPlots DAT, numeric JSON, summary tables and concrete TeX figure sources;
LaTeX renders vector plots. The shared measured-sample styles and signed map
palette are invoked only by the new figures, preserving other plots' defaults.

## 13. Open scientific TODOs

- Verify machine provenance, current/voltage normalization, sensor calibration,
  terminal-voltage reconstruction, averaging intervals and steady-state acceptance.
- Verify actual conductor/stator temperature and equilibrium rather than thermal references.
- Bound requested-key pairing leakage with an independently validated magnetic reference;
  check key/threshold sensitivity before turning this exploration into calibrated inference.
- Obtain more symmetric pairs, independent repeats and calibrated noise/error budgets.
- Separately validate loss, inverter and angle models using additional observables.
- Study local mirror interpolation and correlated uncertainty separately; none is implemented now.
- The complementary magnetic field approximation is reserved for the separate paper;
  no new co-energy/flux-fitting work is part of this task.

## 14. Build and full PDF quality review

Completed on 2026-10-06:

- Both supplied analyzers reproduced their results before manuscript changes;
  both headless exports then completed successfully. Exported script hashes match
  the final scripts. The importer and physical calculation remain byte-identical
  to the arrival snapshots.
- The retained symbolic/numeric validation completed successfully, including
  angle sensitivity, reciprocity, correction signs and the voltage-error confound.
- `scripts/check_architecture.py`, its `--self-test`, and `git diff --check` passed.
- `scripts/build.ps1 flux_map_error_diagnostics` and then
  `scripts/build_all.ps1` completed successfully for all eight registered papers.
  Their final `main.log` files contain no warnings, overfull/underfull boxes or
  missing-character messages. The architecture-smoke fixture is separate from
  those eight paper builds.
- The final diagnostics PDF has 28 pages, twelve vector figures and thirteen
  bibliography entries. All 28 pages were visually reviewed, including equations,
  signs, axis labels, legends, units, captions, glossary and citations. The new
  maps were widened and their inter-panel spacing adjusted; sparse speed-map
  points have outlines so values near zero remain visible. No data clipping or
  smoothing was introduced. Extracted PDF text contains no unresolved `??` tokens.

Final artifact: `output/pdf/flux_map_error_diagnostics.pdf`.
SHA-256: `390dbf71f28cabcd76a9599b3b860296e069ffef8f9d7f9bb54db9eb85c3ec18`.
Scientific open questions in section 13 remain explicit research requirements,
not uncompleted draft production tasks.
