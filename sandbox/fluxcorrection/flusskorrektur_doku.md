# Forschungsnotiz: Physikalische Diagnose und mögliche Korrektur rekonstruierter Flusskennfelder


<!-- BEGIN WRITING GUIDE: GESCHUETZT -->
## 0. Writing Guide – verbindliche Regeln für diese Forschungsnotiz

**Geltungsbereich:** Dieser Guide ist die verbindliche redaktionelle und wissenschaftliche Arbeitsgrundlage für alle künftigen Ergänzungen, Korrekturen, Konsolidierungen und Umstrukturierungen dieser Datei.

**Änderungsschutz:** **Der Writing Guide selbst darf ausschließlich auf ausdrückliche Aufforderung des Nutzers verändert werden.** Ohne einen solchen Auftrag sind seine Aussagen, Reihenfolge und Bedeutung beizubehalten; er darf weder stillschweigend gekürzt, gelöscht, verschoben noch durch neue Regeln ersetzt werden. Ein allgemeiner Auftrag zur Überarbeitung der Forschungsnotiz ist **keine** Erlaubnis, diesen Guide zu verändern. Die übrige Forschungsnotiz darf gemäß diesen Regeln weiterentwickelt werden. Inhaltliche Konflikte mit dem Guide werden offengelegt und mit dem Nutzer geklärt, nicht heimlich durch Änderung des Guides gelöst.

### 0.1 Ziel und wissenschaftliche Perspektive

Die Datei dokumentiert den **aktuellen Erkenntnisstand** zur physikalischen Diagnose und gegebenenfalls begründbaren Korrektur rekonstruierter Flusskennfelder elektrischer Maschinen. Ausgangspunkt sind reale elektrische Messgrößen, ihre Mess- und Modellannahmen sowie die Frage der **Identifizierbarkeit** physikalischer, dissipativer, messtechnischer und numerischer Effekte.

Die historische Drehmomentfrage ist **ein Teilansatz**, nicht mehr das übergeordnete Forschungsziel. Widerstandsfehler, Winkel- und Spannungserfassung, Drehmoment, Coenergy, Integrabilität, Eisenverluste, Mehrdrehzahlmessungen und Approximation sind miteinander verknüpfte Diagnosewerkzeuge. Keine einzelne Hypothese darf ohne Evidenz zum Hauptziel umgedeutet werden.

### 0.2 Darstellung und Gliederung

- **Vom heutigen Verständnis ausgehen:** Zuerst Leitfrage, Begriffe, Modellannahmen, gesicherte Erkenntnisse und aktueller numerischer/experimenteller Stand; danach Hypothesen, Grenzen und nächste Schritte. Der Haupttext ist **kein chronologisches Chatprotokoll**.
- **Forschungsverlauf bewahren:** Wertvolle frühe Ideen, Gegenbeispiele, widerlegte Vermutungen und negative Ergebnisse bleiben fachlich nachvollziehbar, gegebenenfalls in einem ausdrücklich historischen Abschnitt. Keine Erkenntnisse nur deshalb löschen, weil sich die Leitfrage verändert hat. Git-Historie ergänzt, ersetzt aber keine verständliche fachliche Einordnung.
- **Dopplungen konsolidieren:** Jede Aussage soll einen klaren Platz haben. Verwandte Herleitungen zusammenführen und auf bestehende Abschnitte verweisen, anstatt dieselbe Erklärung erneut anzuhängen.
- **Lesbar und präzise schreiben:** Deutsche Fachsprache, konsistente Symbole, kurze Einordnungen vor Gleichungen und nachvollziehbare Interpretation danach. Geometrische Anschauung und aussagekräftige Skizzen/Plots sind ausdrücklich erwünscht; Bilder müssen Annahmen und Grenzen korrekt wiedergeben.

### 0.3 Evidenzstatus und wissenschaftliche Redlichkeit

Jede wichtige Aussage ist ihrer Begründungsstufe nach erkennbar:

1. **Mathematisch hergeleitet:** Aussage folgt unter ausdrücklich angegebenen Voraussetzungen.
2. **Modellabhängig:** Ergebnis eines idealisierten oder bewusst konstruierten physikalischen Ersatzmodells.
3. **Numerisch überprüft:** Ergebnis eines dokumentierten synthetischen oder realen Rechenexperiments; keine automatische Aussage über die physikalische Wahrheit.
4. **Experimentell beobachtet:** Befund aus benannten realen Messdaten, mit Mess- und Datenqualitätsvorbehalten.
5. **Hypothese / offen:** Plausible Deutung, noch nicht identifizierte Ursache, ausstehende Validierung oder offene Entscheidung.

Keine Hypothese als Ergebnis, keine Korrelation als Kausalnachweis und keine numerische Passung als physikalische Validierung darstellen. Grenzen und mögliche Alternativerklärungen sollen in unmittelbarer Nähe der Aussage stehen. Nicht vorhandene Messungen, Referenzwerte oder Literaturbelege werden nicht erfunden.

### 0.4 Mathematik, Notation und Herleitungen

- Variablen, Einheiten, Vorzeichenkonventionen, Modellgrenzen und Gültigkeitsbereiche vor ihrer Verwendung definieren; insbesondere magnetische und elektrische Winkelgeschwindigkeit, Stromkoordinaten, Leistungs-/Drehmomentbilanz und amplitude-invariante dq-Konvention auseinanderhalten.
- Zwischen **zeitlicher Ableitung**, **partieller Ableitung**, **Differential-/Sekanteninduktivität**, **Wegintegral** und **statistischer Approximation** unterscheiden. Die Jacobi-Matrix der Flüsse und die Hesse-Matrix einer Koenergie nur unter den jeweils nötigen Voraussetzungen identifizieren.
- Wesentliche Gleichungen schrittweise herleiten, ihre geometrische Bedeutung erklären und Sonderfälle bzw. Gegenbeispiele prüfen. Keine zusätzlichen Coenergy-Terme oder Fehlergesetze kommentarlos als Naturgesetze einführen.
- Eine aus Coenergy abgeleitete konservative Flusskomponente ist nicht mit dem aus realen Klemmenmessungen rekonstruierten Feld gleichzusetzen. Ein integrables Feld muss nicht physikalisch korrekt sein; Integrabilitätsverletzungen sind ohne Zusatzinformation **nicht eindeutig Eisenverlusten zuzuschreiben**.

### 0.5 Numerische Experimente, Messdaten und Reproduzierbarkeit

- **Rohdaten unverändert erhalten.** Datenimport, Bereinigung/Aggregation, Rekonstruktion, unabhängige Approximation, konservative Projektion und diagnostische Residuen als unterscheidbare Verarbeitungsschritte mit Provenienz dokumentieren. Keine potenziell physikalisch bedeutsamen Abweichungen durch Symmetrisierung oder Coenergy-Fits stillschweigend entfernen.
- Existierende Funktionen und Datenverträge im Repository wiederverwenden; synthetische Lehrmodelle und reale Untersuchungen in getrennten Skripten führen. Messkampagnen, Temperatur-*referenzen*, Drehzahlen, Phasenkonfigurationen und tatsächlich gemessene Größen korrekt benennen.
- Für jede relevante Approximation dokumentieren: Datenquelle, Gruppierung, Trainings-/Validierungs-/Testauswahl, Seed, verwendete Eingangs- und Ausgangsskalierung, Kernel/Basis, Form- und Glättungsparameter, Domänenabdeckung und Fehlermetrik **mit Einheit und Normierungsdefinition**.
- Parameterwahl nur anhand der Entwicklungsdaten begründen; zurückgehaltene Testdaten nicht stillschweigend zur Optimierung verwenden. Ein kleiner Fluss-(N)RMSE bescheinigt **weder Ableitungsgenauigkeit noch Integrabilität oder physikalische Richtigkeit**.
- Normierte Koordinaten verlangen bei Ableitungen die explizite Rücktransformation per Kettenregel. Ein auf einem Rechteck ausgewertetes globales Modell darf außerhalb des tatsächlich gemessenen Bereichs nicht als gesicherte Messinformation erscheinen; Rand- und Extrapolationsprobleme ausdrücklich kennzeichnen.
- Synthetische Belege validieren die numerische Methode **innerhalb ihres Modells**; reale Befunde erfordern eigene Unsicherheits-, Messketten- und Identifizierbarkeitsprüfung.

### 0.6 Arbeitsweise und Pflege der Forschungsnotiz

Die gemeinsame Arbeit folgt dem vereinbarten **Lehrmodus**: zuerst Intuition und selbstständige Herleitung, dann kleine selbst programmierte Schritte mit gezieltem Feedback. Keine ungefragten Komplettlösungen, fertigen Optimierungsalgorithmen oder umfassenden Refactorings. Relevante Erkenntnisse aus neuen Sitzungen fachlich einordnen und in den bestehenden Text integrieren; Zeitstände und noch nicht geprüfte Schritte aktualisieren, ohne erledigte Schritte als offen oder offene Schritte als abgeschlossen darzustellen.


### 0.7 Quellenarbeit als Lernwerkzeug: bekannte Ergebnisse selbst herleiten

**Externe Quellen sind ausdrücklich erlaubt und erwünscht.** Fachbücher, wissenschaftliche Veröffentlichungen, technische Dokumentationen und seriöse Internetquellen dürfen recherchiert und genutzt werden. Die Kenntnis einer veröffentlichten Lösung ist kein Grund, die eigene Herleitung zu überspringen. Umgekehrt ist eine unabhängig nachvollzogene Herleitung **kein Anspruch darauf, das Ergebnis erstmals entdeckt zu haben**.

**Lernprinzip: „Wir kennen eine mögliche Lösung aus der Literatur – und erarbeiten sie dennoch selbst.“**

1. **Problem und Quelle einordnen:** Was beantwortet das Paper tatsächlich? Welche Voraussetzungen, Konventionen, Vereinfachungen und Gültigkeitsgrenzen verwendet es?
2. **Eigene Intuition entwickeln:** Physikalische und geometrische Bedeutung der Größen verstehen; das Problem zunächst möglichst selbst formulieren. Bekannte Resultate als Orientierung, Plausibilitätskontrolle oder Anlass für gezielte Hinweise nutzen, nicht als fertige Antwort zum Abschreiben.
3. **Selbst herleiten:** Die mathematischen Schritte vom Ausgangspunkt an nachvollziehen; notwendige Zwischenschritte, Einheiten, Sonderfälle und alternative Wege untersuchen. Die Lehrbegleitung gibt dafür gezielte Fragen und Hinweise statt ungefragter Komplettlösungen.
4. **Mit der Literatur abgleichen:** Übereinstimmungen, abweichende Konventionen, nicht erfüllte Annahmen und offene Widersprüche benennen. Zwischen einem **bekannten Literaturergebnis**, unserer **eigenständig erarbeiteten Herleitung** und einer möglicherweise **neuen Hypothese** klar unterscheiden.
5. **Reproduzierbar dokumentieren:** Jede tatsächlich verwendete Quelle unmittelbar bei der betreffenden Herleitung/Argumentation und in einer nachvollziehbaren Quellenangabe festhalten. Mindestens Autoren/Institution, Titel, Erscheinungsjahr, bei Veröffentlichungen DOI oder stabile URL, relevante Seiten/Abschnitte/Gleichungen; bei Online-Dokumentation zusätzlich Version/Stand und Abrufdatum, soweit verfügbar. Den konkreten Beitrag der Quelle nennen (z. B. Modellannahme, etablierte Methode, Referenzresultat oder Vergleich). **Keine Quellen oder Prioritätsansprüche erfinden.**

