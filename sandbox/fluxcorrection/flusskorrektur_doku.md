# Forschungsnotiz: Physikalische Diagnose und mögliche Korrektur rekonstruierter Flusskennfelder

**Stand:** 09.10.2026 – theoretische Herleitungen und erste reproduzierbare Experimente mit realen PSM-Messdaten
**Status:** Laufende, hypothesengeleitete Untersuchung; weder ein eindeutiges physikalisches Fehlermodell noch eine validierte Korrekturmethode liegt vor
**Arbeitsweise:** Geometrische Intuition und eigene Herleitungen vor selbst implementierten Python-Experimenten. Numerische Konsistenz, Modellhypothesen und experimentelle Evidenz werden ausdrücklich getrennt.

## 1. Forschungsziel

**Aktuelle übergeordnete Leitfrage (präzisiert am 09.10.2026):** Wie lassen sich aus den verfügbaren Rohmessdaten elektrischer Maschinen physikalisch plausible Flusskennfelder rekonstruieren, systematische Mess-, Parameter- und Modellabweichungen diagnostizieren und gegebenenfalls korrigieren, ohne reale Verlust- und Nichtlinearitätseffekte zu unterdrücken?

Die ursprünglich folgende Drehmomentfrage ist ein wichtiger **Teilansatz**, nicht das alleinige Forschungsziel.

**Leitfrage:** Können wir aus der Abweichung zwischen berechnetem und unabhängig gemessenem Drehmoment Rückschlüsse auf Fehler der rekonstruierten Flusskennfelder $\psi_d(i_d,i_q)$ und $\psi_q(i_d,i_q)$ ziehen – und unter welchen Zusatzannahmen wäre eine Korrektur möglich?

Wir beginnen bewusst mit einer **dreiphasigen PSM**, stationären Betriebspunkten und dem rotorfesten $dq$-Koordinatensystem. Eine Erweiterung auf weitere Maschinenkonfigurationen, Verluste und Messunsicherheiten kommt erst später.

Der aktuelle Lernfortschritt soll **nicht** durch die Übernahme einer fertigen Korrekturlösung übersprungen werden.

## 2. Konventionen und Ausgangsgleichungen

Wir setzen

$$
\omega_e=p\omega_m,\qquad k=\frac32p,
$$

wobei $p$ die Polpaarzahl ist. Für das dreiphasige Modell gilt

$$
\begin{aligned}
u_d&=R_s i_d+\frac{d\psi_d}{dt}-\omega_e\psi_q,\\
u_q&=R_s i_q+\frac{d\psi_q}{dt}+\omega_e\psi_d,\\
M_{\mathrm{em}}&=k(\psi_d i_q-\psi_q i_d).
\end{aligned}
$$

**Wichtige Unterscheidung:** $d\psi/dt$ ist die *zeitliche* Flussänderung in der Spannungsgleichung. Dagegen ist z. B. $\partial\psi_d/\partial i_d$ eine differentielle Induktivität. Bei einem stationären Betriebspunkt mit konstantem $i_d$, $i_q$ und konstantem magnetischem Zustand verschwinden die zeitlichen Ableitungen der $dq$-Flussverkettungen.

Damit vereinfacht sich das System zu

$$
\begin{aligned}
u_d&=R_s i_d-\omega_e\psi_q,\\
u_q&=R_s i_q+\omega_e\psi_d.
\end{aligned}
$$

Für $\omega_e\neq0$ folgt die stationäre Rekonstruktion:

$$
\boxed{\psi_d=\frac{u_q-R_s i_q}{\omega_e}},\qquad
\boxed{\psi_q=\frac{R_s i_d-u_d}{\omega_e}}.
$$

Das sind aus Spannungs- und Strommessung **rekonstruierte** Flüsse, nicht automatisch die wahren magnetischen Flüsse.

## 3. Widerstandsfehler als erste konkrete Fehlerhypothese

Definitionen:

$$
\Delta R=R_{\mathrm{verwendet}}-R_{\mathrm{wahr}},\qquad
\Delta\boldsymbol\psi=\boldsymbol\psi_{\mathrm{berechnet}}-\boldsymbol\psi_{\mathrm{wahr}}.
$$

Bei ansonsten identischen stationären Messgrößen ergibt sich:

$$
\begin{aligned}
\Delta\psi_d&=-\frac{\Delta R}{\omega_e}i_q,\\
\Delta\psi_q&=+\frac{\Delta R}{\omega_e}i_d.
\end{aligned}
$$

**Geometrische Interpretation:** Ein konstanter Widerstandsfehler addiert zu den Flusskennflächen jeweils eine stromabhängig geneigte Ebene. Es handelt sich nicht um eine starre Rotation der gesamten Kennfläche. Bei positivem $i_q$, positiver elektrischer Drehzahl und überschätztem Widerstand wird der rekonstruierte $d$-Fluss kleiner.

Der resultierende elektromagnetische Drehmomentfehler ist – mit der Definition $\Delta M_R=M_{\mathrm{em,berechnet}}-M_{\mathrm{em,wahr}}$ –

$$
\boxed{
\Delta M_R=-\frac{k\Delta R}{\omega_e}\left(i_d^2+i_q^2\right)
}
$$

mit $I_{\mathrm{amp}}^2=i_d^2+i_q^2$.

**Bereits selbst erkannt:**

- Bei festem Betriebspunkt und konstantem $\Delta R$ skaliert der Fehler wie $1/\omega_e$. Bei doppelter positiver Drehzahl halbiert sich der Betrag des Fehlers.
- Bei festem $\omega_e$ ist $\Delta M_R$ über $I_{\mathrm{amp}}^2$ eine Gerade durch den Ursprung; über $I_{\mathrm{amp}}$ ist der Verlauf quadratisch.
- Die Niveaulinien desselben Widerstands-Drehmomentfehlers bilden im $(i_d,i_q)$-Raum Kreise um den Ursprung (sofern das Fehlerniveau für das gegebene Vorzeichen überhaupt erreichbar ist).
- Bei gleichem Strombetrag ist der modellierte Widerstandsfehler unabhängig vom Stromwinkel.
- Der Quotient $\Delta M_R/I_{\mathrm{amp}}^2$ sollte bei fester Drehzahl konstant sein, wird aber für sehr kleine Strombeträge numerisch empfindlich und ist bei $I_{\mathrm{amp}}=0$ undefiniert.

**Datenidee für später:** Zuerst $\Delta M$ über $I_{\mathrm{amp}}^2$ ansehen. Eine nur durch konstanten $\Delta R$ verursachte Abweichung wäre linear. Die Steigung wäre $-k\Delta R/\omega_e$; das ist zunächst ein *äquivalenter* Fehlerparameter und noch kein Nachweis eines physikalisch falsch angenommenen Statorwiderstands.

## 4. Wellenmoment, elektromagnetisches Moment und Verluste

Das gemessene Wellenmoment muss nicht mit dem elektromagnetischen Moment identisch sein. Relevante Anteile sind insbesondere:

- mechanische Verluste (z. B. Lagerreibung, Luftreibung),
- Eisenverluste (u. a. Hysterese und Wirbelströme),
- weitere Messketten-, Betriebszustands- und Modellfehler.

Für **positive Drehzahl**, stationären Betrieb und unsere gewählte Bilanzgrenze verwenden wir zunächst das *vereinfachte* Modell

$$
M_{\mathrm{Welle}}\approx M_{\mathrm{em}}-M_V.
$$

Damit ist der beobachtete Vergleichsfehler

$$
\Delta M_{\mathrm{obs}}
:=M_{\mathrm{em,berechnet}}-M_{\mathrm{Welle,mess}}
\approx \Delta M_R+M_V.
$$

Setzt man **versuchsweise** bei festem $\omega_e$ und festem Temperaturzustand $M_V\approx M_0$ (konstant), entsteht

$$
\boxed{\Delta M_{\mathrm{obs}}\approx
-\frac{k\Delta R}{\omega_e}I_{\mathrm{amp}}^2+M_0}.
$$

Dann ließen sich *unter dieser Annahme* Steigung und Achsenabschnitt einer Geraden als Widerstands-Äquivalent und Verlustmoment-Offset interpretieren. $M_0$ wäre zunächst ein **extrapolierter** Offset bei verschwindendem Statorstrom, nicht automatisch ein direkt gemessener Verlustwert.

**Wichtige Einschränkungen:**

- Mechanische Verluste lassen sich bei konstanter Drehzahl oft näherungsweise konstant setzen.
- Eisenverluste hängen auch von der magnetischen Feldverteilung ab; deshalb müssen sie bei konstantem $\omega_e$ **nicht** konstant sein.
- Auch bei $i_d=i_q=0$ kann eine rotierende PSM aufgrund ihres Permanentmagnetfeldes Eisenverluste besitzen.
- Eine systematische Abweichung von der Geraden zeigt zunächst eine Verletzung unseres einfachen Modells – **nicht eindeutig Sättigung oder Eisenverluste**.
- Für negative Drehzahl muss die Vorzeichenkonvention der Verlustmomente und die Bilanzgrenze neu geprüft werden; die positive-Drehzahl-Form darf nicht blind übertragen werden.
- Ein CAN-Moment ist nicht notwendigerweise ein unabhängiges Wellenmoment. Dessen Ursprung und Kalibrierung wären vor empirischen Schlussfolgerungen zu prüfen.

## 5. Stromrichtung, Flussbetrag und Symmetrie

Für eine idealisierte lineare PSM setzen wir

$$
\psi_d=\psi_{\mathrm{PM}}+L_d i_d,\qquad
\psi_q=L_q i_q.
$$

Damit folgt

$$
\|\boldsymbol\psi\|^2
=(\psi_{\mathrm{PM}}+L_d i_d)^2+(L_q i_q)^2.
$$

Geometrisch und physikalisch haben wir diskutiert:

- Negative $i_d$-Ströme können dem PM-Fluss entgegenwirken (Feldschwächung). Mehr Strombetrag bedeutet deshalb **nicht automatisch** größeren Flussbetrag oder höhere Eisenverluste.
- Die Darstellung allein über $i_d^2$ und $i_q^2$ erhält zwar unterschiedliche d-/q-Gewichtungen, **verliert aber die Vorzeicheninformation**. $i_d=+100\,\mathrm A$ und $i_d=-100\,\mathrm A$ würden gleich dargestellt, obwohl die Magnetisierung unterschiedlich sein kann.
- Daher zunächst den Vergleichsfehler als Fläche $\Delta M(i_d,i_q)$ betrachten, bevor man ihn auf quadratische Größen reduziert.
- Ein stromwinkelabhängiger Verlustanteil kann bei gleichem $I_{\mathrm{amp}}^2$ zu einer **systematischen Aufspaltung/Streuung** statt lediglich zu einer Krümmung einer einzelnen Linie führen.

Beim Wechsel $(i_d,+i_q)\leftrightarrow(i_d,-i_q)$ gilt **im idealisierten Modell**:

$$
\|\boldsymbol\psi(i_d,+i_q)\|^2
=\|\boldsymbol\psi(i_d,-i_q)\|^2
$$

und

