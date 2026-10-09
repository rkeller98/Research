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




# Quick Notes:

Du hast recht. Wir sind tatsächlich in die falsche Richtung abgebogen. Ich habe aus einer möglichen Fehlerursache – dem Statorwiderstand – zunehmend das eigentliche Forschungsziel gemacht.

Dabei ist die viel interessantere Frage, welche Informationen überhaupt in unseren Messdaten stecken, welche physikalisch sinnvoll sind und welche wir korrigieren dürfen, ohne andere Informationen zu zerstören.

## 1. Was wir eigentlich untersuchen

Wir haben eine Maschine, die wir bereits mit einem funktionierenden Mess- und Auswerteverfahren charakterisieren. Daraus erhalten wir unter anderem Flusskennfelder, Drehmomentkennfelder und Verlustinformationen.

Aber wir beobachten Effekte wie stark verkippte Flusskennflächen, Asymmetrien und Abweichungen zwischen verschiedenen physikalischen Modellen.

Dabei müssen wir mindestens vier Dinge auseinanderhalten:

- Physikalisches Verhalten: Sättigung, Kreuzsättigung, Hysterese und Eisenverluste.
- Messfehler: Strom- und Spannungssensoren, Winkeloffsets, Synchronisation und Umrichtereffekte.
- Parameterfehler: beispielsweise ein ungenauer oder temperaturbedingt veränderter Statorwiderstand.
- Numerische Artefakte: Interpolation, Glättung, Approximation und Extrapolation.

Nicht jede Auffälligkeit ist ein Fehler. Und nicht jede mathematisch mögliche Korrektur ist physikalisch sinnvoll.

## 2. Die entscheidende Unterscheidung beim Flusskennfeld

Wir sollten vermutlich drei Ebenen unterscheiden:

Messdaten

Spannung, Strom, Drehzahl, Temperatur, Drehmoment

Rekonstruierte effektive Flusskennfelder

Enthalten die Auswirkungen des verwendeten Ersatzmodells, der Verluste und möglicher Messfehler

Physikalische Modellierung und Diagnose

Konservativer Flussanteil

Kandidat aus einer magnetischen Coenergy; Grundlage für konsistente Induktivitäten

Verbleibende Abweichungen

Mögliche Verlustinformation, Messfehler und Modellfehler – zunächst nicht eindeutig getrennt

Das ist zunächst ein konzeptionelles Modell, noch keine nachgewiesene Zerlegung.

Dein Hinweis zu den Eisenverlusten ist besonders wichtig. Wenn wir ein rekonstruiertes Kennfeld gewaltsam symmetrisieren oder integrabel machen, könnten wir genau diejenigen Abweichungen beseitigen, die wir später zur Bestimmung der Eisenverluste benötigen.

Eine Verbesserung der mathematischen Konsistenz ist nicht automatisch eine Verbesserung der physikalischen Aussagekraft.

## 3. Warum unsere Beschäftigung mit Coenergy trotzdem richtig war

Für ein idealisiertes konservatives magnetisches System gilt:

$$ \boldsymbol\psi\_{\mathrm{mag}}=\nabla_i W'(i_d,i_q) $$

Damit folgt bei hinreichender Glattheit:

$$ \boxed{\frac{\partial\psi_d}{\partial i_q} =\frac{\partial\psi_q}{\partial i_d}} $$

Diese Bedingung ist eine mathematische Eigenschaft des konservativen Modells.

Wenn unser rekonstruiertes Kennfeld diese Eigenschaft verletzt, wissen wir zunächst nur, dass es sich unter den getroffenen Annahmen nicht vollständig durch eine einzige Coenergy-Funktion darstellen lässt.

Wir wissen noch nicht, ob die Ursache Eisenverluste, ein Widerstandsfehler, ein Winkelfehler oder etwas anderes ist. Und selbst ein integrables Feld kann physikalisch falsch sein.

Genau diese Einschränkung hatten wir in unserer Forschungsnotiz bereits herausgearbeitet.&#x20;

Eingefügtes Markdown.md

Eingefügtes Markdown.md



## 4. Wie ich die Forschungsfrage neu formulieren würde

> Wie können wir aus den verfügbaren Rohmessdaten einer elektrischen Maschine ein physikalisch konsistentes Modell rekonstruieren, systematische Mess- und Parameterfehler erkennen und gegebenenfalls korrigieren, ohne tatsächlich vorhandene Verlust- und Nichtlinearitätseffekte zu unterdrücken?

Damit sind Statorwiderstand, Drehmomentvergleich, Coenergy und Mehrdrehzahlmessungen keine voneinander unabhängigen Ziele, sondern unterschiedliche Werkzeuge zur Untersuchung derselben Fragestellung.

Ein ganz wichtiger Punkt: Wir sollten nicht voraussetzen, dass jede Abweichung vom Coenergy-Modell entfernt werden muss. Vielleicht ist sie gerade eine zusätzliche Beobachtungsgröße.

## 5. Wo ich jetzt wieder ansetzen würde

Ich würde zunächst zurück zu den auffällig verkippten Flusskennfeldern gehen.

Nicht mit der Frage, wie wir sie geradeziehen können, sondern:

Wie müsste ein physikalisch sinnvolles Flusskennfeld aussehen, welche Eigenschaften muss es erfüllen und welche Abweichungen können wir auf Basis unserer Messgrößen überhaupt unterscheiden?

Dabei würde ich zuerst an einem idealisierten, verlustfreien PSM-Modell beginnen, dann gezielt Widerstandsfehler, Winkelfehler und vereinfachte Verlusteffekte hinzufügen und jeweils untersuchen, was sich geometrisch an den Flusskennflächen verändert.

Wir könnten dadurch lernen, welche Fehlersignaturen unterscheidbar sind und an welchen Stellen eine Korrektur überhaupt identifizierbar ist.

Und wir bleiben bei unserer Arbeitsweise: Geometrie verstehen, mathematisch herleiten, Annahmen kritisch prüfen und erst danach mit Python experimentieren.

Ich denke, damit sind wir wieder deutlich näher an dem, was wir ursprünglich erforschen wollten.

Beim ersten Punkt gebe ich dir recht. Beim zweiten liegt allerdings ein kleiner Denkfehler vor, der für unsere spätere Fehlerdiagnose ziemlich wichtig ist.

## 1. Kreuzkopplung gehört selbstverständlich auch in ein ideales Modell

Unsere bisherige Definition von „ideal“ war eigentlich nur das einfachste lineare, entkoppelte Referenzmodell.

Wir können genauso gut ein lineares Modell mit konstanten Kreuzinduktivitäten annehmen:

$$ \begin{aligned} \psi_d &= \psi\_{\mathrm{PM}}+L_di_d+L\_{dq}i_q\\\ \psi_q &= L_qi_q+L\_{qd}i_d \end{aligned} $$

Wenn wir eine gemeinsame Coenergy voraussetzen, muss gelten:

$$ \boxed{L\_{dq}=L\_{qd}} $$

Und genau das haben wir gerade hergeleitet.

Eine zusätzliche Einschränkung ergibt sich erst, wenn wir eine bestimmte physikalische Rotorsymmetrie voraussetzen. Bei einer bezüglich der d-Achse spiegelsymmetrischen PSM im korrekt ausgerichteten dq-System gilt beispielsweise:

$$ \psi_d(i_d,-i_q)=\psi_d(i_d,i_q) $$

$$ \psi_q(i_d,-i_q)=-\psi_q(i_d,i_q) $$

Eine konstante Kreuzinduktivität ungleich null würde diese Symmetrie verletzen. Das bedeutet aber keineswegs, dass Kreuzsättigung ausgeschlossen ist.

Wir können beispielsweise eine nichtlineare Coenergy definieren:

$$ W'=\psi\_{\mathrm{PM}}i_d+ \frac12L_di_d^2+ \frac12L_qi_q^2+ \frac{\gamma}{2}i_di_q^2 $$