Quelle und eigener Erkenntnisweg sollen gemeinsam sichtbar bleiben: Die Dokumentation darf weder ein kommentarloses Referat noch eine Darstellung bekannter Mathematik als vermeintlich originäre Entdeckung sein. Auch eine bereits veröffentlichte Herleitung nachzuvollziehen ist ein eigenständiger Lernerfolg.

### 0.8 Verständnis vor bloßer Anwendung; dokumentierte Open Issues

**Mathematik soll verstanden werden und nicht lediglich ein funktionierendes Werkzeug liefern.** Das gilt ausdrücklich auch für anspruchsvolle Themen. Zu einer verstandenen Methode gehören – ihrem Gegenstand angemessen – Problemdefinition und Motivation, geometrische/physikalische Intuition, eigenständig nachvollzogene Herleitung, Voraussetzungen, numerische Umsetzung und Fehlermöglichkeiten sowie die Aussagegrenzen der Ergebnisse. „Die Bibliothek liefert ein Ergebnis“ oder „der Fit sieht gut aus“ reicht als Verständnisnachweis nicht.

**Pragmatische Ausnahme:** Eine etablierte Methode (z. B. Interpolation, glättende Approximation, RBF, numerische Ableitung oder Optimierung) darf zunächst als *bewusst vorläufiges Werkzeug* eingesetzt werden, damit das eigentliche Experiment weitergehen kann. Die Methode gilt damit **nicht** als verstanden oder validiert.

**Verbindliche Open-Issue-Regel:** Für jede wesentlich verwendete, aber mathematisch/physikalisch noch nicht verstandene Methode wird **in dieser Forschungsnotiz** ein ausdrücklich gekennzeichnetes **Open Issue / eine offene Verständnisfrage** festgehalten – möglichst bereits bei der erstmaligen vorläufigen Verwendung, spätestens bei der Dokumentation des Experiments. Der Eintrag enthält:
- **Gegenstand und Einsatz:** Welche Methode wird wofür aktuell benutzt und unter welchen Voraussetzungen?
- **Was ist noch unverstanden?** Konkrete Fragen nach dem *Warum*, dem *Wie*, der Herleitung, der Geometrie, den Annahmen, der Parametrierung oder dem Versagen.
- **Lernziel und Prüfkriterium:** Welche eigene Herleitung, anschauliche Erklärung, Minimalrechnung oder numerische Gegenprobe wird das Verständnis vertiefen?
- **Quellen und Status:** Verwendete Literatur gemäß Abschnitt 0.7 oder „noch keine Quelle ausgewertet“; Status **offen / in Bearbeitung / nachvollzogen**, gegebenenfalls Datum und Verweise auf die spätere Bearbeitung.

Open Issues sind **Lernaufgaben, keine Verschleierung von Unsicherheit und nicht automatisch Softwarefehler oder GitHub-Tickets**. Sie dürfen nicht stillschweigend verschwinden. Nach eigenständigem Durcharbeiten wird die Lösung erläutert und der Status nachvollziehbar aktualisiert; ein bloßer funktionierender Programmaufruf oder das Kopieren einer Literaturformel schließt ein Verständnis-Issue nicht.

### 0.9 Persönlicher Zweck des Projekts

Diese Forschung ist bewusst **ein persönliches Lern- und Entwicklungsprojekt**. Ihr Wert bemisst sich nicht nur an einem funktionierenden Algorithmus, einer schnellen Korrektur oder einer Publikation, sondern daran, das **mathematische, physikalische und methodische Verständnis sowie die eigenständige Problemlösungsfähigkeit** nachhaltig auszubauen. Schwierige Grundlagen dürfen deshalb ausdrücklich vertieft werden. Tempo und Implementierungsumfang sollen dem Lernen dienen, nicht umgekehrt.

**Vorrang:** Der Writing Guide bleibt unverändert, bis sein Inhalt vom Nutzer ausdrücklich zur Änderung freigegeben wird. Überarbeitungen des Forschungsinhalts müssen sich an ihm orientieren.

<!-- END WRITING GUIDE: GESCHUETZT -->
---

**Stand der Fachnotiz:** 10.10.2026  
**Projektstatus:** laufende theoretische und numerische Untersuchung; **keine** physikalisch eindeutig identifizierte oder experimentell validierte Flusskorrektur  
**Primäres Arbeitsverzeichnis:** `sandbox/fluxcorrection/` im Repository `rkeller98/Research`, Arbeitsbranch `topic/fluxcorrection`  
**Lesart:** Mathematisch hergeleitet / modellabhängig / experimentell beobachtet / offen wird ausdrücklich unterschieden.

## 1. Forschungsauftrag und aktuelle Leitfrage

**Leitfrage:** *Wie können wir aus verfügbaren elektrischen Rohmessdaten rekonstruierte Flusskennfelder elektrischer Maschinen auf physikalische Plausibilität und innere Konsistenz untersuchen, systematische Mess- und Modellfehler von realen magnetischen und dissipativen Effekten unterscheiden und – soweit die verfügbaren Informationen ausreichen – begründete Korrekturen ableiten, ohne physikalisch relevante Abweichungen zu unterdrücken?*

Die zentrale zusätzliche Frage ist **Identifizierbarkeit**: Welche Fehlerkomponenten sind aufgrund der beobachteten Größen überhaupt bestimmbar? Wo existieren nicht beobachtbare Freiheitsgrade, und welche unabhängigen Messungen oder begründeten Modellannahmen wären nötig, um sie festzulegen?

**Motivation.** Bei elektrischen Maschinen fallen unter anderem verkippte Flusskennflächen, Asymmetrien und Abweichungen zwischen rekonstruierten Flüssen, Drehmoment, Induktivitäten und Verlustbetrachtungen auf. Nicht jede Auffälligkeit ist ein Messfehler. Echte Sättigung und Kreuzsättigung gehören ebenso zum Maschinenverhalten wie mögliche dissipative Effekte. Die Diagnose soll unterscheiden zwischen:

1. **Physikalischen Effekten:** Sättigung, Kreuzsättigung, Hysterese und Eisenverlusten.
2. **Messketteneffekten:** Strom-/Spannungserfassung, Winkeloffsets, Synchronisierung, PWM-/Umrichtereffekten, Kanal- und Signalkonventionen.
3. **Parameter- und Modellfehlern:** z. B. Statorwiderstand, Temperaturannahmen, stationäres Ersatzmodell und Phasenkonfiguration.
4. **Numerischen Artefakten:** Gruppierung, Interpolation, Glättung, Fit, Ableitung, unzureichender Stützbereich und Extrapolation.

Der ursprüngliche **Drehmomentvergleich** war der Einstieg in die Fragestellung. Er bleibt ein wichtiges Diagnoseinstrument, ist aber **nicht mehr das übergeordnete Forschungsziel**. Die historische Entwicklung einschließlich gescheiterter Eindeutigkeitsannahmen ist in Abschnitt 14 dokumentiert.

### 1.1 Was gilt als Erfolg?

Ein Erfolg wäre zunächst **kein perfekt geglättetes Kennfeld**, sondern ein nachvollziehbarer, reproduzierbarer Befund darüber,

- welche Daten und Modellannahmen einer Flussrekonstruktion zugrunde liegen;
- welche Eigenschaften ein konservatives magnetisches Modell erfüllen muss;
- welche Abweichungen im real rekonstruierten Feld vorkommen und robust nachweisbar sind;
- welche physikalischen Erklärungen mit den Messungen **vereinbar**, **nicht unterscheidbar** oder **widerlegt** sind;
- ob für eine Korrektur genügend unabhängige Information vorliegt.

Eine höhere mathematische Konsistenz ist nicht automatisch eine höhere physikalische Aussagekraft. **Messfeld, Approximation, Modellprojektion und Residuum dürfen einander nicht überschreiben.**

## 2. Datenfluss, Beobachtbarkeit und Evidenzstufen

Der derzeit verwendete Analyseweg lautet:

```text
Unveränderte Rohmessungen + Provenienz
    → vorbereitete / gruppierte stationäre Betriebspunkte
    → rekonstruierte effektive Flussverkettungen aus u, i, Rs, ωe
    → zwei voneinander unabhängige glatte Flussapproximationen
    → Ableitungen, Jacobi-Matrix und Integrabilitäts-/Symmetriediagnose
    → Abgleich mit Messunsicherheit, Drehmoment, Drehzahl und Fehlermodellen
    → gegebenenfalls gesonderte konservative Projektion + erhaltenes Residuum
```

**Wichtig:** Die physikalisch wahren magnetischen Flüsse werden mit dem derzeitigen PSM-Datensatz **nicht direkt gemessen**. Das Ergebnis der stationären Spannungsgleichungen ist ein durch ihre Annahmen bestimmtes, *effektiv rekonstruiertes* Flussfeld. Ein Fit hierauf kann einen Rekonstruktionsfehler nicht von sich aus korrigieren.

Wir halten deshalb drei fachliche Ebenen auseinander:

| Ebene | Was liegt vor? | Was ist damit noch nicht bewiesen? |
| --- | --- | --- |
| Messung | Spannungen, Ströme, Drehzahl, Temperaturreferenzen und ggf. Drehmoment | Korrekte Sensorkalibrierung, stationärer magnetischer Zustand |
| Rekonstruktion | \(\boldsymbol\psi_{\mathrm{rec}}(\boldsymbol i)\) aus gewähltem dq-Ersatzmodell | Identität mit dem konservativen Magnetisierungsfluss |
| Diagnose | Approximationen, \(\mathbf J_\psi\), Residuen, Symmetrie- und Torque-Vergleiche | Eindeutige Zuordnung eines Residuums zu Eisenverlusten oder einem Sensorfehler |

Die mathematischen Formeln der nächsten Kapitel sind innerhalb ihrer definierten Modelle hergeleitet. Reale Messdaten und synthetische Modellnachweise werden in Abschnitt 10 getrennt berichtet.

## 3. Mathematische Grundlagen: dq-Gleichungen und Flussrekonstruktion

### 3.1 Konventionen

Wir betrachten zunächst eine **dreiphasige PSM** mit amplitudeninvarianter dq-Transformation, rotorfesten Achsen und einer konsistenten positiven Motor-/Drehzahlkonvention. Es seien

\[
\boldsymbol i=(i_d,i_q)^\mathsf T,\qquad
\boldsymbol\psi=(\psi_d,\psi_q)^\mathsf T,\qquad
\omega_e=p\,\omega_m,\qquad
k_T=\frac32p,
\]

mit Polpaarzahl \(p\), elektrischer Winkelgeschwindigkeit \(\omega_e\) in rad/s und mechanischer Winkelgeschwindigkeit \(\omega_m\) in rad/s. Der einfache elektromagnetische Drehmomentausdruck lautet

