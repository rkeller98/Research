# Torque-Referenced Consistency Regularization of dq Flux Maps

This active paper owns one question documented in
`docs/paper_portfolio_migration.md`. Read `WRITING_GUIDE.md` and the repository
didactic contract before editing. The manuscript loads canonical `shared/`
notation, glossary and visual styles; its bibliography is limited to actual
citations. Archived composites preserve earlier scientific provenance.

## Reproduce from portable fixtures

From the repository root with `requirements-research.txt` installed:

```powershell
python papers/torque_flux_consistency/numerics/torque_consistency.py
python scripts/evaluate_portfolio.py --save-only
python scripts/test_research_datasets.py
pwsh -File scripts/build.ps1 torque_flux_consistency
```

No raw MAT or installed MeasEval is needed. Fixture identities and limitations
are in `datasets/README.md`; the real experiment writes
`numerics/real_evaluation.json`, CSV evidence and figure PDFs. The default
command prints a scientific summary and displays the figures. CI and headless
automation use `--save-only`, which runs the same assertions and writes the
same artifacts without opening windows. Raw measurements, model predictions
and residuals have distinct meanings. Synthetic tests know truth; real
demonstrations do not establish a physical cause or calibration.

The complete source is `main.tex`, `metadata.tex`, `sections/`, `figures/` and
`bibliography/`. The PDF is exported to `output/pdf/torque_flux_consistency.pdf`.
