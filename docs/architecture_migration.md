# Canonical Publications infrastructure: migration audit

The governing entry point is [WRITING_GUIDE.md](../WRITING_GUIDE.md), followed
by the linked didactic guide and contract. README, template documentation,
paper READMEs and the scientific migration matrix point to this contract.
There was no existing AGENTS.md to update; no parallel agent contract was added.

## Architecture actually loaded

All eight active papers and the template load the same `shared/preamble.tex`.
It resolves the package/configuration, commands, glossary and TikZ/PGFPlots
files relative to the shared source using `import`/`subimport`. Papers refer
to `../../shared/`; the template refers to `../shared/`. Compiling from a paper
directory or through the scripts resolves local scientific content correctly.

Paper directories contain metadata, sections, concrete figures/data, bibliography
and experiments. There is no active paper `includes/` or general `local.tex`.
Old infrastructure copies were preserved under ignored `tmp/architecture_before/`
and `tmp/retired_infrastructure/` as local recovery material, then removed from
the active framework. The unused shared bibliography was also retired; common
bibliography *configuration* stays shared, while each actual database belongs
to its paper. The historical sources now live unchanged under `_archive/`,
outside the active-paper gate; `legacy/` was consolidated in the
[final cleanup](final_cleanup.md). The eight-paper table below records the
earlier infrastructure migration; the current twelve-paper portfolio is listed
in [the completion report](portfolio_completion_report.md).

| Active document | Shared source | Local bibliography | Formatting exception |
|---|---|---|---|
| `eesm_voltage_geometry` | Canonical | `bibliography/references.bib` | None |
| `psm_voltage_geometry` | Canonical | Same local layout | None |
| `iemdc_digest_2024` | Canonical | Same local layout | `venue.tex`: letter, 1-inch margins, 1.6 line spacing |
| `n_dim_rootri` | Canonical | Same local layout | None |
| `recursive_qp_within_simplex` | Canonical | Same local layout | None |
| `temp_eesm_Mopt` | Canonical | Same local layout | None |
| `physics_constrained_flux_maps` | Canonical | Same local layout | None |
| `flux_map_error_diagnostics` | Canonical | Same local layout | None |
| `paper_template` | Canonical | Same local layout | None |

The IEMDC venue file contains external formatting only. Its CSV separator
is specified on its concrete data import; it is not a repository-wide plot
default. Mathematical content in unrelated papers was not rewritten.
Infrastructure, notation, visual roles, and necessary TeX compatibility fixes
were consolidated.

## Notation and glossary decisions

New flux commands were reviewed against the existing vocabulary rather than
copied verbatim from a local preamble:

| Earlier local name | Canonical command | Meaning/key |
|---|---|---|
| `flux`, `current`, `voltage` | Same descriptive names | Flux/current/voltage vectors, Wb/A/V |
| `Jrot` | `rotationgenerator` | Planar 90-degree generator, `sym:jrot` |
| `Rot` | `rotationmatrix` | Active counterclockwise rotation, `sym:rotation`; distinct from copper-loss R |
| `Ldiff` | `Ldiff` | Flux Jacobian, H, `sym:ldiff` |
| `epsR` | `resistanceerror` | Used minus true resistance, ohm, `sym:er` |
| `angerr` | `angleerror` | Estimated minus true electrical angle, rad, `sym:dg` |
| `Eq`, `Oq` | `evenq`, `oddq` | Reflection projections |
| `coen` | `coenergy` | dq-normalized magnetic co-energy, J, `sym:coenergy` |
| `Order` | `bigO` | Mathematical order notation |
| Bare normalized w | `normalizedcoenergy` | Dimensionless W'/(flux base × current base) |

The historical `sym:w` is retained for the complex torque coordinate and
is not reused for energy. Rotation uses R_gamma rather than the copper-loss
matrix R. Electromagnetic torque now uses M and the single `sym:te` key;
the competing `sym:torque` key was removed. Rotor excitation uses `sym:iexc`
consistently. PSM shape/current-to-voltage matrices and EESM matrix commands
render the same symbols as their canonical glossary entries.

Other catalogue collisions were separated: normalized speed uses bar-omega,
hyperbolic allocation uses alpha_hyp, current trajectories use C_i, electrical
flux angle uses gamma_psi, and azimuth uses varphi. Literal uses of the migrated
allocation/speed/trajectory quantities were synchronized in the extended
draft. Generic dummy variables and explicitly declared coordinates do not
automatically become a physical catalogue quantity. The delay convention uses
tau_d, distinct from torque per copper loss tau. Positive tau_d means estimated
phase advance; a physical sensing lag has negative sign in that convention.

Physical entries record units and sign conventions centrally. Glossary names
use mathematical renderings without recursively calling their own tracking
commands. Canonical quantity commands track use; existing literal symbols can
use an explicit `glsadd` when actually present. No active document uses
`glsaddall`. Full papers print only their used subset. Short documents that
disable the appendix still load the dictionary; they skip printable-index
initialization and disable glossary hyperlinks to an absent appendix.

