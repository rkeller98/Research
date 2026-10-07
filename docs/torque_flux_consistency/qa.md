# Prüfung der Research-Dokumentation

Stand 7. Oktober 2026. Der Auftrag wurde am erneut geprüften Git-Stand
`23ab6ef` und den vorhandenen lokalen Änderungen bearbeitet.

Die neue Seite enthält Bestandsanalyse, Konventionen, unabhängige Herleitung,
lokale und globale Beobachtbarkeit, gewichtete Korrektur, elektrische Fusion,
Fehlerquellen, Grenzen, Messplanung und offene Forschungsfragen. Die
mathematische Analyse wurde vor dem isolierten synthetischen Experiment
angelegt. Es wurde keine produktive Korrektur und keine Änderung an realen
Messdaten oder bestehenden Messanalysen vorgenommen.

## Ergebnisse und Darstellung

- 40 numerische Prüfungen bestanden; 1499 synthetische Betriebspunkte und
  100 000 Monte-Carlo-Ziehungen je Strombetrag. Seed und Quelldateihashes sind
  in [results.json](results.json) enthalten und gegen die aktuellen Dateien geprüft.
- Die Standardabweichung des Torque-Flussrauschens weicht an allen sieben
  Strombeträgen um weniger als 0.29 Prozent vom analytischen Wert ab.
- Sechs angeforderte Grafiken und eine zusätzliche Rauschgrafik erzeugt und
  visuell geprüft. Einheiten, Pfeile, Vorzeichen, Legenden, Maskierung des
  Ursprungs und Darstellung der SVD-Nullwerte sind lesbar.
- Alle lokalen Markdown-Links sind gültig. Formelblöcke und Inlineformeln
  wurden geprüft. Die Datei wurde im Codex-Panel zum Öffnen angefordert;
  eine vollständige Sichtprüfung der Markdown-Mathematik im Panel ist nicht
  durch eine beobachtete Vorschau bestätigt.
- `scripts/check_architecture.py` und `git diff --check` bestehen. Neue
  Begriffe sind zentral registriert; vorhandene Glossareinträge und lokale
  Änderungen bleiben erhalten.

PNG-Dateien sind die eingebundenen Research-Grafiken. Der Proof of Concept
erzeugt zusätzlich PDF-Vektorexporte der Grafiken; diese sind gemäß dem
bestehenden `.gitignore` abgeleitete, nicht versionierte Dateien.

## Prüfung der gemeinsamen LaTeX-Infrastruktur

`scripts/build_all.ps1` hat alle neun aktiven Manuskripte erfolgreich gebaut
und nach `output/pdf/` exportiert:

| Manuskript | PDF-Seiten | Sichtgeprüfte Glossar- oder Schlussseite |
|---|---:|---:|
| `eesm_voltage_geometry` | 12 | 12 |
| `flux_map_error_diagnostics` | 31 | 29 |
| `gradient_iso_reconstruction` | 14 | 14 |
| `iemdc_digest_2024` | 6 | 6 |
| `n_dim_rootri` | 5 | 5 |
| `physics_constrained_flux_maps` | 22 | 20 |
| `psm_voltage_geometry` | 14 | 13 |
| `recursive_qp_within_simplex` | 3 | 3 |
| `temp_eesm_Mopt` | 85 | 80 |

Die Seiten wurden mit Poppler gerendert und geprüft; die zwei Flussarbeiten
zusätzlich einzeln. Die neuen unbenutzten Begriffe erscheinen nicht ungefragt
in den vorhandenen Glossaren. Dies ist eine gezielte Sichtprüfung nach der
Glossarerweiterung, keine neue vollständige Layoutprüfung aller 192 PDF-Seiten.

Die ersten Buildversuche trafen auf veraltete Referenz-Hilfsdateien
(`Argument of \@firstoffive has an extra }`). Nach Sicherung unter
`tmp/torque_eesm_build_before_retry/` bzw. `tmp/torque_build_before_retry/`
und Neugenerierung der Hilfsdateien bestehen die Builds ohne Änderung an
Manuskripttexten oder Buildskripten. Das Abschlusslog liegt in
`tmp/torque_build_all_final.log`; gerenderte Prüfbilder und die Auswertung
der Abschlusslogs liegen unter `tmp/torque_pdf_qa/`.

Im Abschlusslog von `flux_map_error_diagnostics` bleibt ein `Overfull \vbox`
von 1.1203 pt im unveränderten Abschnitt zur Winkeldiagnose. Die übrigen
acht Abschlusslogs enthalten keine `Warning:`- oder Overfull-Meldung.
Es sind keine neuen undefinierten Referenzen oder Zitate verblieben.

## Offene experimentelle Voraussetzung

`CAN_Torque_meas` wurde in beiden Datensätzen gefunden; Herkunft, Einheiten,
Unabhängigkeit und die Momentbilanz sind weiterhin zu qualifizieren. Die
numerischen Ergebnisse sind synthetische Modelldemonstrationen und ersetzen
diese Qualifizierung nicht.
