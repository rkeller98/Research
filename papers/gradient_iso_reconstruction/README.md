# Gradient-Iso reconstruction

Aktive Aufarbeitung von `C:/Git/Gradienten_Iso_Verfahren` im gemeinsamen
Research-Framework. Das englische Learning Paper leitet die Methode her,
zeigt ihre Geometrie und trennt überprüfte Eigenschaften von offenen Fragen.

## Was enthalten ist

- Lokale affine Gradienten in N Dimensionen und rekursive Ableitungskomponenten.
- Roh-Hessian, symmetrischer Anteil, Symmetriefehler und Laplacian bei Ordnung 2.
- Iso-Schnitte mit dem vorhandenen VICE `EdgeIntersector`, keine neue Portierung.
- Iso-Coverage als geometrischer Deskriptor mit explizit undefinierten Plateau-Fällen.
- Suchvorschläge, Hüllenprüfung, Herkunftssimplexe und Konditionierungsdiagnostik.
- Konfigurierbare Python-Demo, reproduzierbare Experimente, numerische Daten,
  erklärende TikZ-Bilder und aus den Experimenten erzeugte Abbildungen.

## Schnellstart

Alle Befehle aus `C:/Git/Research`; die vorhandene `.venv` kann verwendet werden:

```powershell
.\.venv\Scripts\python.exe -m pip install -r papers/gradient_iso_reconstruction/requirements.txt
.\.venv\Scripts\python.exe -m pytest papers/gradient_iso_reconstruction/python -q
.\.venv\Scripts\python.exe papers/gradient_iso_reconstruction/python/demo.py --function himmelblau --samples 240 --noise 0.01 --outlier-fraction 0.08 --show
.\.venv\Scripts\python.exe papers/gradient_iso_reconstruction/python/demo.py --order 2 --samples 120 --show
.\.venv\Scripts\python.exe papers/gradient_iso_reconstruction/python/demo.py --dimension 4 --samples 50 --levels 10
.\.venv\Scripts\python.exe papers/gradient_iso_reconstruction/python/experiments.py
.\scripts\build.ps1 gradient_iso_reconstruction
```

Die Demo schreibt standardmäßig nach `tmp/gradient_iso_demo`; mit `--output`
lässt sich der Zielordner ändern. `--show` öffnet die Plotansicht. Der N-D-Plot
zeigt bei mehr als zwei Dimensionen ausdrücklich nur eine Projektion.
`--noise` ist in der Demo relativ zur Standardabweichung des sauberen Feldes;
die quadratischen Paper-Experimente verwenden die dort angegebenen absoluten
Rauschamplituden. Himmelblau ist nur in zwei Dimensionen definiert.

Das gebaute Paper liegt unter `output/pdf/gradient_iso_reconstruction.pdf`.
Die Tabellenwerte werden aus CSV-Ergebnissen erzeugt. Neue Daten erfordern
anschließend einen neuen Paper-Build.

## Eigene Messdaten

```powershell
$env:PYTHONPATH = (Resolve-Path papers/gradient_iso_reconstruction/python).Path
```

```python
import numpy as np
from gradient_iso import Options, reconstruct, search_guidance

# X_phys: (N,d), f: (N,); eindeutige Punkte und endliche Messwerte
scale = np.array([100.0, 200.0])
X = X_phys / scale
clouds = reconstruct(X, f, Options(order=2, levels=15))
gradient_phys = clouds[0].values / scale
H_phys = clouds[1].raw_hessian / scale[None, :, None] / scale[None, None, :]
proposal = search_guidance(clouds, X, minimize=True)
trial_phys = proposal['proposed'] * scale
```

Die Metrik bestimmt Nachbarschaften und Suchrichtungen. Es gibt keine versteckte
Normierung. Jede Ableitungsordnung besitzt eigene Stützpunkte; die Zeilen
verschiedener Ordnungen dürfen nicht einfach gleichgesetzt werden.
`cloud.source_simplices` verweist auf den Eingang der jeweiligen Ordnung.
`condition` beschreibt Zellform, `inverse_edge_norm` auch die Rauschverstärkung
durch kleine Zellen. Die raw-Hessian ist kein zertifizierter Krümmungsschätzer.