The glossary gate checks duplicate keys and command names, not arbitrary
semantic equivalence of TeX expressions. The catalogue was therefore also
reviewed manually. It is a maintained vocabulary, not a claim that a text
scanner can prove all scientific notation consistent.

## Shared visual language and typography

Palette choices live in `shared/config/palette.tex`. TikZ/PGFPlots semantics
live in `shared/tikz/`: reference, measured/fitted curves, estimated quantities,
residuals, coordinate axes/vectors, operating points, regions, annotations,
magnetic materials, phases, transformation arrows and diagram blocks.
General fonts, line weights, patterns, arrows, axis defaults, scalar surfaces
and listings are shared. Prose table columns use the common ragged-right
typography. Any future reusable box environment must also be defined globally;
no local tcolorbox component is present.

Figures retain coordinates, axis labels/ranges, plot expressions, concrete data,
dimensions and diagram placement. They do not define their own palette,
font, line weight or reusable styles. Phase-label/color helper macros in the
IEMDC drawing were eliminated in favor of global phase styles and glossary
symbols. Its one literal `phaseArray` helper is documented as the narrow local
data exception and carries no mathematical meaning or visual rule. Numerical
model helper copies in the two new papers are scientific experiment content,
not duplicated LaTeX infrastructure.

## Enforcement and build workflow

`scripts/check_architecture.py` requires only Python's standard library.
It checks canonical entry paths and bibliography layout, local framework
directories/files, competing glossary/acronym/color/command/style definitions,
`glsaddall`, suspicious helper definitions, raw figure palette references,
fonts, line weights, patterns and arrows, and duplicate shared keys/commands.
Diagnostics direct an author to reuse/add the shared definition. A local helper
requires its nearby `architecture-local-helper` explanation; the check does
not grant exceptions for semantic notation or styles.

The PowerShell wrapper runs the gate from any working directory. `build.ps1`
calls it before compiling, `build_all.ps1` discovers active papers, and
`new_paper.ps1` creates content linked to shared infrastructure. No include
bundle is copied. Scripts compose paths from their own location and use
platform separators, including cleanup's checked build-directory boundary.
The existing latexmk/Biber locale handling is preserved.

## Validation record

Architecture self-tests and the full scan pass. Tests cover forbidden
definitions, comments, metadata fields, the documented literal helper,
semantic figure styles, and rejection of raw figure design. A new-paper
smoke scaffold was created and built successfully from `C:/`, outside the
repository working directory; its files/output were then moved to ignored
`tmp/` so it is not an active extra paper. The template is checked by the gate.

The complete eight-paper LuaLaTeX/Biber build succeeds on Windows/MiKTeX.
Cross-platform path construction was reviewed, but Linux/macOS executions
were not available in this session and are not claimed. Numerical validations
for both new papers pass; results and remaining research limitations are
recorded in [the split report](flux_papers_split.md).

Generated full logs remain in `build/<paper>/main.log`; the console transcript
is `build/architecture_all_console.txt`. The final log/PDF inventory is
`build/pdf_audit.json`.

| Document | Final pages | Log review |
|---|---:|---|
| EESM voltage geometry | 12 | Clean |
| PSM voltage geometry | 14 | Clean |
| IEMDC digest | 6 | Clean |
| N-dimensional contour extraction | 5 | Clean |
| Recursive simplex QP | 3 | Clean |
| Extended EESM optimization draft | 85 | Clean |
| Co-energy reconstruction draft | 14 | Clean |
| Flux-map diagnostics draft | 18 | Clean |

The final logs contain no unresolved citations/references, glossary warnings,
overfull/underfull boxes, or missing-character messages. Narrow comparison
columns use shared ragged-right typography. The three nonfloating landscape
panels use the shared `standalonetable` environment with a caption-level link
anchor. Empty/disabled glossary appendices are not initialized. A missing
Ohm glyph in a new diagnostic table was caught visually and fixed centrally
with a math-symbol unit definition, following the symbol-redeclaration approach
documented in the [official siunitx manual](https://mirrors.ctan.org/macros/latex/contrib/siunitx/siunitx.pdf).

Both new PDFs were rendered in full and their plots, equations, tables,
glossaries and references reviewed. Their close plot legend/title spacing and
the missing unit glyph were corrected and re-rendered. The other active PDFs
were rendered and reviewed in page overviews for migration regressions.
The template also builds directly against shared infrastructure; its generic
placeholder has no used catalogue entries and disables the symbol appendix.
Its demonstrator citation now points to the real Boyd--Vandenberghe standard
reference; the fictional bibliography placeholder was removed.

No combined flux-map paper or smoke-test paper remains active. Source backups
and QA intermediates are ignored local recovery material. No commit, push,
submission or external MeasEval application change was performed.
