# Research Epic #1--#4 completion audit

This audit maps every requested exit criterion to versioned evidence and
contains concise issue comments ready for posting. The GitHub API was
unreachable in the execution environment on 7 October 2026, so the issues were
not remotely commented on or closed by this run.

Scientifically, all listed exit criteria are satisfied. Repository-side QA
passed for the standalone torque experiment, the complete portable portfolio
evaluation, architecture/content checks, deterministic artifacts, finite
JSON/CSV values, clean builds of the four changed papers and visual inspection
of every changed PDF page. The environment did not provide the optional
`jsonschema` and `sympy` packages, so the dataset-schema script and the older
symbolic identifiability script could not be rerun here. The default LuaLaTeX
all-paper command was also blocked by an unwritable external font cache;
PDFLaTeX built every changed paper, while its all-paper fallback reached the
unmodified extended `temp_eesm_Mopt` draft and exhausted TeX memory.

## Exit criteria

| Issue | Exit criterion | Evidence | Assessment |
|---|---|---|---|
| #2 | Sign convention explicit and consistent | `flux_correction_symmetry` gives the voltage signs; `flux_error_identifiability` defines used-minus-true $\varepsilon_R=\hat R_s-R_s$ and correction sign | satisfied |
| #2 | Synthetic resistance mismatch reproduced | Portfolio evaluator: 20 m$\Omega$ at 1000 rad/s reproduces both parity residuals within $3.4\times10^{-21}$ Wb | satisfied |
| #2 | Confounders demonstrated | Current-proportional voltage error has the identical flux perturbation | satisfied; resistance itself unidentifiable |
| #2 | Full-map and selected-region behavior | `flux_correction_symmetry/numerics/real_evaluation.json` reports all-positive-q and 10%-threshold support at 30/70 $^\circ$C | satisfied |
| #2 | Identifiable boundary explicit | Projection identifies forbidden parity components only; “resistance-equivalent” is retained | satisfied |
| #3 | Affine conservative field gives zero curl/circulation | `magnetic_coenergy_consistency/numerics/real_evaluation.json`, `synthetic_checks` | satisfied to roundoff |
| #3 | Nonlinear conservative interpolation artifact quantified | Same report: $9\times9$ P1 curl RMS 0.01287 and path artifact $2.25\times10^{-4}$; refinement behavior stated | satisfied |
| #3 | Pure resistance mismatch analytically reproduced | Same report: 20 m$\Omega$/1000 rad/s gives 40 $\mu$H curl and $1.68\times10^{-5}$ J circulation | satisfied |
| #3 | Local/integrated quantities and support separated | Triangle curl/conditioning and exact path/independent Green integration are reported separately | satisfied |
| #3 | Physical interpretation bounded | Paper distinguishes terminal from magnetic current, interpolation and loss branches | satisfied |
| #4 | Operating-point support matched | 104 common requested labels; 83 points inside both measured-current hulls; maximum pre-interpolation mismatch 0.759 A | satisfied |
| #4 | Inverse-speed prediction tested pointwise | `figures/data/multispeed_pointwise.csv`: fitted 1.124 m$\Omega$, observed/residual RMS 0.362/0.352 mWb, correlation 0.064 | satisfied; sole mechanism is weak |
| #4 | Nuisance mechanisms modeled | Resistance, exact proportional-voltage confounder, two voltage offsets and two flux offsets | satisfied |
| #4 | Rank/conditioning physically scaled | 10 m$\Omega$, 10 mV/A, 0.1 V and 1 mWb scales; rank 5/6; nonnull condition 2481; row scale disclosed as non-covariance | satisfied |
| #4 | Identifiability classified | Resistance/drop exact-unidentifiable; voltage/flux offsets weak; restricted combined directions conditional | satisfied |
| #4 | Terminal versus magnetic current evaluated | No magnetic-current or iron-loss channel exists; classified unidentifiable rather than assumed | satisfied |
| #1 | Derivations, synthetic evidence, real diagnostics, rank and local/integrated tests | Five owning papers and `paper_portfolio_migration.md` | satisfied |
| #1 | Numerical/model/physical interpretation separated | Every owner states the boundary; low residual is never called true flux | satisfied |
| #1 | Publishable notes | Five active papers use canonical shared infrastructure; the four changed PDFs pass source, log and visual QA | satisfied |

## Ready-to-post issue comments

### #2

Completed in `papers/flux_correction_symmetry`. The paper fixes the
used-minus-true resistance sign, reproduces the 20 m$\Omega$ synthetic pattern,
demonstrates the exact current-proportional-voltage confounder, and reports
full-map and selected-region behavior. Reproduce with
`python scripts/evaluate_portfolio.py --save-only` and
`pwsh -File scripts/build.ps1 flux_correction_symmetry`. Limitation: symmetry
identifies forbidden components and a resistance-equivalent pattern, not
physical resistance or a unique cause.

### #3

Completed in `papers/magnetic_coenergy_consistency`. Affine conservation is
zero to roundoff; nonlinear conservative P1 artifacts and pure-resistance curl
are quantified; local metrics are separated from exact path/Green tests with
support and conditioning. Reproduce with
`python scripts/evaluate_portfolio.py --save-only` and
`pwsh -File scripts/build.ps1 magnetic_coenergy_consistency`. Limitation: the
result concerns a terminal-current interpolant and cannot identify magnetic
nonconservativity or its cause.

### #4

Completed in `papers/flux_error_identifiability`. The real two-speed support is
matched, inverse-speed resistance is tested at 83 points, and a physically
scaled six-column nuisance design is classified. Reproduce with
`python papers/flux_error_identifiability/numerics/validate.py`,
`python scripts/evaluate_portfolio.py --save-only`, and
`pwsh -File scripts/build.ps1 flux_error_identifiability`. Limitation:
resistance and current-proportional voltage error are exactly confounded, and
the dataset has no magnetic-current channel.

### #1

The five-paper portfolio supplies derivations, counterexamples, portable real
diagnostics, rank analysis, local/integrated tests and explicit interpretation
boundaries. The refocused `torque_flux_consistency` adds the missing independent
torque regularization: group offsets remain free, the map correction is global,
and observability is the limit rather than the thesis. Reproduce with the
paper-specific commands and `pwsh -File scripts/build_all.ps1`. Limitation: no
portable fixture is calibrated true flux or certified electromagnetic torque.
