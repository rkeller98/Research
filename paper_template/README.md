# Paper content scaffold

Read [WRITING_GUIDE.md](../WRITING_GUIDE.md) first, then this directory's
[DIDACTIC_GUIDE.md](DIDACTIC_GUIDE.md) and the repository didactic contract.

Create a paper with `./scripts/new_paper.ps1 <name>`. The scaffold loads the
canonical `shared/` infrastructure; it does not vendor notation, glossary,
configuration, or visual styles. A paper contains `main.tex`, `metadata.tex`,
sections, concrete figures, bibliography, and optional experiments/data.
There is no `local.tex`. Only externally required publisher formatting may
use an explicit `venue.tex`.

The template uses `../shared/`; the scaffold adjusts this to `../../shared/`
for `papers/<name>/`. Both are directly compilable from their own directories.
Add genuinely new notation or visual semantics to `shared/` after searching
the canonical vocabulary. Print only used glossary entries. Run the
architecture gate and repository build scripts before delivery.

The generic placeholder has no catalogue symbols, so its appendix is disabled.
Set `\showglossarytrue` in metadata when the paper uses glossary quantities;
only those recorded as used are printed.
