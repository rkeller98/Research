# Former sandbox experiments

`PY_RBF.py` is Jan Oellerich's 2026 weg//weiser RBF example. Copyright and all
four kernels, weight solve, normalization, predictions and gradients remain
unchanged. It clears the terminal and runs an 8012-point dense fit at module
load, so it is not a shared importable library or maintained CLI. Only its
input path now resolves relative to the repository, to
`datasets/historical_exports/Dataset_Raw_vs_Fitted_Flux.dat`.

`flux_correction.py` retains the original one-speed/temperature selection,
requested-speed flux inversion, parity pairing and plots. It is historical
exploratory evidence, not a replacement for the active calibrated-convention
and limitation-aware portfolio evaluation. Its import now finds the unchanged
owner-developed `shared/python/raw_ww_data_importer.py`. Its input is the local
ignored `WW_Dataset_Outlier.mat` beside it, moved from the sandbox without
changing its bytes. No raw payload is added to Git. A fresh checkout requires
that original recording to execute the example.

From any working directory, with the research Python dependencies:

```powershell
python <repository>/_archive/sandbox_experiments/PY_RBF.py
python <repository>/_archive/sandbox_experiments/flux_correction.py
```

The RBF entrypoint prints fit statistics; the flux entrypoint opens plots.
Neither participates in `build_all` or `evaluate_portfolio`. See
[the cleanup audit](../../docs/final_cleanup.md) for the original paths and hashes.
