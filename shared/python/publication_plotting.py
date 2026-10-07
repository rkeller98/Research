"""Matplotlib companion to the canonical TeX palette and semantic roles.

Color values are read from shared/config/palette.tex and TeX's dvipsnam.def.
No paper-owned palette is needed. Figure generation requires kpsewhich from
the same TeX distribution used to build the repository papers.
"""
from pathlib import Path
import re
import subprocess

import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap


def configure():
    palette = (Path(__file__).resolve().parents[1] / "config" / "palette.tex").read_text()
    named_path = subprocess.check_output(["kpsewhich", "dvipsnam.def"], text=True).strip()
    named = Path(named_path).read_text()
    colors = {"white": (1., 1., 1.), "black": (0., 0., 0.), "gray": (.5, .5, .5),
              "red": (1., 0., 0.), "green": (0., 1., 0.)}
    for name, channels in re.findall(r"\\DefineNamedColor\{named\}\{([^}]+)\}\s*\{cmyk\}\{([^}]+)\}", named):
        c, m, y, k = map(float, channels.split(","))
        colors[name] = tuple(1 - min(1, component + k) for component in (c, m, y))
    for name, channels in re.findall(r"\\definecolor\{([^}]+)\}\{RGB\}\{([^}]+)\}", palette):
        colors[name] = tuple(float(v) / 255 for v in channels.split(","))
    for name, expression in re.findall(r"\\colorlet\{([^}]+)\}\{([^}]+)\}", palette):
        parts = expression.split("!")
        base = colors[parts[0]]
        if len(parts) > 1:
            weight = float(parts[1]) / 100
            other = colors[parts[2]] if len(parts) > 2 else colors["white"]
            base = tuple(weight*a + (1-weight)*b for a, b in zip(base, other))
        colors[name] = base
    roles = {key: colors["Publication" + value] for key, value in
             {"reference": "Reference", "estimated": "Estimated", "derived": "Derived",
              "guide": "Guide", "highlight": "Highlight", "torque": "Torque"}.items()}
    mpl.rcParams.update({"font.family": "DejaVu Serif", "font.size": 9,
                         "axes.titlesize": 10, "axes.labelsize": 9,
                         "legend.fontsize": 8, "xtick.labelsize": 8,
                         "ytick.labelsize": 8, "axes.grid": True, "grid.alpha": .18,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "lines.linewidth": 1.5, "savefig.dpi": 180,
                         "pdf.fonttype": 42})
    roles["coverage_map"] = LinearSegmentedColormap.from_list(
        "publication_coverage", [colors["white"], roles["derived"]])
    roles["error_map"] = LinearSegmentedColormap.from_list(
        "publication_error", [colors["white"], roles["estimated"]])
    return roles
