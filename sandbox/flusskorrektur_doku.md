# Forschungsnotiz: Flusskorrektur mithilfe des Drehmoments

**Stand:** 08.10.2026, nach dem ersten Zwischenstand fortgeführt  
**Status:** Theoretische Voruntersuchung – keine abgeschlossene Korrekturmethode  
**Arbeitsweise:** Eigene mathematische Herleitungen und spätere Python-Experimente in einer leeren Sandbox; Lehrbücher und vorhandene Paper dienen als Referenzen, nicht als Lösungsvorlagen.

## 1. Forschungsziel

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

### Genau hier beim nächsten Gespräch wieder einsteigen

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

*Dokumentationshistorie: Abschnitte 1–8 erfassen den ersten Zwischenstand vom 08.10.2026; Abschnitte 9–18 erfassen die seitherige gemeinsame Theorieentwicklung. Bestehende Hypothesen sind ausdrücklich als solche markiert. Es wurde noch keine allgemein gültige oder experimentell validierte Flusskorrektur hergeleitet.*
