# Composite source provenance

These are the two complete working-tree composites at the start of the
portfolio migration, including the preceding torque extension. Scientific
TeX/Python/BibTeX/Markdown/JSON/CSV/DAT/PDF content was moved byte-for-byte.
`source_snapshot.json` records the pre-move hashes; migration did not overwrite
these sources with the ZIP's archived copies.

The source base was Research commit `0e53431`; the snapshot also includes the
uncommitted torque manuscript work that preceded this request. Old numbers,
assumptions, data audits, integration notes and original figures remain here
as historical evidence. They are superseded where the active papers report
new portable-dataset experiments.

`physics_constrained_flux_maps` and `flux_map_error_diagnostics` are excluded
from `build_all`, which scans only direct children of `papers/`. Their entry
paths describe their historical location; the archive is not another active
publication or a vendored shared framework.

Raw MATs remain available locally in the ignored archive and Test_Daten
folders, and the original tracked copies remain recoverable from Git history.
They are intentionally excluded from the new versionable source tree. Active
experiments use the small canonical fixtures instead. Source hashes identify
the raw lineage without requiring large historical MAT blobs in a fresh
working checkout.

Section/figure/result ownership and parked concepts are mapped in
`docs/paper_portfolio_migration.md`. Existing regression assertions can be
executed with their output directory redirected to ignored scratch space;
they must not rewrite this archival snapshot.