Daraus folgt:

$$ \begin{aligned} \psi_d&=\psi\_{\mathrm{PM}}+L_di_d+\frac{\gamma}{2}i_q^2\\\ \psi_q&=L_qi_q+\gamma i_di_q \end{aligned} $$

Und unsere Kreuzinduktivität ergibt sich zu:

$$ \boxed{ L\_{dq}=L\_{qd}=\gamma i_q } $$

Wir haben also nichtlineare Kreuzkopplung, Integrabilität und die genannte Maschinensymmetrie gleichzeitig.

Für unser Forschungsmodell würde ich deshalb zwischen Modellvereinfachungen und tatsächlichen physikalischen Einschränkungen unterscheiden.

## 2. Was passiert mit konstanten Flussfehlern?

Wir hatten:

$$ \begin{aligned} \psi_d&=\psi\_{\mathrm{PM}}+L_di_d+c_d\\\ \psi_q&=L_qi_q+c_q \end{aligned} $$

Du vermutest, dass \\(c_d=c_q\\) gelten muss.

Betrachten wir aber die Integrabilitätsbedingung:

$$ \frac{\partial\psi_d}{\partial i_q} = \frac{\partial\psi_q}{\partial i_d} $$

Links erhalten wir:

$$ \frac{\partial}{\partial i_q} (\psi\_{\mathrm{PM}}+L_di_d+c_d)=0 $$

Rechts:

$$ \frac{\partial}{\partial i_d} (L_qi_q+c_q)=0 $$

Damit gilt:

$$ \boxed{0=0} $$

Unabhängig davon, ob \\(c_d=c_q\\) ist oder nicht!

Das bedeutet: Unsere Integrabilitätsbedingung erkennt keine konstanten Flussoffsets.

Wir können für beliebige konstante \\(c_d,c_q\\) sogar eine zusätzliche Coenergy angeben:

