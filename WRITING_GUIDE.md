# Publications writing and architecture contract

**Before creating or substantially editing a publication in this repository,
read this guide first.** Then read [the didactic guide](paper_template/DIDACTIC_GUIDE.md)
and [the didactic contract](docs/didactic_contract.md).

## One notation, one glossary, one visual language, many papers

Papers own content. The repository owns the common mathematical and visual
language. `shared/` is the canonical, actually loaded infrastructure, not a
reference bundle to vendor into papers. Paper directories must not contain
competing mathematical notation, glossary entries, acronyms, colors, reusable
commands, TikZ/PGFPlots styles, or box styles. There is no general `local.tex`.

```
shared/
  preamble.tex, publications.sty  canonical entry points
  commands/                     mathematics and machine notation
  glossary/                     canonical keys, meanings, units, conventions
  config/                       packages, typography, units, palette, listings
  tikz/                         semantic visual language
papers/<name>/
  main.tex, metadata.tex         document order and paper metadata
  sections/, figures/           local scientific content and concrete drawings
  bibliography/                 paper literature database
  numerics/, data/               paper experiments and results
  venue.tex                     external formatting requirements, if needed
```

All normal papers load `../../shared/preamble.tex`; the template loads
`../shared/preamble.tex`. The shared entry point resolves nested dependencies
relative to its own location. Builds run from the paper directory so section,
figure, and bibliography paths remain local. A paper depends on the repository;
copying its directory alone is no longer a supported independent export.

## Search before defining

Before writing sections, search `shared/commands/`, `shared/glossary/`, and
`shared/tikz/`, and inspect related papers for terminology. Reuse existing
notation and semantic styles. If a mathematical or physical concept is new,
define it once in `shared/` with its rendering, meaning, unit, sign convention,
and stable glossary key. Mathematical meaning is almost always reusable.
Never introduce a second definition because a local file is convenient.

Resistance error means **used minus true**, `epsilon_R = hat(R_s) - R_s`.
Electrical angle error means **estimated minus true**,
`delta gamma = hat(gamma) - gamma`, positive for a counterclockwise advance
of the estimated axes. Magnetic co-energy is normalized consistently with
the dq convention; for amplitude-invariant coordinates it is physical
three-phase co-energy divided by 3/2 so its current gradient is dq flux.
Different concepts need different keys; for example co-energy is
`sym:coenergy`, not the complex torque coordinate's historical `sym:w`.

Global definition does not imply global output. Never call `glsaddall` in a
paper. Use glossary commands or canonical quantity commands that record
actual use. An explicit `glsadd` is acceptable for a symbol actually used in
literal mathematics. Print only the entries used by that paper. Glossary
names must not call their own tracking commands recursively.

## Figures express semantics; shared files choose appearance

Concrete figures and numerical data stay local. Use semantic styles such as
`reference curve`, `measured curve`, `fitted curve`, `estimated quantity`,
`error residual`, `coordinate vector`, `constraint curve`, `operating point`,
`feasible region`, and `annotation`. The palette, font, line weights, arrows,
and reusable node/axis defaults belong to `shared/`.

Axis labels, ranges, coordinates, plot expressions, sample density, dimensions,
and diagram placement are local figure content. Colors and reusable visual
rules are not. Avoid literal palette colors and line/font design in papers;
use the corresponding shared style. Do not invent a new global style for an
isolated cosmetic preference. First determine whether an existing semantic
role covers the need. Any future `keyresult`, `intuition`, `warning`, assumption,
or engineering box must be defined once in shared infrastructure; do not add
local tcolorbox designs. No box package is required merely to satisfy this rule.

A genuinely local helper may exist only when it simplifies one figure or
section, carries no reusable mathematical meaning, replaces no glossary
symbol, and defines no visual rule. Document it with
`% architecture-local-helper: commandname - reason` next to its definition.
The linter recognizes this explicit narrow exception; metadata fields
`PaperAbstract` and `PaperKeywords` are ordinary local content.

## Venue requirements are explicit exceptions

Use `venue.tex` only for external publisher requirements: class, page size,
margins, columns, line spacing, or mandated heading format. State the venue
and requirement in comments. It may not define colors, notation, glossary,
figure styles, or general package infrastructure. IEMDC's retained letter
format and line spacing are the current example. Do not use venue configuration
as a replacement for `local.tex`.

## Learning-paper method

The reader should understand **why the result must be true**. Before a major
operation explain the problem, why the operation helps, what it exposes,
what it hides, an alternative view, the necessary assumptions, and what changes
if they fail. Connect algebra, geometry, physics, and engineering where those
views add information. These are thinking rules, not compulsory boxes after
every formula. Distinguish structural results from parameter-dependent facts.
Use limiting and counterfactual cases and small normalized examples. Figures
should show causes and transformations, not only finished curves.

## Bibliography and evidence

Literature databases remain paper-specific. Prefer primary or standard sources,
verify bibliographic facts, paraphrase, and attach citations to claims they
support. Never invent references. Distinguish internal unpublished companion
drafts from published evidence. Mark open source work transparently. A low fit
residual is not proof of physical correctness; synthetic checks are not
experimental validation. Preserve original data and parameters when proposing
corrections.

## Creating and building

Run `./scripts/new_paper.ps1 <paper_name>` from any PowerShell working directory.
It creates content linked to the canonical shared source without infrastructure
copies. Edit metadata, sections, figures, bibliography, and experiments.

```
pwsh -File scripts/check_architecture.ps1
pwsh -File scripts/build.ps1 <paper_name>
pwsh -File scripts/build_all.ps1
```

The scripts use platform-independent path composition and require latexmk,
LuaLaTeX (or pdfLaTeX), and Biber. The Python architecture check is also
available directly as `python scripts/check_architecture.py`. Build scripts
invoke the architecture gate. From a paper directory a direct
`latexmk -lualatex -interaction=nonstopmode -halt-on-error main.tex` works too.
Repository outputs are `build/<paper>/` and `output/pdf/<paper>.pdf`.
Review final logs for undefined references/citations, glossary issues,
overfull boxes, and broken drawings, then inspect rendered PDFs. Existing
unrelated warnings should be documented separately, not hidden by blanket
warning suppression.

## Mandatory checks before writing

- [ ] Read this guide and the linked didactic guides.
- [ ] Search existing notation, glossary, acronyms, and visual styles.
- [ ] Check related papers for terminology and sign conventions.
- [ ] Define the research question and separate assumptions from structural facts.

## Mandatory checks before completion

- [ ] No duplicated symbol or acronym definitions.
- [ ] No local reusable colors, commands, TikZ/PGFPlots or box styles.
- [ ] Sign conventions and units agree with the canonical glossary.
- [ ] Only used entries appear in the paper glossary.
- [ ] Figures use the shared semantic visual language.
- [ ] Sources are real and support the associated claims.
- [ ] Equations are dimensionally consistent; assumptions are explicit.
- [ ] Limiting and counterfactual cases have been checked.
- [ ] Architecture check passes; the paper has no new build warnings/errors.
- [ ] `build_all` succeeds and rendered outputs have been reviewed.

## Enforcement and audit

`scripts/check_architecture.py` scans papers and the template for local
infrastructure, forbidden definition commands, unapproved helper macros,
`glsaddall`, duplicate shared glossary keys, and noncanonical entry paths.
It explains how to reuse/add the canonical definition. Its scan is a practical
guard, not a full TeX parser or proof of semantic equivalence. The migration
audit and paper split are recorded in `docs/architecture_migration.md` and
`docs/flux_papers_split.md`. Keep this guide and the actual structure consistent.
