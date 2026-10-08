# Gradienten-Iso Verfahren: Kurz-Dokumentation

## Ziel
Diese Demo untersucht, ob man aus einer ungeordneten Punktewolke lokale Ableitungsinformation ohne globale Ansatzfunktion gewinnen kann und daraus robuste Outlier-Detektion ableitet.

Kernidee:
1. Delaunay-Triangulation im d-dimensionalen Raum.
2. Pro Simplex lokale affine Approximation und Ableitung (Gradient/Tensor-Komponenten).
3. Iso-Suche je Ableitungskomponente mit `delaunay_search_N`.
4. Dichte der Iso-Punkte als Konsistenzmass.
5. Konfidenzscore und Schwellwertbildung (`mean + sigma * std`) zur Inlier/Outlier-Trennung.

## Wichtige Dateien
- `gradient_iso_pipeline_nd.m`: Allgemeine N-D Pipeline mit Ableitungsordnung `K`.
- `gradient_iso_pipeline_2d.m`: 2D-Wrapper auf die N-D Pipeline.
- `demo_gradient_iso_nd_lab.m`: Interaktive Labor-Demo mit Kennzahlen und Plots.
- `demo_gradient_iso_outlier_validation.m`: Kompakte Validierungsdemo.

## Start
```matlab
clear functions; rehash toolboxcache
cd('C:\Git\Gradienten_Iso_Verfahren')
demo_gradient_iso_nd_lab
```

## Interpretation der Plots (Lab-Fenster)
1. Ground Truth: Rot = kuenstlich injizierte Outlier.
2. Gradient Projection: Lokale Ableitungsstruktur (1. Ordnung).
3. Score: Hoher Score = lokal konsistent/stetiger Bereich.
4. Prediction: Rot = als Outlier klassifiziert.
5. ROC: TPR gegen FPR ueber viele Schwellen.
6. PR: Precision gegen Recall ueber viele Schwellen.

Zusaetzlich bei `d=2`:
- `Gradient-Iso Mesh View` Fenster:
  - Links: Interpolierte Oberflaeche `f(x1,x2)`.
  - Rechts: Interpolierte Score-Oberflaeche mit markierten Outlier-Vorhersagen.

## Bedeutende Parameter
- `d`: Eingabedimension.
- `K` (`approx_order`): Ableitungsordnung.
- `M`: Anzahl Isolinien/-flaechen pro Komponente.
- `validity_range`: Filter fuer zu lange Delaunay-Kanten.
- `sigma_factor`: Schwellwertstaerke in `mean + sigma*std`.
- `noise`, `outlier_frac`, `outlier_strength`: Testschwierigkeit.

## Praktische Empfehlungen
- Fuer schnelle Tests: `d=2..4`, `N=800..1500`, `K=1`.
- Fuer Stabilitaet: zuerst `sigma_factor` in `[0.5, 1.5]` testen.
- Wenn zu viele False Positives: `sigma_factor` erhoehen oder `validity_range` senken.
- Wenn Recall zu gering: `sigma_factor` senken und `M` leicht erhoehen.

## Hinweise
- Hohe Dimension + grosse N kann durch Delaunay teuer werden.
- `Himmelblau` ist nur fuer `d=2` sinnvoll.
- ROC/PR sind aussagekraeftiger als ein einzelner Schwellwertpunkt.
