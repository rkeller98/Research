# Required historical sources

This directory is excluded from active publication discovery and normal builds.

| Source | Retention reason |
|---|---|
| `composite_papers/` | Original composite sources, figures and results, including superseded raw-data assumptions; all 155 snapshot hashes are preserved |
| `original_combined_paper/` | Original PSM/EESM geometry baseline, original PDF and five figures; derivations are mapped to the active papers, while these historical renderings have no byte-identical replacement |
| `gradient_iso_original/` | Original MATLAB implementations, documentation, paper, PDF and benchmarks; intentional algorithm/evaluation differences mean old numerical claims are not adopted |
| `sandbox_experiments/` | Earlier RBF fitting example and flux-symmetry experiment; numerical code and authorship retained, only input/import paths adjusted |

The local ignored `original_combined_paper.zip` duplicates the baseline's seven
scientific files and contains TeX intermediates. It was relocated without
deleting local material; it is not an additional versioned archive. Existing
ignored MATs, intermediates and recovery material remain local and are not
newly added to Git. Historical paths inside untouched source snapshots describe
their original context; the [cleanup audit](../docs/final_cleanup.md) resolves
their current locations.
