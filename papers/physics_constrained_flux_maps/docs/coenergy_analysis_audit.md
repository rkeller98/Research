# Wissenschaftlicher Audit der Co-Energy-/Flux-Map-Analyse

Stand: 2026-10-06, aktueller Working Tree. Gegenstand ist die experimentelle
Python-Analyse, insbesondere `coenergy_path_test.py`, verglichen mit den
Diagnostik-Analyzern. Die bestehenden Paper-Texte, Messdaten und ursprünglichen
Analysemodule wurden nicht verändert. Es wurde kein B-Spline-/RBF-Fitter gebaut.

## 1. Ergebnis und Evidenzgrenze

**Der beobachtete Unterschied ist reproduzierbar und kein Widerspruch zwischen
zwei mathematisch äquivalenten Widerstandsmessungen.** Vorzeichen, Faktor 2,
Pfadorientierung und Widerstands-Invarianz der vorhandenen Pfadformel sind korrekt
für die deklarierte Fehlerkonvention und den unskalierten dq-Flussintegralwert.
Die Größen messen unterschiedliche Eigenschaften des rekonstruierten Feldes.
Sie identifizieren denselben Widerstand nur unter zusätzlichen, hier nicht
nachgewiesenen Annahmen.

Vier zentrale Befunde:

1. Bei 2000 rpm/60 °C werden 8,274010 mΩ aus der High-Current-Parity und
   5,885553 mΩ als Median der Rechteck-Pfadäquivalente reproduziert.
2. Die Parity-Verbesserung betrifft die ausgewählte High-Current-Region.
   Über alle Spiegelpaare steigt der d-Residual-RMS nach dieser Änderung sogar.
3. Der Rechteckwert ist ein flächengemitteltes Curl-Äquivalent, kein lokaler
   Widerstand am eingezeichneten Zielpunkt. Seine Invarianz bei Änderung von
   `R_used` ist eine algebraische Eigenschaft, keine unabhängige Kalibrierung.
4. Komponentenweise lineare Delaunay-Interpolation konservativer nichtlinearer
   Flussproben erhält Integrabilität nicht. Die lokale Dreiecks-Curl ist besonders
   an geometrisch schlecht konditionierten Dreiecken unzuverlässig. Dagegen ist
   der Quadraturfehler bei 500 Punkten im konkreten 60-°C-Versuch viel zu klein,
   um die Widerstandsdiskrepanz von 2,388457 mΩ zu erklären.

Die Daten weisen Inkonsistenz mit dem einfachen gemeinsamen Modell auf; sie
identifizieren deren Ursache nicht. Insbesondere ist weder 8,274 noch 5,886 mΩ
ein hier nachgewiesener tatsächlicher Wicklungswiderstand. Auch die konservative
synthetische Referenz liefert keine obere Fehlergrenze für die unbekannte reale
Magnetik. Eine pauschale Eisenverlust-Erklärung wäre nicht gedeckt.

## 2. Vollständiger Datenfluss und Implementierungsprüfung

Die verpflichtenden Repository-Guides und beide Python-Verzeichnisse wurden
gelesen. Importer, `flux_correction.py` und beide MAT-Dateien sind zwischen den
beiden Paper-Verzeichnissen byte-identisch. Die MAT-Dateien sind v7.3/HDF5.
Die ursprüngliche Pfadanalyse wurde zuerst unverändert mit nichtinteraktivem
Matplotlib-Backend ausgeführt; die einzige Warnung betrifft `plt.show()` unter
diesem Backend, nicht die numerische Rechnung.

| Stufe | Tatsächliche Operation | Konsequenz |
|---|---|---|
| Import | HDF5-Referenzen für Signalnamen und Daten auflösen, zu float64-Vektoren flatten | Keine Maschinenphysik und keine Park-Transformation im Importer |
| Slice | `isclose` auf `PE_Rpm_req` und `Rotor_temp_ref` | Referenzgrößen definieren den Block, nicht verifizierte physikalische Temperaturen |
| Konstanten | Modus von `Const_Machine_R_s` und `Const_Machine_pole_pairs` | Widerstand wird vorausgesetzt, nicht gemessen/geschätzt; Outlier p=3, Multi-RPM p=4 |
| OP-Reduktion | Mittel über gleiche `op_index` | Mittelwerte der gemessenen d/q-Ströme und Spannungen |
| Rekonstruktion | `(uq-R_used*iq)/omega`, `(R_used*id-ud)/omega` | Requested speed liefert `omega=2*pi*p*rpm/60` |
| Key-Reduktion | Requested currents auf zwei Nachkommastellen runden, danach OP-Mittel gleich gewichten | Gemessene elektrische Werte bleiben ungerundet; keine Gewichtung nach ursprünglicher Samplezahl |
| Parity | Exakte requested-key Spiegelpaare, d-Halbdifferenz und q-Halbsumme | Tatsächliche Ströme müssen trotzdem nicht exakt gespiegelt sein |
| Symmetrieäquivalent | `-omega*r_d/a_q`, mit `a_q=(abs(iq_pos)+abs(iq_neg))/2` | Gültig oberhalb 10 % des maximalen Paarbetrags; High-Current-Summary ab 85 % |
| Interpolation | Delaunay auf gemessenen, key-aggregierten Strömen; zwei `LinearNDInterpolator` | Ein gemeinsames Mesh, aber unabhängige affine Komponenten; kein gemeinsames Potential |
| Pfade | d-dann-q und q-dann-d vom Ursprung; 500 gleichmäßige Trapezstützstellen pro Segment | Das Rechteck muss vollständig im konvexen Interpolationsgebiet liegen |
| Ausschluss | Zielbeträge in beiden Achsen jeweils strikt über 10 % des jeweiligen Maximums; NaN-Pfade überspringen | Andere Stützmenge als Parity; Achsenausschluss betrifft Ziele, nicht die Achsenabschnitte der Pfade |
| Pfadäquivalent | `omega*(W_A-W_B)/(2*id*iq)`, anschließend `R_used-delta_R_eq_path` | Vorzeichenbehaftetes Produkt gemessener Zielströme; nicht `abs(id*iq)` |

Relevant sind insbesondere `flux_correction.py:58–105,139–215` und
`coenergy_path_test.py:26–61,64–200,203–275`.
Die Rundung ist eine Quantisierung zur Zuordnung und keine allgemeine
Nähe-Toleranz. Ungepaarte Punkte werden in der Parity-Auswertung nicht
interpoliert. Die Pfadauswertung benutzt dagegen auch ungepaarte Flussproben.

An festen Slice-Konstanten ist die Rekonstruktion linear in den gemittelten
Signalen. Daher ist die gewählte Reihenfolge von Mittelung und Flussrekonstruktion
algebraisch konsistent. Sie behebt aber weder thermische Drift noch variable
Drehzahl oder unzulässige upstream-Mittelung. Die Herkunft der gemessenen
Spannungssignale und die Steady-State-Akzeptanz sind nicht im Code dokumentiert.

## 3. Unabhängige Vorzeichenprüfung

Setze `epsilon_R = R_used - R_true` und verwende exakt die vorgegebenen
stationären Gleichungen:

\[
u_d=R_{\rm true}i_d-\omega_e\psi_q,\qquad
u_q=R_{\rm true}i_q+\omega_e\psi_d.
\]

