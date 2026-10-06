"""Portable architecture gate; standard-library Python only."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = re.compile(r"\\(?:newglossaryentry|newabbreviation|definecolor|colorlet|"
                       r"tikzset|pgfplotsset|newtcolorbox|lstset|lstdefinestyle|"
                       r"DeclareMathOperator|DeclareSIUnit|DeclarePairedDelimiter|newtheorem|newenvironment|newcolumntype|lstdefinelanguage|glsaddall)\b|/\.(?:append\s+)?style\b")
MACRO = re.compile(r"\\(?:newcommand|renewcommand|providecommand|NewDocumentCommand|"
                   r"RenewDocumentCommand|DeclareRobustCommand)\*?\s*\{?\\([A-Za-z]+)")
COLORS = re.compile(r"(?<![A-Za-z])(?:MidnightBlue|BrickRed|ForestGreen|Purple|Orange|"
                    r"blue|red|green|purple|orange|gray|col[A-Z]\w*|Publication[A-Z]\w*)(?:!\d+)?(?=[,\]\s}])")
FIGURE_DESIGN = re.compile(r"\b(?:font|line width)\s*=|>=\s*Latex|\-\{Latex|"
                           r"(?<=[\[,])\s*(?:thin|semithick|thick|very thick|dashed|densely dashed|dotted|<->|->)(?=[,\]])")
MESSAGE = ("This definition appears to belong to the shared Publications infrastructure. "
           "Add or reuse the canonical definition instead of defining it inside a paper.")


def inspect_text(text, path):
    issues = []
    lines = text.splitlines()
    for number, raw in enumerate(lines, 1):
        line = re.split(r"(?<!\\)%", raw, maxsplit=1)[0]
        if FORBIDDEN.search(line):
            issues.append((number, MESSAGE))
        for match in MACRO.finditer(line):
            command = match[1]
            if path.name == "metadata.tex" and command in ("PaperAbstract", "PaperKeywords"):
                continue
            marker = "architecture-local-helper: "+command+" - "
            preceding = "\n".join(lines[max(0, number-3):number])
            if marker not in preceding:
                issues.append((number, MESSAGE+" A genuine local helper needs a documented exception."))
        if "figures" in path.parts and COLORS.search(line):
            issues.append((number, "Use a shared semantic visual style instead of a literal palette color."))
        if "figures" in path.parts and FIGURE_DESIGN.search(line):
            issues.append((number, "Use the shared font, line-weight, pattern or arrow style for this semantic role."))
    return issues


def check(root=ROOT):
    problems = []
    dirs = sorted(p for p in (root/"papers").iterdir() if p.is_dir())+[root/"paper_template"]
    for paper in dirs:
        if not (paper/"main.tex").exists():
            continue
        for forbidden in ("local.tex", "includes"):
            if (paper/forbidden).exists():
                problems.append(f"{paper.relative_to(root)}/{forbidden}: remove local infrastructure; load shared/.")
        main = (paper/"main.tex").read_text(encoding="utf-8-sig")
        expected = "../shared/" if paper.name == "paper_template" else "../../shared/"
        if "\\subimport{"+expected+"}{preamble.tex}" not in main:
            problems.append(f"{paper.relative_to(root)}/main.tex: missing canonical shared entry point.")
        if "\\addbibresource{bibliography/references.bib}" not in main:
            problems.append(f"{paper.relative_to(root)}/main.tex: bibliography must use its content directory.")
        for source in paper.rglob("*"):
            if source.suffix not in (".tex", ".sty"):
                continue
            for line, reason in inspect_text(source.read_text(encoding="utf-8-sig"), source):
                problems.append(f"{source.relative_to(root)}:{line}: {reason}")
    keys = {}
    commands = {}
    for source in (root/"shared").rglob("*.tex"):
        content = source.read_text(encoding="utf-8-sig")
        for key in re.findall(r"\\(?:newglossaryentry|newabbreviation)\{([^}]+)\}", content):
            if key in keys:
                problems.append(f"{source.relative_to(root)}: duplicate canonical glossary key {key}; first in {keys[key]}.")
            keys[key] = source.relative_to(root)
        for match in MACRO.finditer(content):
            command = match[1]
            if command in commands:
                problems.append(f"{source.relative_to(root)}: duplicate canonical command {command}; first in {commands[command]}.")
            commands[command] = source.relative_to(root)
    return problems


def self_test():
    p = Path("papers/example/sections/test.tex")
    assert inspect_text(r"\newcommand{\flux}{\vect\psi}", p)
    assert inspect_text(r"\newglossaryentry{foo}{name={x}}", p)
    assert inspect_text(r"\glsaddall[types={symbols}]", p)
    assert inspect_text(r"\DeclareSIUnit\myunit{foo}", p)
    assert not inspect_text("% \\tikzset{example}", p)
    helper = "% architecture-local-helper: phaseArray - literal data\n\\newcommand{\\phaseArray}{1,2}"
    assert not inspect_text(helper, p)
    assert not inspect_text(r"\newcommand{\PaperAbstract}{content}", p.with_name("metadata.tex"))
    assert inspect_text("\\draw[BrickRed] (0,0)--(1,1);", Path("papers/example/figures/test.tex"))
    assert not inspect_text("\\draw[estimated quantity] (0,0)--(1,1);", Path("papers/example/figures/test.tex"))
    assert inspect_text("\\draw[thin] (0,0)--(1,1);", Path("papers/example/figures/test.tex"))
    assert inspect_text("\\node[font=\\small] {x};", Path("papers/example/figures/test.tex"))
    assert not inspect_text("\\draw[fine line,direction arrow] (0,0)--(1,1);", Path("papers/example/figures/test.tex"))
    print("Architecture checker self-test passed.")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    errors = check()
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    print("Architecture check passed: canonical shared infrastructure, content-only papers.")
