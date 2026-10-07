# Migration and scientific audit

Source: `C:/Git/Gradienten_Iso_Verfahren`, integrated on 7 October 2026.
The original tree is retained under `legacy/gradient_iso_original` with a
SHA-256 manifest. Generated TeX intermediates and the old virtual environment
are excluded. The original directory has not been modified.

| Historical file or group | Active replacement |
| --- | --- |
| `gradient_iso_pipeline_nd.m` | `python/gradient_iso/core.py`: reconstruction, recursion, iso coverage, search proposals |
| `gradient_iso_pipeline_2d.m` | The same dimension-independent API, with two coordinate columns |
| `get_valid_triangulation_vectors.m`, `get_unique_edges_from_delaunayn.m`, all `delaunay_search*.m` | Existing VICE `PointSet`, `SampledField`, `EdgeIntersector`; unchanged three-module snapshot, no new port |
| Himmelblau, outlier, search and laboratory demos | `python/demo.py`, `python/experiments.py`, `python/figures.py` |
| `paper_ieee/main.tex` and old documentation | Six scientific sections, README, didactic guide and this audit |
| Old `generate_results.py`, tables and CSV files | Archived only; new results use one active implementation |

## Intentional differences

- Source-simplex derivatives use the translation-independent anchored edge
  solve, with recorded condition numbers and inverse-edge norms. The old
  augmented solve had a rank check but no noise-scale diagnostic.
- The edge filter uses RMS length over unique undirected spatial edges,
  matching VICE. MATLAB computed its RMS over simplex-edge occurrences;
  therefore even the same filter factor need not retain identical edges.
- The scoring sum retains all VICE cuts. Vertex cuts retain per-edge
  multiplicity, but there is no repeated copy of an entire edge for every
  incident simplex. Chunking changes memory use, not the Gaussian sum.
- Constant/empty components produce NaN coverage with a status, rather than
  an epsilon score. Constant derivative fields may be exact.
- Ordered mixed partials, the raw Hessian, its symmetric part, the antisymmetry
  defect and trace are exposed separately. Recursion estimates a new field
  at every stage; no general higher-order convergence guarantee is claimed.
- Top-order score transfer always uses support coordinates, not row-count
  equality. Transfer distance is retained. Gradient steps no longer multiply
  an uncalibrated score into a claimed confidence step.
- The old `mean + sigma*std` threshold remains for comparison, with sample
  standard deviation. Raising sigma increases low-score flags; the original
  short-document tuning advice had the direction reversed.
- Synthetic first-order labels follow **all source vertices**. Nearest input
  labels remain in NPZ outputs only to audit the original evaluation choice.
- The earlier Python benchmark capped at 2500 simplices, duplicated shared
  edges, chose an unseeded global pair-distance bandwidth, and averaged only
  32 nearest cuts. It was a different algorithm from MATLAB and its numerical
  results are not reused.

## Interpretation changes

The active paper distinguishes interpolation correctness, derivative accuracy,
iso geometry and confidence calibration. A smooth scalar objective is not
automatically a physical potential. Delaunay does not regularize noisy values.
Laplacian sign does not distinguish a bowl from every saddle. Neither a
convex-hull check nor an attractive plot certifies physical feasibility.

Affine counterexamples, quadratic accuracy/noise checks, full recursive
curvature checks, paired contamination comparisons and actual synthetic
trial gains are reproducible. Seeds are independent realizations; cells
within a realization share data and are not independent validation samples.
The baseline result applies to strong injected jumps, not an industrial
outlier detector. The new low-score iso ranking performs poorly and is
reported as such.

## Backend provenance

The VICE repository revision at initial inspection was
`1ecd269739833ae343e864d91fdeb2d2c5669342`.
`data/provenance.json` contains module SHA-256 hashes and the actual runtime
versions. A parallel edit made the live intersector temporarily syntactically
invalid during validation. The final package therefore imports a pinned,
unchanged three-module snapshot from that Git revision, with only empty
package scaffolds added. The complete experiment suite was regenerated against
the pinned snapshot. Its hashes are in `python/vendor/provenance.json`.
Set `VICE_MEASEVAL_SOURCE` to opt into a live backend. The external checkout's
ongoing edits were not modified or reverted.