Einsetzen in die Rekonstruktion ergibt ohne Näherung:

\[
\widehat\psi_d-\psi_d=-\frac{\varepsilon_R}{\omega_e}i_q,
\qquad
\widehat\psi_q-\psi_q=+\frac{\varepsilon_R}{\omega_e}i_d.
\]

Mit \(J=\begin{bmatrix}0&-1\\1&0\end{bmatrix}\) ist der Fehler
\(\varepsilon_R J\boldsymbol i/\omega_e\). Ein zu großer eingesetzter
Widerstand senkt den d-Fluss bei positivem q-Strom und erhöht den q-Fluss bei
positivem d-Strom. Das stimmt mit beiden Implementierungen überein.

Für ein tatsächlich spiegelgleiches Paar eines parity-konformen Grundfeldes:

\[
r_d=-\frac{\varepsilon_R}{\omega_e}|i_q|,\qquad
r_q=\frac{\varepsilon_R}{\omega_e}i_d,
\qquad \Delta R_{\rm eq,sym}=-\omega_e r_d/|i_q|=\varepsilon_R.
\]

Bei unterschiedlich großen, aber entgegengesetzt gerichteten gemessenen
q-Strömen ist der Widerstandsanteil von \(r_d\) exakt
\(-\varepsilon_R a_q/\omega_e\). Das Grundfeld kann zusätzlich in die
Halbdifferenz lecken, weil die beiden gemessenen Argumente nicht spiegelgleich
sind. Bei veränderter Widerstandshypothese ist dieser Leakage-Anteil unverändert.
Somit verschiebt sich das Symmetrieäquivalent um die Widerstandsänderung; seine
Verschiebung belegt für sich keine physikalische Fehlerkorrektur.

Die symbolische Prüfung ist unabhängig in `audit_symbolic.py` implementiert.
Der numerische Injektionstest durchläuft zusätzlich die ursprüngliche
Spannungsrekonstruktion und Pairing-Implementierung.

## 4. Direkte Pfadherleitung und Green-Prüfung

Die vorhandenen Pfade sind

\[
A:(0,0)\to(x,0)\to(x,y),\qquad
B:(0,0)\to(0,y)\to(x,y),\quad x=i_d,\ y=i_q.
\]

Für den reinen Widerstandsfehler liefert A auf dem vertikalen Segment
\(\varepsilon_Rxy/\omega_e\); sein horizontaler Achsenanteil ist null.
B liefert auf dem horizontalen Segment
\(-\varepsilon_Rxy/\omega_e\); sein vertikaler Achsenanteil ist null.
Ein konservatives Grundfeld hat auf beiden Pfaden denselben Wert. Deshalb

\[
\boxed{W_A-W_B=2\varepsilon_Rxy/\omega_e},\qquad
\boxed{\Delta R_{\rm eq,path}=\omega_e(W_A-W_B)/(2xy)}.
\]

Der Faktor 2 entsteht durch die beiden entgegengesetzten Segmentbeiträge.
Die zweite unabhängige Herleitung benutzt

\[
r_{\rm curl}=\partial_x\widehat\psi_q-\partial_y\widehat\psi_d
=2\varepsilon_R/\omega_e.
\]

Die orientierte Randkurve ist A gefolgt vom umgekehrten B. Für \(xy>0\)
ist ihre Orientierung gegen den Uhrzeigersinn; für \(xy<0\) im Uhrzeigersinn.
Die stets gültige Schreibweise lautet

\[
W_A-W_B=\int_0^x\int_0^y r_{\rm curl}(\xi,\eta)\,d\eta\,d\xi
=\operatorname{sgn}(xy)\iint_{A_{\rm geom}}r_{\rm curl}\,dA.
\]

Ein unorientiertes Flächenintegral allein wäre bei den vielen negativen
d-Stromzielen falsch. Die ursprüngliche Division durch `id*iq` behandelt
dies korrekt. Numerische Tests decken alle vier Quadranten sowie positive,
negative und verschwindende injizierte Widerstandsfehler ab.

Für ein allgemeines Feld folgt

\[
\boxed{\Delta R_{\rm eq,path}(x,y)
=\frac{\omega_e}{2|xy|}\iint_{A_{\rm geom}}r_{\rm curl}\,dA}.
\]

Das ist ein **area-averaged resistance-equivalent curl residual**. Das lokale
Äquivalent wäre dagegen \(\Delta R_{\rm eq,curl}=\omega_e r_{\rm curl}/2\).
Der Zielpunkt beschriftet hier das Integrationsrechteck. Er darf nicht als Ort
einer lokalen Material-/Widerstandsidentifikation gelesen werden.
Ein einzelnes kleines Rechteckresiduum kann positive und negative Curl-Anteile
verdecken; endliche Rechtecktests beweisen keinen überall verschwindenden Curl.
Auch die ungewichtete Verteilung über alle Zielpunkte entspricht weder einer
einheitlichen Flächengewichtung noch unabhängigen Experimenten: Die Rechtecke
überlappen stark und teilen dieselben Flussproben.

Beispiel aus dem 60-°C-Datensatz: Bei ungefähr (−1096,60 A,170,91 A) beträgt
das lokale Dreiecksäquivalent −2,425 mΩ, das Rechteckmittel jedoch +2,947 mΩ.
Das ist kein Vorzeichenfehler. Am Messpunkt selbst ist der P1-Gradient außerdem
mehrdeutig; der lokale Tabellenwert ist der von `find_simplex` gewählte angrenzende
Dreieckswert, nicht eine eindeutig definierte Ableitung am Vertex.

## 5. Warum das zurückgerechnete Pfadäquivalent invariant ist

Ändere bei denselben Spannungen, Strömen und derselben Geschwindigkeit den
eingesetzten skalaren Widerstand um einen beliebigen konstanten Betrag \(h\):

\[
\widehat{\boldsymbol\psi}_{R+h}
=\widehat{\boldsymbol\psi}_{R}+\frac{h}{\omega_e}J\boldsymbol i.
\]

Das zusätzliche Feld ist affin. Daher reproduziert es die lineare
baryzentrische Interpolation auf dem unveränderten Mesh exakt. Auch die
gleichmäßige Trapezquadratur integriert diesen Zusatz exakt. Damit

\[
(W_A-W_B)_{R+h}=(W_A-W_B)_R+2hxy/\omega_e,
\quad \Delta R_{\rm eq,path}(R+h)=\Delta R_{\rm eq,path}(R)+h,
\]

\[
\boxed{(R+h)-\Delta R_{\rm eq,path}(R+h)=R-\Delta R_{\rm eq,path}(R)}.
\]

Im 60-°C-Versuch beträgt \(h=0,579010336\) mΩ. Der maximale verbleibende
punktweise Unterschied in `R_eq_path` ist nur \(1,39\cdot10^{-16}\) Ω.
Zusätzliche Tests benutzen −3,1 und +4,7 mΩ in allen Quadranten.