\[
M_{\mathrm{em}}=k_T(\psi_di_q-\psi_qi_d).
\]

Bei **anderen Phasensystemen** muss insbesondere der Drehmomentfaktor gesondert qualifiziert werden; er darf nicht stillschweigend von einer dreiphasigen PSM übernommen werden.

### 3.2 Zeitliche Ableitung versus Stromableitung

Die allgemeinen dq-Spannungsgleichungen lauten unter diesen Vorzeichenkonventionen

\[
\begin{aligned}
u_d&=R_si_d+\frac{d\psi_d}{dt}-\omega_e\psi_q,\\
u_q&=R_si_q+\frac{d\psi_q}{dt}+\omega_e\psi_d.
\end{aligned}
\]

Die Terme \(d\psi_d/dt\) und \(d\psi_q/dt\) beschreiben **zeitliche** Änderungen. Davon zu unterscheiden sind die partiellen **Stromableitungen** der Kennfelder, z. B. \(\partial\psi_d/\partial i_q\), welche die differentiellen Induktivitäten definieren.

Für einen stationären dq-Zustand mit zeitlich konstanten Flussverkettungen verschwinden die Zeitableitungen. Daher

\[
u_d=R_si_d-\omega_e\psi_q,\qquad
u_q=R_si_q+\omega_e\psi_d.
\]

Bei \(\omega_e\neq0\) erhalten wir durch Umstellen

\[
\boxed{
\psi_{d,\mathrm{rec}}=\frac{u_q-R_si_q}{\omega_e},\qquad
\psi_{q,\mathrm{rec}}=\frac{R_si_d-u_d}{\omega_e}.
}
\]

**Gültigkeitsgrenze:** Diese Formeln verwenden genau die eingesetzten Spannungs-, Strom-, Widerstands- und Drehzahlwerte; sie isolieren **keinen** Eisenverlustanteil, Winkelmessfehler oder Spannungsrekonstruktionsfehler. Bei stillstehender Maschine ist diese stationäre Division durch \(\omega_e\) nicht möglich.

## 4. Konservative Magnetisierung, Coenergy und differentielle Induktivitäten

### 4.1 Geometrische Bedeutung einer gemeinsamen Coenergy

