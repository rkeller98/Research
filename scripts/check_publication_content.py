"""Check reachable local publication inputs, figures, labels and citations."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def check(paper):
    seen, errors = set(), []
    def visit(path):
        if path in seen:
            return
        if not path.is_file():
            errors.append("missing input: " + path.relative_to(ROOT).as_posix())
            return
        seen.add(path)
        text = re.sub(r"(?<!\\)%[^\n]*", "", path.read_text(encoding="utf-8-sig"))
        for name in re.findall(r"\\(?:input|include)\{([^}]+)\}", text):
            if "\\" in name:
                continue
            target = paper / name
            visit(target if target.suffix else target.with_suffix(".tex"))
        for name in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", text):
            if "\\" in name:
                continue
            target = paper / name
            candidates = [target] if target.suffix else [target.with_suffix(ext) for ext in [".pdf", ".png", ".jpg"]]
            if not any(p.is_file() for p in candidates):
                errors.append("missing figure: " + name)
    visit(paper / "main.tex")
    texts = [re.sub(r"(?<!\\)%[^\n]*", "", p.read_text(encoding="utf-8-sig")) for p in seen]
    content = "\n".join(texts)
    labels = re.findall(r"\\label\{([^}]+)\}", content)
    duplicates = sorted({key for key in labels if labels.count(key) > 1})
    errors.extend("duplicate label: " + key for key in duplicates)
    references = set()
    for names in re.findall(r"\\(?:[cC]ref|eqref|ref|autoref|[cC]pageref)\*?\{([^}]+)\}", content):
        references.update(x.strip() for x in names.split(","))
    errors.extend("missing label: " + key for key in sorted(references - set(labels)) if "\\" not in key)
    bib_files = [paper / name for name in re.findall(r"\\addbibresource(?:\[[^\]]*\])?\{([^}]+)\}", content)]
    keys = set()
    for file in bib_files:
        if not file.is_file():
            errors.append("missing bibliography: " + str(file.relative_to(ROOT)))
        else:
            keys.update(re.findall(r"@\w+\{([^,]+),", file.read_text(encoding="utf-8-sig")))
    citations = set()
    for names in re.findall(r"\\(?:[a-zA-Z]*cite[a-zA-Z]*)(?:\[[^\]]*\])*\{([^}]+)\}", content):
        citations.update(x.strip() for x in names.split(","))
    errors.extend("missing citation: " + key for key in sorted(citations - keys))
    return dict(paper=paper.name, reachable_tex=len(seen), labels=len(labels), citations=len(citations), errors=errors)


if __name__ == "__main__":
    result = [check(p.parent) for p in sorted((ROOT / "papers").glob("*/main.tex"))]
    (ROOT / "docs/publication_structure_qa.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    errors = [(row["paper"], e) for row in result for e in row["errors"]]
    for paper, error in errors:
        print(paper, error)
    assert not errors, "Publication content checks failed"
    print(f"All {len(result)} active papers: inputs, figures, labels and citations resolved.")