Das ist ein guter Implementierungs-Sanity-Test. Es ist kein Beleg, dass
`R_eq_path` den tatsächlichen Widerstand kennt. Beispielsweise hinterlässt
ein anderes nichtkonservatives Feld seine gesamte Zirkulation in diesem Wert.
Die Invarianz setzt unveränderte Daten, Koordinaten, Stützmenge, Geschwindigkeit,
lineare Interpolation und lineare Integrationsoperation voraus; adaptive
Filterung oder nichtlineare Regularisierung kann sie numerisch zerstören.

## 6. Voraussetzungen einer skalaren magnetischen Co-Energy

Mathematisch muss die Einsform \(\psi_d\,di_d+\psi_q\,di_q\) exakt sein.
Für ein C¹-Feld ist gleiche gemischte Ableitung lokal notwendig. Auf einem
offenen einfach zusammenhängenden Gebiet ist sie hinreichend; bei Löchern
muss zusätzlich die Zirkulation um nicht kontrahierbare Schleifen verschwinden.
Ein C²-Potential erzeugt eine symmetrische Differentialinduktivitätsmatrix.
Positive Differentialinduktivität ist eine zusätzliche Stabilitäts-/Passivitätsfrage,
nicht die Definition von Integrabilität.

Die Verbindung zwischen verlustfreiem magnetischem Mehrtor, Co-Energy und
Reziprozität folgt aus der terminalen Energiebilanz bei festgehaltener Geometrie.
Auch bei nichtlinearer Magnetik müssen die Kreuzableitungen gleich sein, wenn
die Flüsse Ableitungen desselben Zustands-Potentials sind.
[Haus und Melcher, Kapitel 11, besonders §11.7](https://ocw.mit.edu/courses/res-6-001-electromagnetic-fields-and-energy-spring-2008/0f814aee1c72517df7d7e7e96b7365e1_11.pdf)
und [Jebai et al., §II-C](https://arxiv.org/html/1403.6641v1) liefern dafür
Standard- beziehungsweise primäre Autorenquellen.

| Physikalischer Aspekt | Folgerung für einen zweidimensionalen statischen W′-Ansatz |
|---|---|
| Magnetostatisch / quasi-statisch | Eine eindeutige Gleichgewichtsmagnetik bei festem Zustand kann ein Potential tragen; langsame Messung allein beweist Verlustfreiheit nicht |
| Verlustfreies reziprokes magnetisches Subsystem | Passende Strom-Fluss-Paare erlauben eine konservative Beschreibung; ein verlustbehaftetes Gesamtsystem kann trotzdem ein separat modelliertes Speichersubsystem haben |
| Sättigung / Kreuzsättigung | Verändern die Hesse-Matrix und Kopplung, erzeugen allein keinen Curl eines korrekten Potentials |
| PM-Bias | Ein fester reversibler Magnetzustand erlaubt beispielsweise einen linearen Potentialterm; PMs sind kein Integrabilitätshindernis |
| Hysterese | Gleiche Ströme können bei anderer Vorgeschichte andere Flüsse ergeben; zwei Stromkoordinaten reichen dann nicht als Zustandsbeschreibung |
| Wirbelströme | Zusätzliche innere Strom-/Flusszustände; deren stationäre Eliminierung kann eine frequenzabhängige scheinbare Kennlinie erzeugen |
| Eisenverluste | Gemessener Strom kann Speicher- und Verlustzweige speisen; der richtige Strom für die Magnetik muss modellbezogen bestimmt werden |
| Raumharmonische | Bei fester Rotorposition kann ein größeres Potential existieren; eine zweidimensionale Fundamental-/Mittelwertkarte benötigt eine konsistente Reduktion |
| Dynamik | Fehlende Fluss-Zeitableitungen, zeitliche Phasenverschiebungen oder unvollständiger stationärer Zustand verfälschen die verwendete stationäre Inversion |

Feste Temperatur, Magnetzustand und mechanische Geometrie beziehungsweise eine
konsistente rotorpositionsgemittelte Beschreibung gehören zur Modellklasse.
Eine current-unabhängige Mittelung konservativer Potentiale erhält grundsätzlich
deren Gradientstruktur; current-abhängige Auswahl/Gewichtung muss das nicht tun.
Das ist eine mathematische Folgerung, keine nachgewiesene Eigenschaft der
upstream-Mittelung dieser Messdateien.

## 7. Parity und Conservation sind unabhängig

Für einen skalaren Gradient-Fit ist **Integrabilität/Reziprozität notwendig**,
wenn das Feld exakt repräsentiert werden soll. Reflection-Parity ist eine
zusätzliche maschinen-, geometrie- und koordinatenabhängige Bedingung.
Ein Least-Squares-Potential kann auch inkonsistente Daten approximieren;
sein konstruktiv verschwindender Curl beweist dann nur die Modellstruktur.

Ein explizites dimensionsloses Gegenbeispiel ist
\(\psi_d=1+y^2,\ \psi_q=y\): d-even und q-odd gelten exakt, aber
\(r_{\rm curl}=-2y\neq0\). Umgekehrt ist
\(\widetilde{\boldsymbol\psi}(\widehat{\boldsymbol i})
=R(-\alpha)\boldsymbol\psi(R(\alpha)\widehat{\boldsymbol i})\)
der Gradient von \(W'(R(\alpha)\widehat{\boldsymbol i})\). Eine kohärente
konstante Winkelrotation erhält Integrabilität und verdreht die Symmetrieachse.
Winkelabhängige oder inkohärente Transformationen fallen nicht unter diese Aussage.

Eine direkte Darstellung des scheinbaren Konflikts liefert außerdem das Feld
\(\psi_d=\psi_{pm}+L_dx+a y,\ \psi_q=L_qy+b x\).
Sein Symmetrieäquivalent aus dem d-Kanal ist \(-\omega_e a\), sein
Pfadäquivalent \(\omega_e(b-a)/2\). Das q-even Residuum trägt \(b x\).
Erst für \(b=-a\), also den reinen Widerstands-Fingerabdruck, stimmen die
beiden Äquivalente überein. Sind etwa \(a=b\neq0\), ist das Feld konservativ,
obwohl die ausgewählte q-Parity verletzt ist. Eine Änderung von R zur
Beseitigung des d-odd Terms erzeugt dann erst Curl. Die beiden Operationen
optimieren keine identische physikalische Eigenschaft.

Sun und Xiao behandeln Parity, gleiche inkrementelle Kreuzinduktivitäten und
Induktivitätskontinuität ausdrücklich als separate Kriterien; ihr Modell
berücksichtigt Eisenverluste und Raumharmonische ausdrücklich nicht.
[Sun und Xiao (2020), §2.1–2.2](https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/iet-epa.2020.0137)
stützt diese Trennung, nicht die automatische Übertragbarkeit auf eine
verlustbehaftete Terminalstromkarte. **Bessere Parity muss weder besseren Curl
noch kleinere Pfadresiduen erzeugen.**

## 8. Eisenverluste und die korrekten Stromkoordinaten

Die stationäre Spannungsinversion und die konservative Magnetik sind zwei
verschiedene Schritte. Unter passendem Terminalmodell kann die Inversion einen
Fluss liefern, während dessen Abhängigkeit vom gemessenen Statorstrom keine
konservative magnetische Beziehung ist.

In einem Parallelzweig-Modell gilt schematisch
\(\boldsymbol i_s=\boldsymbol i_{mag}+\boldsymbol i_{Fe}\).
Die Magnetik ist dann zunächst in Magnetisierungsstromkoordinaten zu beschreiben.
Richter, Dollinger und Doppelbauer stellen diesen Unterschied sowie das Matching
motorischer/generatorischer **magnetischer Zustände** dar. Sie zeigen, dass sich
dabei die gemessenen Ströme durch Verlustströme unterscheiden können.
[Richter et al. (2014), §II, Fig. 3 und Gleichungen 9–16](https://publikationen.bibliothek.kit.edu/1000045029/3503760).
Dies unterscheidet sich vom bloßen Spiegeln requested-current keys.

Eine unabhängige algebraische Illustration, ohne Anspruch auf ein identifiziertes
Modell dieser Maschine: Sei \(\boldsymbol\psi=L\boldsymbol i_{mag}\) mit
\(L=\operatorname{diag}(L_d,L_q)\), und
\(\boldsymbol i_{Fe}=cJ\boldsymbol\psi\),
\(c=\omega_e/R_{Fe}\). Dieser Zweig dissipiert positive Leistung
\(\|\omega_eJ\boldsymbol\psi\|^2/R_{Fe}\). Dann

\[
\frac{\partial\boldsymbol\psi}{\partial\boldsymbol i_s}
=L(I+cJL)^{-1}
=\frac{1}{1+c^2L_dL_q}
\begin{bmatrix}L_d&cL_dL_q\\-cL_dL_q&L_q\end{bmatrix},
\]

\[
r_{\rm curl,is}=-2cL_dL_q/(1+c^2L_dL_q)\neq0.
\]

Die zugrunde liegende Magnetik in \(i_{mag}\) ist dennoch konservativ.
Ein einfaches Modell dieser Form würde übrigens gemeinsame Symmetrie- und
Curl-Äquivalente erzeugen; es erklärt die konkrete Diskrepanz nicht automatisch.
Leckinduktivitäten, PM-Bias und nichtlineare/veränderliche Verlustzweige erfordern
eine passend erweiterte Beschreibung.

Eine reine Variablenumbenennung löst das Problem nicht: Für
\(i_{mag}=f(i_s)\) wäre der Gradient von \(W'(f(i_s))\)
gleich \(Df(i_s)^T\psi_{mag}\), nicht allgemein gleich dem rekonstruierten
Flussvektor \(\psi_{mag}\). Die konservative Einsform muss vollständig
transformiert werden.

Die final publizierte Kullick/Hackl-Arbeit zu nichtlinearen steady-state
Maschinenkarten ist eine **Induktionsmaschinen**-Arbeit, keine Validierung eines
PMSM-Potentials in Terminalstromkoordinaten. Ihr publizierter DOI ist
[10.1109/TIE.2022.3153811](https://doi.org/10.1109/TIE.2022.3153811),
IEEE TIE 70(1), 211–221, 2023; die Autorenliste der
[Autoreninstitution](https://lmres.ee.hm.edu/forschung/publikationen/) bestätigt
die Journalversion. Der Verlustmodell-/steady-state-Kontext ist relevant,
die Maschinenklassen dürfen nicht gleichgesetzt werden. Die publizierte
synchronmaschinenbezogene ICIT-Arbeit von Hackl/Kullick/Monzen
[10.1109/ICIT46573.2021.9453497](https://doi.org/10.1109/ICIT46573.2021.9453497)
wird als Kontext geführt; ihr Volltext war hier nicht direkt über den Publisher
zugänglich. Keine spezifische Gleichung dieses Audits hängt von ihm ab.

## 9. dq-/Park-Normierung und die Bedeutung von W_A/W_B

Die Python-Dateien führen keine abc→dq-Transformation aus. Deren Skalierung
muss aus Messsystem/DSP-Dokumentation oder unabhängiger Energiebilanz kommen.
Für gleichartig amplitude-invariant transformierte Strom- und Flusskoordinaten
bei festem Winkel und ohne Zero-Sequence gilt

\[
dW'_{phys}=\tfrac32(\psi_d\,di_d+\psi_q\,di_q).
\]

Bei orthonormaler power-invariant Transformation ist der Faktor 1.
Allgemein bestimmt das Transformationsmetric die Einsform; ungleiche Skalierung
von Strom und Spannung/Fluss kann mehr als einen globalen Faktor verlangen.
Die Transformation von Winkel beziehungsweise mechanischer Lage muss bei dieser
Stromdifferentiation festgehalten werden.

Es gibt **provisorische numerische Hinweise** auf amplitude-invariante
Stromkoordinaten: Der Median von `PE_I_AC_meas_Arms / hypot(id,iq)` ist bei
40/60/80 °C 0,707499/0,707659/0,707102 und bei 1000/3000 rpm
0,708494/0,704586. Das ist nahe \(1/\sqrt2\).
Beim Outlier bestätigt `CAN_I_AC_meas_Arms` diese Größenordnung. Die ausgewerteten
Yokogawa-Phasenstrom-/Leistungssignale und `PE_U_AC_meas_Vrms` sind jedoch null;
sie liefern keine unabhängige Spannungs-/Leistungsnormierung. Im Multi-RPM-Satz
ist auch das genannte CAN-RMS-Signal null. Signalnamen allein sind kein Nachweis.
Die Verhältnisse wurden auf rohen Slice-Samples mit einem transparenten
10-%-Nennerfilter geprüft; RMS/Harmoniken/Mittelungsintervalle sind nicht
gleichbedeutend mit fundamentalem dq-Betrag.

`W_A` und `W_B` sind daher zunächst **dq-Flussintegrale mit Dimension Wb·A**.
Ist das Feld nicht konservativ, sind es zwei pfadabhängige Proxys und keine zwei
gemessenen Werte eines magnetischen Zustands-Potentials. Selbst bei geklärter
Skalierung fehlt ein absoluter Energie-Referenzwert. Die Paper-Notation definiert
bereits normalisiertes W′; die tatsächliche Messsystem-Normierung bleibt zusätzlich
zu verifizieren.

Für einen gemeinsamen konstanten Faktor \(\kappa\) gilt
\(\Delta W_{phys}=\kappa\Delta W_{dq}\). Dann lautet die Pfadformel
\(\Delta R=\omega_e\Delta W_{phys}/(2\kappa xy)\).
Wenn physikalische Joule in den Zähler eingesetzt werden, ohne den Nenner
anzupassen, entsteht ein Faktorfehler. Die aktuelle Implementierung verwendet
jedoch durchgehend unskalierte dq-Flussintegrale und ist diesbezüglich intern
konsistent. Ein globales \(3/2\) kann die Pfadabhängigkeit und die beiden
gegengerichteten Widerstandsäquivalente nicht erklären.

Die zusätzliche Ausgabe
\(\rho=|W_A-W_B|/[0,5(|W_A|+|W_B|)]\) ist eine deskriptive relative
Pfaddifferenz, kein relativer Fehler gegenüber echter Co-Energy. Sie hängt
auch von den gemeinsamen konservativen Beiträgen und vom Startpunkt ab und
kann bei fast verschwindenden Integralen groß werden. Ihre obere Schranke 2
ist algebraisch; 200 % bedeuten nicht einen gemessenen Energiefehler von 200 %.

## 10. Interpolation, lokale Curl und Quadratur

`LinearNDInterpolator` interpoliert auf jedem Delaunay-Dreieck linear
baryzentrisch und gibt außerhalb der konvexen Hülle standardmäßig NaN zurück.
[SciPy-Dokumentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.LinearNDInterpolator.html).
Die Komponenten sind C⁰-kontinuierlich, ihre Gradienten sind stückweise konstant
und springen über Kanten. Der gemeinsame Mesh erzwingt keine symmetrische
Jacobi-Matrix. Kanten tragen bei einem kontinuierlichen P1-Feld keinen
zusätzlichen Sprungterm der Feldwerte zur distributionellen Curl bei; deshalb
ist die flächenweise Green-Prüfung hier zulässig.

Der Audit berechnet zwei lokale Diagnosen, ohne eine davon als wahre Ableitung
zu akzeptieren:

- **P1-Dreiecksgradient:** analytischer baryzentrischer Gradient; exakt für den
  vorhandenen Interpolator, aber stark von Dreiecksgeometrie und Datenfehlern abhängig.
- **Lokale lineare Regression:** 12/24/48 nächste gemessene Stromnachbarn,
  radius-skalierte Koordinaten, Gewichte `1/(1+(distance/radius)^2)`;
  unconstrained least squares, mit dokumentiertem Radius und Design-Kondition.
  Kein konservativer oder symmetrieerzwungener Fit. Räumliche Mittelung kann
  echte Struktur unterdrücken und an Grenzen Ableitungsbias erzeugen.

Bei 60 °C enthält der Mesh 8234 Dreiecke. Das lokale
\(\omega_e r_{curl}/2\) hat Median −0,2165 mΩ, MAD 4,8687 mΩ, aber
ungewichteten RMS **2983,7 mΩ** und Extrema etwa −155108 bis +128366 mΩ.
Die maximale geometrische Edge-Kondition ist 15605,5; der maximale
Umkreisradius 788738 A ist ein Warnsignal für fast kollineare Randdreiecke.
Solche lokalen Extremwerte dürfen nicht als physikalische Widerstandsstruktur
interpretiert werden.

Eine zusätzlich ausgewiesene, rein geometrische Sensitivitätsauswertung mit
Edge-Kondition ≤10 behält 7991 Dreiecke und 99,208 % der Hüllenfläche;
der ungewichtete RMS sinkt auf 10,438 mΩ. Die vollständigen Daten bleiben
unverändert exportiert. Dieser Schwellenwert ist kein validierter physikalischer
Filter. Auch gut geformte Dreiecke können verrauschte Ableitungen liefern.

Die lokale Regression liefert für k=12/24/48 die Median/MAD-Werte
−0,893/1,648, −0,953/1,141 und −1,083/0,983 mΩ. Diese verschiedenen
räumlichen Gewichtungen sind nicht mit dem Median der Rechteckmittel identisch.
Ein über die gesamte Hüllenfläche gewichtetes Curl-Äquivalent beträgt −1,719 mΩ;
es nutzt ein anderes Gebiet als die vielen Rechtecke. Keine dieser Zahlen ist
eine zusätzliche Widerstandsidentifikation.

**Exakte P1-Pfadintegration:** `audit_coenergy.py` schneidet jedes Segment an
allen Mesh-Kanten und integriert den affinen Anteil jedes Teilsegments exakt.
Unabhängig davon werden Dreiecke mit dem Zielrechteck geclippt und
`curl * Schnittfläche` aufsummiert. Bei acht deterministisch ausgewählten
realen Rechtecken stimmen beide Ergebnisse mit maximal
\(2,54\cdot10^{-14}\) Wb·A überein. Synthetische Tests liefern dieselbe
Green-Konsistenz. Das prüft Implementierung und Orientierung, nicht die
physikalische Richtigkeit des Interpolators.

Für 64 deterministisch über die nach d/q-Keys sortierte gültige Zielmenge
verteilte Rechtecke (34 positive, 30 negative q-Ziele) ergibt die Trapezquadratur:

| Punkte je Segment | RMS-Fehler von ΔR_path gegenüber exakter P1-Integration, mΩ |
|---:|---:|
| 50 | 0,006432 |
| 100 | 0,001389 |
| 250 | 0,000300 |
| 500 | 0,0000798 |
| 1000 | 0,0000215 |
| 2000 | 0,00000717 |

Über **alle 2869** gültigen 60-°C-Ziele beträgt der 500-Punkte-RMS-Fehler
0,0000766 mΩ und der maximale absolute Fehler 0,000628 mΩ.
Der Pfadmedian bleibt mit exakter P1-Integration bei 5,885512 mΩ.
Damit ist die konkrete 2,388-mΩ-Diskrepanz kein Effekt unzureichender
Trapez-Stützstellen. Höhere N verbessert die Quadratur, nicht das Mesh-Modell.

Die konvexe Hülle ist kein Beleg dichter experimenteller Abdeckung:
Delaunay überbrückt auch innere Messlücken. Lange Dreiecke und extrapolationsnahe
Achsenstrecken sind zusätzlich zu NaN-Prüfungen zu untersuchen. Dass ein Ziel
innerhalb liegt, genügt nicht; seine beiden anderen Rechteck-Ecken müssen
ebenfalls innerhalb liegen. Für ein konvexes Gebiet genügt dann die Eckenprüfung
für das ganze Rechteck. Auf komplexer realer Stützgeometrie könnte das konvexe
Mesh trotzdem ungemessene Zwischenräume verdecken.

## 11. Synthetische Ground Truth

Die Modelle wurden vor Ergebnisbetrachtung explizit festgelegt. Sie werden an
allen **4220 tatsächlich gemessenen OP-Stromkoordinaten** des 60-°C-Slices
ausgewertet; die originale Key-Aggregation erzeugt wieder 4154 Punkte.
Die Ströme oder requested keys der Messung werden nicht verändert.
Der Vergleich der Pfade verwendet dieselben 64 deterministischen Zielrechtecke.

Mit \(I_*=1279,685295\) A, \(\psi_*=0,2\) Wb,
\(x=i_d/I_*,y=i_q/I_*\) ist das lineare Potential

\[
W'_A/(\psi_*I_*)=0,8x+0,5x^2+0,65y^2.
\]

Das konservative gesättigte/cross-saturated Potential lautet

\[
W'_B/(\psi_*I_*)=0,8x+0,5x^2+0,65y^2
-0,02x^4-0,025y^4-0,03x^2y^2+0,02xy^2.
\]

Es ist q-even und hat symmetrische Hesse-Matrix. Auf \(|x|,|y|\le1,1\)
gelten die konservativen Schranken H_dd≥0,6370, H_qq≥0,7762 und
|H_dq|≤0,1892, also positive Differentialgewinne per strikter
Diagonaldominanz. Die negative quartische Krümmung modelliert lokale
Sättigung; das Polynom ist ausdrücklich keine globale Materialkennlinie.
Die gemessenen Punkte und die kleine Winkelrotation bleiben im geprüften Bereich.

Die Widerstandsinjektion ist \(\varepsilon_R=+2\) mΩ. Aus den
analytischen Flüssen einschließlich Bias werden synthetische Spannungen erzeugt,
die der unveränderte Analyzer wieder invertiert. Der Winkeltest verwendet
die exakte kohärente Argument-/Vektorrotation um 0,04 rad.

| Test | Analytischer Feld-Curl | Interpoliertes ΔR_path: Median / RMS, mΩ | Parity-Äquivalent: Median über alle gültigen Originalpaare, mΩ |
|---|---|---:|---:|
| A linear konservativ | 0 | 0 / <10⁻¹² | −0,018273 |
| B gesättigt konservativ | 0 | 0,000251 / 0,013565 | −0,017635 |
| C linear +2 mΩ | 2ε_R/ω | 2,000000 / 2,000000 | 1,981727 |
| C gesättigt +2 mΩ | 2ε_R/ω | 2,000251 / 2,002938 | 1,982365 |
| D kohärenter Winkeloffset | 0 | 0,000225 / 0,013326 | −1,100211 |

Der RMS in der Tabelle ist der RMS der Größe selbst, bei C also nicht der
Fehler relativ zu 2 mΩ. Im nichtlinearen B-Test ist die interpolierte
Pfadäquivalentabweichung maximal 0,081585 mΩ an diesen 64 Rechtecken.
Das analytische Flussfeld wird zusätzlich direkt entlang der Pfade integriert:
Gauss-Legendre mit acht Punkten je Segment ist für diese Polynome exakt.
Sein maximaler Loop-Fehler ist unter \(5\cdot10^{-14}\) Wb·A.

Nichtlineare OP→Key-Mittelung ist grundsätzlich eine zusätzliche Fehlerquelle:
der Mittelwert von Gradienten an leicht verschiedenen Strömen ist nicht exakt
der Gradient am gemittelten Strom. Eine separate Prüfung wertet B daher direkt
an den 4154 aggregierten Stromkoordinaten aus. Der P1-Pfadäquivalent-RMS bleibt
0,013564 mΩ; die Differenz zur originalgetreuen OP-/Key-Pipeline hat nur
0,00000216 mΩ RMS an diesen 64 Zielen. Das Artefakt dieses konkreten B-Tests
stammt somit fast vollständig von der Interpolation. Diese kleine Differenz ist
keine allgemeine Schranke für reale Wiederholungsstreuung.

**Die nichtlinearen interpolierten Tests sind nicht null bis zur
Maschinengenauigkeit.** Das ist ein gefundenes Interpolationsartefakt, kein
Verlust- oder Sättigungsnachweis. P1-Dreieckscurl kann beim exakt konservativen
B-Test sogar Ω-große Äquivalente in schmalen Randdreiecken erzeugen. Die lokale
Regression hat dort je nach k RMS-Bias 0,0153–0,0297 mΩ; auch Glättung liefert
keine automatisch exakte konservative Ableitung.

**Die ursprünglichen Symmetriepaare sind ebenfalls nicht exakt gespiegelt in
gemessenen Stromkoordinaten.** Deshalb bleibt schon beim linearen konservativen
Modell eine kleine Parity-Leakage; im linearen C-Test liegt der absolute Median
bei 1,981727 statt exakt 2 mΩ. Eine exakte analytische Mirror-Auswertung liefert
in A/B null und in C 2 mΩ bis zur Rundungsgenauigkeit. Die Differenz zwischen
injiziertem und uninjiziertem Originalpaar-Ergebnis beträgt punktweise exakt
2 mΩ innerhalb 10⁻¹² Ω. Dasselbe gilt für den Curl- und Pfad-Inkrementtest.
Es wurden also weder Koordinaten passend gemacht noch Toleranzen gewählt, um
die vorhandene Paargeometrie fälschlich als ideal erscheinen zu lassen.

Beim linearen Modell reproduzieren Curl und Path den absoluten injizierten
Fehler: maximale P1-Curlabweichung unter 10⁻¹⁰ Ω, Pfadabweichung unter
10⁻¹² Ω. Alle drei lokalen Regressionsskalen reproduzieren das affine Feld
ebenfalls bis zur Rundungsgenauigkeit. Der Winkeltest bestätigt die zentrale
Trennung: starke Parity-Verletzung bei weiterhin konservativem analytischem Feld.

Grenzen dieses Ground-Truth-Tests: eine glatte explizite Modellfamilie, eine
reale Koordinatengeometrie, keine synthetischen Hysterese-/Sensor-/Loss-Zustände,
keine Kalibrierung gegen reale unbekannte Derivationen. Kleine Fehler in diesem
Modell schließen größere Interpolationsfehler einer stärker gekrümmten oder
verrauschten realen Karte nicht aus.

## 12. Reale Resultate und zu korrigierende Schlussfolgerungen

Die beiden Datensätze werden getrennt behandelt; unterschiedliche Polpaarzahlen
und fehlende Maschinen-Provenienz erlauben keine gemeinsame Widerstandskalibrierung.
Alle Widerstandswerte in der folgenden Tabelle sind mΩ. Die Symmetrie-Spalte
ist der bisherige High-Current-Summary, die Pfad-Spalte der Median über eine
andere Menge gültiger Rechtecke. MAD ist unskaliert und kein Konfidenzintervall.

| Datensatz | rpm | Rotorref. °C | OP / Keys | Parity-Paare / High | Pfadziele / Hull-Skips | R_eq,sym | R_eq,path Median / MAD | Exakter P1-Pfadmedian |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Outlier | 2000 | 40 | 4220 / 4154 | 1172 / 79 | 2868 / 3 | 7,599140 | 5,007865 / 1,783325 | 5,007792 |
| Outlier | 2000 | 60 | 4220 / 4154 | 1172 / 80 | 2869 / 2 | 8,274010 | 5,885553 / 1,728698 | 5,885512 |
| Outlier | 2000 | 80 | 4220 / 4154 | 1172 / 79 | 2839 / 32 | 8,963406 | 6,488047 / 1,769623 | 6,487975 |
| Multi-RPM | 1000 | 70 | 109 / 104 | 39 / 6 | 65 / 4 | 12,156625 | 5,960078 / 2,405193 | 5,960063 |
| Multi-RPM | 3000 | 70 | 109 / 104 | 39 / 7 | 45 / 24 | 15,334054 | 3,809622 / 2,991105 | 3,808417 |

Hull-Skips zählen nur Ziele nach Achsenausschluss; im Outlier verbleiben vorher
2871, im Multi-RPM 69 Zielkandidaten. Der starke Unterschied von 65 zu 45
gültigen Multi-RPM-Rechtecken macht deren Medianvergleich zusätzlich
stützmengenabhängig. Hier wird daraus keine punktweise Speed-Curl-Hypothese
abgeleitet. Das bereits vorhandene gemeinsame 36-Paar-Parity-Speed-Experiment
bleibt separat gültig; sein direkter Scaling-Test wird nicht durch diese
unterschiedlichen Rechteckmengen ersetzt.

Für den zentralen 60-°C-Versuch sind die Änderungen besonders aufschlussreich:

| Metrik | R_used=7,695 mΩ | R_used=8,274010 mΩ |
|---|---:|---:|
| High-Current d-Residual-RMS, mWb | 1,100092 | 0,219939 |
| High-Current q-Residual-RMS, mWb | 0,487494 | 0,277063 |
| High-Current Vektor-Residual-RMS, mWb | 1,203268 | 0,353747 |
| Alle Paare: d-Residual-RMS, mWb | 1,746480 | 1,954456 |
| Alle Paare: q-Residual-RMS, mWb | 1,308799 | 1,183835 |
| Alle Paare: Vektor-Residual-RMS, mWb | 2,182464 | 2,285030 |
| Median relative Pfaddifferenz, % | 3,488090 | 4,226703 |
| Median ΔR_eq,path, mΩ | 1,809447 | 2,388457 |
| Median R_eq,path, mΩ | 5,885553 | 5,885553 |

Die Differenz der beiden Median-Pfaddifferenzen ist 0,738613 Prozentpunkte;
der Median der punktweisen Differenzen ist dagegen 0,875 Prozentpunkte.
Diese zwei Operationen sind nicht identisch. Die vorhandene Ausgabe rechnet
den letzteren korrekt, aber ein Bericht muss die Metrik benennen.

### Gültig bleibende Aussagen

- Terminalspannungsinversion, Fehler-Vorzeichen und Widerstands-Fingerabdruck.
- High-Current-Parity kann unter der Hypothese durch eine skalare R-Änderung
  deutlich kleiner werden; räumlich konstantes Äquivalent gilt nicht global.
- Exakte konstante kohärente Winkelrotation kann Reziprozität erhalten und
  gleichzeitig die beobachtete q-Parity verletzen.
- Ein stromproportionaler Spannungsfehler kann denselben Widerstands-Bias
  erzeugen; weder Symmetrie noch Curl/Pfade trennen ihn automatisch von Rs.
- Analytische Sättigung und Cross-Saturation eines Potentials erzeugen keinen Curl.
- Die bereits formulierten Modellgrenzen und die Zurückhaltung gegenüber
  eindeutigem Ursachen-/Korrekturclaim sind gerechtfertigt.

### Präzisierungen beziehungsweise Korrekturen

- „Die Flusssymmetrie verbessert sich“ muss Stützmenge und Metrik nennen:
  High-Current verbessert sich, globale d- und Vektor-RMS hier nicht.
- „Co-Energy wird pfadabhängiger“ sollte heißen: Die rekonstruierten,
  interpolierten dq-Flussintegrale dieser Pfade weichen stärker voneinander ab.
  Ein existierendes physikalisches Zustands-Potential wird damit nicht gemessen.
- `R_eq_path(id,iq)` und seine 3D-Darstellung sind rectangle-indexed,
  flächengemittelte Äquivalente. Der Originalplot beschriftet dies nicht ausreichend.
- Der Invarianztest beweist die affine R-Abhängigkeit der Implementierung,
  nicht den richtigen physikalischen Widerstand.
- Ein konservatives nichtlineares Feld muss nach unabhängiger P1-Interpolation
  nicht exakt konservativ sein. Lokale Dreiecks-Curl-Spitzen sind ohne
  Geometrie-/Noise-Prüfung keine belastbare Magnetikdiagnose.
- Dimension Wb·A bedeutet nicht automatisch physikalische absolute Joule.

Beide Größen müssten denselben R_true liefern, wenn das unbekannte Grundfeld
in den verwendeten Koordinaten konservativ **und** reflection-symmetrisch ist,
nur ein einziger konstanter Widerstandsmismatch vorliegt, Ströme/Spannungen/Winkel/
Geschwindigkeit konsistent sind, die Paare echte Spiegel sind und numerische
Interpolation/Integration hinreichend genau sind. Die aktuelle Diskrepanz
zeigt, dass diese gemeinsame Beschreibung nicht nachgewiesen ist. Sie benennt
nicht, welche einzelne Annahme scheitert.

Liu et al. behandeln explizit Flusskennfeldidentifikation unter unbekanntem
Schaltungswiderstand und Inverternichtlinearität. Die veröffentlichte
Abstract-/Metadatenquelle ist
[IEEE TII 14(2), 556–568 (2018), DOI 10.1109/TII.2017.2722470](https://ieeexplore.ieee.org/document/7967682/).
Dies stützt die Relevanz der konkurrierenden Unsicherheiten; ihr Verfahren
wird hier nicht nachgebaut und belegt keine konkrete Ursache der vorliegenden Daten.

## 13. Empfohlener nächster Forschungsschritt

**Zunächst die Messkoordinaten und die gemeinsame physikalische Baseline
validieren, bevor ein konservatives Potential auf diese Daten gefittet wird.**

1. Messsystem-Parkmatrizen, Strom-/Spannungsskalierung, Winkelkonvention,
   Spannungsrekonstruktion, Zeitabgleich, Mittelungsfenster und tatsächliche
   Drehzahl dokumentieren. Die RMS-Verhältnisse sind ein Ansatzpunkt, kein
   Ersatz für die Transformation. Prüfen, welche Verlust-/Leistungskanäle
   tatsächlich verfügbar sind; vorhandene Nullkanäle sind keine Loss-Messung.
2. Unabhängigen DC-/Vierleiter-Widerstand bei dokumentierter Wicklungstemperatur
   und stabilem Magnet-/Thermalzustand erfassen. Rotor-/Stator-Referenzen allein
   beweisen keinen Leiterzustand. Das trennt eine echte Widerstandskalibrierung
   von der Wahl eines diagnostischen Residualnullpunkts.
3. Auf einer gut abgedeckten gemeinsamen Stützregion geschlossene **lokale**
   Stromraum-Schleifen verschiedener Größe und Anker auswerten. Ergebnisse
   mit Mesh-Geometrie, Regressionsradius und Wiederholmessungsstreuung vergleichen.
   Kleine Schleifen begrenzen räumliche Mittelung, verstärken aber Rauschen;
   ihre Größe muss durch das Fehlerbudget begründet werden. Kein Residuum
   verschwindet durch bloße Benennung als Widerstand.
4. Erst mit unabhängigen Spannungs-, Leistungs-, Winkel- und Thermalgrößen
   prüfen, ob ein loss-aware Modell beziehungsweise Magnetisierungsstromkoordinaten
   erforderlich sind. Motor-/Generator-Matching nach magnetischem Zustand und
   positive/negative Drehzahlmessungen können zusätzliche Richtungen liefern.
   Die vorhandenen Daten identifizieren Eisenverluste, Sensorik und Inverter
   noch nicht getrennt.
5. Danach entscheiden, welches Subsystem ein W′-Fit repräsentieren soll.
   Ein konservativer Fit darf später die Abweichung zur angenommenen Klasse
   quantifizieren; er darf nicht die offene physikalische Interpretation durch
   konstruktiv nullgesetzten Curl verdecken. Parity und Conservation separat
   validieren und unbekannte Beiträge ausdrücklich als Residuum erhalten.

## 14. Literaturprüfung und Zugriffsgrenzen

| Quelle | Primärer Zugriff / überprüfter Beitrag |
|---|---|
| Sun, X.; Xiao, X. (2020), IET EPA 14(11), 2044–2050, DOI 10.1049/iet-epa.2020.0137 | Publisher-Volltext: getrennte Kriterien und ausgeschlossene Eisenverluste/Raumharmonische |
| Haus, H. A.; Melcher, J. R. (1989), *Electromagnetic Fields and Energy*, Kap. 11 | MIT-Veröffentlichung des Standardwerks: terminale Energiebilanz, Co-Energy und Reziprozität |
| Jebai, A. K.; Combes, P.; Malrait, F.; Martin, P.; Rouchon, P. (2014), *Energy-based modeling of electric motors*, arXiv:1403.6641 | Autorenpreprint, als solcher bezeichnet: Energieformulierung und Konstruktionssymmetrien |
| Richter, J.; Dollinger, A.; Doppelbauer, M. (2014), ICEM, 1635–1641, DOI 10.1109/ICELMACH.2014.6960401 | Institutioneller Volltext: Magnetisierungs-/Verlustströme und Matching magnetischer Zustände |
| Liu, K. et al. (2018), IEEE TII 14(2), 556–568, DOI 10.1109/TII.2017.2722470 | Publisher-Abstract/Metadaten: Widerstands-/Inverterunsicherheit; keine Übernahme nicht gelesener Detailgleichungen |
| Kullick, J.; Hackl, C. M. (2023), IEEE TIE 70(1), 211–221, DOI 10.1109/TIE.2022.3153811 | Journalversion priorisiert, Autoreninstitution bestätigt DOI; Induktionsmaschinen-Kontext |
| Hackl, C. M.; Kullick, J.; Monzen, N. (2021), ICIT, 1348–1355, DOI 10.1109/ICIT46573.2021.9453497 | Publizierte Version identifiziert; synchronmaschinenbezogener Kontext, Volltextzugriff begrenzt |
| De Belie, F. M. L. L. et al. (2005), *A Nonlinear Discrete-Time Model for Saturated Surface Permanent-Magnet Synchronous Machines*, ACOMEN | [Institutioneller Volltext](https://epes.ugent.be/publications/fulltexts/2005002.pdf): §2.2 trennt Co-Energy der Magnetik und separat modellierte Verluste; die qd-Konvention wird nicht ungeprüft übertragen |
| Melkebeek, J. A. A.; Willems, J. L. (1990), *Reciprocity relations for the mutual inductances between orthogonal axis windings in saturated salient-pole machines*, DOI 10.1109/28.52681 | Primärreferenz in Jebai nachvollzogen; Publisher-Volltext hier nicht zugänglich. Keine sekundär gelesene Detailaussage als geprüfter Primärbefund verwendet |

Der publizierte Journalpfad und die einschlägige synchrone Konferenzarbeit
werden getrennt vom früheren Kullick/Hackl-Preprint geführt. Die tatsächlich
benötigten physikalischen Schlussfolgerungen stützen sich auf zugängliche
Primär-/Standardquellen und die expliziten unabhängigen Herleitungen oben.

## 15. Reproduktion, Dateien und ausgeführte Prüfungen

Aus dem Repository-Root, mit NumPy, pandas, SciPy, h5py und Matplotlib:

```powershell
$env:MPLBACKEND='Agg'
python papers/physics_constrained_flux_maps/python/coenergy_path_test.py
python papers/physics_constrained_flux_maps/python/audit_coenergy.py
python papers/physics_constrained_flux_maps/python/audit_observables.py
python papers/physics_constrained_flux_maps/python/audit_symbolic.py
python scripts/check_architecture.py
git diff --check
```

`audit_symbolic.py` benötigt zusätzlich SymPy. In dieser Sitzung lief es mit
dem gebündelten Python/SymPy 1.14.0; die experimentellen Läufe verwendeten
Python 3.13.12, NumPy 2.4.4, SciPy 1.17.1, pandas 3.0.6, h5py 3.16.0 und
Matplotlib 3.11.2. Fehlende Plot-Abhängigkeiten lagen sitzungsbezogen im
ignorierten `tmp/diagnostics_dependencies` und wurden per PYTHONPATH eingebunden;
dieser Pfad ist keine dauerhafte Repository-Abhängigkeit.

Alle drei Audit-Skripte liefen erfolgreich. Die Assertions prüfen unabhängig
Vorzeichen, Faktor 2, alle Pfadorientierungen, Green-Konsistenz, beliebige
Widerstandsverschiebungen sowie analytische und numerische Injektionsergebnisse.
Der erste Audit-Probelauf hatte einen Listen-/NumPy-Typfehler in einer neuen
Assertion (`abs(list)`); dieser wurde zu `np.abs` korrigiert und der komplette
Audit danach erfolgreich wiederholt. Ursprüngliche Berechnungen und Daten wurden
dabei nicht geändert. Die erfolgreichen Ergebnisse umfassen alle fünf realen Slices.

Ergebnisdateien unter `docs/audit_data/`:

- `audit_results.json`: volle Präzision, Softwareversionen, ursprüngliche
  Quell-/Input-SHA-256, Slice-Ergebnisse und synthetische Tests.
- `observable_checks.json`: alle Quadranten-/Invarianzprüfungen, High-/Full-Parity,
  beobachtbare RMS-Verhältnisse und zusätzliche geometrische Sensitivität.
- `symbolic_checks.json`: unabhängig geprüfte exakte Identitäten.
- `*_paths.csv`: alle unverändert gültigen realen Rechtecke, Originalquadratur
  und exakte P1-Pfadintegrale; keine Residualauswahl nach Ergebnis.
- `outlier60_triangle_curl.csv`: sämtliche Dreiecke, Curl, Kreuzinduktivitäten,
  Fläche, Kondition und Umkreisradius.
- `outlier60_local_regression.csv`: alle 4154 Punkte und drei Nachbarschaftsskalen.
- `local_vs_area.csv`, `green_check.csv`, `quadrature_convergence.csv`:
  deterministischer lokaler/integraler Vergleich und numerische Kontrolle.
- `synthetic_*.csv`: analytische und interpolierte Schleifenwerte auf identischen Zielen.
- `outlier_signal_names.txt`: vollständige Signalnamen zur Nachvollziehbarkeit
  der Normierungs-/Messkanalprüfung.

Die SHA-256 der Eingaben sind weiterhin
`a44f89af86f059e2f6d93b557febea5f42bd0108816c8ee0a40bd03083be53cf` (Outlier)
und `086fe72012e19d5a04ea99fbda63b7f5f7b25d4a3c9806ea55507e1d6b8afc74`
(Multi-RPM). Mehrere Manifeste dokumentieren jeweils die für ihren Lauf
vorhandenen Quellen; später hinzugefügte Audit-Skripte werden vom jeweils
späteren Observable-/Symbolic-Manifest erfasst.

Dieser Auftrag verändert keine Paper-These und finalisiert kein Paper.
Die empfohlenen physikalischen Folgemessungen und die ausstehende Normierungsklärung
bleiben offene Forschungsschritte. Ein kleiner numerischer Rest oder ein schöner
Fit wäre kein Ersatz für diese Klärung.

Abschließende Repository-Prüfung: `scripts/check_architecture.py` und
`git diff --check` bestanden. Die SHA-Prüfung bestätigt unveränderte MAT-Daten,
unveränderte ursprüngliche Analysequellen und Übereinstimmung der Auditquellen
mit den jeweiligen Ergebnismanifesten. Es wurden keine TeX-Quellen geändert;
ein neuer Paper-/PDF-Abschluss ist nicht Bestandteil dieses Analyseauftrags.