`coverage` kann NaN sein. `iso_status` erklärt konstante Komponenten, leere
Schnitte oder unzureichende Stützpunkte. Hohe Coverage ist keine kalibrierte
Konfidenz. `threshold` erhält die historische Vergleichsregel; ein größerer
`sigma_factor` markiert **mehr** Punkte unterhalb der Schwelle.
Die Suchschritte nutzen standardmäßig keine Coverage-Skalierung. Ihre Richtung
kommt vom Gradienten; außerhalb der Datenhülle liegende Vorschläge werden
markiert. Eigene Nebenbedingungen und Akzeptanzmessungen bleiben erforderlich.

## Geometrie-Abhängigkeit

`python/vendor` enthält genau die drei numerischen VICE-Module aus Revision
`1ecd269739833ae343e864d91fdeb2d2c5669342`, unverändert und mit Hashmanifest.
Kleine `__init__.py`-Dateien bilden nur die Paketstruktur. So ist das Paper
auch während paralleler VICE-Entwicklung reproduzierbar. Es gibt weder eine
zweite Intersector-Implementierung noch einen MATLAB-Fallback.

Für einen ausdrücklichen Test der aktuellen VICE-Arbeitskopie:

```powershell
$env:VICE_MEASEVAL_SOURCE = 'C:/Git/GUI_VICE-MeasurementEvalKit/SourceCode/python'
.\.venv\Scripts\python.exe -m pytest papers/gradient_iso_reconstruction/python -q
# Danach zurück zum reproduzierbaren Snapshot:
Remove-Item Env:VICE_MEASEVAL_SOURCE
```

Die Demo unterstützt zusätzlich `--vice-source`. Vergleiche bei Backendwechseln
`data/provenance.json`; eine neue Version kann Numerik und API ändern.

## Wissenschaftlicher Stand

Affine Gradienten, die Interpolationsinvariante und geometrische Rauschfortpflanzung
sind geprüft. Rauschfreie Gradienten werden im quadratischen Test genauer,
wenn die Punktwolke dichter wird. Bei festem Rauschen kann Verfeinerung schaden.
Die vollständige Hessian-Rekursion hat bereits im rauschfreien quadratischen
Test erhebliche Fehler und erhält deshalb keine allgemeine Genauigkeitsbehauptung.

Der bisherige Low-Coverage-Ausreißerscore schneidet in den dokumentierten
Himmelblau-Realisierungen schlecht ab. Die Auswertung folgt den tatsächlich
verwendeten Simplexvertices statt bloß dem nächsten Messpunkt. Die klaren
synthetischen Sprünge begünstigen den lokalen Residuenvergleich; das ist keine
industrielle Validierung. Kurze Suchschritte verbessern den einfachen
synthetischen Test meist, ohne damit eine geschlossene Suchstrategie zu beweisen.

## Dateien

| Pfad | Zweck |
| --- | --- |
| `main.tex`, `sections/` | Paper mit Herleitung, Gegenbeispielen und Evidenz |
| `python/gradient_iso/` | Aktive numerische Methode |
| `python/demo.py` | Ersatz der MATLAB-Demos |
| `python/experiments.py`, `python/figures.py` | Vollständige Reproduktion |
| `python/tests/` | Unabhängige numerische und API-Prüfungen |
| `data/` | CSV/NPZ, generierte Tabellen, Zusammenfassung und Provenienz |
| `figures/generated/` | Aus Daten erzeugte Bilder; PNG im Git, PDF regenerierbar |
| `docs/migration.md` | Datei-Zuordnung und begründete Änderungen |
| `../../legacy/gradient_iso_original/` | Unveränderte Ursprungsdateien mit Manifest |

Das Ursprungsverzeichnis wurde erhalten. Der gemeinsame Schreib-, Notations-
und Bildvertrag liegt in `../../WRITING_GUIDE.md`.
