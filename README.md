# Publications

**Read [WRITING_GUIDE.md](WRITING_GUIDE.md) before creating or substantially
editing a paper.** It is the repository's writing, notation, and visual contract.

This repository uses **one notation, one glossary, one visual language, many
papers**. `shared/` is the canonical source actually loaded by every paper.
There are no paper-vendored infrastructure bundles and no general `local.tex`.

```
shared/              canonical notation/styles plus dataset, model and numeric helpers
paper_template/      content scaffold linked to shared/
papers/              scientific content, local bibliography, figures, experiments
scripts/             scaffold, architecture gate, builds, cleanup
docs/                didactic contract, migration and paper-split reports
build/               generated intermediates
output/pdf/          exported PDFs
datasets/            small canonical OP CSV/manifest fixtures and provenance
concepts/            research ideas without a separately validated paper claim
_archive/            required historical sources and experiments, excluded from normal builds
sandbox/             free personal experiments; no maintained tools or canonical datasets
```

The active flux portfolio has five independent research questions:

- `flux_correction_symmetry`: reflection residuals and justified model projection.
- `magnetic_coenergy_consistency`: reciprocity and path-integrability tests.
- `flux_correction_coenergy`: gradient reconstruction through a common potential.
- `torque_flux_consistency`: torque projection, radial ambiguity and a qualified six-phase data comparison.
- `flux_error_identifiability`: geometric error transformations, rank and confounding.

The former composites are preserved under `_archive/composite_papers/`, outside
normal builds. Independent-reference correction and further co-energy parameter
derivation remain concepts. See [portfolio and migration](docs/paper_portfolio_migration.md)
and [completion/QA report](docs/portfolio_completion_report.md).

The older geometry baseline and original Gradient-Iso sources live once under
`_archive/`. The owner's unchanged `RawDataImporter` is available in
`shared/python/raw_ww_data_importer.py`; its signal-only v7.3 API remains distinct
from the metadata-preserving v5/v7.3 `measurement_io` reader. Historical DAT
exports are retained separately from the canonical fixtures in
`datasets/historical_exports/`. See the [cleanup audit](docs/final_cleanup.md)
for the path map, preservation evidence and validation.

The existing PSM/EESM voltage geometry, simplex/iso reconstruction, IEMDC digest,
N-dimensional contour extraction, recursive simplex QP and extended EESM
optimization drafts remain active and are rebuilt by the same scripts.

Eight small [canonical datasets](datasets/README.md) provide PSM/EESM/ASM evidence
without raw MAT files or a local MeasEval installation. Raw `Test_Daten/` remains
ignored. The Multi-RPM source is a two-system six-phase configuration: total
amplitude-invariant torque uses kT=(6/2)p, resolving the leading factor-two
mismatch without a fitted sensor gain. CAN calibration and mechanical losses
remain open. [The research note](docs/torque_flux_consistency.md) retains the
original observability development and synthetic proof of concept.

## Start and validate a paper

Read the writing guide, [didactic guide](paper_template/DIDACTIC_GUIDE.md),
and [didactic contract](docs/didactic_contract.md), then use PowerShell:

```
./scripts/new_paper.ps1 my_paper
./scripts/check_architecture.ps1 -SelfTest
./scripts/build.ps1 my_paper
./scripts/build_all.ps1
```

PowerShell 7 works on Windows, Linux, and macOS; Windows PowerShell 5.1 is
also supported. Builds require latexmk, LuaLaTeX (default) or pdfLaTeX, Biber,
and Python 3 for the architecture check. All path discovery is relative to
the script location. Use `-Engine pdflatex` for a pdfLaTeX build.

Builds execute inside each paper, write intermediates to `build/<name>/`,
and export `output/pdf/<name>.pdf`. `build_all.ps1` discovers all active
`papers/*/main.tex`. Direct builds also work from a paper directory:

```
latexmk -lualatex -interaction=nonstopmode -halt-on-error main.tex
```

Papers depend on the canonical repository `shared/` directory. Copying one
paper alone is no longer an independent-build contract. An export must include
the shared source at the referenced relative location. Bibliographies,
metadata, scientific sections, figures, and numerical experiments remain
paper-owned. Only explicit publisher formatting belongs in `venue.tex`.

The canonical glossary loads all definitions but prints only used entries;
`glsaddall` is forbidden. The architecture gate catches local infrastructure
copies and competing notation/styles. See [the migration audit](docs/architecture_migration.md)
for what was consolidated and how the builds were checked.