Für ein idealisiert konservatives magnetisches System kann eine skalare *normierte* Koenergie \(W'(i_d,i_q)\) existieren mit

\[
\boldsymbol\psi_{\mathrm{mag}}=\nabla_iW'
=\begin{bmatrix}
\partial W'/\partial i_d\\
\partial W'/\partial i_q
\end{bmatrix}.
\]

Anschaulich sind \(\psi_d\) und \(\psi_q\) die beiden lokalen Steigungen **einer einzigen Potentiallandschaft** in zwei Stromrichtungen. Im amplitudeninvarianten dreiphasigen dq-System ist die hier gebrauchte Coenergy hinsichtlich des \(3/2\)-Faktors normiert; die entsprechend bilanzierte dreiphasige magnetische Koenergie trägt diesen Faktor zusätzlich. Die genaue Energie-/Leistungskonvention bleibt bei Verallgemeinerungen explizit anzugeben.

Die Jacobi-Matrix des Flusses ist

\[
\mathbf L_{\mathrm{diff}}
:=\mathbf J_{\psi}
=
\begin{bmatrix}
L_{dd}&L_{dq}\\
L_{qd}&L_{qq}
\end{bmatrix}
=
\begin{bmatrix}
\partial\psi_d/\partial i_d & \partial\psi_d/\partial i_q\\
\partial\psi_q/\partial i_d & \partial\psi_q/\partial i_q
\end{bmatrix}.
\]

Wenn \(W'\) mindestens zweimal stetig differenzierbar ist, gilt die Gleichheit gemischter zweiter Ableitungen:

\[
\boxed{L_{dq}=L_{qd}.}
\]

Die **Integrabilitäts- bzw. Reziprozitätsbedingung** für ein zunächst unabhängig gegebenes Flussfeld lautet damit

\[
\boxed{
r_{\mathrm{int}}:=
\frac{\partial\psi_d}{\partial i_q}
-\frac{\partial\psi_q}{\partial i_d}=0.
}
\]

Unsere Residualkonvention ist damit **das Negative** des üblichen skalaren 2D-Curls \(\partial_{i_d}\psi_q-\partial_{i_q}\psi_d\); Vorzeichen dürfen beim Vergleich nicht unbemerkt wechseln. Auf einem einfach zusammenhängenden Gebiet ist das verschwindende Residuum unter geeigneten Glattheitsannahmen hinreichend für ein skalares Potential. Die zugehörigen Wegintegrale

\[
\Delta W'=\int_\Gamma \boldsymbol\psi\cdot d\boldsymbol i
\]

sind dann unabhängig vom gewählten Weg zwischen zwei festgehaltenen Strompunkten. Die Bezeichnung *Wegintegral* ist hier präziser als „partielle Integration“.

### 4.2 Konservativ bedeutet nicht linear oder entkoppelt

Als einfaches Referenzmodell diente

\[
\psi_d=\psi_{\mathrm{PM}}+L_di_d,\qquad
\psi_q=L_qi_q,\qquad
W'_0=\psi_{\mathrm{PM}}i_d+\frac12L_di_d^2+\frac12L_qi_q^2.
\]

Dies ist **ein spezielles lineares Modell**, nicht die Definition physikalisch idealer Magnetisierung. Um Kreuzsättigung *didaktisch* zu modellieren, kann eine bewusst konstruierte gemeinsame Coenergy beispielsweise enthalten

\[
W'=W'_0+\frac{\gamma}{2}i_di_q^2+\frac{\beta}{2}i_d^2i_q^2.
\]

Aus dem Gradienten folgen

\[
\begin{aligned}
\psi_d&=\psi_{\mathrm{PM}}+L_di_d+\frac{\gamma}{2}i_q^2+\beta i_di_q^2,\\
\psi_q&=L_qi_q+\gamma i_di_q+\beta i_d^2i_q.
\end{aligned}
\]

Erneutes Differenzieren liefert

\[
\boxed{
\begin{aligned}
L_{dd}&=L_d+\beta i_q^2,\\
L_{qq}&=L_q+\gamma i_d+\beta i_d^2,\\
L_{dq}&=L_{qd}=\gamma i_q+2\beta i_di_q.
\end{aligned}}
\]

Somit können die **Hauptinduktivitäten stromabhängig** und die **Kreuzinduktivitäten symmetrisch** sein. Die Koeffizienten \(\gamma,\beta\) sind **nicht aus unseren realen Messungen identifiziert**, sondern dienen zur nachvollziehbaren Modellkonstruktion. Die Herleitung einer zusätzlichen Coenergy-Funktion ist stets auf ihre Voraussetzungen und Auswirkungen auf **alle** Flusskomponenten zu prüfen.

### 4.3 Symmetrie ist eine eigene Hypothese

Eine idealisiert zur d-Achse spiegelsymmetrische PSM im korrekt orientierten dq-System kann die Beziehungen

\[
\psi_d(i_d,-i_q)=\psi_d(i_d,i_q),\qquad
\psi_q(i_d,-i_q)=-\psi_q(i_d,i_q)
\]

erfüllen. Diese Forderung ist **nicht** bereits aus der Existenz einer Coenergy ableitbar. Konstant nichtverschwindende Kreuzinduktivitäten könnten diese Symmetrie verletzen, während nichtlineare Kreuzsättigung mit beiden Bedingungen vereinbar ist.

Konstante Flussoffsets \((c_d,c_q)\) besitzen verschwindende Kreuzableitungen und sind selbst integrabel:

\[
\Delta W'=c_di_d+c_qi_q.
\]

Die Integrabilitätsprüfung übersieht solche Offsets, obwohl sie z. B. die Symmetrie und das berechnete Moment verändern können:

\[
\Delta M=k_T(c_di_q-c_qi_d).
\]

**Konsequenz:** Integrabilität, vorausgesetzte Maschinensymmetrie und unabhängige Fluss-/Drehmomentreferenzen prüfen **verschiedene** Eigenschaften. Eine konservative Kennfläche kann dennoch einen physikalisch falschen Offset oder eine falsche Skalierung aufweisen.

## 5. Was sich aus einem Drehmomentvergleich bestimmen lässt – und was nicht

### 5.1 Die beobachtete Flussrichtung

Für festgehaltene \(i_d,i_q\) sei ein additiver Flussunterschied \(\delta\boldsymbol\psi\) definiert, so dass \(\delta M=M_{\mathrm{ziel}}-M_{\mathrm{rec}}\) gilt. Dann folgt **exakt** (nicht nur infinitesimal), weil das Drehmoment bei fixen Strömen linear in den Flüssen ist:

\[
\delta M=k_T(i_q\delta\psi_d-i_d\delta\psi_q)
=k_T\,\underbrace{\begin{bmatrix}i_q&-i_d\end{bmatrix}}_{\boldsymbol a^\mathsf T}
\delta\boldsymbol\psi.
\]

Der Beobachtungsvektor ist zum Stromvektor orthogonal:

\[
\boldsymbol a^\mathsf T\boldsymbol i=i_qi_d-i_di_q=0.
\]

**Geometrie:** Der Drehmomentvergleich erkennt bei gegebenem Strom nur die Projektion eines Flussunterschiedes auf die Richtung \((i_q,-i_d)\), also **senkrecht zum Strom**. Die zum Strom **parallele** Komponente liegt im Nullraum. Bei \(\boldsymbol i=\boldsymbol0\) liefert das ideale Drehmoment überhaupt keine Flussinformation.

Ein Messpunkt liefert damit **eine skalare** Gleichung für zwei unbekannte Flussunterschiede. Auch \(N\) getrennte Strompunkte geben ohne weitere Einschränkungen zunächst nur \(N\) skalare Gleichungen für \(2N\) Korrekturkomponenten.

### 5.2 Warum selbst Drehmoment **und** Coenergy nicht eindeutig sind

Nehmen wir an, ein physikalisch zulässiges Zielfeld erfüllt bereits sowohl eine Drehmomentbedingung als auch die Integrabilität. Ein Zusatz

\[
\boldsymbol h(\boldsymbol i)=c(\boldsymbol i)\,\boldsymbol i
\]

bleibt drehmomentneutral, weil \(i_qh_d-i_dh_q=0\). Damit auch **der Zusatz** integrabel ist, muss gelten

\[
\frac{\partial(ci_d)}{\partial i_q}
=
\frac{\partial(ci_q)}{\partial i_d}
\quad\Longleftrightarrow\quad
i_d\frac{\partial c}{\partial i_q}
=i_q\frac{\partial c}{\partial i_d}.
\]

Wir wählen \(s=i_d^2+i_q^2\) und \(c=f(s)\). Mit der Kettenregel folgt

\[
\partial_{i_d}c=2i_df'(s),\qquad
\partial_{i_q}c=2i_qf'(s).
\]

Beide Seiten werden dadurch zu \(2i_di_qf'(s)\). Für jede hinreichend glatte Funktion \(f\) existiert somit die drehmomentneutrale **und** integrable Familie

\[
\boxed{\boldsymbol h=f(i_d^2+i_q^2)\,\boldsymbol i.}
\]

Geometrisch ist \(c\) entlang der Kreistangentialrichtung \((-i_q,i_d)\) konstant. Auf rotationszusammenhängenden Bereichen beschreibt \(f(I^2)\) die entsprechende radiale Lösungsfamilie (am Ursprung sind zusätzliche Regularitätsfragen zu berücksichtigen). Die Aussage setzt voraus, dass **bereits ein** gemeinsames zulässiges Zielfeld gefunden wurde; der Zusatz repariert ein nichtintegrables Ausgangsfeld nicht.

Der konstante Spezialfall \(\boldsymbol h=c\boldsymbol i\) verändert z. B. \(L_{dd}\) um \(c\). Auch **differentielle Induktivitäten können also ohne Änderung des Drehmoments und ohne Reziprozitätsverletzung anders ausfallen**.

Ein vorgegebener Ursprungspunkt \(\psi_d(0,0)=\psi_{\rm PM}\), \(\psi_q(0,0)=0\) bestimmt eine solche radiale Freiheitsfunktion **nicht**, da der Zusatz am Ursprung für reguläres \(f\) verschwindet. Eine zusätzliche unabhängige Flussmessung bei einem bestimmten Radius würde grundsätzlich nur dort Information über \(f\) liefern. Ein ganzes Feld bleibt ohne weitere unabhängige Beobachtungen/Annahmen mehrdeutig.

**Gesichertes negatives Forschungsergebnis (innerhalb des Modells):** Drehmomentdaten zusammen mit Reziprozität liefern **keine allgemeine eindeutige Flusskorrektur**.

## 6. Mess- und Parameterfehler als prüfbare Hypothesen

### 6.1 Falscher Statorwiderstand

Wir definieren die Fehlerkonvention in diesem Teil ausdrücklich als

\[
\Delta R:=R_{\rm verwendet}-R_{\rm wahr},\qquad
\Delta\boldsymbol\psi:=
\boldsymbol\psi_{\rm rec}-\boldsymbol\psi_{\rm wahr}
\]

bei **unveränderten gemessenen** \(u,i,\omega_e\) und ideal stationären dq-Gleichungen. Direktes Subtrahieren der Rekonstruktionsformeln ergibt

\[
\boxed{
\Delta\psi_d=-\frac{\Delta R}{\omega_e}i_q,\qquad
\Delta\psi_q=+\frac{\Delta R}{\omega_e}i_d
}
\]

und damit

\[
\boxed{
\Delta M_R=-\frac{k_T\Delta R}{\omega_e}(i_d^2+i_q^2).
}
\]

Geometrisch erzeugt ein konstanter Widerstandsmismatch **geneigte Zusatzebenen**, keine starre Rotation des Flussfelds. Der Flussfehler ist **senkrecht** zu \(\boldsymbol i\), der Drehmomentfehler bei konstanter positiver Drehzahl quadratisch im Strombetrag und **bei gleichem Strombetrag unabhängig vom Stromwinkel**. Bei unveränderten Strömen und Modellannahmen skaliert er mit \(1/\omega_e\).

Die Niveaulinien eines gegebenen Widerstands-Drehmomentfehlers bilden Kreise um den Stromursprung, soweit das Vorzeichen des verlangten Niveaus realisierbar ist. \(\Delta M_R/I^2\) ist nur für \(I\neq0\) definiert und bei sehr kleinem \(I\) numerisch empfindlich. Eine Gerade von \(\Delta M_R\) über \(I^2\) hätte im Modell die Steigung \(-k_T\Delta R/\omega_e\), die aber zunächst **nur einen äquivalenten Fehlereffekt** beschreibt.

Bei festgehaltenem Fluss bewirkt eine Änderung des Widerstands \(\delta\boldsymbol u_R=\delta R\,\boldsymbol i\); bei festem Widerstand bewirkt eine **radiale** Flussänderung \(c\boldsymbol i\) die Spannungsänderung \(\delta\boldsymbol u_{\rm radial}=\omega_ec(-i_q,i_d)^\mathsf T\). Diese **speziellen Spannungskomponenten** sind orthogonal. Sie dürfen nicht mit dem oben stehenden, **orthogonalen Flussausgleich** bei unveränderten Spannungswerten verwechselt werden.

### 6.2 Winkel, Spannung und tatsächlicher Betriebszustand

Ein falsch bestimmter Rotorwinkel, eine fehlerhafte Strom-/Spannungssynchronisierung oder eine falsch rekonstruierte Maschinenklemmen-Spannungsgrundschwingung können die Flusskennfelder ebenfalls systematisch verändern. Ein Steuergeräte-Sollwert oder eine intern geschätzte dq-Spannung ist **nicht automatisch** die tatsächliche Grundschwingung an den Maschinenklemmen. PWM-Totzeiten, Halbleiterabfälle, Abtast-/Mittelungsstrategien und Zeitbezug sind separat zu untersuchen; die Fehlerrichtung ist **nicht allgemein vorgegeben**.

Für den Winkeloffset wurde hier **noch keine vollständige Identifizierbarkeits- oder Fehlerformel hergeleitet**. Er bleibt eine konkurrierende Hypothese und darf nicht allein aus einer beobachteten Neigung behauptet werden. Ebenso ist ein temperaturabhängiger \(R_s\) nicht mit dem in den Messdaten hinterlegten, zur Rekonstruktion verwendeten Wert identisch.

## 7. Energie, Wellenmoment, Verluste und Stromrichtung

### 7.1 Ideale elektrische Leistungsbilanz

Multiplizieren wir die stationären Gleichungen aus Abschnitt 3 mit \(i_d\) bzw. \(i_q\) und addieren, erhalten wir

\[
u_di_d+u_qi_q
=R_s(i_d^2+i_q^2)+\omega_e(\psi_di_q-\psi_qi_d).
\]

Für die amplitudeninvariante dreiphasige Konvention folgt

\[
P_{\rm el}=\frac32(u_di_d+u_qi_q),\qquad
P_{\rm Cu}=\frac32R_s(i_d^2+i_q^2),
\]

und innerhalb des **idealen Modells ohne separat angesetzte Eisenverluste**:

\[
\boxed{P_{\rm el}=P_{\rm Cu}+\omega_mM_{\rm em}.}
\]

Ersetzen wir die Flüsse in \(M_{\rm em}\) durch die **aus denselben elektrischen Größen rekonstruierten** Flüsse, entsteht nur die umgestellte Leistungsbilanz:

\[
M_{\rm em,rec}
=\frac{3}{2\omega_m}\left[
u_di_d+u_qi_q-R_s(i_d^2+i_q^2)
\right].
\]

**Wichtige Identifizierbarkeitsgrenze:** Das elektrisch rekonstruierte „Drehmoment aus Fluss“ ist **keine zusätzliche unabhängige Beobachtung**. Erst ein ausreichend unabhängiger Moment-/Leistungskanal fügt eine neue Information hinzu.

### 7.2 Verluste in einer anderen Bilanzgrenze

Für stationäre positive Drehzahl betrachteten wir ergänzend **näherungsweise**

\[
P_{\rm el}\approx
\frac32R_sI^2+P_{\rm Fe}+P_{\rm mech}
+\omega_mM_{\rm Welle}.
\]

Diese Bilanz enthält explizite Verlustterme und darf nicht unkommentiert mit der vorangegangenen idealen Bilanz identifiziert werden. Insbesondere muss geklärt sein, ob ein rekonstruiertes Flussfeld Magnetisierungsfluss oder effektiven Klemmenfluss repräsentiert. Das im Datensatz vorhandene CAN-Moment ist **ohne Nachweis der Quelle/Kalibrierung** nicht automatisch ein unabhängig gemessenes Wellenmoment.

Mit \(Y:=P_{\rm el}-\omega_mM_{\rm Welle}\) gilt in diesem Modell

\[
Y\approx\frac32R_sI^2+P_{\rm Fe}+P_{\rm mech}.
\]

**Zusatzhypothese:** Wären die übrigen Verluste bei fester Drehzahl und Temperatur näherungsweise stromunabhängig, \(P_{\rm Fe}+P_{\rm mech}\approx P_0\), läge \(Y\) über \(I^2\) auf einer Geraden mit Steigung \(\frac32R_s\) und Achsenabschnitt \(P_0\). Das ist **kein allgemeines Verlustgesetz**: Auch Eisenverluste können mit \(I^2\) korrelieren und dadurch die scheinbare Steigung verändern. Der Achsenabschnitt wäre eine Extrapolation, nicht zwingend ein direkt gemessener Nullstrom-Verlust.

### 7.3 Stromrichtung ist nicht Strombetrag

Das lineare PSM-Modell liefert

\[
\|\boldsymbol\psi\|^2
=(\psi_{\rm PM}+L_di_d)^2+(L_qi_q)^2.
\]

Negativer d-Strom kann dem PM-Fluss entgegenwirken. Somit bedeutet größerer Strombetrag **nicht automatisch** größere magnetische Flussverkettung oder höhere Eisenverluste. Eine Reduktion auf \(i_d^2,i_q^2\) verwirft die Vorzeicheninformation. Zur Diagnose daher zuerst die **Flächen über \((i_d,i_q)\)** betrachten.

Für gespiegelte Betriebspunkte \((i_d,+i_q)\) und \((i_d,-i_q)\) ist im linearen spiegelsymmetrischen Modell der Flussbetrag gleich und das ideale elektromagnetische Moment vorzeicheninvertiert. **Unter der zusätzlichen** Annahme eines gleichen Verlustmoments \(M_V\) bei gleicher positiver Drehzahl gilt

\[
M_{\rm mess,+}=M_{\rm em}-M_V,\qquad
M_{\rm mess,-}=-M_{\rm em}-M_V,
\]

und damit

\[
M_V=-\frac{M_{\rm mess,+}+M_{\rm mess,-}}{2},\qquad
M_{\rm em}=\frac{M_{\rm mess,+}-M_{\rm mess,-}}{2}.
\]

Eine solche Paarbildung ist eine **modellabhängige diagnostische Idee**, keine garantierte Eisenverlusttrennung: Symmetrie des realen Verlustmoments, identische magnetische Zustände und wirklich unabhängige Messsignale sind erst nachzuweisen.

Zwei Betriebspunkte mit **gleichem** \(I^2\) besitzen im Widerstandsmodell gleiche Kupferverluste, können aber sehr unterschiedliche magnetische Zustände aufweisen. Eine Differenz von \(Y\) bei solchen Punkten zeigt zunächst nur übrige Verluste bzw. verletzte Annahmen/Messfehler. Ein Vergleich bei **verschiedenen** \(I^2\), aber gleichen übrigen Verlusten würde dagegen im vereinfachten Modell \(R_s\) zugänglich machen – die Gleichheit dieser übrigen Verluste ist gerade die schwierig zu begründende Voraussetzung.

### 7.4 Flussbetrag-Niveaulinien und ein Zirkelschluss

Die vereinfachte Hypothese \(P_{\rm Fe}\approx F(\omega_e,\|\boldsymbol\psi\|)\) ist **kein allgemeines Eisenverlustmodell**. Lokal verteilte Flussdichten, Oberwellen, Sättigung und Hysterese werden dadurch nicht zuverlässig erfasst.

Für das lineare Flussmodell liefert \(\|\boldsymbol\psi\|=\psi_{\rm ref}\) die Ellipse

\[
(\psi_{\rm PM}+L_di_d)^2+L_q^2i_q^2=\psi_{\rm ref}^2
\]

mit Mittelpunkt \((-{\psi_{\rm PM}}/{L_d},0)\) und Halbachsen
\(\psi_{\rm ref}/|L_d|\), \(\psi_{\rm ref}/|L_q|\), soweit \(L_d,L_q\neq0\).
Auf ihr können **unterschiedliche Strombeträge** liegen; ihre physikalische Befahrbarkeit ist zusätzlich zu prüfen.

**Zirkelschluss:** Um Punkte vermeintlich gleichen Flussbetrags auszuwählen, benötigen wir bereits einen Fluss, den wir unter Umständen gerade mit dem **gesuchten** \(R_s\) aus Spannungen rekonstruieren. Ohne unabhängige Information erzeugt dieses Auswahlverfahren keine eindeutige Widerstands-/Eisenverlustidentifikation.

## 8. Weitere Information aus echten Mehrdrehzahlmessungen

Zwei stationäre Messungen **derselben Maschine** bei gleichem \((i_d,i_q)\) und ausreichend gleichem Temperatur-/Magnetisierungszustand, aber verschiedenen \(\omega_{e,1}\neq\omega_{e,2}\), liefern im idealen dq-Modell

\[
u_{q,j}=R_si_q+\omega_{e,j}\psi_d,\qquad
u_{d,j}=R_si_d-\omega_{e,j}\psi_q,\qquad j=1,2.
\]

**Nur unter der zusätzlichen Annahme**, dass \(R_s\) und der betreffende magnetische Fluss über beide Drehzahlzustände gleich bleiben, liefert die Differenzbildung

\[
\boxed{
\psi_d=\frac{u_{q,2}-u_{q,1}}{\omega_{e,2}-\omega_{e,1}},
\qquad
\psi_q=-\frac{u_{d,2}-u_{d,1}}{\omega_{e,2}-\omega_{e,1}}.
}
\]

Mit mehreren Geschwindigkeiten können die jeweiligen Spannungen näherungsweise als Gerade über \(\omega_e\) untersucht werden. In diesem Modell liefern die Steigungen \(\psi_d\) bzw. \(-\psi_q\), die Achsenabschnitte \(R_si_q\) bzw. \(R_si_d\). Bei \(i_q=0\) enthält der q-Achsenabschnitt keine Information über \(R_s\); analog ist der d-Achsenabschnitt bei \(i_d=0\) dafür unbrauchbar.

Diese Herleitung setzt **zusätzliche echte Messzustände** voraus. Eine Datei, in der lediglich Drehzahl- oder Winkelkanäle geändert wurden, gilt nicht als unabhängiges Drehzahlexperiment. Drehzahlabhängige Eisenverluste, Spannungsrekonstruktionsfehler und thermische Änderungen können die angenommenen linearen Steigungen verfälschen.

**Status:** Theoretisch hergeleitet, im aktuellen PSM-Experiment nicht unabhängig nachgewiesen.

## 9. Vereinfachtes Eisenverlustmodell: integrable Magnetisierung, nichtintegrables rekonstruiertes Feld

### 9.1 Warum eine Verlustleistung allein nicht reicht

Eine skalare Eisenverlustleistung bestimmt noch keinen **zweidimensionalen** Verluststrom und auch keinen eindeutigen Fehler \((\delta\psi_d,\delta\psi_q)\). Selbst ein etabliertes spezifisches Verlustmodell auf Basis lokaler Flussdichte \(B(\mathbf x,t)\) liefert ohne zusätzliche Feld-/Ersatzmodellannahmen nicht unmittelbar zwei dq-Flusskorrekturen. Ein detailliertes Eisenverlustmodell wird hier **noch nicht** behauptet.

### 9.2 Bewusst einfaches dq-Ersatzschaltbild

Für eine synthetische Untersuchung wurde angenommen, dass der gemessene Statorstrom aus Magnetisierungs- und Eisenverluststrom besteht:

\[
\boldsymbol i_s=\boldsymbol i_m+\boldsymbol i_{\rm Fe},\qquad
\boldsymbol i_{\rm Fe}=\frac{\boldsymbol e}{R_{\rm Fe}},\qquad
\boldsymbol e=\omega_e
\begin{bmatrix}-\psi_q\\\psi_d\end{bmatrix},
\]

mit **konstantem isotropem** \(R_{\rm Fe}>0\) und linearem magnetischem Flussfeld

\[
\psi_d=\psi_{\rm PM}+L_di_{d,m},\qquad \psi_q=L_qi_{q,m}.
\]

Der magnetische Fluss ist bezüglich der **Magnetisierungsströme** konservativ. Die Transformation zu Statorströmen folgt aus Einsetzen der Spannungen:

\[
\begin{aligned}
i_{d,s}&=i_{d,m}-\frac{\omega_eL_q}{R_{\rm Fe}}i_{q,m},\\
i_{q,s}&=i_{q,m}+\frac{\omega_e}{R_{\rm Fe}}
(\psi_{\rm PM}+L_di_{d,m}).
\end{aligned}
\]

Definieren wir

\[
a=\frac{\omega_eL_q}{R_{\rm Fe}},\qquad
b=\frac{\omega_eL_d}{R_{\rm Fe}},\qquad
c=\frac{\omega_e\psi_{\rm PM}}{R_{\rm Fe}},
\]

so ist diese Abbildung affin:

\[
\boxed{
\boldsymbol i_s=
\underbrace{\begin{bmatrix}1&-a\\b&1\end{bmatrix}}_{\mathbf A}
\boldsymbol i_m+\begin{bmatrix}0\\c\end{bmatrix}.
}
\]

Mit \(\det\mathbf A=1+ab\) und

\[
\mathbf A^{-1}=\frac{1}{1+ab}
\begin{bmatrix}1&a\\-b&1\end{bmatrix}
\]

ergibt die Kettenregel

\[
\mathbf J_{\psi,s}
=\underbrace{\begin{bmatrix}L_d&0\\0&L_q\end{bmatrix}}_{\mathbf J_{\psi,m}}
\mathbf A^{-1}
=
\frac{1}{1+ab}
\begin{bmatrix}L_d&aL_d\\-bL_q&L_q\end{bmatrix}.
\]

Die beiden Kreuzableitungen sind für \(\omega_e>0\), \(L_d,L_q,R_{\rm Fe}>0\) **betragsgleich und vorzeichenverschieden**, denn \(aL_d=bL_q\). Somit

\[
\boxed{
r_{\rm int}
=\frac{aL_d+bL_q}{1+ab}
=\frac{2\omega_eL_dL_qR_{\rm Fe}}
{R_{\rm Fe}^2+\omega_e^2L_dL_q}.
}
\]

**Geometrische Einsicht:** Ein magnetisches Coenergy-Modell kann bezüglich des Magnetisierungsstroms integrabel sein und in einem Ersatzmodell, das die Gesamtstatorströme als Koordinaten verwendet, dennoch ein **nichtintegrables Flussfeld** hervorbringen. Das ist eine **konkrete mögliche** Erklärung einer Integrabilitätsverletzung, **kein Beweis**, dass ein reales Residuum ausschließlich von Eisenverlusten stammt.

### 9.3 Frequenz- und Leistungssymmetrie

Für konstante Modellparameter und unveränderten Magnetisierungszustand ist

\[
r_{\rm int}(-\omega_e)=-r_{\rm int}(\omega_e),
\]

aber

\[
P_{\rm Fe}
=\frac32\frac{\omega_e^2}{R_{\rm Fe}}
(\psi_d^2+\psi_q^2),
\qquad
P_{\rm Fe}(-\omega_e)=P_{\rm Fe}(\omega_e).
\]

Die modellierte Verlust**leistung** ist also gerade, das Residuum ist ungerade in der elektrischen Drehzahl. Mittelung der Residuen bei \(+\omega_e\) und \(-\omega_e\) würde den hier modellierten ungeraden Anteil auslöschen – **nicht** die real dissipierte Leistung. Tatsächliche negative Drehzahlen wurden im aktuellen experimentellen Vergleich **nicht** aufgezeichnet; für die Ableitungsdiagnose bei positiver Drehzahl werden sie auch nicht vorausgesetzt.

Der theoretische Betrag von \(r_{\rm int}\) steigt im Modell bei kleinen \(|\omega_e|\) zunächst an, besitzt bei \(|\omega_e|=R_{\rm Fe}/\sqrt{L_dL_q}\) ein Maximum und sinkt danach wieder. Dieser Verlauf darf nicht als allgemeine Eisenverlustkurve einer realen Maschine interpretiert werden.

### 9.4 Numerische Kontrolle des synthetischen Modells

Im eigenständigen Python-Experiment `flux_loss_experiment.py` wurden verwendet:

| Modellgröße | Wert |
| --- | ---: |
| \(\psi_{\rm PM}\) | 0,08 Vs |
| \(L_d\), \(L_q\) | 0,0005 H und 0,0008 H |
| \(f_e\), \(\omega_e\) | 100 Hz und \(2\pi\cdot100\) rad/s |
| \(R_{\rm Fe}\) | 10 Ω |

Die numerische Gradientenauswertung der analytischen linearen Coenergy ergab maximal etwa \(10^{-15}\,\mathrm{Vs}\) Abweichung der Flusskomponenten im strukturierten Testgitter. Das analytische Residuum beträgt etwa

\[
r_{\rm int}\approx5{,}02\cdot10^{-5}\,\mathrm H.
\]

Diese Größen prüfen die **eigene algebraische/numerische Umsetzung dieses gewählten Modells**, nicht die physikalische Richtigkeit des konstanten Eisenverlustwiderstands.

## 10. Reale Untersuchung: Datenbasis, Rekonstruktion und Geometrie

### 10.1 Vorhandene Datensätze und wiederverwendete Software

Arbeitsbranch: [`topic/fluxcorrection`](https://github.com/rkeller98/Research/tree/topic/fluxcorrection). Getrennte Experimente: [synthetisches Modell](https://github.com/rkeller98/Research/blob/topic/fluxcorrection/sandbox/fluxcorrection/flux_loss_experiment.py) und [Analyse realer Daten](https://github.com/rkeller98/Research/blob/topic/fluxcorrection/sandbox/fluxcorrection/real_flux_analysis.py). Der aktuell im Gespräch weiterentwickelte lokale Python-Stand kann dem letzten gepushten Skript voraus sein; genaue Reproduktionsstände sind vor Veröffentlichung als Commit und Umgebung einzufrieren.

Die vorhandenen Import- und Aufbereitungsfunktionen werden **wiederverwendet**, statt erneute unabhängige Parser zu bauen:

- [RawDataImporter](https://github.com/rkeller98/Research/blob/topic/fluxcorrection/shared/python/raw_ww_data_importer.py) liest einzelne Signale aus MATLAB-v7.3-Rohmessungen.
- [`operating_points()`](https://github.com/rkeller98/Research/blob/topic/fluxcorrection/scripts/extract_research_datasets.py) gruppiert anhand der Messkontexte, berechnet Mittelwerte und ausgewählte Streuungsgrößen.
- [`load_dataset()`](https://github.com/rkeller98/Research/blob/topic/fluxcorrection/shared/python/canonical_dataset.py) liest den bereits exportierten, checksumgeprüften CSV-/JSON-Verbund.

Der in der Lernübung ausgewählte Datensatz `psm_temperature_2500` stammt aus `Flux/PSM_Measdata.mat`; seine Spalten, Konventionen, Quellen und Einschränkungen sind im [Datensatz-Manifest](https://github.com/rkeller98/Research/blob/topic/fluxcorrection/datasets/psm_temperature_2500.json) dokumentiert.

| Merkmal | Stand der Datenerhebung/-aufbereitung |
| --- | --- |
| Maschinentyp | dreiphasige PSM, \(p=3\) |
| Drehzahlreferenz | 2500 min⁻¹ |
| Temperaturreferenzen | 30 °C und 70 °C |
| Aggregierte Betriebspunkte | insgesamt 680, davon 340 bei 70 °C Referenz |
| Loggerwerte der 70-°C-Gruppe | 1020 Einträge, je 3 je Betriebspunkt |
| Flussquelle | aus gruppierten \(u_d,u_q,i_d,i_q,R_s,\omega_e\) rekonstruierte Werte |
| Messfeldform im Stromraum | ungefähr eine Halbscheibe in der linken dq-Stromebene |

Der Betriebspunktindex allein darf **nicht** ungeprüft über verschiedene Drehzahl-/Temperatur-/Erregungszustände hinweg zum Gruppieren genutzt werden. Die drei Loggerwerte sind keine garantierten unabhängigen Sensorreplikate. Eine **Temperaturreferenz** ist keine kalibrierte Ist-Temperatur.

### 10.2 Erste Beobachtung

Für die 70-°C-Referenzpunkte wurden separat

\[
\psi_{d,\rm rec}=\frac{u_q-R_si_q}{\omega_e},\qquad
\psi_{q,\rm rec}=\frac{R_si_d-u_d}{\omega_e}
\]

berechnet und ohne vorausgehende Flächenglättung als farbkodierte Punkte über der \((i_d,i_q)\)-Ebene betrachtet. **Beobachtet:** \(\psi_d\) verändert sich hauptsächlich entlang \(i_d\), \(\psi_q\) hauptsächlich entlang \(i_q\); Kreuzabhängigkeiten sind erkennbar. Dieser Befund ist **noch keine eindeutige physikalische Kreuzsättigungsdiagnose**, da das Feld rekonstruiert ist.

Das nicht rechteckige Punktgebiet ist entscheidend: `np.gradient(psi_d)` auf einer einfachen 1D-Liste von Messpunkten würde Nachbarn **in der Array-Reihenfolge**, nicht in physikalischer d- oder q-Richtung vergleichen. Ein strukturiertes Gitter aus `np.meshgrid` hatte im synthetischen Experiment diese Ausrichtung; die realen Punkte besitzen sie nicht.

## 11. Kontinuierliche Approximation der gemessenen Flussfelder

### 11.1 Warum vor der Diagnose approximiert wird

Um partielle Ableitungen zu gewinnen, wurde zunächst eine **glättende** Approximation statt exakter Punktinterpolation gewählt. Triangulation mit stückweise linearen Flächen liefert pro Dreieck konstante Ableitungen und Sprünge an Dreiecksgrenzen; ungünstige Dreiecksformen und Rauschen können die Ableitungen verzerren. Lokale Least-Squares-Ebenen liefern Mittelsteigungen, lösen das einseitige **Informationsdefizit am Rand** aber ebenfalls nicht. Eine globale glatte RBF ist deshalb ein praktikabler erster Versuch – **keine Garantie genauer Ableitungen am Rand**.

Die zwei Funktionen werden **voneinander unabhängig** angenähert:

\[
\hat\psi_d=f_d(i_d,i_q),\qquad
\hat\psi_q=f_q(i_d,i_q).
\]

Ein direkter Fit einer einzigen Potentialfunktion \(W'\) mit \(\hat{\boldsymbol\psi}=\nabla_iW'\) würde die Reziprozität bereits **per Konstruktion erzwingen** und damit die derzeit gesuchte Abweichung möglicherweise aus dem Untersuchungsobjekt entfernen. Eine konservative Projektion ist ein **späteres**, getrennt zu bewertendes Modell; ihr Residuum muss erhalten bleiben.

Für die Analyse der ersten Flussableitungen genügt \(C^1\)-Glattheit, \(C^2\) ist für weitergehende Ableitungsuntersuchungen zweckmäßig. Allein eine \(C^2\)-Fläche kann jedoch sehr schlechte Ableitungen besitzen. **Ein kleiner Flussfehler ist kein kleiner Gradientenfehler.**

### 11.2 Normierung: mathematisch sinnvoll, physikalisch rücktransformieren

Die SciPy-RBF benötigt die Eingabe in der Form

\[
X_{\rm train}=
\begin{bmatrix}i_{d,1}&i_{q,1}\\ \vdots&\vdots\\i_{d,N}&i_{q,N}\end{bmatrix}
\in\mathbb R^{N\times2}.
\]

Die beiden zunächst eindimensionalen Stromarrays werden mit `np.column_stack` als **gepaarte Zeilen** angeordnet. `np.meshgrid` ist erst für das spätere regelmäßige Auswertegitter erforderlich.

Bei nichtnormierten Strömen in Ampere hängt die räumliche Wirkung des RBF-Formparameters von der Größenordnung der Stromkoordinaten ab. Deshalb verwenden wir einen **gemeinsamen** nur aus Trainingsdaten bestimmten Referenzstrom:

\[
\boxed{
I_{\rm ref}=\max_{k\in{\rm Train}}\sqrt{i_{d,k}^2+i_{q,k}^2},
\quad
\tilde i_d=i_d/I_{\rm ref},
\quad
\tilde i_q=i_q/I_{\rm ref}.
}
\]

Die isotrope Normierung erhält die relativen Abstände und Winkel im dq-Stromraum. Training, Test und späteres Gitter werden **mit demselben** \(I_{\rm ref}\) transformiert. Eine getrennte Skala für Testpunkte wäre methodisch inkonsistent. Die **Flusszielwerte** wurden im aktuellen Experiment nicht normiert.

Das spätere Ableiten nach **physikalischen** Ampere verlangt die Kettenregel, z. B.

\[
\boxed{
\frac{\partial\hat\psi_d}{\partial i_q}
=\frac1{I_{\rm ref}}\frac{\partial\hat\psi_d}{\partial\tilde i_q},
\qquad
\frac{\partial\hat\psi_q}{\partial i_d}
=\frac1{I_{\rm ref}}\frac{\partial\hat\psi_q}{\partial\tilde i_d}.
}
\]

Bei zweifacher Ableitung kommt bei gleicher Skalierung \(1/I_{\rm ref}^2\) hinzu. Erst so stimmen Betrag und Einheit der differentiellen Induktivitäten.

### 11.3 Verwendete RBF als **vorläufiges Werkzeug**

In `scipy.interpolate.RBFInterpolator` wurde der inverse-multiquadric-Kernel verwendet:

\[
\phi(r)=\frac{1}{\sqrt{1+(\varepsilon r)^2}},\qquad
r=\|\tilde{\boldsymbol i}-\tilde{\boldsymbol i}_k\|_2.
\]

Für normierte Ströme sind \(r\) und \(\varepsilon\) dimensionslos. Ohne diese Normierung hätte \(\varepsilon\) die Einheit \(\mathrm A^{-1}\). Das erste Experiment mit \(\varepsilon=1\,\mathrm A^{-1}\) und sehr großen relativen Stromabständen ergab im Plot einen schlechten Fit. Nach Umstellung auf normierte Koordinaten wurden im aktuellen, noch nicht systematisch optimierten Versuch verwendet:

\[
\boxed{
\mathrm{kernel}=\texttt{inverse\_multiquadric},\quad
\varepsilon=1,\quad \mathrm{smoothing}=0.01,\quad
\mathrm{neighbors}=\texttt{None}.
}
\]

Der Formparameter \(\varepsilon\) legt die räumliche Skala der radialen Basisfunktionen fest; `smoothing` reguliert die Datenanpassung. Die verwendete Klasse kann zudem einen polynomialen Anteil besitzen; da `degree` **nicht ausdrücklich gesetzt wurde**, ist dessen effektiver Wert anhand der eingesetzten SciPy-Version und der Bibliotheksdokumentation zu verifizieren. Für den gewählten Kernel ist in der konsultierten SciPy-Dokumentation der Standardwert **Grad 0** angegeben [S1]. Einen linearen Term mit Grad 1 haben wir bisher **nicht** eigens getestet.

Die Bibliotheksimplementierung und die Basisfunktion werden **bewusst vorläufig benutzt**. Ihre Herleitung und die Bedeutung von Kernelmatrix, Koeffizienten, Regularisierung und Kondition sind **offene Lernaufgaben**, keine bereits persönlich nachvollzogenen Resultate (siehe OI-MATH-002). Die tatsächlich konsultierte API-Dokumentation und ihr Quellenstatus sind unter [S1] festgehalten.

## 12. Train-/Testauswertung: Resultate und Grenzen

### 12.1 Aufteilung und Bewertung

Die 340 gruppierten 70-°C-Betriebspunkte wurden anhand **gemeinsamer Indizes** zufällig aufgeteilt:

\[
N_{\rm train}=272\;(80\,\%),\qquad
N_{\rm test}=68\;(20\,\%).
\]

Die protokollierte Auswertung verwendete `np.random.default_rng(42)`. Zwischenzeitlich wurde der feste Seed versuchsweise weggelassen; ein fixer Seed gewährleistet **Wiederholbarkeit**, nicht automatisch einen besseren Split. Alle Strom- und Flussarrays desselben Betriebspunkts müssen identisch partitioniert werden. \(I_{\rm ref}\) stammt ausschließlich aus den Trainingspunkten.

Für Residuen \(e_k=\hat\psi_k-\psi_k\) gilt

\[
\mathrm{RMSE}
=\sqrt{\frac1N\sum_{k=1}^N e_k^2}
=\sqrt{\operatorname{Var}(e)+\bar e^{\,2}}.
\]

Die Standardabweichung \(\sqrt{\operatorname{Var}(e)}\) entfernt den mittleren Fehler; sie ist **nicht allgemein** identisch mit RMSE. Ein konstanter Bias kann deshalb bei `np.std(e)` unsichtbar bleiben.

Zusätzlich wurde der Bereich des **jeweiligen Trainingsflusses** als Normierung verwendet:

\[
\boxed{
\mathrm{NRMSE}_{\rm range}[\%]
=100\frac{\mathrm{RMSE}}
{\max(\psi_{\rm train})-\min(\psi_{\rm train})}.
}
\]

Derselbe aus Training berechnete Nenner gilt für dessen Testauswertung. Diese Prozentzahlen beziehen sich **auf den Spannweiten-NRMSE**, nicht auf die relative Abweichung an einem beliebigen Einzelpunkt oder auf eine physikalische Referenzinduktivität.

### 12.2 Beobachtete Zahlen (explorativer Versuch, Seed 42)

Konfiguration: 70 °C Temperatur**referenz**, RBF `inverse_multiquadric`, \(\varepsilon=1\), \(\mathrm{smoothing}=0.01\), normierte Stromkoordinaten.

| Fluss und Teilmenge | RMSE [Vs] | RMSE [mVs] | NRMSE (Train-Range) |
| --- | ---: | ---: | ---: |
| \(\psi_d\), Training | 0,0004757326 | 0,4757 | 0,8427 % |
| \(\psi_d\), Test | 0,0005744879 | 0,5745 | 1,0176 % |
| \(\psi_q\), Training | 0,0006027503 | 0,6028 | 0,2883 % |
| \(\psi_q\), Test | 0,0005974741 | 0,5975 | 0,2858 % |

**Beobachtung:** In dieser zufälligen Aufteilung sind Trainings- und Testfehler ähnlicher Größenordnung. Das zeigt **keinen offensichtlichen starken Unterschied** zwischen ihnen. Der dokumentierte d-Test-NRMSE liegt ausdrücklich **leicht über 1 %**, auch wenn andere informelle Aufteilungen oft darunter lagen. Der q-Fluss hat trotz eines teils größeren absoluten Fehlers einen kleineren NRMSE, weil seine beobachtete Spannweite größer ist.

**Einschränkungen:**
- Ein guter Test-RMSE am **selben Messfeld** prüft vor allem Interpolation nahe vorhandener Punkte, nicht neue Drehzahlen, Temperaturen, Maschinen oder Extrapolation.
- Wiederholte visuelle Anpassungen und die Betrachtung von Testkennzahlen haben den ursprünglichen Test-Holdout **explorativ mitgenutzt**. Für einen finalen wissenschaftlichen Generalisierungsnachweis wäre ein neuer, vorab eingefrorener und unabhängig ausgewerteter Testansatz notwendig.
- Eine systematische Hyperparameter-/Kernel-Kreuzvalidierung **innerhalb der Entwicklungsdaten** wurde noch nicht durchgeführt.
- Die Messstreuung der Loggerwerte ist keine vollständige Unsicherheit von \(\psi_{\rm rec}\). Unsicherheiten von \(u\), \(i\), \(R_s\) und \(\omega_e\) sowie deren Korrelationen müssen gesondert betrachtet werden.
- **Niedriger Fluss-(N)RMSE erlaubt noch keinerlei quantitativen Schluss über \(L_{dq}\), \(L_{qd}\) oder \(r_{\rm int}\).**

Ein LHS-informierter diskreter Holdout aus **tatsächlich gemessenen** Betriebspunkten ist als optionales Konzept für MeasEval in [Weg-Weiser/GUI_VICE-MeasurementEvalKit#293](https://github.com/Weg-Weiser/GUI_VICE-MeasurementEvalKit/issues/293) dokumentiert. Er ist **keine Voraussetzung** für die aktuelle Lernübung.

## 13. Nächste mathematische Diagnose und Entscheidungsregeln

### 13.1 Vom kontinuierlichen RBF-Modell zum Gitter

Die nächste selbst zu implementierende Übung besteht darin, Stromachsen mit `np.linspace` zu definieren und per `np.meshgrid` ein reguläres zweidimensionales Auswertegitter zu erzeugen. Die Gitterarrays mit `ravel()` oder `reshape(-1)` zu Punktspalten \((i_d,i_q)\) zusammenführen, **durch den bestehenden Trainingswert** \(I_{\rm ref}\) normieren und die zwei vorhandenen RBF-Funktionen getrennt auswerten. Anschließend die Flusswerte zur Gitterform zurückordnen.

**Geometrische Grenze:** Das umschließende Rechteck enthält viele Orte außerhalb der halbkreisförmigen Messpunktwolke. Wir müssen das tatsächlich unterstützte Gebiet und die Randnähe gesondert kennzeichnen bzw. maskieren. Die Tatsache, dass ein globaler Approximator dort Funktionswerte liefert, **erzeugt keine fehlenden Messinformationen**.

### 13.2 Differentialrechnung vor einer möglichen Korrektur

Aus den zwei unabhängigen Flussfunktionen zunächst

\[
\mathbf J_{\hat\psi}(i_d,i_q)
=\begin{bmatrix}
\partial_{i_d}\hat\psi_d & \partial_{i_q}\hat\psi_d\\
\partial_{i_d}\hat\psi_q & \partial_{i_q}\hat\psi_q
\end{bmatrix}
\]

und

\[
r_{\rm int}(i_d,i_q)=
\partial_{i_q}\hat\psi_d-\partial_{i_d}\hat\psi_q
\]

bestimmen. Die analytische Ableitung einer RBF und endliche Differenzen auf dem Gitter sind zu unterscheiden. Numerische Ableitungen müssen die Gitterabstände und bei normierten Koordinaten die **Kettenregel** beachten. Die Plausibilität der Ableitungen ist zunächst an einem **bekannten synthetischen Feld** unabhängig zu prüfen. Später die Robustheit gegenüber Kernelwahl, Glättung, Punktabdeckung, Ableitungsverfahren und Randnähe untersuchen.

Erst nach dieser Diagnose kommen Wegintegrale, ein mögliches konservatives Potential, ein konservativ/nichtkonservativ zerlegtes Modell oder eine physikalisch motivierte Korrektur in Betracht. Dabei ist

\[
\boldsymbol\psi_{\rm rec}
=\nabla_iW' +\boldsymbol r
\]

**zunächst lediglich eine mögliche mathematische Modellzerlegung**; \(\boldsymbol r\) ist nicht per Definition „der Eisenverlust“. Eine Korrektur darf den Messbefund nicht stillschweigend ersetzen.

### 13.3 Kriterien für belastbare Schlussfolgerungen

Eine im realen Flussfeld beobachtete Asymmetrie oder Integrabilitätsverletzung wird erst dann physikalisch aussagekräftiger, wenn sie **gegenüber numerischen Wahlmöglichkeiten robust**, im gemessenen Strombereich unterstützt und gegenüber der verfügbaren Unsicherheitsabschätzung erkennbar ist. Für eine eindeutige Ursachenzuordnung wären weitere, unterscheidungskräftige Informationen nötig: z. B. thermisch/elektrisch qualifizierte Widerstandswerte, unabhängige Klemmenspannungen oder Drehmomente, reproduzierbare Vergleiche echter Drehzahlzustände oder andere physikalisch begründete Beobachtungen.

**Derzeitiger Stand:** Es liegt **keine** belastbare reale Integrabilitätskarte, keine quantifizierte Ableitungsunsicherheit und **kein** eindeutig identifiziertes physikalisches Flusskorrekturmodell vor.

## 14. Historischer Forschungsweg und bewahrenswerte negative Ergebnisse

Die Chronologie soll den heutigen Forschungsinhalt **erklären**, nicht seine Reihenfolge bestimmen:

| Etappe | Ursprüngliche Frage / Versuch | Bleibende Erkenntnis |
| --- | --- | --- |
| Drehmoment als Flusskorrektur | Lassen sich zwei Flussfehler aus einem Drehmomentunterschied bestimmen? | Nur eine Projektion sichtbar; radiale Nullraumrichtung nicht beobachtbar (Abschnitt 5). |
| Drehmoment **plus** Coenergy | Kann Integrabilität die Mehrdeutigkeit beseitigen? | Nein. \(f(I^2)\boldsymbol i\) bleibt torque-neutral und integrabel. |
| Widerstandsdiagnose | Erklärt \(R_s\) die auffällige Neigung? | Ein Widerstandsmismatch besitzt eine klare geometrische Signatur, ist aber nur eine mögliche Ursache (Abschnitt 6). |
| Stromsymmetrie und Verlustbetrachtung | Lässt sich Kupfer-, Eisen- und mechanischer Verlustanteil allein durch Spiegelung oder Strombetrag trennen? | Nur unter starken, expliziten Gleichheitsannahmen; weitere Informationsquellen erforderlich (Abschnitt 7). |
| Mehrdrehzahlansatz | Eliminieren Drehzahldifferenzen \(R_s\)? | Ja, **im idealen Modell** bei konstantem Fluss-/Temperaturzustand und echten verschiedenen Messungen (Abschnitt 8). |
| Coenergy und Eisenverlustzweig | Wie kann ein magnetisch konservatives Feld nichtkonservativ erscheinen? | Im gewählten Verlustzweig durch die Stator-/Magnetisierungsstrom-Abbildung; das ist **nicht** der allgemeine Nachweis einer realen Ursache (Abschnitt 9). |
| Reale PSM + RBF | Können wir geeignete glatte Felder aus unregelmäßigen Messdaten erhalten? | Vorläufig niedrige wertbezogene Fehler, Ableitungen und Randzuverlässigkeit **noch offen** (Abschnitte 10–13). |

Die ausführliche erste, stärker chronologische Fassung ist über die [Git-Vorgängerversion vom 10.10.2026](https://github.com/rkeller98/Research/blob/29068b91a801e1be09e91fbbe877840a16d2c5d4/sandbox/fluxcorrection/flusskorrektur_doku.md) nachvollziehbar. Diese Verlinkung dient dem **historischen Nachlesen**, nicht als Ersatz für die heute hier vollständig dokumentierten Kernaussagen.

**Bewusste Korrektur früherer Missverständnisse:** „Ideale Maschine“ ist nicht dasselbe wie „linear-entkoppelter Fluss“; eine konservative Coenergy kann Kreuzsättigung modellieren. Konstante Offsets können Integrabilität bestehen, obwohl sie das Drehmoment verändern. Eine glatte globale Fitfläche kann am Rand auswertbar sein, ohne dort durch Messungen gedeckt zu sein. Ein gemessener CAN-Wert ist nicht automatisch eine unabhängige Wellenmomentmessung. Und ein kleiner RMSE ist kein Gütenachweis einer partiellen Ableitung.

## 15. Open Issues – nachzuarbeitende Verständnis- und Forschungsfragen

**Pflegeregel:** Die Einträge sind absichtlich **offene Lernaufgaben** nach Writing Guide 0.8. Genutzte, noch nicht selbst verstandene Methoden dürfen im Experiment stehen, werden aber nicht als mathematisch erschlossen dargestellt. Schließen erst nach eigener Herleitung/anschaulicher Erklärung und dokumentierter Gegenprüfung – **nicht allein, weil Python eine Zahl ausgibt**. Quellen und Ergebnisse bei Bearbeitung direkt beim jeweiligen Thema nachtragen.

### OI-MATH-001 – Interpolation versus glättende Approximation

- **Status:** Offen.
- **Einsatz:** Unregelmäßige Flussmesspunkte sollen in kontinuierliche Funktionen überführt werden.
- **Fragen:** Was lösen Interpolation und Regression *jeweils* mathematisch? Wie entstehen Normalgleichungen, Pseudoinverse und überbestimmte Systeme? Wie wirken Rauschen, Modellkomplexität, Regularisierung, Kondition und Randgeometrie?
- **Lernnachweis:** Ein einfaches 1D-Beispiel mit bekannten Daten, gezieltem Rauschen und bekannter Ableitung selbst herleiten und beide Verfahren vergleichen.
- **Quellen:** Noch keine externe Methodenquelle eigenständig vertieft; bei Bearbeitung ergänzen.

### OI-MATH-002 – RBF, Kernelmatrix, Parameter und Polynomanteil

- **Status:** Offen; SciPy wird gegenwärtig **vorläufig als Werkzeug** genutzt.
- **Einsatz:** `RBFInterpolator` auf den normierten dq-Trainingsdaten mit inverse-multiquadric-Kernel, \(\varepsilon=1\), `smoothing=0.01`.
- **Fragen:** Woher kommt die radiale Darstellungsform? Wie entstehen RBF-Koeffizienten und Gleichungssystem samt optionalem Polynom, Nebenbedingungen und Regularisierung? Warum hängen Verhalten und Kondition von \(\varepsilon\), Punktabständen, Skalierung und `smoothing` ab? Was ist der tatsächliche Default von `degree` der installierten Version?
- **Lernnachweis:** Kleine RBF mit wenigen Zentren selbst aufstellen, Koeffizienten ohne Bibliothek herleiten, mit SciPy vergleichen und die Formparameter geometrisch erklären.
- **Quellen:** SciPy-API-Beschreibung [S1] als **bereits konsultierte Funktionsreferenz**; ihre mathematische Erklärung ist **noch nicht** als eigene Herleitung abgeschlossen. Geeignete weitere Literatur erst nach tatsächlicher Lektüre eintragen.

### OI-MATH-003 – Ableitungen, Kettenregel und Randstabilität

- **Status:** Offen.
- **Einsatz:** Geplante \(\mathbf J_{\hat\psi}\) und \(r_{\rm int}\)-Felder.
- **Fragen:** Wie unterscheidet sich die Ableitung einer glatten RBF von `np.gradient()` auf einer ausgewerteten Matrix? Wie werden Strom-Normierung und Gitterabstand rücktransformiert? Wie verstärken Fitfehler, Schrittweiten und unzureichender Daten-Support die Ableitungsfehler?
- **Lernnachweis:** Bekannte synthetische Flussflächen mit analytischen Gradienten vergleichen; Gitterschritte und Glättungen systematisch variieren; Rand- und Innenfehler getrennt betrachten.
- **Quellen:** Noch keine externe Herleitungsquelle eigenständig ausgewertet; nachtragen.

### OI-MATH-004 – Bias, Varianz, Validierung und räumliche Datenaufteilung

- **Status:** Vertiefung offen; Random Split, RMSE und NRMSE wurden umgesetzt.
- **Einsatz:** Bewertung und zukünftige Parameterwahl glatter Flussapproximationen.
- **Fragen:** Was erklärt der Bias-Varianz-Trade-off mathematisch? Warum reicht der Trainingsfehler nicht? Wann entsteht Leakage? Wie verändert sich die Interpretation bei nahen Nachbarpunkten und wiederholten Loggerwerten? Was misst eine Unsicherheit der Fluss**rekonstruktion** im Vergleich zum Fitfehler?
- **Lernnachweis:** An einfachen Beispielen zwei unterschiedlich komplexe Modelle mit getrennten Entwicklungs-/Testpunkten beurteilen; alternative räumliche Validierung und deren Aussagegrenzen herleiten.
- **Quellen:** Noch keine vertiefende externe Quelle eigenständig ausgewertet; nachtragen.

### OI-PHYS-001 – Eisenverluste aus Messgrößen physikalisch identifizieren

- **Status:** Offen; konstantes \(R_{\rm Fe}\)-Modell nur synthetisch geprüft.
- **Fragen:** Welche dq-Modellparameter sind bei verfügbarer \((u,i,\omega,M)\)-Information überhaupt identifizierbar? Unter welchen Voraussetzungen kann ein reales Residuum von Winkel-, Widerstands-, Sensor- und Spannungseffekten unterschieden werden? Welche Rolle spielen tatsächliche lokale Flussdichten und Materialmodelle?
- **Lernnachweis:** Konkurrenzhypothesen mathematisch auf unterscheidbare Signaturen prüfen, unabhängige Vergleichsgrößen und Unsicherheiten benennen, anschließend erst reale Daten quantitativ auswerten.
- **Quellen:** Eigene modellbasierte Herleitung in Abschnitt 9; externe physikalische Fachquellen erst nach tatsächlicher Lektüre ergänzen.

### OI-RESEARCH-001 – Wie überprüft man Reziprozität an realen RBF-Feldern robust?

- **Status:** Offen.
- **Aufgabe:** Unterstütztes Gebiet definieren; beide Kreuzableitungen und ihr Residuum berechnen; Ergebnisse mit synthetischem Kontrollfeld, anderen Glättungen/Basen, Unsicherheiten und Randabstand vergleichen; erst dann mögliche konservative Projektion erwägen.
- **Erfolgskriterium:** Trennung nach numerisch belastbarer Beobachtung, physikalischem Modellbezug und weiterhin unbestimmter Ursache.
- **Quellen:** Bereits hergeleitete Grundlagen in Abschnitten 4, 9 und 13; ergänzende Literatur später nachvollziehbar anführen.

## 16. Quellen, Reproduktionsbasis und Attribution

### 16.1 Tatsächlich konsultierte externe Quelle

**[S1] SciPy Developers:** *scipy.interpolate.RBFInterpolator*, SciPy-API-Referenz, online, https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.RBFInterpolator.html (eingesehen am **10.10.2026**; beim späteren Reproduktionslauf lokale SciPy-Version per `scipy.__version__` dokumentieren). **Hier verwendeter Beitrag:** verfügbare Kernel, inverse-multiquadric-Definition, Parameter `epsilon`, `smoothing`, `neighbors`, `degree`, Defaultverhalten und mathematische **Beschreibung** des RBF-Ansatzes. Die offizielle Dokumentation zu kennen bedeutet **nicht**, dass die Herleitung schon selbst erarbeitet wurde: Lernstatus OI-MATH-002 bleibt offen.

### 16.2 Eigene Quellcodes und Datensatz-Provenienz

- **[P1]** [`datasets/psm_temperature_2500.json`](https://github.com/rkeller98/Research/blob/topic/fluxcorrection/datasets/psm_temperature_2500.json) und dazugehörige CSV: Datensatzidentität, Spalten, Erfassungs- und Aggregationskonventionen, SHA-256 der zugrunde liegenden MAT-Quelle, Einschränkungen, Flussformeln.
- **[P2]** [`datasets/README.md`](https://github.com/rkeller98/Research/blob/topic/fluxcorrection/datasets/README.md): Inventar, Duplikat-/Provenienzprüfung, Grenzen bei CAN und Temperatur, Abgrenzung künstlicher Geschwindigkeitsvarianten.
- **[P3]** [`shared/python/raw_ww_data_importer.py`](https://github.com/rkeller98/Research/blob/topic/fluxcorrection/shared/python/raw_ww_data_importer.py), [`shared/python/canonical_dataset.py`](https://github.com/rkeller98/Research/blob/topic/fluxcorrection/shared/python/canonical_dataset.py) und [`scripts/extract_research_datasets.py`](https://github.com/rkeller98/Research/blob/topic/fluxcorrection/scripts/extract_research_datasets.py): tatsächlich verwendete Import-/Aggregations-/Ladewege.
- **[P4]** [`sandbox/fluxcorrection/flux_loss_experiment.py`](https://github.com/rkeller98/Research/blob/topic/fluxcorrection/sandbox/fluxcorrection/flux_loss_experiment.py) und [`sandbox/fluxcorrection/real_flux_analysis.py`](https://github.com/rkeller98/Research/blob/topic/fluxcorrection/sandbox/fluxcorrection/real_flux_analysis.py): synthetischer und realer Arbeitscode; **vor der Reproduktion** prüfen, ob die weiterentwickelte lokale Sitzung versioniert/pusht ist.
- **[P5]** [MeasEval Issue #293](https://github.com/Weg-Weiser/GUI_VICE-MeasurementEvalKit/issues/293): LHS-informierte Teilmengenauswahl **real vorhandener** Stützpunkte als optionales späteres Produktkonzept.
- **[H1]** [Vorgängerfassung der Forschungsnotiz](https://github.com/rkeller98/Research/blob/29068b91a801e1be09e91fbbe877840a16d2c5d4/sandbox/fluxcorrection/flusskorrektur_doku.md): vollständiger älterer chronologischer Notizstand und Zwischenfragen; **historischer Nachweis**, keine zusätzliche unabhängige Quelle.

**Transparenz:** Die im Projekt vorhandenen Lehrbücher sind mögliche **künftige** Referenzen. Solange kein konkreter Abschnitt daraus für eine Herleitung geprüft wurde, wird ihnen **kein tatsächlich verwendeter Beleg** zugeschrieben. Neue Web-, Buch- oder Paperquellen müssen beim jeweiligen Argument sowie mit prüfbarer Fundstelle hier ergänzt werden (Writing Guide 0.7).

### 16.3 Reproduktionshinweise für den jetzigen Befund

Dokumentierte Eingaben: Daten-ID `psm_temperature_2500`, Filter `rotor_temp_ref ≈ 70 °C`, Training/Test mit 80/20-Indexpermutation Seed 42, \(I_{\rm ref}=\max\sqrt{i_d^2+i_q^2}\) **nur aus Trainingspunkten**, SciPy-RBF-Kernel `inverse_multiquadric`, `epsilon=1`, `smoothing=0.01`, unabhängige d-/q-Zielmodelle. Bewertungsgrößen: RMSE in Vs, NRMSE in Prozent der **Trainingsspanne**. Offene Reproduktionsdetails: exakter Commit des lokal genutzten Skripts, Python-/SciPy-/NumPy-Version und endgültige Cross-Validation-/Testpolitik; vor formaler Publikation ergänzen.

## 17. Arbeitsauftrag für die nächste Sitzung

Wir steigen **nicht** beim historischen Drehmoment-Offset oder einer fertigen Korrekturformel ein, sondern bei den **bereits aufgebauten normierten unabhängigen RBF-Funktionen** für reale \(\psi_d,\psi_q\).

**Nächste selbst zu erarbeitende Programmieraufgabe:** Ein regelmäßiges Stromgitter erzeugen, es als \(N\times2\)-Punktmatrix für die beiden RBFs vorbereiten und auf das tatsächlich unterstützte Stromgebiet beschränken. Danach die Kreuzableitungen bestimmen, ihre Einheiten und numerische Belastbarkeit prüfen und **erst dann** das Integrabilitätsresiduum interpretieren.

**Begleitendes Lernziel:** OI-MATH-002 zur RBF-Grundlage bleibt explizit offen. Das Gitter darf zunächst pragmatisch erstellt werden, ohne dass die Herleitung der RBF schon abgeschlossen sein muss – die fachliche Lücke wird nicht verschwiegen.

**Nicht vorwegnehmen:** Ein korrigiertes magnetisches Flussfeld, eine Eisenverlustidentifikation oder eine validierte Reziprozitätsverletzung in den realen Messdaten liegt **noch nicht** vor.
