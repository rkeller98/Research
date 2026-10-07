# Validation record — 7 October 2026

## Numerical and integration checks

- 18 pytest checks passed, including affine fields in 2-D/3-D/4-D, exact
  linear-vector differentiation, Hessian component order, physical scaling,
  row permutations, constant-component behavior, independent Gaussian sums,
  Monte Carlo noise covariance, plateau intersections, circumcenter geometry,
  explicit failure paths, threshold monotonicity and rank-metric ties.
- The two-order 2-D demo completed with 227 first-order and 430 second-order
  representatives. All its trial proposals stayed inside the input hull and
  improved the synthetic quadratic objective in this realization.
- The 4-D demo completed with 617 representatives. About 99.4% of proposals
  stayed inside the hull; about 98.7% of those improved this objective.
  These are demonstration results, not a convergence guarantee.
- The complete experiment/figure script ran against the pinned VICE subset.
  A further complete run reproduced all **11 numerical output files**
  (CSV, NPZ and summary JSON) byte for byte. Generated PDF figure timestamps
  are not part of that deterministic-byte comparison.
- All 24 archived source files matched their recorded SHA-256 hashes.
- All three VICE source blobs matched `python/vendor/provenance.json`.
  `.gitattributes` preserves their byte-level line-ending contracts.

## Publication checks

- The architecture gate and its self-test passed.
- The new paper compiled to 14 pages with LuaLaTeX/Biber.
- Its final log had no LaTeX warnings, undefined references/citations,
  overfull boxes or underfull boxes.
- Every page was rendered and inspected; figures, tables, equation labels,
  source listing, used-symbol appendix and references were reviewed. An
  independent text-block check found no material outside page margins.
- `scripts/build_all.ps1` completed for all nine active papers after the
  shared glossary and Python-listing additions. Existing papers were not
  scientifically revised by this task.

## Scope of evidence

Synthetic derivative accuracy, source-vertex contamination labels and actual
one-step objective gains are separately reported. The recursive Hessian has
substantial clean-data error, and low iso coverage does not reliably rank
contamination in the demonstrated datasets. No confidence calibration,
real-machine validation, higher-order convergence theorem or controller
acceptance guarantee is claimed.

The original directory and parallel edits to the external VICE checkout were
preserved. Pre-existing changes in the flux-map audit files were not edited.