$$
M_{\mathrm{em}}(i_d,+i_q)=-M_{\mathrm{em}}(i_d,-i_q).
$$

**Arbeitshypothese:** Wenn die Eisenverluste näherungsweise durch eine für $\pm i_q$ symmetrische Größe beschrieben werden können, sind auch die Verlustmomente an diesen Betriebspunkten ähnlich. Das ist **keine allgemein bewiesene Symmetrie realer Eisenverluste**.

Für denselben **positiven** Drehzahlsinn, betragsmäßig gleiche elektromagnetische Momente und denselben Verlustmomentwert $M_V$ folgt als idealisierter Vergleich

$$
\begin{aligned}
M_{\mathrm{mess},+}&=+M_{\mathrm{em}}-M_V,\\
M_{\mathrm{mess},-}&=-M_{\mathrm{em}}-M_V.
\end{aligned}
$$

Daraus:

$$
\boxed{M_{V}=-\frac{M_{\mathrm{mess},+}+M_{\mathrm{mess},-}}{2}},\qquad
\boxed{M_{\mathrm{em}}=\frac{M_{\mathrm{mess},+}-M_{\mathrm{mess},-}}{2}}.
$$

**Beobachtung:** Der Drehmomentfehler eines konstanten Widerstandsmismatchs ist bezüglich $i_q$ *gerade* (wegen $i_q^2$). Bei der Differenz zweier gespiegelter, aus den Flüssen berechneter Momente hebt sich daher dieser identische Fehleranteil auf; die Addition bewahrt ihn, mischt ihn aber mit gemeinsamen Verlustanteilen. Eine eindeutige experimentelle Trennung verlangt weitere Annahmen oder Messinformationen.

## 6. Allgemeiner Flussfehler: zentrale neue Herleitung

Wir lassen jetzt offen, **warum** das Flusskennfeld fehlerhaft ist. Für einen festen Strombetriebspunkt schreiben wir

$$
\psi_{d,\mathrm{calc}}=\psi_{d,\mathrm{true}}+\Delta\psi_d,\qquad
\psi_{q,\mathrm{calc}}=\psi_{q,\mathrm{true}}+\Delta\psi_q.
$$

Da das Drehmoment bei **festgehaltenem** $i_d,i_q$ linear in $\psi_d,\psi_q$ ist, können wir das Differential direkt als exakte endliche Fehlerbeziehung verwenden:

$$
\begin{aligned}
\frac{\partial M}{\partial\psi_d}&=ki_q,\\
\frac{\partial M}{\partial\psi_q}&=-ki_d.
\end{aligned}
$$

Daraus:

$$
\boxed{\Delta M=k(i_q\Delta\psi_d-i_d\Delta\psi_q)}
$$

mit $\Delta M=M_{\mathrm{em,calc}}-M_{\mathrm{em,true}}$ (**hier** kein Wellenmoment und kein Verlustmoment in $\Delta M$).

Als Skalarprodukt:

$$
\frac{\Delta M}{k}=
\underbrace{\begin{bmatrix}i_q\\-i_d\end{bmatrix}}_{\mathbf a}^{\!T}
\underbrace{\begin{bmatrix}\Delta\psi_d\\\Delta\psi_q\end{bmatrix}}_{\Delta\boldsymbol\psi}.
$$

Wir haben erkannt, dass für den Stromvektor $\mathbf i=[i_d,i_q]^T$ gilt:

$$
\boxed{\mathbf a^T\mathbf i=i_qi_d-i_di_q=0.}
$$

**Geometrische Schlussfolgerung:** Der Drehmoment-Beobachtungsvektor $\mathbf a$ steht senkrecht auf dem Stromvektor $\mathbf i$. Ein Flussfehler **parallel zu $\mathbf i$** erzeugt deshalb bei diesem festen Betriebspunkt **keinen Drehmomentfehler**. Ein Drehmomentvergleich beobachtet nur eine bestimmte Projektion des Flussfehlervektors.

Dies ist die bisher wichtigste Erkenntnis: **Aus einem einzigen Drehmomentwert können die zwei Flussfehlerkomponenten an einem Betriebspunkt nicht eindeutig rekonstruiert werden.** Die drehmomentunsichtbare Stromrichtung gehört zum **Nullraum** der Abbildung. Für $\mathbf i=\mathbf0$ ist die gesamte Abbildung null – dann enthält das elektromagnetische Drehmoment überhaupt keine Information über den Fluss.

**Nicht verwechseln:** Die zunächst geäußerte Vermutung „orthogonaler Flussfehler = Winkelfehler“ wurde **nicht** als allgemeine Fehlerursache bestätigt. Die Orthogonalität kennzeichnet hier die geometrische Nichtbeobachtbarkeit einer Flussänderung; sie beweist keinen Sensorwinkelfehler.

## 7. Gesicherter Stand, Modellannahmen und offene Punkte

### Mathematisch hergeleitet (innerhalb des festgelegten Modells)

1. Stationäre Flussrekonstruktion aus $u_d,u_q,i_d,i_q,R_s,\omega_e$ bei $\omega_e\neq0$.
2. Widerstandsinduzierter Flussfehler und $\Delta M_R\propto-I_{\mathrm{amp}}^2/\omega_e$.
3. Konstanter Widerstandsfehler erzeugt winkelunabhängige Drehmomentfehler bei gleichem Strombetrag und gleicher Drehzahl.
4. Exakte lineare Drehmoment-Fehlerbeziehung $\Delta M=k(i_q\Delta\psi_d-i_d\Delta\psi_q)$ bei festen Strömen.
5. Nullraumrichtung parallel zum Stromvektor: Diese Flusskorrekturkomponente ist punktweise durch Drehmoment nicht beobachtbar.

### Noch unbestätigte physikalische Vereinfachungen

- Magnetisches Verhalten als ideale PSM, teils mit konstanten $L_d,L_q$.
- Eisenverluste näherungsweise von symmetrischen Flussbetragsgrößen abhängig.
- Verlustmoment $M_V$ bei fester Drehzahl und Temperatur näherungsweise konstant oder wenigstens symmetrisch bei $\pm i_q$.
- Verwendetes Drehmomentsignal stellt tatsächlich ein geeignetes, unabhängig gemessenes Moment dar.
- Strom-, Fluss-, Drehmoment- und Drehzahlkonventionen sind konsistent; Messwerte repräsentieren dieselben stationären Betriebspunkte.

### Frühere offene Forschungsfrage – inzwischen bearbeitet

> **Frage beim ersten Zwischenstand:** Reichen die Drehmomente vieler Betriebspunkte aus, um die beiden Flussfehlerkomponenten eindeutig zu bestimmen, oder bleibt die Mehrdeutigkeit erhalten?

**Zwischenzeitliches Ergebnis:** Die Mehrdeutigkeit bleibt auch für das gesamte Kennfeld bestehen. Die anschließende Untersuchung von Coenergy, Leistungsbilanz und Mehrdrehzahlmessungen ist ab Abschnitt 9 dokumentiert.

## 8. Geplanter weiterer Arbeitsmodus

1. **Geometrische Intuition**: Richtung, Projektion, Niveaumengen und Nullraum skizzieren.
2. **Eigene Herleitung**: Jede zusätzliche Annahme bewusst formulieren und ihre Folgen selbst mathematisch entwickeln.
3. **Minimaler Python-Versuch**: Erst nach Verständnis; Code wird selbst geschrieben und gemeinsam überprüft.
4. **Synthetische Daten**: An bekanntem Flussfehler prüfen, welche Anteile rekonstruierbar sind.
5. **Reale Messungen später**: Ein eigener qualifizierter Datensatz kann dann gezielt geplant/aufgenommen werden. Reale Verlust- und Messketteneffekte getrennt untersuchen.

**Arbeitsregel für die Betreuung:** Keine fertigen Optimierungsansätze oder vollständigen Implementierungen ohne ausdrückliche Nachfrage. Die bisherige Analyse ist ein **Forschungsstand**, kein Beweis, dass eine eindeutig physikalisch richtige Flusskorrektur bereits möglich wäre.

---

> **Fortsetzung nach dem ersten Zwischenstand:** Die Abschnitte 9–18 sind eine chronologische, fachlich geordnete Erweiterung. Sie unterscheiden weiterhin nachgewiesene Aussagen, bewusst vereinfachte Modelle und noch nicht beantwortete Fragen.
## 9. Warum ein gesamtes Drehmomentkennfeld den Fluss nicht eindeutig festlegt

Bei jedem von null verschiedenen Stromvektor gilt für eine additive Flusskorrektur

$$
\delta M=k(i_q\,\delta\psi_d-i_d\,\delta\psi_q).
$$

Um **zwei verschiedene Fehlerkonventionen** nicht zu vermischen, verwenden wir ab hier die Schreibweise

$$
\boxed{\delta\boldsymbol\psi
:=\boldsymbol\psi_{\mathrm{ziel}}-\boldsymbol\psi_{\mathrm{rec}}.}
$$

In den Abschnitten 3 und 6 bedeutete dagegen $\Delta\boldsymbol\psi=\boldsymbol\psi_{\mathrm{calc}}-\boldsymbol\psi_{\mathrm{true}}$. Beide Vorzeichenkonventionen sind zulässig, führen aber bei der Drehmomentdifferenz zu unterschiedlichen Vorzeichen. Hier wird fortan $\delta M=M_{\mathrm{ziel}}-M_{\mathrm{rec}}$ passend zur additiven Korrektur verwendet.

Für $N$ diskrete Betriebspunkte entstehen aus dem Drehmomentvergleich zunächst $N$ skalare Gleichungen für $2N$ Flusskorrekturkomponenten. An jedem Punkt beschreibt die Gleichung für einen vorgegebenen Drehmomentunterschied eine **Gerade** im $(\delta\psi_d,\delta\psi_q)$-Raum. Das gesamte Kennfeld ist dadurch allein nicht eindeutig festgelegt.

**Geometrischer Kern:** Der Vektor $(i_q,-i_d)^\mathsf T$ beobachtet nur den Anteil des Flussfehlers, der **senkrecht zum Stromvektor** liegt. Ein Zusatz $c\boldsymbol i$ ist drehmomentneutral, denn

$$
\delta M_{\mathrm{zusatz}}=k(i_q c i_d-i_d c i_q)=0.
$$

Bei $\boldsymbol i=\boldsymbol0$ verschwindet die Drehmomentinformation vollständig. Glattheit des Kennfeldes allein behebt die Mehrdeutigkeit nicht.

## 10. Was die Integrabilitätsbedingung bedeutet

### 10.1 Intuition: ein Flussfeld aus einer gemeinsamen Landschaft

Für ein idealisiertes, konservatives magnetisches System kann es eine skalare magnetische Coenergy $W'(i_d,i_q)$ geben, deren Steigungen in den beiden Stromrichtungen die Flussverkettungen liefern:

$$
\psi_d=\frac{\partial W'}{\partial i_d},\qquad
\psi_q=\frac{\partial W'}{\partial i_q}.
$$

Anschaulich sind $\psi_d$ und $\psi_q$ die beiden Komponenten des Gradienten einer einzigen „Potentiallandschaft“. Wenn diese Landschaft genügend glatt ist, dürfen wir die Reihenfolge der gemischten Ableitungen vertauschen:

$$
\boxed{\frac{\partial\psi_d}{\partial i_q}
=\frac{\partial\psi_q}{\partial i_d}.}
$$

Das ist die **Integrabilitäts- oder Reziprozitätsbedingung**. Sie ist lokal notwendig; auf einem einfach zusammenhängenden Gebiet und bei geeigneter Glattheit ist sie auch hinreichend für ein skalares Potential. Ein konservatives Feld liefert unabhängig vom gewählten Integrationsweg zwischen zwei Strompunkten dieselbe Coenergy-Differenz.

### 10.2 Die Bedingung betrifft das korrigierte Gesamtfeld

Wir suchen

$$
\boldsymbol\psi_{\mathrm{ziel}}
=\boldsymbol\psi_{\mathrm{rec}}+\delta\boldsymbol\psi.
$$

Wenn das **Zielfeld** integrabel sein soll, muss gelten:

$$
\frac{\partial(\psi_{d,\mathrm{rec}}+\delta\psi_d)}{\partial i_q}
=
\frac{\partial(\psi_{q,\mathrm{rec}}+\delta\psi_q)}{\partial i_d}.
$$

Umstellen ergibt die für eine möglicherweise **nichtintegrable Rekonstruktion** gültige Korrekturbedingung:

$$
\boxed{
\frac{\partial\delta\psi_d}{\partial i_q}
-\frac{\partial\delta\psi_q}{\partial i_d}
=
-\left(
\frac{\partial\psi_{d,\mathrm{rec}}}{\partial i_q}
-\frac{\partial\psi_{q,\mathrm{rec}}}{\partial i_d}
\right).}
$$

**Wichtige gemeinsame Präzisierung:** Wir dürfen die ursprünglichen Terme nur dann wegkürzen, wenn **auch das rekonstruierte Ausgangsfeld** bereits integrabel ist. Die physikalische Korrektheit des **gesuchten Zielfeldes** darf eine Modellanforderung sein; sie beweist aber nicht, dass die ursprüngliche Rekonstruktion diese Anforderung erfüllt.

Ein Feld kann zudem **integrabel und trotzdem physikalisch falsch** sein. Die Integrabilität allein liefert keine absolute Flusskalibrierung.

## 11. Mehrdeutigkeit trotz Drehmoment **und** Coenergy

### 11.1 Gegenbeispiel mit konstantem Faktor

Angenommen, wir haben bereits irgendein Zielfeld gefunden, das sowohl die Drehmomentgleichung als auch die Integrabilitätsbedingung erfüllt. Wir addieren einen weiteren Anteil

$$
\boldsymbol h=c\boldsymbol i,
\qquad h_d=c i_d,\quad h_q=c i_q,
$$

wobei $c$ eine Konstante mit der Einheit einer Induktivität ist.

- **Drehmoment:** $k(i_qh_d-i_dh_q)=0$.
- **Integrabilität:** $\partial h_d/\partial i_q=0$ und $\partial h_q/\partial i_d=0$; beide Seiten sind gleich.
- **Trotzdem anderes Flussfeld:** Für $c\neq0$ und $I>0$ ist $\boldsymbol h\neq0$.

Somit existieren unendlich viele Flussfelder, die beide Bedingungen erfüllen, **falls überhaupt eine passende Ausgangslösung existiert**. Dieses Gegenbeispiel **repariert** ein nichtintegrables Ausgangsfeld nicht; es zeigt, dass sich eine bereits gefundene gültige Lösung drehmoment- und integrabilitätserhaltend verändern lässt.

### 11.2 Ortsabhängiger radialer Faktor

Die Erweiterung lautete

$$
\boldsymbol h=c(i_d,i_q)\boldsymbol i.
$$

Der Drehmomentbeitrag bleibt **für jede** Funktion $c$ null. Aus der Integrabilitätsbedingung und der Produktregel folgt jedoch

$$
\frac{\partial(c i_d)}{\partial i_q}
=\frac{\partial(c i_q)}{\partial i_d}
\quad\Longleftrightarrow\quad
\boxed{i_d\frac{\partial c}{\partial i_q}
=i_q\frac{\partial c}{\partial i_d}.}
$$

Setzen wir $s=I^2=i_d^2+i_q^2$ und $c=f(s)$, so ergibt die Kettenregel

$$
\frac{\partial c}{\partial i_d}=2i_d f'(s),\qquad
\frac{\partial c}{\partial i_q}=2i_q f'(s).
$$

Beide Seiten der Bedingung werden dann zu $2i_di_qf'(s)$: Die Gleichheit gilt also für jede ausreichend glatte Funktion $f$. Die zunächst im Kopf vermuteten Singularitäten auf den Winkelhalbierenden waren ein Rechenversehen, keine physikalische oder mathematische Singularität.

### 11.3 Geometrische Interpretation und allgemeine Form

Umgestellt können wir schreiben

$$
\begin{bmatrix}-i_q&i_d\end{bmatrix}
\nabla_i c=0.
$$

Der erste Vektor ist die **Tangentialrichtung** an einen Kreis $i_d^2+i_q^2=I^2$. Die Gleichung besagt: Die Richtungsableitung von $c$ **entlang dieses Kreises ist null**. Der Faktor darf zwischen Kreisen variieren, nicht aber entlang eines zusammenhängenden Kreises.

In Polarkoordinaten ist das $\partial c/\partial\theta=0$. Auf einem vollen, rotationszusammenhängenden Stromgebiet gilt deshalb (für $I>0$)

$$
\boxed{\boldsymbol h=f(I^2)\boldsymbol i.}
$$

Die Form $f(I^2)$ ist eine **radiale Lösungsfamilie**; für die Darstellung und Glattheit direkt am Ursprung sind passende Regularitätsannahmen nötig. Der entscheidende Befund bleibt: Die Mehrdeutigkeit umfasst **eine ganze unbekannte radiale Funktion**, nicht nur eine Zahl $c$.

### 11.4 Bezug zu differentiellen Induktivitäten

Für konstantes $c$ verändert $\boldsymbol h=c\boldsymbol i$ zum Beispiel

$$
\delta L_{dd}
=\frac{\partial(c i_d)}{\partial i_d}=c.
$$

Daher können zwei torque- und coenergy-konsistente Felder **unterschiedliche differentielle Induktivitäten** besitzen. Eine bereits bekannte, richtige $L_{dd}$-Kennfläche als Hilfsbedingung anzunehmen, wäre hier zirkulär: Die differentiellen Induktivitäten sollen **aus dem korrigierten Flusskennfeld** berechnet werden.

## 12. Warum ein einzelner Fluss-Referenzpunkt die Radialfunktion nicht bestimmt

Für die ideale PSM gilt am Ursprung

$$
\psi_d(0,0)=\psi_{\mathrm{PM}},\qquad\psi_q(0,0)=0.
$$

Bei $\boldsymbol i=\boldsymbol0$ verschwindet aber der radiale Zusatz $f(I^2)\boldsymbol i$ für jeden **endlichen, regulären** Wert von $f(0)$. Diese physikalisch sinnvolle Referenzbedingung schränkt die drehmomentunsichtbare radiale Korrektur **am Ursprung nicht ein**.

An einem anderen Strompunkt, etwa bei $i_q=0$, $i_d=-100\,\mathrm A$, wäre

$$
 h_q=0,\qquad h_d=f(100^2)i_d.
$$

Eine unabhängige d-Flussreferenz könnte dort **einen** Wert $f(100^2)$ festlegen – aber nicht den Wert bei $I=200\,\mathrm A$ oder bei allen übrigen Radien. Nur unter einer zusätzlichen Annahme wie „$f$ ist überall konstant“ könnte eine einzelne geeignete Referenzmessung die ganze verbleibende **konstante** Zusatzmode bestimmen. Der d-Fluss am Punkt $i_q=0$ ist aus dem Drehmoment allein gerade **nicht** beobachtbar.

## 13. Messgrößen festhalten: Spannung, Widerstand und Flussänderungen

### 13.1 Forschungsentscheidung zu den Eingangsgrößen

Die gemessenen Strom-, Spannungs-, Drehzahl- und Drehmomentwerte sollen zunächst **feste Beobachtungen** sein; wir passen sie nicht beliebig an, um das Kennfeld „schön“ zu machen. Das bedeutet **nicht**, dass jede Beobachtung exakt die physikalische Wahrheit ist: Die Messkette ist später gesondert zu qualifizieren.

Der Statorwiderstand ist besonders unsicher, unter anderem durch Messverfahren und Temperatur. Eine Abweichung um einige mΩ kann bei kleinen Maschinenwiderständen bereits bedeutsam sein. Die Spannung verdient ebenfalls Aufmerksamkeit:

- Die tatsächlichen Maschinenklemmen-Spannungsgrundschwingungen sind nicht automatisch identisch mit vom Controller berechneten oder kommandierten $dq$-Spannungen.
- PWM-Abtastphase, Synchronisierung, Mittelung, Totzeit, Halbleiterspannungsabfälle und Modulation können Unterschiede verursachen.
- Eine Controller-Spannung ist **nicht generell größer** als die echte Klemmenspannung; Richtung und Betrag des Fehlers hängen von den Randbedingungen ab.
- Als erste Theorie betrachten wir eine ausgewählte Spannung als fest, bevor wir elektrische Fehlerquellen gemeinsam identifizieren.

### 13.2 Flussänderung bei unveränderter gemessener Spannung

Ändern wir den angenommenen Widerstand um $\delta R$, den berechneten Fluss um $\delta\boldsymbol\psi$ und halten $u_d,u_q,i_d,i_q,\omega_e$ fest, so folgt aus den stationären Spannungsgleichungen

$$
\begin{aligned}
0&=\delta R\,i_d-\omega_e\,\delta\psi_q,\\
0&=\delta R\,i_q+\omega_e\,\delta\psi_d.
\end{aligned}
$$

Für $\omega_e\neq0$ folgt

$$
\boxed{\delta\boldsymbol\psi
=\frac{\delta R}{\omega_e}
\begin{bmatrix}-i_q\\i_d\end{bmatrix}.}
$$

Der widerstandsbedingte Flussunterschied ist **orthogonal zum Stromvektor**. Er liegt somit in der Richtung, die das Drehmoment beobachtet; sein Drehmomentbeitrag ist

$$
\delta M=-\frac{k\,\delta R}{\omega_e}I^2.
$$

Die bereits besprochene **radiale** Zusatzkorrektur $\boldsymbol h=c\boldsymbol i$ ist davon zu unterscheiden: Sie ist drehmomentneutral, würde aber bei festem $R_s$ eine Spannung verändern.

### 13.3 Spannungsrichtungen vergleichen

Bei unverändertem Fluss verursacht eine Widerstandsänderung

$$
\delta\boldsymbol u_R=\delta R\begin{bmatrix}i_d\\i_q\end{bmatrix}.
$$

Bei festem Widerstand verursacht ein radialer Flusszusatz $c\boldsymbol i$

$$
\delta\boldsymbol u_{\mathrm{radial}}
=\omega_e c\begin{bmatrix}-i_q\\i_d\end{bmatrix}.
$$

Die beiden **speziell so definierten** Spannungsänderungsvektoren sind orthogonal. Bei $I>0$ und $\omega_e\neq0$ können sie sich nicht beide ungleich null zu null addieren. **Das widerspricht Abschnitt 13.2 nicht:** Dort war eine *orthogonale Flussänderung* erlaubt, die den Widerstandsbeitrag an den festen Spannungsmesswerten tatsächlich kompensieren kann. Orthogonalität der Spannungskomponenten gilt **nicht für beliebige Flussänderungen**.

**Wissenschaftliche Grenze:** Bei bekanntem $R_s$, idealer stationärer Spannungsgleichung und $\omega_e\neq0$ sind beide Flusskomponenten aus den Messwerten festgelegt. Ist $R_s$ unsicher, können unterschiedliche Kombinationen aus $R_s$ und dem senkrechten Flussanteil **dieselben gemessenen Spannungen** erklären.

## 14. Elektrische Leistungsbilanz und was der Torque-Ansatz wirklich hinzufügt

Multiplizieren wir $u_d=R_si_d-\omega_e\psi_q$ mit $i_d$, $u_q=R_si_q+\omega_e\psi_d$ mit $i_q$ und addieren, folgt

$$
 u_di_d+u_qi_q=R_s(i_d^2+i_q^2)+\omega_e(\psi_di_q-\psi_qi_d).
$$

Für die zunächst betrachtete **dreiphasige, amplitudeninvariante $dq$-Transformation** multiplizieren wir mit $3/2$. Wegen $\omega_e=p\omega_m$ und $M_{\mathrm{em}}=(3/2)p(\psi_di_q-\psi_qi_d)$ erhalten wir im **idealen stationären Modell ohne getrennte Eisenverlustbranche**

$$
\boxed{P_{\mathrm{el}}=P_{\mathrm{Cu}}+\omega_m M_{\mathrm{em}},}
$$

wobei

$$
P_{\mathrm{el}}=\frac32(u_di_d+u_qi_q),\qquad
P_{\mathrm{Cu}}=\frac32R_sI^2.
$$

Setzen wir die *aus genau denselben Spannungsdaten* rekonstruierten Flüsse in die Drehmomentgleichung ein, folgt bei $\omega_m\neq0$ lediglich

$$
\boxed{
M_{\mathrm{em,calc}}
=\frac{3}{2\omega_m}
\left[u_di_d+u_qi_q-R_sI^2\right].}
$$

**Erkenntnis:** Das aus $u,i,R_s,\omega$ berechnete „Drehmoment aus Fluss“ ist **keine zusätzliche unabhängige Messinformation**; es ist dieselbe elektrische Leistungsbilanz in anderer Form. Zusätzliche Information liefert erst ein **hinreichend unabhängiger** Drehmoment- oder Leistungsreferenzkanal.

### 14.1 Wellenmoment und weitere Verluste

Für eine vereinfachte stationäre **Gesamtleistungsbilanz** betrachten wir bei positiver Drehzahl

$$
\boxed{
P_{\mathrm{el}}
\approx\frac32R_sI^2+P_{\mathrm{Fe}}+P_{\mathrm{mech}}
+\omega_mM_{\mathrm{Welle}}.}
$$

Daraus dürfen wir **nicht ohne weitere Modellklärung** folgern, dass der aus den idealen $dq$-Gleichungen berechnete Momentwert bereits das wahre, eisenverlustbereinigte elektromagnetische Moment ist. Es kommt darauf an, ob das rekonstruierte Flussfeld die tatsächliche Magnetisierung oder eine effektive Klemmenfluss-Größe repräsentiert und wo die Eisenverluste im Ersatzmodell bilanziert werden. Die beiden Bilanzen sind Modellgleichungen mit **unterschiedlichen expliziten Verlustannahmen**, keine voneinander unabhängigen physikalischen Beweise.

Wellen- und elektromagnetisches Drehmoment sind wegen Eisen- und mechanischen Verlusten im Allgemeinen verschieden. Das gemessene Moment darf also nicht kommentarlos als $M_{\mathrm{em}}$ eingesetzt werden; bei umgekehrter Drehrichtung müssen Leistungs- und Verlustvorzeichen konsistent behandelt werden. Ebenso ist die Herkunft eines CAN-Moments auf eine tatsächlich unabhängige Drehmomentmessung zu prüfen.

## 15. Trennung von Kupferverlusten und übrigen Verlusten: Strombetrag und Richtung

Definieren wir für die obige angenäherte Gesamtbilanz

$$
Y:=P_{\mathrm{el}}-\omega_m M_{\mathrm{Welle}},\qquad I^2=i_d^2+i_q^2.
$$

Dann gilt unter den vereinfachten Modellannahmen

$$
Y\approx\frac32R_sI^2+P_{\mathrm{Fe}}+P_{\mathrm{mech}}.
$$

Wenn wir bei **konstanter Drehzahl, Temperatur und näherungsweise stromunabhängigen Verlusten** $P_{\mathrm{Fe}}+P_{\mathrm{mech}}=P_0$ setzen, entsteht die Gerade

$$
\boxed{Y\approx\underbrace{\frac32R_s}_{\text{Steigung}}I^2
+\underbrace{P_0}_{\text{Achsenabschnitt}}.}
$$

In diesem vereinfachten Fall wären Widerstand und Verlustoffset aus mehreren Strombeträgen identifizierbar. **Eine gemessene Gerade beweist jedoch nicht, dass ihre Steigung nur Kupferverluste enthält:** Falls der Eisenverlustanteil ebenfalls proportional zu $I^2$ ist, kann er die Steigung verfälschen.

### 15.1 Vergleich zweier Stromrichtungen bei gleichem Strombetrag

Für die Betriebspunkte $A=(-100\,\mathrm A,0)$ und $B=(0,100\,\mathrm A)$ gilt $I_A^2=I_B^2$. Ihre modellierten Kupferverluste sind gleich. Bei gleicher Drehzahl und gleichem Temperaturzustand dürfen wir die mechanischen Verluste **näherungsweise** ebenfalls gleich setzen.

Eine Differenz von $Y_A$ und $Y_B$ wäre dann im Modell auf unterschiedliche Eisenverluste beziehungsweise auf verletzte Modellannahmen/Messfehler zurückzuführen. **Den Widerstand isoliert dieser Vergleich nicht**, denn der Kupferterm fällt gerade heraus.

### 15.2 Unterschiedliche Strombeträge bei hypothetisch gleichem Verlustniveau

Für zwei Betriebspunkte mit gleichen Eisen- und mechanischen Verlusten, aber $I_A^2\neq I_B^2$, gilt dagegen

$$
\boxed{Y_A-Y_B=\frac32R_s(I_A^2-I_B^2).}
$$

Damit könnte man **unter der Gleichheitsannahme** $R_s$ berechnen. Das Hauptproblem ist nun, solche Betriebspunkte ohne zusätzliche unbekannte Größen zu finden.

## 16. Konstanter Flussbetrag als hypothetische Verlust-Niveaulinie – und der Zirkelschluss

Als grobe Arbeitshypothese verwendeten wir

$$
P_{\mathrm{Fe}}\approx F(\omega_e,\lVert\boldsymbol\psi\rVert).
$$

Das ist **kein allgemeines Eisenverlustgesetz**: Lokal verteilte Flussdichten, Oberwellen, Sättigung und Hysterese können selbst bei gleichem Betrag der $dq$-Flussverkettung zu unterschiedlichen Eisenverlusten führen.

Für die idealisierte lineare PSM mit konstanten Induktivitäten

$$
\psi_d=\psi_{\mathrm{PM}}+L_di_d,\qquad
\psi_q=L_qi_q
$$

liefert die Vorgabe eines konstanten Flussbetrags

$$
\boxed{(\psi_{\mathrm{PM}}+L_di_d)^2+L_q^2i_q^2
=\psi_{\mathrm{ref}}^2.}
$$

Das ist bei von null verschiedenen $L_d,L_q$ eine **Ellipse** im Stromraum, mit Mittelpunkt

$$
\boxed{(i_{d,M},i_{q,M})=
\left(-\frac{\psi_{\mathrm{PM}}}{L_d},0\right)}
$$

und Halbachsen $\psi_{\mathrm{ref}}/|L_d|$ und $\psi_{\mathrm{ref}}/|L_q|$. Auf derselben Flussellipse können verschiedene Strombeträge liegen. Wenn wir bei $i_q=0$, $\psi_d>0$ beginnen und $|i_q|$ erhöhen, muss $i_d$ zunächst weiter ins Negative gehen, um den Betrag konstant zu halten; die Änderung ist am Startpunkt erster Ordnung null und beginnt quadratisch.

**Geometrische Existenz ist nicht gleich praktische Messbarkeit:** Strom-, Spannungs-, Temperatur- und Entmagnetisierungsgrenzen müssen eingehalten werden. Ein Vorzeichenwechsel von $\psi_d$ ist für die Existenz unterschiedlicher Strombeträge auf einer zulässigen Teilkurve nicht erforderlich; er bedeutet auch nicht automatisch Prüfstandsinstabilität.

**Gemeinsam erkannter Zirkelschluss:** Um die Flussellipse und damit vermeintlich gleiche Eisenverluste auszuwählen, bräuchten wir $\boldsymbol\psi$. Den Fluss berechnen wir bisher aber aus $u,i,\omega_e$ und dem **gesuchten $R_s$**. Die Auswahl der Vergleichspunkte hängt somit bereits von der Unbekannten ab, die wir anhand dieser Punkte bestimmen wollen. Ein iteratives Verfahren wäre denkbar, aber **ohne unabhängige Zusatzinformation noch kein eindeutiger physikalischer Nachweis**.

## 17. Mehrdrehzahlansatz: den Widerstandsanteil durch Differenzen eliminieren

Um den Zirkelschluss zu umgehen, haben wir zwei **stationäre Messungen derselben Maschine am gleichen Strombetriebspunkt** bei verschiedenen elektrischen Winkelgeschwindigkeiten betrachtet:

$$
\begin{aligned}
u_{q,1}&=R_si_q+\omega_{e,1}\psi_d,\\
u_{q,2}&=R_si_q+\omega_{e,2}\psi_d.
\end{aligned}
$$

**Hier und nur hier nehmen wir zusätzlich an**, dass sich bei festem $(i_d,i_q)$ und gleicher Temperatur sowohl $R_s$ als auch der zugrunde liegende magnetische Fluss **zwischen den Drehzahlmessungen nicht ändern**. Drehzahlabhängige Verlust-, Dynamik-, Umrichter- und Erfassungseffekte bleiben zunächst außerhalb des Modells.

Subtraktion liefert für $\omega_{e,1}\neq\omega_{e,2}$:

$$
\boxed{
\psi_d=
\frac{u_{q,2}-u_{q,1}}{\omega_{e,2}-\omega_{e,1}}.}
$$

Der entsprechende d-Spannungsvergleich lautet

$$
\begin{aligned}
u_{d,1}&=R_si_d-\omega_{e,1}\psi_q,\\
u_{d,2}&=R_si_d-\omega_{e,2}\psi_q,
\end{aligned}
$$

also

$$
\boxed{
\psi_q=-\frac{u_{d,2}-u_{d,1}}{\omega_{e,2}-\omega_{e,1}}.}
$$

Im Grenzfall einer variierenden Drehzahl bei weiterhin festem Strom- und Temperaturzustand gilt unter denselben Annahmen

$$
\boxed{\left.\frac{\partial u_q}{\partial\omega_e}\right|_{i_d,i_q,T}=\psi_d,\qquad
\left.\frac{\partial u_d}{\partial\omega_e}\right|_{i_d,i_q,T}=-\psi_q.}
$$

**Geometrische Interpretation:** $u_q(\omega_e)$ ist eine Gerade mit Steigung $\psi_d$ und Achsenabschnitt $R_si_q$; $u_d(\omega_e)$ hat Steigung $-\psi_q$ und Achsenabschnitt $R_si_d$. Ein auf mehrere Drehzahlen verteilter Vergleich könnte die Flusskomponenten damit **ohne vorherige Kenntnis des Statorwiderstands** bestimmen und den Widerstand im vereinfachten Modell über die Achsenabschnitte zugänglich machen.

Anders als eine zusätzliche Drehmomentberechnung aus derselben Einzelmessung nutzt dieser Vergleich **zusätzliche Messzustände**. Seine Unabhängigkeit ist allerdings bedingt: Die für die Spannungsrekonstruktion tatsächlich verwendeten Grundschwingungen müssen zur Modellannahme passen. Bei gleichem Strom und gleicher Temperatur darf $\psi$ nicht unbemerkt drehzahlabhängig sein. Tatsächliche Messdaten müssen dieselbe Maschine und möglichst identische Strompunkte enthalten. Eine künstlich nur in Drehzahlkanälen modifizierte Datei wäre keine unabhängige Drehzahlmessung.

### 17.1 Physikalische und experimentelle Vorbehalte

- Für eine gültige Steigung braucht es unterschiedliche $\omega_e$ und identische, stationäre magnetische Zustände.
- Bei Geschwindigkeitsabhängigkeit von Fluss, Widerstand oder Spannungserfassung wäre die gemessene Steigung **nicht einfach** der gesuchte magnetische Fluss.
- Messrauschen, zeitliche Synchronisierung und PWM-Spannungsbestimmung beeinflussen besonders die numerische Steigung; größere Drehzahlabstände können helfen, ändern aber möglicherweise den Zustand.
- Der am Anfang der Untersuchung vorausgesetzte Faktor $k=3p/2$ gilt für unsere dreiphasige Konvention; andere Maschinen- oder Phasenkonfigurationen müssen entsprechend qualifiziert werden.

## 18. Aktueller Erkenntnisstand und konkrete Stelle zum Weiterarbeiten

### Mathematisch gezeigt (jeweils unter den erklärten Modellbedingungen)

1. Ein einzelner Drehmomentwert bestimmt nur **eine Projektion** des zweidimensionalen Flussvektors.
2. Auch ein gesamtes Drehmomentkennfeld zusammen mit einer Integrabilitätsforderung bestimmt den Fluss **nicht eindeutig**: Mindestens der radiale Zusatz $f(I^2)\boldsymbol i$ bleibt frei.
3. Der radial drehmomentneutrale Zusatz kann **differentielle Induktivitäten verändern**.
4. Ändern wir $R_s$ bei **fixierten Spannungs- und Stromwerten**, ist der dafür nötige Flussunterschied **senkrecht zum Strom** und beeinflusst das Drehmoment.
5. Ein aus denselben stationären Spannungsgrößen rekonstruierter Fluss mit anschließender Momentberechnung liefert keine neue unabhängige Gleichung; es ist die umgestellte **ideale elektrische Leistungsbilanz**.
6. Unter der expliziten Mehrdrehzahlannahme, dass Fluss und Widerstand beim Variieren von $\omega_e$ konstant bleiben, erscheinen $\psi_d$ und $-\psi_q$ als **Spannungssteigungen**.

### Hypothesen, die später gezielt geprüft werden müssten

- Gültigkeit der verwendeten stationären $dq$-Gleichungen mit den real verfügbaren Spannungs- und Stromkanälen.
- Unabhängigkeit und Bilanzgrenze des gemessenen Wellenmoments; Trennung von Eisen-, mechanischen und weiteren Verlusten.
- Stabiler thermischer Zustand; möglichst dieselben Strombetriebspunkte über mehrere **echte** Drehzahlen.
- In welchem Bereich eine einfache Beschreibung der Eisenverluste über den Betrag der Flussverkettung akzeptabel ist.
- Ob Spannung, Strom, Winkelreferenz und Abtastzeitpunkte übereinstimmen; Controller-Spannungen sind allenfalls ein gesondert zu qualifizierender Vergleichskanal.
- Keiner der bislang diskutierten Ansätze ist bereits als eindeutige Korrektur **realer** Flusskennfelder validiert.

### Historischer Einstiegspunkt vom 08.10.2026 (heute durch Abschnitt 26 überholt)

Wir standen zuletzt bei der Geradendarstellung

$$
u_q(\omega_e)=\underbrace{\psi_d}_{m_q}\,\omega_e
+\underbrace{R_si_q}_{b_q},
\qquad
u_d(\omega_e)=\underbrace{-\psi_q}_{m_d}\,\omega_e
+\underbrace{R_si_d}_{b_d}.
$$

**Offene Übungsfrage:** Wie lässt sich $R_s$ aus einem oder beiden Achsenabschnitten bestimmen? Welche Stromkomponente muss dafür ungleich null sein, und was passiert beispielsweise bei $i_q=0$? Die Antwort soll wieder **selbst hergeleitet** werden.

Danach erst entscheiden, ob eine formale Identifizierbarkeitsanalyse oder ein minimales **selbst programmiertes** Experiment mit synthetischen Messdaten sinnvoll ist.

---

*Dokumentationshistorie: Abschnitte 1–8 erfassen den ersten Zwischenstand vom 08.10.2026, Abschnitte 9–18 die daran anschließende Theorieentwicklung. Die Abschnitte 19–26 ersetzen die früheren unstrukturierten Quick Notes durch eine fachlich geordnete Erweiterung bis zum 09.10.2026. Alte Lernfragen sind als historische Zwischenstände zu lesen, nicht als aktueller Arbeitsauftrag.*

---

## 19. Präzisiertes Forschungsziel und Trennung der Informationsebenen

### 19.1 Was untersuchen wir tatsächlich?

Das übergeordnete Problem ist **nicht die Bestimmung eines einzelnen Statorwiderstands**, sondern die Frage, wie zuverlässig die üblichen Mess- und Rekonstruktionsverfahren das magnetische Verhalten einer elektrischen Maschine wiedergeben. Ausgangspunkt sind unter anderem auffällig verkippte Flusskennflächen, Symmetrieverletzungen und Abweichungen zwischen Fluss-, Drehmoment- und Verlustbetrachtungen.

Mindestens vier Ursachenklassen sind ausdrücklich auseinanderzuhalten:

1. **Reale Physik:** magnetische Sättigung und Kreuzsättigung, Hysterese, Eisenverluste, gegebenenfalls Zustands- und Frequenzabhängigkeiten.
2. **Messkette:** Spannungs- und Stromsensorik, Rotorlage beziehungsweise Winkeloffset, Synchronisierung, Abtastung, PWM-/Umrichtereffekte.
3. **Modell- und Parameterfehler:** etwa ein unzutreffender oder temperaturabhängiger Statorwiderstand, ungeeignete stationäre Gleichungen oder unvollständige Verlustzweige.
4. **Numerische Artefakte:** Interpolation, Glättung, Funktionsansatz, schlecht konditionierte Ableitungen, Randeffekte und Extrapolation.

**Leitprinzip:** Nicht jede Abweichung ist ein Fehler. Eine mathematische Korrektur ist nur dann wünschenswert, wenn wir wissen, welche Information sie erhält beziehungsweise entfernt. Die mögliche Ursache muss aus voneinander unterscheidbaren Beobachtungen und begründeten Zusatzannahmen abgeleitet werden.

### 19.2 Drei fachliche Ebenen

**Ebene A – Beobachtungen:** gemessene beziehungsweise bereitgestellte Spannungen, Ströme, Drehzahlen, Temperaturinformationen und Drehmomentkanäle, jeweils mit Herkunft und Messkonvention.

**Ebene B – Rekonstruiertes effektives Flussfeld:** `ψd_rec(id,iq)`, `ψq_rec(id,iq)` aus den gewählten stationären Spannungsgleichungen und dem eingesetzten `Rs`. Dieses Feld enthält im Allgemeinen bereits Einflüsse des Ersatzmodells und möglicher Fehler.

**Ebene C – Physikalisches Modell und Diagnose:** ein möglicher konservativer magnetischer Anteil aus einer Koenergie sowie verbleibende, separat auszuwertende Abweichungen. Die konzeptionelle Zerlegung

\[
\boldsymbol\psi_{\mathrm{rec}}=\nabla_{\boldsymbol i}W' + \boldsymbol r
\]

ist **keine experimentell bewiesene oder eindeutige Zerlegung in Magnetisierung und Eisenverluste**. Im Residuum können ebenso Sensor-, Widerstands-, Winkel-, Spannungs- und Approximationsfehler enthalten sein.

Daher bleiben Rohbeobachtungen, rekonstruierte Flussfelder, unabhängige glatte Fits, mögliche Koenergieprojektionen und deren Residuen als getrennte Datensichten verfügbar. Weder Symmetrisierung noch Coenergy-Projektion darf die Ausgangsinformation stillschweigend überschreiben.

### 19.3 Was unsere Prüfungen aussagen dürfen

- **Integrabilität/Reziprozität** prüft, ob ein hinreichend glattes Feld lokal als Gradient eines gemeinsamen Skalarpotentials darstellbar ist; sie bestimmt weder Flussoffsets noch eine eindeutige Ursache eines Residuums.
- **Maschinensymmetrie** prüft zusätzliche, **explizit angenommene** Rotor-/dq-Symmetrien; sie ist nicht für jede Maschine und jeden Verlustmechanismus automatisch gültig.
- **Drehmoment und Leistungsbilanz** liefern je nach Herkunft der Referenz mehr oder weniger unabhängige Information. Aus denselben `u`-, `i`- und `Rs`-Werten zurückgerechnetes Moment ist keine unabhängige Messung (vgl. Abschnitt 14).
- **Mehrdrehzahlvergleiche** können zusätzliche Beobachtungen liefern, benötigen aber echte unterschiedliche Messzustände und überprüfte Annahmen gleicher Magnetisierung und Temperatur (vgl. Abschnitt 17).

Die Identifizierbarkeitsgrenze aus Abschnitten 9–12 bleibt bestehen: Ein drehmomentneutraler, integrabler radialer Zusatz \(\boldsymbol h=f(i_d^2+i_q^2)\boldsymbol i\) kann trotz Drehmoment- und Coenergy-Konsistenz unsichtbar bleiben.

## 20. Konservative Magnetisierung, Kreuzsättigung und Symmetrie

### 20.1 Konservative Referenz ist nicht gleich lineare Maschine

Für eine idealisierte konservative PSM führen wir ein ausreichend glattes, auf die amplitudeninvarianten dq-Größen normiertes Potential ein:

\[
\boldsymbol\psi_{\mathrm{mag}}=\nabla_{\boldsymbol i}W'(i_d,i_q),
\qquad
\mathbf L_{\mathrm{diff}}=\frac{\partial\boldsymbol\psi}{\partial\boldsymbol i}
=\nabla_{\boldsymbol i}^{2}W'.
\]

Hierbei gilt die Reziprozität:

\[
L_{dq}:=\frac{\partial\psi_d}{\partial i_q}
=\frac{\partial\psi_q}{\partial i_d}=:L_{qd}.
\]

Die **gesamte dreiphasige** magnetische Koenergie benötigt bei amplitudeninvarianter dq-Transformation zusätzlich den Faktor \(3/2\); das hier verwendete `W'` ist ein entsprechend **normiertes mathematisches Potential**.

Eine lineare entkoppelte PSM ist nur das einfachste Rechenbeispiel:

\[
W'_0=\psi_{\mathrm{PM}}i_d+\tfrac12 L_di_d^2+\tfrac12 L_qi_q^2,
\quad
\psi_d=\psi_{\mathrm{PM}}+L_di_d,\quad \psi_q=L_qi_q.
\]

Kreuzkopplung ist nicht per se ein Fehler und nicht auf nichtintegrable Modelle beschränkt. Auch lineare Modelle mit konstanten Kreuzkoeffizienten sind möglich, **sofern** die für die Koenergie nötige Symmetrie `Ldq=Lqd` gilt.

### 20.2 Zusätzliche Rotorsymmetrie ist eine eigene Annahme

Für eine bezüglich der d-Achse spiegelsymmetrische PSM bei korrekt ausgerichtetem dq-System ist beispielsweise zu erwarten:

\[
\psi_d(i_d,-i_q)=\psi_d(i_d,i_q),
\qquad
\psi_q(i_d,-i_q)=-\psi_q(i_d,i_q).
\]

Eine **konstante** von null verschiedene Kreuzinduktivität würde diese konkrete Symmetrie verletzen; **nichtlineare Kreuzsättigung** muss sie nicht verletzen.

Ein bewusst konstruiertes, integrables Beispiel:

\[
W'=W'_0+\tfrac{\gamma}{2}i_di_q^2
\quad\Longrightarrow\quad
\begin{cases}
\psi_d=\psi_{\mathrm{PM}}+L_di_d+\tfrac{\gamma}{2}i_q^2,\\
\psi_q=L_qi_q+\gamma i_di_q.
\end{cases}
\]

Daraus folgen `Ldd=Ld`, `Lqq=Lq+γ id` sowie `Ldq=Lqd=γ iq`. Dieser Term wurde **zur Illustration konstruiert**, nicht aus Rohmessungen oder einem allgemein gültigen Sättigungsgesetz abgeleitet.

Mit einer weiteren möglichen Kopplung \(\Delta W'_2=\tfrac{\beta}{2}i_d^2i_q^2\) erhalten wir:

\[
L_{dd}=L_d+\beta i_q^2,\qquad
L_{qq}=L_q+\gamma i_d+\beta i_d^2,\qquad
L_{dq}=L_{qd}=\gamma i_q+2\beta i_di_q.
\]

Damit zeigt sich, dass zusätzliche Koenergieterme mehrere Induktivitätskomponenten zugleich beeinflussen. Ein dauerhaft konstantes `Ldd` auf der d-Achse ist eine **Beschränkung dieses gewählten Modellansatzes**, keine Aussage über die reale Maschine. Für flexible magnetische Modelle sind ausreichend glatte RBF- oder B-Spline-Funktionen langfristig plausibler als ein einzelnes hochgradiges globales Polynom.

### 20.3 Integrabilität übersieht konstante Flussoffsets

Für additive Konstanten \(\Delta\psi_d=c_d\), \(\Delta\psi_q=c_q\) gilt weiterhin `Ldq=Lqd`, weil die Ableitungen der Offsets null sind. Ein solches Feld besitzt den zusätzlichen Potentialterm

\[
\Delta W'=c_di_d+c_qi_q,
\]

obwohl es physikalisch falsch kalibriert sein kann. Seine Drehmomentabweichung ist dagegen

\[
\Delta M=\tfrac32p(c_di_q-c_qi_d).
\]

Integrabilität, Symmetrie, absolute Referenz und unabhängige Drehmomentinformation sind deshalb **komplementäre, nicht austauschbare Diagnosen**. Keine davon garantiert allein die wahre Flusskennfläche.

## 21. Vereinfachtes Eisenverlust-Ersatzmodell und seine geometrische Signatur

### 21.1 Warum eine Verlustleistung allein das Flussfeld nicht bestimmt

Ein materialspezifischer Bertotti-Ansatz beschreibt näherungsweise Anteile der Eisenverlustleistung, beispielsweise Hysterese-, Wirbelstrom- und Exzessverluste als Funktionen von Frequenz und **lokaler magnetischer Flussdichte**. Die örtliche Flussdichte `B(x,t)` ist nicht identisch mit einer dq-Flussverkettung. Ohne weitere Feld-, Geometrie- oder FEM-Informationen und ein passendes Ersatzmodell lässt sich aus einem skalaren `PFe` kein eindeutiger zweikomponentiger Flussfehler ableiten.

Zur **kontrollierten Modelluntersuchung** nutzen wir daher vorerst einen idealisierten, stationären dq-Eisenverlustzweig mit konstantem `RFe`, **nicht** ein validiertes Modell realer Maschinenverluste.

### 21.2 Magnetisierungsstrom und gemessener Statorstrom

Das bewusst vereinfachte Ersatzmodell unterscheidet:

\[
\boldsymbol i_s=\boldsymbol i_m+\boldsymbol i_{\mathrm{Fe}},\qquad
\boldsymbol i_{\mathrm{Fe}}=\frac{\boldsymbol e}{R_{\mathrm{Fe}}},\qquad
\boldsymbol e=\omega_e\begin{bmatrix}-\psi_q\\\psi_d\end{bmatrix}.
\]

Die konservative magnetische Koenergie wird in diesem Modell als Funktion von \(\boldsymbol i_m\) beschrieben; als Kennfeldkoordinaten der Messung erscheinen dagegen die Statorströme \(\boldsymbol i_s\).

Mit der linearen magnetischen Referenz \(\psi_d=\psi_{\mathrm{PM}}+L_di_{d,m}\), \(\psi_q=L_qi_{q,m}\) definieren wir

\[
a=\frac{\omega_eL_q}{R_{\mathrm{Fe}}},\quad
b=\frac{\omega_eL_d}{R_{\mathrm{Fe}}},\quad
c=\frac{\omega_e\psi_{\mathrm{PM}}}{R_{\mathrm{Fe}}}.
\]

Dann folgt die **affine Koordinatentransformation**

\[
\begin{bmatrix}i_{d,s}\\i_{q,s}\end{bmatrix}
=
\underbrace{\begin{bmatrix}1&-a\\b&1\end{bmatrix}}_{\mathbf A}
\begin{bmatrix}i_{d,m}\\i_{q,m}\end{bmatrix}
+\begin{bmatrix}0\\c\end{bmatrix},
\quad
\mathbf A^{-1}=\frac{1}{1+ab}
\begin{bmatrix}1&a\\-b&1\end{bmatrix}.
\]

Das ursprüngliche Stromgitter kann dadurch verschoben, geschert und anisotrop verformt werden. Diese Abbildung ist **nicht allgemein eine starre Rotation**.

### 21.3 Reziprozität in unterschiedlichen Stromkoordinaten

Für die magnetisierenden Ströme ist die Jacobi-Matrix im linearen Modell symmetrisch und diagonal:

\[
\mathbf J_{\psi,m}=
\begin{bmatrix}L_d&0\\0&L_q\end{bmatrix}.
\]

Bei Darstellung derselben magnetischen Flussverkettung als Funktion der **Statorströme** ergibt die Kettenregel:

\[
\mathbf J_{\psi,s}
=\mathbf J_{\psi,m}\mathbf A^{-1}
=\frac{1}{1+ab}
\begin{bmatrix}L_d&aL_d\\-bL_q&L_q\end{bmatrix}.
\]

Damit sind die Kreuzableitungen bei positiver Drehzahl und positiven Induktivitäten betragsgleich, aber entgegengesetzt:

\[
\frac{\partial\psi_d}{\partial i_{q,s}}
=\frac{aL_d}{1+ab},\qquad
\frac{\partial\psi_q}{\partial i_{d,s}}
=-\frac{bL_q}{1+ab},\qquad aL_d=bL_q.
\]

Das in dieser Notiz verwendete **Integrabilitätsresiduum** ist daher

\[
\boxed{
r_{\mathrm{int}}
:=\frac{\partial\psi_d}{\partial i_{q,s}}
-\frac{\partial\psi_q}{\partial i_{d,s}}
=\frac{2\omega_e L_dL_qR_{\mathrm{Fe}}}
{R_{\mathrm{Fe}}^2+\omega_e^2L_dL_q}
}.
\]

Achtung zur Konvention: Der gewöhnliche zweidimensionale `curl` eines Vektorfelds \((\psi_d,\psi_q)\) wird häufig mit dem **umgekehrten Vorzeichen** definiert.

Im linearen Modell mit konstanten Parametern ist `r_int` bei fester Geschwindigkeit im gesamten Strombereich konstant. Für unsere synthetischen Parameter lag es bei ungefähr \(5{,}02\cdot10^{-5}\,\mathrm H\). Die ursprüngliche Magnetisierungs-Koenergie bleibt dabei integrabel: Die Asymmetrie entsteht durch die Beschreibung über \(\boldsymbol i_s\) statt \(\boldsymbol i_m\).

### 21.4 Frequenzsymmetrie ist nicht Leistungssymmetrie

Unter unveränderten Modellparametern folgt:

\[
r_{\mathrm{int}}(-\omega_e)=-r_{\mathrm{int}}(\omega_e).
\]

Die im Widerstandszweig umgesetzte dreiphasige Leistung lautet hingegen

\[
P_{\mathrm{Fe}}=\tfrac32\frac{e_d^2+e_q^2}{R_{\mathrm{Fe}}}
=\tfrac32\frac{\omega_e^2}{R_{\mathrm{Fe}}}
(\psi_d^2+\psi_q^2)
\]

und ist bei unverändertem magnetischem Zustand und konstantem `RFe` eine **gerade** Funktion von \(\omega_e\). Eine Mittelung von Residuen bei positiver und negativer Drehzahl würde den *ungeraden Modellanteil* eliminieren – nicht die reale dissipierte Verlustleistung. Unsere hier betrachteten **realen Messungen liegen nur bei positiver Drehzahl**; ein Vorzeichenvergleich ist derzeit keine verfügbare experimentelle Prüfung.

**Grenze:** Ein nicht verschwindendes Reziprozitätsresiduum realer Messdaten ist noch **kein eindeutiger Eisenverlustnachweis**. Der Spezialfall demonstriert lediglich, dass ein dissipativer Zweig eine solche scheinbare Verletzung erzeugen *kann*. Die vorliegende Modellform kann auch reale Verlustcharakteristiken nicht vollständig abbilden.

## 22. Reale Messdaten: Auswahl, Qualität und Rekonstruktion (09.10.2026)

### 22.1 Dokumentierte Datenbasis

Das aktive Experiment liegt in `rkeller98/Research`, Branch `topic/fluxcorrection`, unter `sandbox/fluxcorrection/`:

- `flux_loss_experiment.py`: bekanntes synthetisches magnetisches Modell, einfacher Eisenverlustzweig, Koenergie, Stromabbildung und analytischer/numerischer Jacobi-Vergleich.
- `real_flux_analysis.py`: Einlesen aggregierter PSM-Betriebspunkte, stationäre Flussrekonstruktion, Split, getrennte RBF-Approximationen und Fitdiagnostik.
- `shared/python/raw_ww_data_importer.py`: signalbasierter Rohdatenimport aus MATLAB-v7.3-MAT.
- `shared/python/canonical_dataset.py`: `load_dataset(dataset_id)` zum Lesen der bereits gruppierten, validierten CSV-/JSON-Messdatensätze.
- `scripts/extract_research_datasets.py`: `operating_points(...)` zur deterministischen Gruppierung/Statistik aus den ursprünglichen MAT-Daten.

Für die erste Untersuchung verwenden wir `psm_temperature_2500` aus `datasets/`: dreiphasige PSM, Polpaarzahl `p=3`, nominell \(2500\,\mathrm{min}^{-1}\), Temperatur**referenzen** \(30^\circ\mathrm C\) und \(70^\circ\mathrm C\). Die ursprüngliche MAT-Datei `Flux/PSM_Measdata.mat` enthält 2040 Loggereinträge. Daraus wurden 680 aggregierte Betriebspunkte gebildet, **340 davon bei der 70-°C-Referenz**. Jeder Betriebspunkt besitzt in dieser Messung drei Loggerwerte; dies sind **nicht zwingend drei unabhängige physikalische Messungen**.

Die Geometrie der Betriebspunkte ist näherungsweise ein **Halbkreis in der linken \((i_d,i_q)\)-Halbebene**. Es liegt somit gerade **kein** volles rechteckiges Messgitter vor. Das Gebiet und seine Randbereiche müssen in späteren Auswertungen explizit berücksichtigt werden.

Die canonical Fixtures speichern unter anderem `id`, `iq`, `ud`, `uq`, `omega_e`, `rs_used`, `rotor_temp_ref`, `sample_count`, die Streuungsfelder wie `id_std` und `ud_std` sowie die bereits rekonstruierten `psi_d` und `psi_q`. Gemessene elektrische Geschwindigkeit und Temperaturreferenz dürfen nicht gedankenlos durch angeforderte Drehzahl oder als tatsächlich gemessene Rotortemperatur interpretiert werden.

### 22.2 Flussrekonstruktion aus aggregierten Beobachtungen

Für jeden stationären Betriebspunkt wurde unter den **idealen** stationären dq-Annahmen gerechnet:

\[
\psi_{d,\mathrm{rec}}
=\frac{u_q-R_si_q}{\omega_e},\qquad
\psi_{q,\mathrm{rec}}
=\frac{R_si_d-u_d}{\omega_e},\qquad\omega_e\ne0.
\]

In Python wurden die Quotienten aus den Betriebspunkt-Mittelwerten gebildet; das ist im Allgemeinen nicht identisch mit einer Mittelung beliebiger Quotienten einzelner Loggereinträge. Der gespeicherte `rs_used` ist der **in den Daten verwendete Parameter**, keine unabhängig bestätigte wahre Widerstandsmessung. Die daraus berechneten Flüsse sind zunächst **rekonstruierte effektive Flüsse**, keine unmittelbar gemessene magnetische Referenz.

Beobachtung beim direkten Scatterplot: \(\psi_d\) verändert sich überwiegend entlang \(i_d\), \(\psi_q\) überwiegend entlang \(i_q\); zusätzlich sind Kreuzabhängigkeiten erkennbar. Deren Ursache kann **noch nicht** eindeutig als physikalische Kreuzsättigung oder als Mess-/Modellartefakt klassifiziert werden.

## 23. Warum wir getrennte glatte Flussapproximationen benötigen

### 23.1 Irreguläre Messpunkte und Ableitungen

`np.gradient()` arbeitet entlang von **Array-Achsen** und kann bei passenden strukturierten Koordinaten auch ungleiche Abstände berücksichtigen. Für eine flache Liste unregelmäßig verteilter Strompunkte ist die Reihenfolge der Arrayelemente jedoch **keine räumliche Ableitungsrichtung**. Direktes `np.gradient(psi_d)` würde deshalb keine sinnvolle partielle Ableitung nach `id` oder `iq` liefern.

Triangulation mit stückweise linearen Flächen ist zwar möglich, bietet aber pro Dreieck nur konstante Gradienten und führt zu Sprüngen an Kanten. Messrauschen und schmale Dreiecke können Ableitungen deutlich verstärken. Lokale lineare Least-Squares-Regression über viele Nachbarpunkte unterdrückt Rauschen teilweise, löst aber **das einseitige Informationsdefizit am Rand nicht**. Die Moore-Penrose-Pseudoinverse oder `np.linalg.lstsq()` löst die numerische Regression; sie garantiert keine physikalisch korrekte Ableitung.

### 23.2 Globale Approximation, jedoch keine erfundene Randevidenz

Für unsere erste Kennfeldanalyse werden die beiden rekonstruierten Flussfelder **unabhängig** glatt approximiert:

\[
\hat\psi_d=f(i_d,i_q),\qquad \hat\psi_q=g(i_d,i_q).
\]

Dafür kommen beispielsweise regulierte RBFs oder geeignete B-Splines in Frage. Ein einzelnes globales hochgradiges Polynom ist nicht die bevorzugte Wahl. Eine nachträgliche Auswertung auf einem regelmäßigen Grid macht Visualisierung, Linienintegrale und numerische Ableitungen einfach; die analytischen Ableitungen des Funktionsansatzes wären bei entsprechender Implementierung oft noch vorteilhafter.

Eine globale Funktion kann zwar an jedem Randpunkt ausgewertet werden, **ersetzt aber nicht die fehlenden Messinformationen** außerhalb bzw. am Rand des ursprünglichen Halbscheiben-Supports. Evaluation und Integrationswege außerhalb des unterstützten Gebiets sind als Extrapolation zu markieren oder zu maskieren.

**Für die Integrabilitätsdiagnose dürfen wir nicht zuerst eine einzige Coenergy fitten.** Mit \(\hat{\boldsymbol\psi}=\nabla W'\) wäre \(\hat L_{dq}=\hat L_{qd}\) bereits per Konstruktion erzwungen, und wir könnten das zu untersuchende Signal nicht mehr unabhängig beobachten. Erst nach der Diagnose kann eine gesonderte Coenergy-Projektion mit gespeichertem Residuum sinnvoll sein.

### 23.3 Glattheitsanforderungen

Für \(\partial\psi_d/\partial i_q\) und \(\partial\psi_q/\partial i_d\) reicht zunächst \(\hat\psi_d,\hat\psi_q\in C^1\). Für weitere Ableitungen der Induktivitäten ist \(C^2\) eine sinnvolle stärkere Anforderung. Eine `C²`-glatte Funktion muss aber **weder geringe Ableitungsfehler noch physikalisch plausible Gradienten** besitzen. Zu starke Regularisierung unterdrückt echte Strukturen, zu schwache Regularisierung modelliert Rauschen. Numerische und physikalische Validierung sind zu trennen.

## 24. RBF-Experiment vom 09.10.2026: Normierung, Parameter und Ableitungen

### 24.1 Warum wir die Stromkoordinaten normieren

Der aktuelle `scipy.interpolate.RBFInterpolator` verwendet `kernel="inverse_multiquadric"`. Eine Basisfunktion kann geschrieben werden als

\[
\phi(r)=\frac{1}{\sqrt{1+(\varepsilon r)^2}},\qquad
r=\sqrt{(\Delta i_d)^2+(\Delta i_q)^2}.
\]

Ohne Koordinatennormierung hätte \(\varepsilon\) die Dimension \(\mathrm A^{-1}\). Bei Stromabständen von vielen Ampere machte die erste unnormierte Wahl \(\varepsilon=1\,\mathrm A^{-1}\) die RBFs sehr schmal. Die visuelle Flussapproximation war entsprechend unbefriedigend; auch `smoothing=3` war im damaligen Parametermaßstab ein ungünstiger Versuch.

**Entscheidung:** Wir skalieren beide Stromachsen mit demselben **ausschließlich aus den Trainingsdaten** ermittelten Referenzstrom,

\[
I_{\mathrm{ref}}
=\max_{k\in\mathrm{Train}}\sqrt{i_{d,k}^2+i_{q,k}^2},
\qquad
\tilde{\boldsymbol i}_k
=\frac1{I_{\mathrm{ref}}}\begin{bmatrix}i_{d,k}\\i_{q,k}\end{bmatrix}.
\]

Diese gemeinsame Skalierung erhält die relativen geometrischen Abstandsverhältnisse der beiden Stromachsen. Die Eingabematrix hat `N × 2`-Form: **jede Zeile ein Betriebspunkt, jede Spalte eine Koordinate**. `np.column_stack((id_train,iq_train))` kombiniert dafür zwei 1D-Arrays spaltenweise.

Nach der Normierung wird der RBF-Abstand \(\tilde r\) dimensionslos, ebenso \(\varepsilon\). **Alle späteren Test- oder Grid-Koordinaten müssen exakt dasselbe `Iref` benutzen**; erneutes Normieren pro Datenpartition würde das Modell inkonsistent auswerten. Die **Flusszielwerte selbst wurden im aktuellen Experiment nicht skaliert**.

### 24.2 Verwendete Einstellungen – experimentell, nicht optimal

Für beide Flusskennfelder wurde zuletzt unabhängig gewählt:

\[
\mathrm{kernel}=\texttt{inverse\_multiquadric},\qquad
\varepsilon=1,\qquad
\mathrm{smoothing}=0.01.
\]

Diese Parameter wurden zunächst pragmatisch über die sichtbare Fitqualität ausprobiert. Sie sind **noch nicht kreuzvalidiert und nicht als optimal nachgewiesen**. Der RBF-Formparameter \(\varepsilon\) bestimmt die räumliche Ausdehnung der Basisfunktionen; `smoothing` reguliert die Anpassung an die Messwerte. Die Wirkung beider Parameter ist im Kontext der Kernelmatrix, der Eingangsskalierung und des gewählten polynomialen Anteils zu verstehen; eine isolierte absolute Schwelle für `smoothing` ist nicht allgemein sinnvoll.

Wir verwenden **zwei unabhängige RBF-Modelle** und werten ihre Ausgaben zunächst an Trainings- und Testkoordinaten aus. Ein vollständiges räumliches Evaluationsgitter und die Ableitungen der **realen** RBF-Felder wurden noch **nicht** implementiert.

### 24.3 Kettenregel: Ableitungen nach physikalischem Strom

Die normierten Koordinaten seien \(\tilde i_d=i_d/I_{\mathrm{ref}}\), \(\tilde i_q=i_q/I_{\mathrm{ref}}\). Eine RBF-Ableitung nach den normierten Koordinaten ist **nicht** direkt eine differentielle Induktivität in Henry:

\[
\boxed{
\frac{\partial\hat\psi_d}{\partial i_q}
=\frac1{I_{\mathrm{ref}}}
\frac{\partial\hat\psi_d}{\partial\tilde i_q},\qquad
\frac{\partial\hat\psi_q}{\partial i_d}
=\frac1{I_{\mathrm{ref}}}
\frac{\partial\hat\psi_q}{\partial\tilde i_d}.
}
\]

Alle Einträge der Jacobi-Matrix brauchen bei dieser isotropen Skalierung genau den Faktor \(1/I_{\mathrm{ref}}\). Eine zusätzliche Ableitung einer Flusskomponente hätte den Faktor \(1/I_{\mathrm{ref}}^2\). Bei differenziell skalierten Achsen müssten stattdessen die **jeweiligen** Achsenskalierungen berücksichtigt werden.

## 25. Trainings-/Testaufteilung und quantitative Ergebnisse (09.10.2026)

### 25.1 Tatsächlich verwendeter Split

Für den ersten Versuch wurden die 340 aggregierten 70-°C-Betriebspunkte über einen zufällig permutierten **Indexvektor** aufgeteilt. Derselbe Index wurde konsistent auf `id`, `iq`, `psi_d` und `psi_q` angewandt; die Paarung der Messgrößen bleibt so erhalten.

\[
N_{\mathrm{Train}}=272\;(80\%),\qquad
N_{\mathrm{Test}}=68\;(20\%).
\]

Die dokumentierte Auswertung nutzte `np.random.default_rng(42)`; zwischenzeitlich wurde der Seed auch weggelassen, um das Verhalten bei wechselnden Aufteilungen explorativ zu betrachten. Ein **fester Seed sichert Reproduzierbarkeit, nicht prinzipiell höhere Qualität**.

Trainings- und Testkoordinaten werden beide mit dem **Trainings-`Iref`** transformiert. Die RBFs werden nur mit den Trainingspunkten gefittet. Die übrigen Punkte dienen zur Prüfung der Vorhersage – zunächst auf **ungesehenen Punkten derselben Messkampagne**, nicht auf einer unabhängigen Maschinenmessung.

### 25.2 RMSE, Standardabweichung und Normierung

Mit \(e_k=\hat\psi_k-\psi_k\) gilt

\[
\mathrm{RMSE}=\sqrt{\frac1N\sum_{k=1}^N e_k^2}
=\sqrt{\operatorname{Var}(e)+\bar e^{\,2}}.
\]

`np.std(e)` berechnet lediglich die **Streuung um den mittleren Fehler**. Bei einem konstanten systematischen Offset kann sie null sein, obwohl der RMSE ungleich null bleibt.

Um die unterschiedlichen Fluss-Amplituden vergleichbar einzuordnen, wurde **bereichsnormierter RMSE** verwendet:

\[
\mathrm{NRMSE}_{\mathrm{range}}[\%]
=100\frac{\mathrm{RMSE}}
{\max(\psi_{\mathrm{Train}})-\min(\psi_{\mathrm{Train}})}.
\]

Die beiden Bezugsbereiche werden **nur aus den Trainingszielwerten** bestimmt und für Training und Test gleich beibehalten. Ein RMSE ohne Normierung bleibt als physikalischer Flussfehler in Vs sehr wichtig; der NRMSE ist eine **zusätzliche relative Einordnung**, kein Ersatz.

### 25.3 Gemessene Ergebnisse des derzeitigen RBF-Experiments

Konfiguration: `inverse_multiquadric`, `epsilon=1`, `smoothing=0.01`, train-only normierte Stromkoordinaten, dokumentierter Seed 42.

| Ziel / Datensatz | RMSE [Vs] | RMSE [mVs] | NRMSE (Train-Range) [%] |
| --- | ---: | ---: | ---: |
| \(\psi_d\), Training | 0.0004757326 | 0.4757 | 0.8427 |
| \(\psi_q\), Training | 0.0006027503 | 0.6028 | 0.2883 |
| \(\psi_d\), Test | 0.0005744879 | 0.5745 | 1.0176 |
| \(\psi_q\), Test | 0.0005974741 | 0.5975 | 0.2858 |

**Beobachtungsstatus:** Die Fehler von Trainings- und zurückgehaltenen Punkten liegen in vergleichbarer Größenordnung. Bei wiederholt gewechselter Zufallsaufteilung erschien die Anpassung visuell und hinsichtlich des normierten Fehlers meist stabil. Dies sind vorläufige explorative Beobachtungen, **kein systematischer statistischer Stabilitätsnachweis**; insbesondere liegt der hier dokumentierte d-Test-NRMSE **leicht über 1 %**.

Der q-Fluss besitzt in diesem Datensatz einen deutlich größeren Wertebereich als der d-Fluss. Deshalb kann er trotz größerem **absolutem** RMSE einen kleineren **bereichsnormierten** RMSE aufweisen.

### 25.4 Was diese Ergebnisse nicht beweisen

- Der Fluss-RMSE ist kein Maß für die Genauigkeit der **Gradienten** oder des Differenzenresiduums `Ldq-Lqd`. Differenzieren kann insbesondere lokale Fit-Schwingungen stark verstärken.
- Durch wiederholtes Prüfen der Testpunkte und visuelle Parameteranpassungen wird der frühere Holdout **indirekt für die Modellwahl genutzt**. Ein späterer unabhängiger Abschlusstest benötigt daher eine **neu und vorab eingefrorene** Testbasis oder eine andere echte externe Messkampagne.
- Die beobachtete Streuung von drei Loggerwerten je Betriebspunkt ist nicht automatisch eine kalibrierte Messunsicherheit des rekonstruierten Flusses; Strom, Spannung, Geschwindigkeit, Widerstand und ihre Korrelationen beeinflussen dessen Unsicherheit.
- Unregelmäßige räumliche Punktabstände machen den randomisierten Holdout zu einem vor allem auf **Interpolation** gerichteten Test; er prüft weder Extrapolation noch die genaue Randableitung zuverlässig.
- Weder eine glatte RBF noch eine aus ihr gezeichnete Fläche beweist physikalische Integrabilität oder die Ursache einer Abweichung.

## 26. Ab hier fortsetzen: Arbeitsprotokoll und offene Untersuchungen

### 26.1 Unmittelbar nächster mathematischer/numerischer Schritt

Die beiden unabhängigen RBF-Modelle sind vorläufig ausreichend, um einen **ersten explorativen** Ableitungsvergleich zu beginnen. Der folgende Ablauf ist bewusst noch **kein validierter Korrekturalgorithmus**:

1. **Geometrie und Grid:** Stromachsen mit `np.linspace` erzeugen, `np.meshgrid` aufbauen, die `100×100`-Koordinaten in `N×2` Zeilen umformen, mit demselben Trainings-`Iref` normieren und die RBFs darauf auswerten. Maskieren bzw. kennzeichnen, welche Punkte tatsächlich vom gemessenen Halbscheiben-Gebiet gestützt werden.
2. **Gradienten:** Zunächst die Kettenregel aus Abschnitt 24.3 beachten. Analytische RBF-Ableitungen oder numerische Differenzen mit überprüfter Schrittweite verwenden; `np.gradient` auf einem genügend fein ausgewerteten, korrekt orientierten Grid höchstens als bewusst geprüften Näherungsweg.
3. **Jacobi- und Integrabilitätsdiagnose:** \(\mathbf J_\psi\) und \(r_{\mathrm{int}}=L_{dq}-L_{qd}\) über das **unterstützte Gebiet** bestimmen. Ränder, schwach unterstützte Regionen, Vorzeichen und die Einheit Henry eindeutig ausweisen.
4. **Numerische Stabilität:** RBF-Kernel, `epsilon`, Glättungsstärke, Gridauflösung und gegebenenfalls B-Spline-Vergleich variieren. Robustheit der **Ableitungen**, nicht nur Fluss-RMSE, prüfen. Bekannte synthetische Felder dienen als mathematische Kontrolle.
5. **Physikalische Diagnose:** Nichtintegrabilität und Symmetrieresiduen vor einer möglichen konservativen Coenergy-Projektion untersuchen. Eine solche Projektion und ihr Rest müssen separat erhalten bleiben.
6. **Identifizierbarkeit:** Drehzahl-, Temperatur- und Stromzustände, unabhängige Drehmoment-/Leistungsreferenzen, Widerstands- und Winkelhypothesen sowie alternative Verlustmodelle gegeneinander testen. Bei den verfügbaren realen Daten fehlen gegenwärtig negative Drehzahlen für einen direkten Odd/Even-Test.

### 26.2 Noch nicht erledigt

- Kein systematischer, leakage-freier Vergleich mehrerer Hyperparameterkonfigurationen mittels Kreuzvalidierung auf Entwicklungspunkten.
- Kein belastbarer Vergleich analytischer RBF-Ableitungen mit numerischen Grid-Ableitungen.
- Keine quantitative Unsicherheitsfortpflanzung von `u`, `i`, `Rs`, `ωe` auf \(\psi\) und \(\mathbf J_\psi\).
- Keine experimentell nachgewiesene Zuordnung eines realen `r_int` zu Eisenverlusten.
- Keine Bestimmung der tatsächlichen magnetischen Coenergy aus realen Messungen und keine physikalisch eindeutige Flusskorrektur.

Die Idee einer LHS-informierten Auswahl **tatsächlich gemessener** Holdout-Betriebspunkte ist als mögliches allgemeines MeasEval-Konzept im Issue [Weg-Weiser/GUI_VICE-MeasurementEvalKit#293](https://github.com/Weg-Weiser/GUI_VICE-MeasurementEvalKit/issues/293) dokumentiert. Sie ist hier **nicht** die Voraussetzung für den nächsten Lernschritt; der gegenwärtige Random Split reicht als erste numerische Übung.

### 26.3 Unverändert geltende Lern- und Forschungsregel

**Lehrmodus:** Fragen und kleine überprüfbare Herleitungen vor Komplettlösungen; Python wird primär selbst geschrieben. Nicht bereits implementierte oder validierte Ergebnisse werden nicht als nachgewiesen formuliert.

**Forschungsmodus:** Originaldaten und Modellannahmen nachvollziehbar erhalten, Ergebnisse nach **mathematisch bewiesen / modellabhängig / experimentell beobachtet / offen** unterscheiden und einen fit- oder koenergiebasierten Verlust von Information ausdrücklich vermeiden.

*Stand 09.10.2026: Reale PSM-Flüsse wurden rekonstruiert und getrennt über zwei normierte RBF-Modelle approximiert; Trainings- und Testfehler wurden bestimmt. Die eigentliche Integrabilitätsprüfung der realen Flussfelder und eine physikalisch belastbare Korrektur stehen noch aus.*