$$ \boxed{\Delta W'=c_di_d+c_qi_q} $$

Ihre Ableitungen ergeben genau die beiden konstanten Flussabweichungen.

Das hat eine wichtige Konsequenz: Ein Kennfeld kann vollständig integrabel sein und trotzdem einen systematischen Offset enthalten.

Ein \\(c_q\neq0\\) wäre beispielsweise anhand der zuvor genannten Maschinensymmetrie auffällig, aber nicht anhand der Integrabilitätsbedingung.

## 3. Was wir gerade über unsere Fehlerdiagnose gelernt haben

Wir haben zwei sehr unterschiedliche Prüfungen kennengelernt:

| Eigenschaft            | Was können wir erkennen?                                                         |
| ---------------------- | -------------------------------------------------------------------------------- |
| Integrabilität         | Verletzungen der Reziprozität differentieller Induktivitäten                     |
| Maschinensymmetrie     | Abweichungen von einer vorausgesetzten geometrischen oder magnetischen Symmetrie |
| Absolute Flussreferenz | Bestimmte Offsets, die durch die beiden anderen Prüfungen unentdeckt bleiben     |

Das ist für unsere Idee eines idealen Referenzmodells plus analysierbaren Abweichungen ein wichtiger Baustein.

### Eine Frage würde ich gerne noch untersuchen

Angenommen, wir haben einen konstanten Fehler \\(c_d\\) oder \\(c_q\\). Die Integrabilitätsbedingung erkennt ihn nicht.

Was passiert aber, wenn wir mit diesem fehlerhaften Flusskennfeld das elektromagnetische Drehmoment berechnen?

$$ M=\frac32p(\psi_di_q-\psi_qi_d) $$

Würde ein konstanter Flussfehler auch beim Drehmomentvergleich unsichtbar bleiben, oder erzeugt er dort eine charakteristische Abweichung?

Damit könnten wir verschiedene physikalische Konsistenzprüfungen sinnvoll miteinander verbinden.

Der Schritt war tatsächlich zu groß. Ich habe dort einfach einen zusätzlichen Coenergy-Term eingeführt, ohne zu erklären, wie man überhaupt auf diesen Term kommt und warum er genau diese Form hat.

Wir leiten ihn jetzt her. Und deine Antwort zum Drehmoment stimmt ebenfalls – darauf kommen wir am Ende zurück.

## 1. Ausgangspunkt: Unser lineares Modell

Wir haben zunächst zwei Flusskennfelder angenommen:

$$ \begin{aligned} \psi_d &= \psi\_{\mathrm{PM}}+L_di_d\\\ \psi_q &= L_qi_q \end{aligned} $$

Wir wollen eine gemeinsame Coenergy-Funktion \\(W'(i_d,i_q)\\), deren partielle Ableitungen diese Flüsse ergeben:

$$ \psi_d=\frac{\partial W'}{\partial i_d}, \qquad \psi_q=\frac{\partial W'}{\partial i_q} $$

Dazu integrieren wir die erste Gleichung nach \\(i_d\\):

$$ W'=\psi\_{\mathrm{PM}}i_d+\frac12L_di_d^2+g(i_q) $$

Warum \\(g(i_q)\\)? Weil beim Ableiten nach \\(i_d\\) jede Funktion, die ausschließlich von \\(i_q\\) abhängt, verschwindet.

Jetzt verlangen wir zusätzlich:

$$ \frac{\partial W'}{\partial i_q}=L_qi_q $$

Also muss gelten:

$$ g(i_q)=\frac12L_qi_q^2+C $$

Wir wählen die irrelevante additive Konstante \\(C=0\\) und erhalten:

$$ \boxed{W'\_0=\psi\_{\mathrm{PM}}i_d+\frac12L_di_d^2+\frac12L_qi_q^2} $$

Bis hierhin haben wir nichts Neues angenommen. Wir haben nur unsere beiden linearen Flussgleichungen integriert.

## 2. Jetzt möchten wir Kreuzkopplung einführen

Bisher hängt \\(\psi_d\\) ausschließlich von \\(i_d\\) und \\(\psi_q\\) ausschließlich von \\(i_q\\) ab.

Wir wollen jetzt bewusst ein Modell konstruieren, bei dem beispielsweise auch \\(i_q\\) den d-Fluss beeinflusst.

Nehmen wir zusätzlich an, dass unsere Maschine bezüglich \\(i_q\\) spiegelsymmetrisch ist.

Dann darf sich \\(\psi_d\\) beim Vorzeichenwechsel von \\(i_q\\) nicht verändern.

Welche einfache Funktion erfüllt diese Bedingung?

$$ i_q^2 $$

Denn:

$$ (-i_q)^2=i_q^2 $$

Wir ergänzen daher versuchsweise:

$$ \boxed{\Delta\psi_d=\frac{\gamma}{2}i_q^2} $$

Dabei beschreibt \\(\gamma\\) die Stärke der zusätzlichen Kopplung. Der Faktor \\(1/2\\) ist lediglich eine praktische Wahl für die spätere Ableitung.

Schematisch: Eine quadratische Zusatzfunktion ist gerade symmetrisch bezüglich \\(i_q=0\\). Ein negatives \\(\gamma\\) würde die Parabel umdrehen.

Aber Achtung: Das ist eine bewusst gewählte Modellannahme, keine zwingende physikalische Gesetzmäßigkeit. Wir hätten auch \\(i_q^4\\) oder andere gerade Funktionen wählen können.

## 3. Was erzwingt jetzt die Integrabilitätsbedingung?

Wir haben den zusätzlichen d-Fluss festgelegt:

$$ \Delta\psi_d=\frac{\gamma}{2}i_q^2 $$

Die Integrabilitätsbedingung verlangt:

$$ \frac{\partial\psi_d}{\partial i_q} = \frac{\partial\psi_q}{\partial i_d} $$

Wir leiten unseren Zusatzterm nach \\(i_q\\) ab:

$$ \frac{\partial\Delta\psi_d}{\partial i_q} =\gamma i_q $$

Damit wissen wir, dass für den zugehörigen q-Flusszusatz gelten muss:

$$ \frac{\partial\Delta\psi_q}{\partial i_d} =\gamma i_q $$

Jetzt kommt der interessante Schritt:

Welche Funktion müssen wir nach \\(i_d\\) ableiten, damit \\(\gamma i_q\\) herauskommt?

Wir integrieren nach \\(i_d\\):

$$ \Delta\psi_q=\gamma i_di_q+h(i_q) $$

Den freien Anteil \\(h(i_q)\\) setzen wir für unser einfaches Kreuzkopplungsmodell auf null.

Damit erhalten wir:

$$ \boxed{\Delta\psi_q=\gamma i_di_q} $$

Die beiden zusätzlichen Flussanteile sind also nicht beliebig. Sobald wir einen festgelegt haben, schränkt die Integrabilitätsbedingung den anderen ein.

## 4. Woher stammt nun der Coenergy-Term?

Wir kennen unsere beiden zusätzlichen Flussanteile:

$$ \begin{aligned} \Delta\psi_d&=\frac{\gamma}{2}i_q^2\\\ \Delta\psi_q&=\gamma i_di_q \end{aligned} $$

Wir suchen eine Funktion \\(\Delta W'\\), deren Ableitungen genau diese beiden Ausdrücke liefern.

Dazu integrieren wir den ersten Ausdruck nach \\(i_d\\):

$$ \Delta W' =\int\frac{\gamma}{2}i_q^2\\,di_d $$

Da \\(i_q\\) bei dieser partiellen Integration konstant gehalten wird:

$$ \boxed{\Delta W'=\frac{\gamma}{2}i_di_q^2} $$

Eine zusätzliche Funktion nur von \\(i_q\\) lassen wir wieder weg.

Zur Kontrolle leiten wir nach \\(i_q\\) ab:

$$ \frac{\partial\Delta W'}{\partial i_q} =\gamma i_di_q $$

Das ist genau unser gewünschter q-Flusszusatz!

Daher stammt die Gleichung von vorhin:

$$ \boxed{ W'=W'\_0+\frac{\gamma}{2}i_di_q^2 } $$

Der wichtigste Punkt ist: Ich habe diesen Term nicht aus der tatsächlichen Maschine hergeleitet, sondern als einfaches, mit der angenommenen Symmetrie und Integrabilität verträgliches Modell konstruiert.

## 5. Und was passiert beim Drehmoment?

Auch deine zweite Aussage stimmt.

Nehmen wir an, die Flussverkettungen enthalten konstante Fehler \\(c_d\\) und \\(c_q\\).

Dann ergibt sich für den Drehmomentfehler:

$$ \boxed{ \Delta M=\frac32p(c_di_q-c_qi_d) } $$

Konstante Flussfehler werden von der Integrabilitätsbedingung nicht erkannt, können aber das berechnete Drehmoment verändern.

Allerdings kann der Drehmomentfehler an bestimmten Betriebspunkten auch null sein, obwohl beide Flussfehler vorhanden sind. Außerdem müssen wir bei einem Vergleich zum gemessenen Wellenmoment wieder die Verluste berücksichtigen.

Ich würde an dieser Stelle gerne noch bei der Kreuzkopplung bleiben, bevor wir weitere Fehlerquellen untersuchen.

Eine Verständnisfrage: Wir haben durch unseren zusätzlichen Coenergy-Term folgendes Flussmodell erhalten:

$$ \begin{aligned} \psi_d&=\psi\_{\mathrm{PM}}+L_di_d+\frac{\gamma}{2}i_q^2\\\ \psi_q&=L_qi_q+\gamma i_di_q \end{aligned} $$

Wenn wir daraus die differentielle Induktivität

$$ L\_{qq}=\frac{\partial\psi_q}{\partial i_q} $$

berechnen, was erhalten wir dann? Und was bedeutet das für die Abhängigkeit der q-Induktivität vom d-Strom?

Das ist die direkte Verbindung zwischen unserer Coenergy und den nichtlinearen Induktivitätskennfeldern, die wir später bestimmen möchten.


\\(L\_{dd}=L_d\\) ist richtig! Bei \\(L\_{qq}\\) fehlt dir noch der Faktor \\(i_d\\). Und bei den Kreuzinduktivitäten müssen wir etwas genauer unterscheiden.

Gehen wir die Ableitungen durch.

## 1. Unsere Flussgleichungen

$$ \begin{aligned} \psi_d&=\psi\_{\mathrm{PM}}+L_di_d+\frac{\gamma}{2}i_q^2\\\ \psi_q&=L_qi_q+\gamma i_di_q \end{aligned} $$

Dabei nehmen wir \\(L_d,L_q,\gamma\\) zunächst als Konstanten an.

### Differentielle d-Induktivität

$$ L\_{dd}=\frac{\partial\psi_d}{\partial i_d} $$

Da die übrigen Terme nicht von \\(i_d\\) abhängen, folgt:

$$ \boxed{L\_{dd}=L_d} $$

Das hast du richtig erkannt.

### Differentielle q-Induktivität

$$ L\_{qq}=\frac{\partial\psi_q}{\partial i_q} $$

Wir leiten beide Terme einzeln ab:

$$ \frac{\partial}{\partial i_q} \left(L_qi_q+\gamma i_di_q\right) $$

Bei dieser Ableitung halten wir \\(i_d\\) konstant. Somit:

$$ \boxed{L\_{qq}=L_q+\gamma i_d} $$

Das Interessante: Obwohl \\(L_q\\) in unserem Modell konstant ist, hängt die tatsächliche differentielle q-Induktivität \\(L\_{qq}\\) vom d-Strom ab.

## 2. Was ist mit \\(L\_{dq}\\) und \\(L\_{qd}\\)?

Hier ist deine Vermutung

$$ L\_{qd}i_d=L\_{dq}i_q $$

nicht allgemein richtig.

Die Kreuzinduktivitäten sind durch partielle Ableitungen definiert:

$$ L\_{dq}=\frac{\partial\psi_d}{\partial i_q}, \qquad L\_{qd}=\frac{\partial\psi_q}{\partial i_d} $$

Für unser Modell erhalten wir:

$$ \boxed{L\_{dq}=L\_{qd}=\gamma i_q} $$

Die Induktivitäten selbst müssen gleich sein, nicht ihre Produkte mit den jeweiligen Strömen.

Wir können das gesamte Ergebnis als Matrix schreiben:

$$ \boxed{ \mathbf L\_{\mathrm{diff}}= \begin{bmatrix} L_d&\gamma i_q\\\ \gamma i_q&L_q+\gamma i_d \end{bmatrix} } $$

Diese Matrix ist die Hesse-Matrix unserer Coenergy.

Eine wichtige Feinheit: Ein stromabhängiger Koeffizient, mit dem wir einen Strom in einer Flussgleichung multiplizieren, ist nicht automatisch identisch mit der entsprechenden differentiellen Induktivität. Deshalb müssen wir bei nichtlinearen Modellen wirklich ableiten.

## 3. Eine geometrisch interessante Beobachtung

Betrachten wir jetzt den Sonderfall \\(i_q=0\\).

Dann gilt:

$$ L\_{dq}=L\_{qd}=0 $$

Aber gleichzeitig:

$$ L\_{qq}=L_q+\gamma i_d $$

Meine Frage: Wie interpretierst du das physikalisch?

Wir haben an diesem Betriebspunkt keine differentiellen Kreuzinduktivitäten. Trotzdem verändert sich \\(L\_{qq}\\), wenn wir \\(i_d\\) verändern.

Ist das ein Widerspruch, oder beschreiben diese beiden Aussagen unterschiedliche Eigenschaften unseres Flusskennfeldes?

Ja, genau in die Richtung! Ein quadratischer Term in \\(i_d\\) wäre eine einfache Möglichkeit, damit \\(L\_{qq}\\) nicht mehr linear von \\(i_d\\) abhängt.

Allerdings muss es nicht zwingend eine gerade Potenz sein. Hier müssen wir zwischen der Abhängigkeit von \\(i_d\\) und der von \\(i_q\\) unterscheiden.

## 1. Warum wir einen höheren Potenzterm benötigen

Unser bisheriger Coenergy-Zusatz lautet:

\\[ \Delta W'=\frac{\gamma}{2}i_di_q^2 \\]

Wir leiten zweimal nach \\(i_q\\) ab:

\\[ \frac{\partial\Delta W'}{\partial i_q} =\gamma i_di_q \\]

\\[ \frac{\partial^2\Delta W'}{\partial i_q^2} =\gamma i_d \\]

Damit haben wir eine lineare Abhängigkeit von \\(i_d\\).

Wenn wir jetzt eine quadratische Abhängigkeit von \\(i_d\\) erhalten möchten, können wir beispielsweise ergänzen:

\\[ \boxed{\Delta W'\_2=\frac{\beta}{2}i_d^2i_q^2} \\]

Beachte: Dieser Coenergy-Term ist insgesamt von vierter Ordnung, nicht von zweiter.

## 2. Was ergibt sich für \\(L\_{qq}\\)?

Wir erweitern unser Modell:

\\[ W'=W'\_0+ \frac{\gamma}{2}i_di_q^2+ \frac{\beta}{2}i_d^2i_q^2 \\]

Zweimaliges Ableiten nach \\(i_q\\) liefert:

\\[ \boxed{L\_{qq}=L_q+\gamma i_d+\beta i_d^2} \\]

Das ist jetzt eine Parabel statt einer Geraden.

Linearer AnsatzQuadratischer Ansatz

0,50,7751,051,3251,6−3−2.5−2−1.5−1−0.50

Illustrative, normierte Modellparameter – keine realen Maschinenwerte

Eine höhere Potenz erlaubt eine Krümmung. Das bedeutet noch nicht, dass dieser Verlauf das reale Sättigungsverhalten richtig beschreibt.

## 3. Warum gerade Potenzen nicht überall notwendig sind

Wenn wir weiterhin die angenommene Rotorsymmetrie bezüglich \\(i_q\\) verlangen, sollte die Coenergy eine gerade Funktion von \\(i_q\\) sein.

Daher sind Terme wie \\(i_q^2\\) oder \\(i_q^4\\) naheliegend.

Für \\(i_d\\) besteht diese Forderung dagegen nicht. Wir können also grundsätzlich sowohl \\(i_d^2\\) als auch \\(i_d^3\\) oder andere Abhängigkeiten verwenden.

Noch allgemeiner könnten wir schreiben:

\\[ \boxed{\Delta W'=\frac12 f(i_d)i_q^2} \\]

Dabei beschreibt \\(f(i_d)\\), wie der d-Strom die q-Induktivität beeinflusst.

Das ist ein ziemlich nützlicher Gedanke: Wir können die nichtlineare Kopplung über eine einzige Funktion beschreiben und die zugehörigen Flussverkettungen durch Ableiten konsistent erzeugen.

## 4. Eine interessante Konsequenz

Wir hatten zuvor:

\\[ L\_{dd}=L_d \\]

Jetzt haben wir aber einen zusätzlichen Coenergy-Term eingeführt:

\\[ \Delta W'\_2=\frac{\beta}{2}i_d^2i_q^2 \\]

Meine Frage an dich:

Bleibt \\(L\_{dd}\\) damit weiterhin konstant, oder wird jetzt auch die differentielle d-Induktivität stromabhängig?

Versuch es durch zweimaliges partielles Ableiten nach \\(i_d\\) herauszufinden.

Damit sehen wir unmittelbar, warum eine einzige zusätzliche Coenergy-Funktion mehrere Induktivitätskennfelder gleichzeitig beeinflusst.

Fast! Du hast recht, dass durch zweimaliges Ableiten nach \\(i_d\\) die Abhängigkeit von \\(i_d\\) verschwindet. Aber die Abhängigkeit von \\(i_q\\) bleibt erhalten.

Schauen wir uns das an.

Unsere Coenergy lautet:

\\[ W'=W'\_0+\frac{\gamma}{2}i_di_q^2+\frac{\beta}{2}i_d^2i_q^2 \\]

Für die differentielle d-Induktivität gilt:

\\[ L\_{dd}=\frac{\partial^2 W'}{\partial i_d^2} \\]

### Erste Ableitung nach \\(i_d\\)

Wir behandeln \\(i_q\\) dabei als Konstante:

\\[ \psi_d=\frac{\partial W'}{\partial i_d} =\psi\_{\mathrm{PM}}+L_di_d+ \frac{\gamma}{2}i_q^2+\beta i_di_q^2 \\]

### Zweite Ableitung nach \\(i_d\\)

\\[ \boxed{L\_{dd}=L_d+\beta i_q^2} \\]

Das ist interessant: Unsere differentielle d-Induktivität ist jetzt unabhängig von \\(i_d\\), aber abhängig von \\(i_q\\).

Wir haben also:

\\[ \begin{aligned} L\_{dd}&=L_d+\beta i_q^2\\\ L\_{qq}&=L_q+\gamma i_d+\beta i_d^2 \end{aligned} \\]

Beide Induktivitäten sind stromabhängig, obwohl wir nur einen zusätzlichen Coenergy-Term eingeführt haben.

### Was bedeutet das physikalisch?

Der q-Strom verändert in diesem Modell die differentielle d-Induktivität und umgekehrt. Genau solche Wechselwirkungen möchten wir mit einem Kreuzsättigungsmodell erfassen.

Allerdings ist die konkrete Richtung der Veränderung vom Vorzeichen von \\(\beta\\) abhängig.

Eine Frage zum Verständnis:

Wenn wir \\(i_q=0\\) setzen, erhalten wir

\\[ L\_{dd}=L_d. \\]

Bedeutet das, dass unsere Maschine auf der gesamten d-Achse keine magnetische Sättigung zeigen kann?

Oder ist das lediglich eine Einschränkung unseres bisher gewählten Coenergy-Modells?

Da bin ich weitgehend bei dir. Ich glaube sogar, dass das für unsere Forschung der sinnvollere Weg ist. Wir sollten nicht versuchen, ein komplexes magnetisches Verhalten durch immer höhere globale Polynome zu beschreiben, sondern die physikalischen Eigenschaften direkt in die Struktur unseres Approximationsmodells einbauen.

Ein wichtiger Unterschied ist allerdings: B-Splines sind selbst stückweise Polynome. Das Problem ist also nicht grundsätzlich die Verwendung von Polynomen, sondern insbesondere die Verwendung eines einzelnen globalen Polynoms mit wenigen Koeffizienten, das das gesamte Kennfeld beschreiben soll.

## 1. Wir fitten die Coenergy, nicht zwei unabhängige Flusskennfelder

Genau hier sehe ich den größten Vorteil deiner Idee.

Statt

\\[ \psi_d=f_d(i_d,i_q),\qquad \psi_q=f_q(i_d,i_q) \\]

unabhängig voneinander zu approximieren, beschreiben wir nur eine skalare Funktion:

\\[ \boxed{W'(i_d,i_q)=f(i_d,i_q)} \\]

Dabei könnte \\(f\\) beispielsweise durch eine RBF-Approximation oder eine Tensorprodukt-B-Spline-Fläche dargestellt werden.

Aus dieser Funktion ergeben sich automatisch:

\\[ \underbrace{\nabla_i W'}\_{\text{Flussverkettungen}} = \begin{bmatrix} \psi_d\\\ \psi_q \end{bmatrix} \\]

und

\\[ \underbrace{\nabla_i^2W'}\_{\text{differentielle Induktivitäten}} = \begin{bmatrix} L\_{dd}&L\_{dq}\\\ L\_{qd}&L\_{qq} \end{bmatrix} \\]

Für eine hinreichend glatte Coenergy folgt unmittelbar:

\\[ \boxed{L\_{dq}=L\_{qd}} \\]

Das ist eine sehr schöne Eigenschaft: Wir erzwingen die Integrabilität nicht nachträglich, sondern sie ergibt sich bereits aus der Modellarchitektur.

## 2. RBF oder B-Spline?

Beides erscheint mir grundsätzlich geeignet.

| Eigenschaft                        | RBF                               | B-Spline                            |
| ---------------------------------- | --------------------------------- | ----------------------------------- |
| Unregelmäßig verteilte Messpunkte  | Sehr gut geeignet                 | Möglich, aber aufwendiger           |
| Lokale Veränderbarkeit             | Abhängig vom Kernel               | Sehr gut                            |
| Glatte Ableitungen                 | Abhängig vom Kernel               | Über Grad und Knoten steuerbar      |
| Kompakte Darstellung               | Abhängig von Zentrenzahl          | Gut mit geeigneter Knotenzahl       |
| Kontrollierbares Verhalten am Rand | Benötigt besondere Aufmerksamkeit | Ebenfalls, aber lokal gut steuerbar |

Wichtig ist, dass unser Modell mindestens zweimal stetig differenzierbar sein sollte, damit wir die differentiellen Induktivitäten sauber bestimmen können. Kubische B-Splines können beispielsweise bei einfachen inneren Knoten \\(C^2\\)-Stetigkeit liefern.

Streng mathematisch muss die Funktion übrigens nicht analytisch sein. Es reicht, wenn sie ausreichend glatt ist und ihre Ableitungen zuverlässig berechnet werden können.

## 3. Der Fit darf nicht alle Abweichungen beseitigen

Hier würde ich an deine ursprüngliche Forschungsfrage anknüpfen.

Wir könnten zunächst konzeptionell schreiben:

\\[ \boxed{ \boldsymbol\psi\_{\mathrm{rec}} = \nabla_i W' + \boldsymbol r } \\]

Dabei ist:

- \\(\nabla_i W'\\) unser konservativer, aus einer Coenergy abgeleiteter Flussanteil.
- \\(\boldsymbol r\\) die verbleibende Abweichung zwischen rekonstruiertem und konservativ modelliertem Flussfeld.

Das wäre zunächst eine Modellzerlegung, keine eindeutige physikalische Trennung.

Denn im Residuum können sowohl Eisenverlusteffekte als auch Widerstands-, Winkel- und Spannungsmessfehler sowie Approximationsfehler stecken.

Und genau deshalb ist deine Warnung so wichtig: Wenn der Interpolator zu stark glättet oder wir das gesamte Residuum als unerwünscht behandeln, verlieren wir möglicherweise die Informationen, die wir später analysieren wollen.

## 4. Eine weitere wichtige Frage: Interpolation oder Approximation?

Ein Interpolator versucht, die Messwerte exakt zu treffen.

Aber unsere Messwerte sind nicht fehlerfrei.

Wenn wir ein sehr flexibles Modell verwenden, kann es auch Messrauschen hervorragend interpolieren. Besonders bei den Ableitungen kann das problematisch werden:

\\[ W'\ \longrightarrow\ \boldsymbol\psi\ \longrightarrow\ \mathbf L\_{\mathrm{diff}} \\]

Die zweite Ableitung reagiert oft deutlich empfindlicher auf lokale Schwankungen als die Ausgangsfunktion.

Deshalb würde ich eine glatte, physikalisch eingeschränkte Approximation einer exakten Interpolation zunächst vorziehen. Das müssen wir aber anhand synthetischer Daten überprüfen, statt es einfach vorauszusetzen.

## 5. Unser Referenzmodell würde ich deshalb neu definieren

Wir brauchen nicht zwingend eine lineare PSM als eigentliches Ideal.

Ich würde vielmehr unterscheiden:

Ideales magnetisches Modell: Ein verlustfreies, konservatives und möglicherweise stark nichtlineares magnetisches System, beschrieben durch eine Coenergy \\(W'\\).

Reales Messmodell: Die aus den gemessenen Spannungen, Strömen und weiteren Größen rekonstruierte Flussinformation einschließlich der Effekte, die unsere vereinfachten stationären Spannungsgleichungen nicht explizit modellieren.

Damit wäre die Linearität nur noch ein besonders einfacher Spezialfall.

### Wo ich mathematisch gerne weitermachen würde

Bevor wir über konkrete RBF-Kernels, Stützstellen oder Optimierungsverfahren sprechen, würde ich eine grundlegende Frage untersuchen:

Wenn wir unsere Coenergy so approximieren, dass ihre Ableitungen möglichst gut zu den gemessenen Flussverkettungen passen, wie stellen wir fest, ob eine verbleibende Abweichung physikalisch bedingt ist oder lediglich durch unseren Approximator entsteht?

Das ist meiner Meinung nach die zentrale Schwierigkeit deines Vorschlags.

Ein besonders guter nächster Schritt wäre deshalb, zunächst ein bekanntes synthetisches, konservatives und nichtlineares Flusskennfeld zu konstruieren und zu prüfen, welche Fehler allein durch die Approximation entstehen. Anschließend könnten wir gezielt einen bekannten Messfehler hinzufügen und sehen, ob sich beide unterscheiden lassen.

Damit hätten wir eine belastbare Grundlage, bevor wir an die realen Messdaten gehen.

Dein Einwand ist berechtigt. Ein synthetisches Flusskennfeld kann uns zeigen, ob unsere mathematische Methode funktioniert. Es kann aber nicht beweisen, dass diese Methode die Fehler einer realen Maschine richtig erkennt.

Gerade bei den Eisenverlusten wird das problematisch. Selbst wenn wir beispielsweise ein Bertotti-Modell verwenden, simulieren wir nur diejenigen physikalischen Effekte, die wir vorher ausdrücklich in dieses Modell eingebaut haben.

Wir riskieren also, einen Algorithmus zu entwickeln, der hervorragend funktioniert, solange die Realität genau unseren Annahmen entspricht.

Ich würde deshalb zwischen zwei Fragestellungen unterscheiden:

1. Mathematische Validierung: Kann unser Coenergy-Approximator ein bekanntes, nichtlineares und konservatives Flussfeld rekonstruieren? Welche Approximationsfehler entstehen dabei?
2. Physikalische Validierung: Können wir aus realen Spannungs-, Strom-, Drehzahl- und Drehmomentmessungen unterschiedliche physikalische Effekte voneinander unterscheiden?

Die erste Frage können synthetische Felder gut beantworten. Für die zweite reichen sie allein nicht aus.

## 1. Was Bertotti uns liefert – und was nicht

Ein häufig verwendeter Ansatz für die spezifischen Eisenverluste ist vereinfacht:

\\[ p\_{\mathrm{Fe}}= \underbrace{k_h f B^\alpha}\_{\text{Hysterese}} +\underbrace{k_c f^2B^2}\_{\text{klassische Wirbelströme}} +\underbrace{k\_{\mathrm{ex}}(fB)^{3/2}}\_{\text{Exzessverluste}} \\]

Dabei sind \\(B\\) und \\(f\\) die lokale Flussdichteamplitude und Magnetisierungsfrequenz. Die Koeffizienten müssen zum Material und zum Modell passen.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://help.altair.com\&sz=32)

help.altair.com

+1



Das Modell beschreibt einen Energieverlust pro Zeit und Materialmenge. Aber wir suchen letztlich die Auswirkungen auf unsere gemessenen Größen:

\\[ u_d,\\;u_q,\\;i_d,\\;i_q,\\;\psi_d,\\;\psi_q,\\;M \\]

Hier fehlt eine Verbindung.

Denn die lokale Flussdichte \\(B(\mathbf x,t)\\) ist nicht identisch mit unserer Flussverkettung \\(\psi_d(i_d,i_q)\\). Um aus Bertotti realistische Maschinenverluste zu berechnen, benötigen wir normalerweise Informationen über die räumliche magnetische Feldverteilung, beispielsweise aus FEM.

Hinzu kommt, dass einfache Verlustmodelle rotierende Magnetisierungen, Oberwellen und nichtsinusförmige Flussdichten nur eingeschränkt erfassen.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.sciencedirect.com\&sz=32)

ScienceDirect

+1



Selbst ein exakt bekannter Eisenverlustwert sagt uns noch nicht eindeutig, wie sich die beiden dq-Flusskennfelder verändern.

## 2. Eine wichtige mathematische Beobachtung

Wir könnten Eisenverluste im Ersatzschaltbild zunächst über einen zusätzlichen Verluststrom \\(\mathbf i\_{\mathrm{Fe}}\\) repräsentieren.

Dann gilt in einem entsprechenden vereinfachten dq-Ersatzmodell:

\\[ \mathbf i_s=\mathbf i\_{\mathrm{mag}}+\mathbf i\_{\mathrm{Fe}} \\]

Die magnetische Coenergy hängt in diesem Modell vom Magnetisierungsstrom ab. Gemessen wird hingegen der gesamte Statorstrom.

Für die Spannung \\(\mathbf e\\) über dem modellierten Eisenverlustzweig könnten wir schreiben:

\\[ P\_{\mathrm{Fe}}=\frac32\mathbf e^\mathsf T\mathbf i\_{\mathrm{Fe}} \\]

Das ist allerdings nur eine skalare Gleichung für zwei unbekannte Verluststromkomponenten.

Wir haben also erneut ein Identifizierbarkeitsproblem.

Erst durch eine weitere Annahme, beispielsweise einen isotropen Eisenverlustwiderstand mit

\\[ \mathbf i\_{\mathrm{Fe}}=\frac{\mathbf e}{R\_{\mathrm{Fe}}}, \\]

legen wir eine konkrete Verluststromrichtung fest.

Das zeigt, warum ein Bertotti-Leistungsverlustmodell allein noch kein eindeutiges Modell der Flusskennfeldverzerrung ist.

Passend dazu gibt es eine experimentelle IPMSM-Untersuchung aus 2025, die ausdrücklich den Einfluss von Eisenverlusten auf die Flussrekonstruktion behandelt und verschiedene Verlustzweige im dq-Ersatzschaltbild betrachtet.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.jstage.jst.go.jp\&sz=32)

jstage.jst.go.jp



## 3. Wie ich unsere Untersuchung deshalb aufbauen würde

Ich würde nicht versuchen, sofort ein vollständiges synthetisches Maschinenmodell zu bauen. Stattdessen würde ich die Validierung in drei Ebenen aufteilen:

| Ebene         | Aufgabe                                                             | Was wir damit nachweisen können                                       |
| ------------- | ------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Numerisch     | Bekannte Coenergy mit RBF/B-Spline rekonstruieren                   | Güte des Approximators und seiner Ableitungen                         |
| Modellbasiert | Verlustzweige, Widerstands- und Sensorfehler im Messmodell ergänzen | Ob bekannte Fehlermechanismen charakteristische Abweichungen erzeugen |
| Experimentell | Reale Rohdaten und unabhängige Messinformationen untersuchen        | Welche Effekte tatsächlich auftreten und unterscheidbar sind          |

Gerade die zweite Ebene sollte von den ursprünglichen Spannungs- und Stromgrößen ausgehen, statt künstliche Flussfehler zu addieren.

Anschließend würden wir die Daten durch dieselbe Flussrekonstruktion schicken, die wir auch bei realen Messungen verwenden.

So können wir untersuchen, ob beispielsweise ein Eisenverlustzweig eine scheinbare Verkippung erzeugt und welche Informationen eine Coenergy-Approximation davon erhält oder entfernt.

## 4. Was ich außerdem für entscheidend halte

Wir sollten verschiedene Approximatoren auf denselben Daten vergleichen.

Wenn eine Auffälligkeit nur bei einem bestimmten RBF-Kernel oder einer bestimmten B-Spline-Knotenzahl auftritt, ist sie möglicherweise ein Approximationsartefakt.

Wenn eine strukturierte Abweichung bei unterschiedlichen geeigneten Approximationen bestehen bleibt, bei Wiederholungsmessungen reproduzierbar ist und beispielsweise systematisch von der Drehzahl abhängt, wird sie physikalisch interessanter.

Das beweist noch keine bestimmte Fehlerursache, gibt uns aber deutlich mehr Informationen als die reine Minimierung eines Fitfehlers.

Für mich folgt daraus auch eine wichtige Grundregel für unsere spätere Auswertung:

Wir behalten immer das rekonstruierte Kennfeld, das konservative Coenergy-Modell und das zugehörige Residuum getrennt. Kein Modell darf die ursprüngliche Messinformation einfach überschreiben.

## Mein Vorschlag für unseren nächsten mathematischen Schritt

Wir untersuchen zunächst ein einfaches magnetisches System mit einer Coenergy \\(W'(i_d,i_q)\\) und ergänzen einen Eisenverlustzweig im Ersatzschaltbild.

Dann gehen wir der Frage nach:

Wie verändert sich die aus den Klemmenmessungen rekonstruierte Flusskennfläche, wenn ein Teil des Statorstroms in unserem Ersatzmodell nicht zur Magnetisierung beiträgt?

Das wäre eine konkrete Verbindung zwischen Coenergy, Eisenverlusten und den Verkippungen, die wir tatsächlich beobachten.

Bertotti könnten wir später ergänzen, um die Verlustleistung realistischer zu beschreiben. Aber zuerst sollten wir verstehen, wie eine dissipative Komponente überhaupt in unserer Flussrekonstruktion sichtbar wird.

Eine physikalische Feinheit halten wir für später fest: Unser bisheriges \(W'\) ist ein auf die dq-Größen normiertes Coenergy-Potential. Bei einer amplitudeninvarianten dq-Transformation benötigt die gesamte dreiphasige magnetische Coenergy noch den Faktor \(3/2\). Für unsere bisherigen Gradientenberechnungen bleibt alles korrekt.



Genau richtig! Damit haben wir jetzt beide Kreuzableitungen unseres Flusskennfeldes im Statorstromraum bestimmt.

Du hast erhalten:

\\[ \boxed{\frac{\partial\psi_q}{\partial i\_{d,s}}=-\frac{L_qb}{1+ab}} \\]

Vergleichen wir das mit unserer vorherigen Herleitung:

\\[ \boxed{ \begin{aligned} \frac{\partial\psi_d}{\partial i\_{q,s}}&=\frac{L_da}{1+ab}\\\\[6pt] \frac{\partial\psi_q}{\partial i\_{d,s}}&=-\frac{L_qb}{1+ab} \end{aligned}} \\]

## 1. Was fällt uns auf?

Für positive Drehzahl und positive Induktivitäten sind \\(a\\) und \\(b\\) positiv.

Damit ist:

- Die erste Kreuzableitung positiv.
- Die zweite Kreuzableitung negativ.

Unsere Integrabilitätsbedingung ist also verletzt!

\\[ \frac{\partial\psi_d}{\partial i\_{q,s}} \neq \frac{\partial\psi_q}{\partial i\_{d,s}} \\]

Das bedeutet: Obwohl unser ursprüngliches magnetisches Flussfeld aus einer Coenergy abgeleitet wurde, ist das über den Statorströmen dargestellte Flussfeld nicht mehr konservativ.

## 2. Jetzt kommt eine interessante mathematische Eigenschaft

Erinnern wir uns:

\\[ a=\frac{\omega_eL_q}{R\_{\mathrm{Fe}}}, \qquad b=\frac{\omega_eL_d}{R\_{\mathrm{Fe}}} \\]

Damit gilt:

\\[ L_da=L_qb=\frac{\omega_eL_dL_q}{R\_{\mathrm{Fe}}} \\]

Unsere beiden Kreuzableitungen sind also sogar betragsgleich, aber vorzeichenverschieden!

Der Integrabilitätsfehler lautet:

\\[ \boxed{ r\_{\mathrm{int}} = \frac{\partial\psi_d}{\partial i\_{q,s}} - \frac{\partial\psi_q}{\partial i\_{d,s}} = \frac{L_da+L_qb}{1+ab} } \\]

Er ist für unser lineares Modell bei fester Drehzahl über den gesamten Stromraum konstant.

Das ist eine konkrete mathematische Signatur unseres vereinfachten Eisenverlustmodells. Es bedeutet allerdings noch nicht, dass wir jede solche Signatur in realen Messdaten eindeutig Eisenverlusten zuordnen dürfen.

## 3. Deine nächste Aufgabe

Wir haben jetzt eine analytische Gleichung für den Integrabilitätsfehler.

Setze unsere Definitionen für \\(a\\) und \\(b\\) in \\(r\_{\mathrm{int}}\\) ein und vereinfache den Ausdruck so weit wie möglich.

Danach untersuchen wir zwei Fragen:

1. Wie verändert sich der Integrabilitätsfehler mit der Drehzahl?
2. Was passiert im Grenzfall \\(R\_{\mathrm{Fe}}\to\infty\\)?

Anschließend können wir den analytischen Ausdruck in Python mit dem numerisch berechneten Curl des Flusskennfeldes vergleichen.

Damit hätten wir unseren ersten wichtigen Test: Kann ein modellierter Eisenverlusteffekt eine scheinbare Verletzung der magnetischen Integrabilitätsbedingung erzeugen?

Genau richtig! Damit haben wir jetzt beide Kreuzableitungen unseres Flusskennfeldes im Statorstromraum bestimmt.

Du hast erhalten:

\\[ \boxed{\frac{\partial\psi_q}{\partial i\_{d,s}}=-\frac{L_qb}{1+ab}} \\]

Vergleichen wir das mit unserer vorherigen Herleitung:

\\[ \boxed{ \begin{aligned} \frac{\partial\psi_d}{\partial i\_{q,s}}&=\frac{L_da}{1+ab}\\\\[6pt] \frac{\partial\psi_q}{\partial i\_{d,s}}&=-\frac{L_qb}{1+ab} \end{aligned}} \\]

## 1. Was fällt uns auf?

Für positive Drehzahl und positive Induktivitäten sind \\(a\\) und \\(b\\) positiv.

Damit ist:

- Die erste Kreuzableitung positiv.
- Die zweite Kreuzableitung negativ.

Unsere Integrabilitätsbedingung ist also verletzt!

\\[ \frac{\partial\psi_d}{\partial i\_{q,s}} \neq \frac{\partial\psi_q}{\partial i\_{d,s}} \\]

Das bedeutet: Obwohl unser ursprüngliches magnetisches Flussfeld aus einer Coenergy abgeleitet wurde, ist das über den Statorströmen dargestellte Flussfeld nicht mehr konservativ.

## 2. Jetzt kommt eine interessante mathematische Eigenschaft

Erinnern wir uns:

\\[ a=\frac{\omega_eL_q}{R\_{\mathrm{Fe}}}, \qquad b=\frac{\omega_eL_d}{R\_{\mathrm{Fe}}} \\]

Damit gilt:

\\[ L_da=L_qb=\frac{\omega_eL_dL_q}{R\_{\mathrm{Fe}}} \\]

Unsere beiden Kreuzableitungen sind also sogar betragsgleich, aber vorzeichenverschieden!

Der Integrabilitätsfehler lautet:

\\[ \boxed{ r\_{\mathrm{int}} = \frac{\partial\psi_d}{\partial i\_{q,s}} - \frac{\partial\psi_q}{\partial i\_{d,s}} = \frac{L_da+L_qb}{1+ab} } \\]

Er ist für unser lineares Modell bei fester Drehzahl über den gesamten Stromraum konstant.

Das ist eine konkrete mathematische Signatur unseres vereinfachten Eisenverlustmodells. Es bedeutet allerdings noch nicht, dass wir jede solche Signatur in realen Messdaten eindeutig Eisenverlusten zuordnen dürfen.

## 3. Deine nächste Aufgabe

Wir haben jetzt eine analytische Gleichung für den Integrabilitätsfehler.

Setze unsere Definitionen für \\(a\\) und \\(b\\) in \\(r\_{\mathrm{int}}\\) ein und vereinfache den Ausdruck so weit wie möglich.

Danach untersuchen wir zwei Fragen:

1. Wie verändert sich der Integrabilitätsfehler mit der Drehzahl?
2. Was passiert im Grenzfall \\(R\_{\mathrm{Fe}}\to\infty\\)?

Anschließend können wir den analytischen Ausdruck in Python mit dem numerisch berechneten Curl des Flusskennfeldes vergleichen.

Damit hätten wir unseren ersten wichtigen Test: Kann ein modellierter Eisenverlusteffekt eine scheinbare Verletzung der magnetischen Integrabilitätsbedingung erzeugen?

Genau! Damit haben wir einen interessanten Zusammenhang sichtbar gemacht: Unser Integrabilitätsresiduum steigt zunächst mit der Drehzahl, erreicht ein Maximum und fällt anschließend wieder ab.

Wichtig: Dieser Verlauf ergibt sich aus unserem vereinfachten Eisenverlustmodell mit konstantem \\(R\_{\mathrm{Fe}}\\). Er ist noch keine allgemeingültige Aussage über reale Maschinen.

Bevor wir wieder zu unseren Flusskennfeldern zurückkehren, möchte ich noch eine Eigenschaft untersuchen.

Wir haben:

\\[ r\_{\mathrm{int}}(\omega_e)= \frac{2\omega_e L_dL_qR\_{\mathrm{Fe}}} {R\_{\mathrm{Fe}}^2+\omega_e^2L_dL_q} \\]

Was passiert, wenn du \\(\omega_e\\) durch \\(-\omega_e\\) ersetzt?

Ist die Funktion gerade, ungerade oder weder noch?

Damit können wir eine weitere mathematische Eigenschaft unseres Modells verstehen, die später für die Fehlerdiagnose interessant sein könnte.

Genau! Unser Integrabilitätsresiduum ist unter den getroffenen Modellannahmen punktsymmetrisch zum Ursprung.

Mathematisch bedeutet das, dass die Funktion ungerade ist:

\\[ \boxed{r\_{\mathrm{int}}(-\omega_e)=-r\_{\mathrm{int}}(\omega_e)} \\]

Denn in unserem Ausdruck

\\[ r\_{\mathrm{int}}(\omega_e)= \frac{2\omega_e L_dL_qR\_{\mathrm{Fe}}} {R\_{\mathrm{Fe}}^2+\omega_e^2L_dL_q} \\]

ändert bei einer Drehzahlumkehr nur der Zähler sein Vorzeichen. Der Nenner bleibt unverändert.

Das bedeutet:

- Positive und negative Drehzahlen erzeugen betragsmäßig gleiche Integrabilitätsresiduen.
- Das Vorzeichen des Residuums kehrt sich um.
- Bei \\(\omega_e=0\\) verschwindet das Residuum.

Aber Achtung: Wir haben damit nur die Symmetrie des Integrabilitätsresiduums gezeigt, nicht die Symmetrie sämtlicher Messfehler.

## Eine interessante physikalische Konsequenz

Betrachten wir jetzt die Eisenverlustleistung unseres Modells:

\\[ P\_{\mathrm{Fe}}=\frac32\frac{e_d^2+e_q^2}{R\_{\mathrm{Fe}}} \\]

mit

\\[ e_d=-\omega_e\psi_q,\qquad e_q=\omega_e\psi_d. \\]

Meine Frage: Wenn wir bei unverändertem magnetischem Zustand die Drehrichtung umkehren, ist dann auch die Eisenverlustleistung punktsymmetrisch zum Ursprung?

Oder ist sie möglicherweise achsensymmetrisch bezüglich \\(\omega_e=0\\)?

Das ist eine interessante Unterscheidung zwischen einer dissipierten Leistung und der mathematischen Signatur, die sie in unserem rekonstruierten Flussfeld hinterlassen kann.

Genau! Die Eisenverlustleistung ist in unserem Modell achsensymmetrisch zur y-Achse, also eine gerade Funktion der elektrischen Drehzahl.

Wir setzen die induzierten Spannungen ein:

\\[ P\_{\mathrm{Fe}}=\frac32\frac{e_d^2+e_q^2}{R\_{\mathrm{Fe}}} \\]

Damit ergibt sich:

\\[ \boxed{ P\_{\mathrm{Fe}}(\omega_e) =\frac32\frac{\omega_e^2}{R\_{\mathrm{Fe}}} (\psi_d^2+\psi_q^2) } \\]

Da die Drehzahl quadriert wird, gilt bei unverändertem magnetischem Zustand und konstantem \\(R\_{\mathrm{Fe}}\\):

\\[ \boxed{P\_{\mathrm{Fe}}(-\omega_e)=P\_{\mathrm{Fe}}(\omega_e)} \\]

## Was haben wir damit herausgefunden?

Wir haben zwei unterschiedliche Symmetrien:

| Größe                                           | Symmetrie bezüglich \\(\omega_e\\) |
| ----------------------------------------------- | ---------------------------------- |
| Eisenverlustleistung \\(P\_{\mathrm{Fe}}\\)     | Gerade – achsensymmetrisch         |
| Integrabilitätsresiduum \\(r\_{\mathrm{int}}\\) | Ungerade – punktsymmetrisch        |

Physikalisch interessant: Die Maschine dissipiert in unserem Modell bei beiden Drehrichtungen dieselbe Eisenverlustleistung. Trotzdem kehrt sich das Vorzeichen der dadurch verursachten Integrabilitätsverletzung um.

Das könnte später bei unserer Fehlerdiagnose interessant werden. Allerdings haben wir noch nicht bewiesen, dass reale Maschinen dieselbe einfache Symmetrie aufweisen.

### Eine letzte Überlegung dazu

Angenommen, wir messen die Flusskennfelder bei \\(+100\\,\mathrm{Hz}\\) und \\(-100\\,\mathrm{Hz}\\).

Wir bilden anschließend den Mittelwert ihrer Integrabilitätsresiduen:

\\[ \overline r\_{\mathrm{int}} =\frac{r\_{\mathrm{int}}(+100)+r\_{\mathrm{int}}(-100)}{2} \\]

Was passiert mit unserem modellierten Eisenverlusteinfluss bei dieser Mittelwertbildung?

Danach gehen wir wieder zu Python und überprüfen unsere analytische Herleitung numerisch.

Genau! Die beiden Nebendiagonaleinträge hast du richtig berechnet. Es fehlt lediglich noch ein gemeinsamer Faktor, der aus der Matrixinversion entsteht.

## 1. Berechnen wir die vollständige Matrix

Unsere Transformationsmatrix lautet:

\\[ \mathbf A= \begin{bmatrix} 1&-a\\\ b&1 \end{bmatrix} \\]

Ihre Inverse ist:

\\[ \mathbf A^{-1} =\frac{1}{1+ab} \begin{bmatrix} 1&a\\\ -b&1 \end{bmatrix} \\]

Jetzt multiplizieren wir mit unserer differentiellen Induktivitätsmatrix:

\\[ \mathbf J\_{\psi,s} = \begin{bmatrix} L_d&0\\\ 0&L_q \end{bmatrix} \mathbf A^{-1} \\]

Damit erhalten wir:

\\[ \boxed{ \mathbf J\_{\psi,s} =\frac{1}{1+ab} \begin{bmatrix} L_d&aL_d\\\ -bL_q&L_q \end{bmatrix} } \\]

Die von dir berechneten Terme \\(aL_d\\) und \\(-bL_q\\) stehen also genau an den richtigen Stellen.

## 2. Was bedeutet das geometrisch?

Vorher war unsere Jacobi-Matrix diagonal. Eine Änderung des d-Stroms beeinflusste nur den d-Fluss und eine Änderung des q-Stroms nur den q-Fluss.

Jetzt haben wir zusätzliche Kreuzableitungen:

\\[ \begin{aligned} \frac{\partial\psi_d}{\partial i\_{q,s}}&=\frac{aL_d}{1+ab}\\\\[6pt] \frac{\partial\psi_q}{\partial i\_{d,s}}&=-\frac{bL_q}{1+ab} \end{aligned} \\]

Die entscheidende Beobachtung: Die beiden Kreuzableitungen haben bei positiver Drehzahl unterschiedliche Vorzeichen.

Unsere Jacobi-Matrix ist daher nicht mehr symmetrisch. Das ist die zuvor hergeleitete Integrabilitätsverletzung im Statorstromraum.

Wichtig ist die Unterscheidung: Die ursprüngliche magnetische Induktivitätsmatrix bezüglich der Magnetisierungsströme bleibt symmetrisch. Erst die Beschreibung derselben Flüsse über den gesamten Statorströmen erzeugt diese Asymmetrie.

## 3. Jetzt überprüfen wir das in Python

Ergänze im Hauptprogramm:

```
a = OMEGA_E * LQ / R_FEb = OMEGA_E * LD / R_FEA = np.array([    [1, -a],    [b,  1]])J_psi_m = np.diag([LD, LQ])J_psi_s = J_psi_m @ np.linalg.inv(A)print(J_psi_s)
```

Damit können wir kontrollieren, ob unsere analytische Herleitung mit der numerischen Matrixmultiplikation übereinstimmt.

Deine nächste Aufgabe: Berechne anschließend direkt aus `J_psi_s` das Integrabilitätsresiduum

\\[ \boxed{r\_{\mathrm{int}}=J\_{\psi,s}[0,1]-J\_{\psi,s}[1,0]} \\]

und vergleiche es mit unserer analytischen Formel.

Dann haben wir die mathematische Herleitung erstmals unabhängig über die Matrixrechnung überprüft.

Genau! Der Faktor 2 entsteht, weil unsere beiden Kreuzableitungen betragsgleich sind, aber unterschiedliche Vorzeichen haben.

Wir hatten:

\\[ \frac{\partial\psi_d}{\partial i\_{q,s}} =\frac{aL_d}{1+ab} \\]

und

\\[ \frac{\partial\psi_q}{\partial i\_{d,s}} =-\frac{bL_q}{1+ab} \\]

Da \\(aL_d=bL_q\\), erhalten wir:

\\[ \begin{aligned} r\_{\mathrm{int}} &=\frac{aL_d-(-bL_q)}{1+ab}\\\\[4pt] &=\boxed{\frac{2aL_d}{1+ab}} \end{aligned} \\]

Mit unseren Parametern ergibt das ungefähr:

\\[ \boxed{r\_{\mathrm{int}}\approx5{,}02\cdot10^{-5}\\,\mathrm H} \\]

Damit haben wir unsere frühere Herleitung über die Jacobi-Matrix bestätigt.

### Wie machen wir weiter?

Ich würde als Nächstes das Integrabilitätsresiduum direkt numerisch aus den Flusskennfeldern bestimmen, statt es aus unserer bekannten analytischen Modellgleichung zu berechnen.

Denn bei echten Messdaten kennen wir die zugrunde liegende Transformation nicht.

Dafür müssen wir allerdings lernen, wie man partielle Ableitungen auf unserem verzerrten Stromgitter berechnet.

Das führt uns zur Kettenregel für mehrere Variablen – und zeigt gleichzeitig, warum eine Jacobi-Matrix geometrisch so nützlich ist.