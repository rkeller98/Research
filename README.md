# Publications

**Read [WRITING_GUIDE.md](WRITING_GUIDE.md) before creating or substantially
editing a paper.** It is the repository's writing, notation, and visual contract.

This repository uses **one notation, one glossary, one visual language, many
papers**. `shared/` is the canonical source actually loaded by every paper.
There are no paper-vendored infrastructure bundles and no general `local.tex`.

```
shared/              canonical commands, glossary, palette, styles, configuration
paper_template/      content scaffold linked to shared/
papers/              scientific content, local bibliography, figures, experiments
scripts/             scaffold, architecture gate, builds, cleanup
docs/                didactic contract, migration and paper-split reports
build/               generated intermediates
output/pdf/          exported PDFs
legacy/              historical source archive; not part of the active framework
```

The active papers include PSM and EESM voltage geometry, the IEMDC digest,
N-dimensional contour extraction, recursive simplex QP, the extended EESM
optimization draft, and the two complementary flux-map drafts:

- `physics_constrained_flux_maps`: admissible co-energy reconstruction and fitting.
- `flux_map_error_diagnostics`: experimental symmetry residuals, resistance-equivalent interpretation, and limits of causal attribution.
- `gradient_iso_reconstruction`: local simplex derivatives, recursive derivative
  clouds, iso geometry, synthetic validation and an audited Python migration
  using the existing VICE geometry implementation.

The former combined `dq_flux_symmetry_diagnostics` directory has been split;
it is not an additional active paper. See [the split report](docs/flux_papers_split.md).

The [torque/flux consistency research note](docs/torque_flux_consistency.md)
connects torque projections to the existing voltage, resistance-equivalent and
co-energy diagnostics. It includes six geometric/observability figures and an
isolated synthetic proof of concept; no measured maps or production correction
are changed. Torque-channel provenance remains an experimental prerequisite.

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
