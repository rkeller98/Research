# On the Interpretation of Symmetry Residuals in Experimental dq Flux-Linkage Maps

Read [WRITING_GUIDE.md](../../WRITING_GUIDE.md) first. This independent academic
draft analyzes the spatial, thermal-reference and speed dependence of forbidden
symmetry components in two supplied test-bench datasets. A resistance-equivalent
residual is a conditional diagnostic, not an identified winding resistance.
No product workflow or experimental magnetic field fitting is included.

## Reproduce from the repository root

Requirements: Python 3, NumPy, pandas, SciPy, h5py, Matplotlib; NumPy and SymPy
for the retained synthetic checks. Version details and SHA-256 input/script
hashes are recorded in `figures/data/experimental/*_results.json`.

```powershell
python papers/flux_map_error_diagnostics/python/analyze_outlier_dataset.py --no-plots --export
python papers/flux_map_error_diagnostics/python/analyze_multi_rpm_dataset.py --no-plots --export
python papers/flux_map_error_diagnostics/numerics/validate.py
./scripts/build.ps1 flux_map_error_diagnostics
./scripts/build_all.ps1
```

Run both experimental exports before the build. Without `--no-plots` the original
interactive figures remain available. The publication figures use exported DAT
values and Python-generated PGFPlots drawings, rendered as vectors by LaTeX.
Canonical colors, markers, axes and typography live in `shared/`.

`raw_ww_data_importer.py` only exposes named HDF5 signals. `flux_correction.py`
contains the preserved reconstruction/pairing/equivalent-residual calculation.
`analyze_outlier_dataset.py` compares rotor references at fixed requested speed;
`analyze_multi_rpm_dataset.py` compares speeds at fixed rotor reference.
`export_experiments.py` exports their results and the requested direct speed check;
it performs no magnetic fit, missing-partner interpolation or outlier removal.

Defaults: requested speed is the reconstruction breakpoint; requested-current
keys are rounded to 0.01 A; measured electrical quantities are never rounded.
Equivalent residuals require measured pair magnitude strictly above 10% of the
slice maximum. High-current summaries include magnitudes at or above 85%.
Raw MAD is unscaled and is descriptive spread, not a confidence interval.
Repeated operating-index groups are averaged equally at the requested-key stage.

The outlier file uses three pole pairs and 2000 rpm at rotor references 40/60/80 C;
the multi-speed file uses four pole pairs and 1000/3000 rpm at a 70 C reference.
They are kept separate. Recorded stator references do not verify actual winding
temperatures, and upstream voltage calibration/acquisition details remain open.

The retained synthetic experiment checks signs, exact coherent rotation,
reciprocity preservation, angle sensitivity, conditional identification and
current-proportional voltage confounding. Its known magnetic helper is reused
unchanged; no companion-paper implementation was started or edited for this task.

The complete results, source positioning, evidence limits, figures and QA record
are in [the experimental report](../../docs/flux_map_experimental_validation.md).
The PDF export is `output/pdf/flux_map_error_diagnostics.pdf`.
