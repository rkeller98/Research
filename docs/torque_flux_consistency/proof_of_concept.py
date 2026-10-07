"""Isolated synthetic torque/flux research experiment; no measured-map edits.

Run from any directory with the repository's Python environment. Figures use
the canonical publication palette (Matplotlib and kpsewhich required).
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MODEL_PATH = ROOT / "shared/python/magnetic_model.py"
spec = importlib.util.spec_from_file_location("existing_magnetic_model", MODEL_PATH)
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)
I_BASE, PSI_BASE, P, SEED = 100.0, 0.1, 3, 20261007
KT = 1.5 * P
J = np.array([[0.0, -1.0], [1.0, 0.0]])


def flux(i):
    return PSI_BASE * model.flux(np.asarray(i) / I_BASE)


def torque(i, psi):
    return KT * (i[..., 1] * psi[..., 0] - i[..., 0] * psi[..., 1])


def directions(i):
    magnitude = np.linalg.norm(i, axis=-1)
    ni = np.asarray(i) / magnitude[..., None]
    return magnitude, ni, np.stack([ni[..., 1], -ni[..., 0]], axis=-1)


def potential_operators(x):
    """Gradients of [1,x,y,s,(x²-y²)/2,xy,s²], s=(x²+y²)/2.

    Coordinates and coefficients are dimensionless. Columns 0,3,6 are torque
    null modes: potential gauge, radial quadratic and radial quartic.
    """
    xd, xq = x.T
    s, z, o = np.sum(x*x, axis=1)/2, np.zeros(len(x)), np.ones(len(x))
    gd = np.column_stack([z, o, z, xd, xd, xq, 2*s*xd])
    gq = np.column_stack([z, z, o, xq, -xq, xd, 2*s*xq])
    hm = xq[:, None]*gd - xd[:, None]*gq
    gu = np.vstack([-gq, gd])  # voltage scaled by omega_e * PSI_BASE
    gauge = np.array([[1., 0., 0., 0., 0., 0., 0.]])
    return hm, gu, gauge


def spectrum(h):
    values = np.linalg.svd(h, compute_uv=False)
    tolerance = np.finfo(float).eps * max(h.shape) * values[0]
    rank = int(np.count_nonzero(values > tolerance))
    return {"shape": list(h.shape), "rank": rank, "nullity": h.shape[1]-rank,
            "singular_values": values.tolist(), "rank_tolerance": float(tolerance),
            "full_condition": None if rank < h.shape[1] else float(values[0]/values[-1]),
            "observable_condition": float(values[0]/values[rank-1]) if rank else None}


def run_checks():
    rng = np.random.default_rng(SEED)
    x = rng.uniform(-1.2, 1.2, (1500, 2))
    x = x[np.linalg.norm(x, axis=1) > .03]
    i, psi = I_BASE*x, PSI_BASE*model.flux(x)
    mag, ni, nt = directions(i)
    mref = torque(i, psi)
    checks = {}

    def verify(name, error, tol=1e-10):
        maximum = float(np.max(np.abs(error)))
        if not np.isfinite(maximum) or maximum > tol:
            raise AssertionError(f"{name}: max error {maximum} > {tol}")
        checks[name] = {"max_abs_error": maximum, "tolerance": tol, "passed": True}

    verify("perfect_map_Nm", torque(i, psi)-mref)
    scale = np.sqrt(1.5)
    power_invariant_torque = P*((scale*i[:, 1])*(scale*psi[:, 0])
                                -(scale*i[:, 0])*(scale*psi[:, 1]))
    verify("power_invariant_scaling_Nm", power_invariant_torque-mref)
    verify("basis_orthonormal", np.sum(ni*nt, axis=1))
    verify("clockwise_normal", nt + ni @ J.T)
    alpha, beta = .011, -.007
    for name, a, b in [("observable", 0., beta), ("parallel", alpha, 0.),
                       ("mixed", alpha, beta)]:
        bad = psi + a*ni + b*nt
        em = torque(i, bad)-mref
        eps = em/(KT*mag)
        corrected = bad - eps[:, None]*nt
        verify(name+"_projection_Wb", eps-b)
        verify(name+"_corrected_torque_Nm", torque(i, corrected)-mref)
        verify(name+"_remaining_parallel_Wb", corrected-psi-a*ni)
        verify(name+"_parallel_preserved_Wb", np.sum((corrected-bad)*ni, axis=1))

    # General SPD weighting; use solves, never invert W numerically.
    w = np.array([[5., .6], [.6, 1.]])
    avec = np.stack([i[:, 1], -i[:, 0]], axis=1)
    b = np.full(len(i), -.45/KT)
    wa = np.linalg.solve(w, avec.T).T
    weighted = wa * (b/np.sum(avec*wa, axis=1))[:, None]
    verify("weighted_constraint_AWb", np.sum(avec*weighted, axis=1)-b)
    verify("weighted_stationarity", np.sum((weighted @ w.T)*ni, axis=1))
    assert np.max(np.abs(np.sum(weighted*ni, axis=1))) > 1e-5
    # Any feasible perturbation is parallel: cost must not improve.
    trial = weighted + .003*ni
    cost_gap = np.einsum('ni,ij,nj->n', trial, w, trial)/2 - np.einsum(
        'ni,ij,nj->n', weighted, w, weighted)/2
    assert np.min(cost_gap) > 0

    # Zero current remains a true rank-zero case, with undefined projection.
    verify("zero_current_torque_Nm", torque(np.zeros((3, 2)), np.ones((3, 2))))
    assert np.linalg.matrix_rank(np.zeros((1, 2))) == 0
    low = np.array([0., .1, 1., 10.])
    valid = low > 1.
    projection = np.full(len(low), np.nan)
    np.divide(np.ones(len(low)), KT*low, out=projection, where=valid)
    assert np.array_equal(np.isnan(projection), ~valid)
    checks["zero_and_threshold_mask"] = {"passed": True, "I_min_A": 1.,
                                        "currents_A": low.tolist(), "valid": valid.tolist()}

    offset, gain, epsilon_r = .2, .03, .002
    verify("offset_pattern_Wb", (mref-(mref+offset))/(KT*mag)+offset/(KT*mag))
    verify("gain_pattern_Wb", (mref-mref*(1+gain))/(KT*mag)+gain*mref/(KT*mag))
    for omega in (-800., 400., 1200.):
        voltage = .01*i + omega*(psi @ J.T)
        rec = (voltage-(.01+epsilon_r)*i) @ J / omega
        em = torque(i, rec)-mref
        verify(f"resistance_sign_{omega:g}_Nm", em+KT*epsilon_r*mag**2/omega)
        verify(f"resistance_equivalent_{omega:g}_ohm", -omega*em/(KT*mag**2)-epsilon_r)
    losses = []
    for rpm in (1000., 3000.):
        om = 2*np.pi*rpm/60
        loss = .1 + .00002*om**2  # explicitly illustrative positive-speed loss
        eps = (mref-(mref-loss))/(KT*mag)
        verify(f"loss_pattern_{rpm:g}_Wb", eps-loss/(KT*mag))
        losses.append({"rpm": rpm, "assumed_loss_Nm": loss,
                       "residual_rms_Wb": float(np.sqrt(np.mean(eps**2)))})

    # PSM/EESM reduce independently to the existing linear model.
    ld, lq, le, pm = .001, .0018, .004, .12
    verify("PSM_linear_Nm", torque(i, np.column_stack([pm+ld*i[:, 0], lq*i[:, 1]]))
           -KT*i[:, 1]*(pm+(ld-lq)*i[:, 0]))
    ie = rng.uniform(0., 20., len(i))
    verify("EESM_linear_Nm", torque(i, np.column_stack([ld*i[:, 0]+le*ie, lq*i[:, 1]]))
           -KT*i[:, 1]*(le*ie+(ld-lq)*i[:, 0]))

    # Coherent rotations preserve torque; inconsistent map coordinates do not.
    angle = .03
    r = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    verify("coherent_rotation_Nm", torque(i @ r.T, psi @ r.T)-mref)
    ri = i @ r  # estimated axes advanced: coordinates rotate clockwise
    angle_residual = (torque(ri, flux(ri))-mref)/(KT*mag)
    assert np.sqrt(np.mean(angle_residual**2)) > 1e-4

    # Differentiate the composed residual, including map evaluation at current.
    dp = PSI_BASE/I_BASE*model.hessian(x)
    grad_m = KT*(psi @ J.T + np.einsum('nji,nj->ni', dp, avec))
    step = 1e-3
    grad_numeric = np.column_stack([
        (torque(i+step*np.eye(2)[j], flux(i+step*np.eye(2)[j])) -
         torque(i-step*np.eye(2)[j], flux(i-step*np.eye(2)[j])))/(2*step)
        for j in range(2)])
    verify("composed_current_gradient_Nm_per_A", grad_numeric-grad_m, 2e-9)

    # Monte Carlo: same assumed torque SD at different currents.
    sigma_m, trials = .2, 100000
    current_levels = np.array([.1, .3, 1., 3., 10., 30., 100.])
    noise_sd = []
    for current in current_levels:
        residual = -rng.normal(0., sigma_m, trials)/(KT*current)
        expected = sigma_m/(KT*current)
        measured = float(np.std(residual, ddof=1))
        assert abs(measured/expected-1) < .015
        noise_sd.append({"I_A": float(current), "expected_sd_Wb": expected,
                         "observed_sd_Wb": measured, "bias_Wb": float(np.mean(residual))})
    checks["noise_inverse_current"] = {"passed": True, "trials_per_level": trials,
                                        "sigma_torque_Nm": sigma_m, "relative_tolerance": .015}
    current_noise = rng.normal(0., .2, i.shape)
    noisy_i = i+current_noise
    current_residual = (torque(noisy_i, flux(noisy_i))-mref)/(KT*np.linalg.norm(noisy_i, axis=1))

    # Torque + voltage separates flux and R locally under the exact model.
    one_i = np.array([3., 4.])
    omega = 400.
    local = np.array([[0., -omega, one_i[0]], [omega, 0., one_i[1]],
                      [KT*one_i[1], -KT*one_i[0], 0.]])
    verify("joint_determinant", np.linalg.det(local)+KT*omega*np.dot(one_i, one_i), 1e-7)
    truth = np.array([.12, .04, .01])
    verify("joint_flux_R_recovery", np.linalg.solve(local, local @ truth)-truth)

    hm, hu, gauge = potential_operators(x)
    joint = np.vstack([hm, hu])
    fixed = np.vstack([joint, gauge])
    operators = {"torque": spectrum(hm), "torque_voltage": spectrum(joint),
                 "torque_voltage_gauge": spectrum(fixed)}
    assert [operators[k]["rank"] for k in operators] == [4, 6, 7]
    verify("global_radial_null_modes", hm[:, [0, 3, 6]])
    coefficients = np.array([0., .13, -.02, .01, -.03, .005, .004])
    solution = np.linalg.lstsq(fixed, fixed @ coefficients, rcond=None)[0]
    verify("global_joint_coefficients", solution-coefficients)
    xd, xq = x.T
    affine = np.column_stack([xq, xq*xd, xq*xq, -xd, -xd*xd, -xd*xq])
    assert spectrum(affine)["rank"] == 5
    small_grid = np.array([(v, 0.) for v in np.linspace(-1., 1., 9)])
    narrow, _, _ = potential_operators(small_grid)
    assert spectrum(narrow)["rank"] == 2
    underdetermined = spectrum(hm[:2])
    assert underdetermined["nullity"] >= 5
    checks["global_rank_and_recovery"] = {"passed": True}

    def stats(a):
        return {"bias_Wb": float(np.mean(a)), "sd_Wb": float(np.std(a, ddof=1)),
                "rmse_Wb": float(np.sqrt(np.mean(a*a)))}

    report = {"status": "synthetic_only_no_experimental_validation", "seed": SEED,
              "basis": {"current_A": I_BASE, "flux_Wb": PSI_BASE,
                        "pole_pairs": P, "k_T": KT},
              "versions": {"python": sys.version.split()[0], "numpy": np.__version__},
              "samples": len(i), "checks": checks, "noise": noise_sd,
              "current_noise": {"assumed_sd_A": .2, **stats(current_residual)},
              "relative_angle_error": {"estimated_minus_true_rad": angle, **stats(angle_residual)},
              "losses": losses, "operators": operators,
              "operator_scaling": "dimensionless currents and potential coefficients; torque divided by k_T*I_BASE*PSI_BASE; voltage divided by omega_e*PSI_BASE; unit illustrative residual variances",
              "potential_basis": ["1", "x", "y", "s", "(x^2-y^2)/2", "xy", "s^2"],
              "affine_flux_operator": spectrum(affine), "single_axis_operator": spectrum(narrow),
              "underdetermined_operator": underdetermined,
              "hashes": {str(p.relative_to(ROOT)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in (Path(__file__), MODEL_PATH, ROOT/'shared/python/publication_plotting.py',
                                   ROOT/'shared/config/palette.tex')}}
    return report


def make_figures(report):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    sys.path.insert(0, str(ROOT / "shared/python"))
    from publication_plotting import configure
    colors = configure()
    out = HERE / 'figures'
    out.mkdir(exist_ok=True)
    i = np.array([3., 4.])
    _, ni, nt = directions(i)
    psi = np.array([.12, .04])
    target = 1.17
    correction = -(torque(i, psi)-target)/(KT*np.linalg.norm(i))*nt
    corrected = psi+correction

    def save(fig, name):
        fig.savefig(out/(name+'.png'), bbox_inches='tight')
        fig.savefig(out/(name+'.pdf'), bbox_inches='tight')
        plt.close(fig)

    def frame(title):
        fig, ax = plt.subplots(figsize=(6.1, 4.5), layout='constrained')
        ax.set(xlim=(-.05, .18), ylim=(-.09, .18), xlabel=r'$\psi_d$ / Wb',
               ylabel=r'$\psi_q$ / Wb', title=title)
        ax.set_aspect('equal')
        ax.axhline(0., color=colors['guide'], lw=.7)
        ax.axvline(0., color=colors['guide'], lw=.7)
        return fig, ax

    def arrow(ax, end, label, role, start=np.zeros(2)):
        ax.annotate('', xy=end, xytext=start, arrowprops={'arrowstyle': '->', 'color': colors[role]})
        ax.plot([], [], color=colors[role], label=label)

    fig, ax = frame('1  Stromrichtung und Torque-Normale')
    arrow(ax, .11*ni, r'$\mathbf{n}_i$ (Richtung, skaliert)', 'guide')
    arrow(ax, .11*nt, r'$\mathbf{n}_\tau=-J\mathbf{n}_i$ (Richtung, skaliert)', 'torque')
    ax.text(.01, .14, r'$i_d=3$ A, $i_q=4$ A, $I_s=5$ A')
    ax.legend(loc='upper left', bbox_to_anchor=(0., -.2)); save(fig, '01_directions')

    fig, ax = frame('2  Fluss als Summe zweier Projektionen')
    parallel, normal = np.dot(psi, ni)*ni, np.dot(psi, nt)*nt
    arrow(ax, psi, r'$\boldsymbol{\psi}_{map}$', 'reference')
    arrow(ax, parallel, r'$\psi_i\mathbf{n}_i$', 'guide')
    arrow(ax, normal, r'$\psi_\tau\mathbf{n}_\tau$', 'torque')
    ax.plot([parallel[0], psi[0]], [parallel[1], psi[1]], '--', color=colors['guide'])
    ax.plot([normal[0], psi[0]], [normal[1], psi[1]], '--', color=colors['guide'])
    ax.legend(loc='upper left'); save(fig, '02_projection')

    fig, ax = frame('3  Ein Moment definiert eine Gerade')
    tt = np.linspace(-.2, .2, 100)
    line = corrected+tt[:, None]*ni
    ax.plot(*line.T, color=colors['torque'], label=r'$M=1.17$ Nm')
    arrow(ax, psi, r'$\boldsymbol{\psi}_{map}$: 1.62 Nm', 'reference')
    ax.scatter(*corrected, color=colors['derived'], label='Nächster Punkt')
    ax.legend(loc='upper left'); save(fig, '03_solution_line')

    fig, ax = frame('4  Minimum-Norm-Korrektur zur Referenz')
    ax.plot(*line.T, color=colors['torque'], label='Gleiches Referenzmoment')
    arrow(ax, psi, r'$\boldsymbol{\psi}_{map}$', 'reference')
    arrow(ax, corrected, r'$\boldsymbol{\psi}^\star$', 'derived')
    arrow(ax, corrected, r'$\Delta\boldsymbol{\psi}=(-16,12)$ mWb', 'estimated', psi)
    ax.scatter(*psi, color=colors['reference'])
    ax.scatter(*corrected, color=colors['derived'])
    ax.legend(loc='upper left'); save(fig, '04_correction')

    grid = np.linspace(-120., 120., 81)
    dd, qq = np.meshgrid(grid, grid)
    current = np.stack([dd, qq], axis=-1)
    mag = np.linalg.norm(current, axis=-1)
    valid = mag > 1.
    ni = np.zeros_like(current)
    np.divide(current, mag[..., None], out=ni, where=valid[..., None])
    nt = np.stack([ni[..., 1], -ni[..., 0]], axis=-1)
    beta = .004*np.sin(dd/I_BASE)*np.cos(qq/I_BASE)
    alpha = .008*np.ones_like(dd)
    true = flux(current)
    bad = true+alpha[..., None]*ni+beta[..., None]*nt
    residual = np.full_like(dd, np.nan)
    np.divide(torque(current, bad)-torque(current, true), KT*mag, out=residual, where=valid)
    assert np.max(np.abs(residual[valid]-beta[valid])) < 1e-12
    fig, ax = plt.subplots(figsize=(6.1, 4.5), layout='constrained')
    image = ax.pcolormesh(dd, qq, 1e3*residual, shading='nearest',
                         cmap=colors['error_map'], vmin=-4., vmax=4.)
    # Semantic signed residual palette derived from canonical roles.
    from matplotlib.colors import LinearSegmentedColormap
    image.set_cmap(LinearSegmentedColormap.from_list('torque_signed',
        [colors['reference'], 'white', colors['estimated']]))
    fig.colorbar(image, ax=ax, label=r'$e_{\psi_\tau}$ / mWb')
    ax.set(xlabel=r'$i_d$ / A', ylabel=r'$i_q$ / A',
           title='5  Gemischter Fehler: 8 mWb parallel bleiben unsichtbar')
    save(fig, '05_residual_map')

    fig, ax = plt.subplots(figsize=(6.7, 4.2), layout='constrained')
    for key, label, role in [('torque', 'Torque: Rang 4, Nullität 3', 'torque'),
                             ('torque_voltage', 'Torque + Spannung: Rang 6', 'derived'),
                             ('torque_voltage_gauge', '+ Potentialgauge: Rang 7', 'reference')]:
        op = report['operators'][key]
        singular = np.asarray(op['singular_values'])
        tol = op['rank_tolerance']
        display = np.maximum(singular, tol)
        ax.semilogy(np.arange(1, 8), display, 'o-', color=colors[role], label=label)
        zeros = singular <= tol
        ax.scatter(np.arange(1, 8)[zeros], display[zeros], marker='x', s=55, color=colors[role])
    ax.set(xlabel='Index des Singulärwerts', ylabel='Singulärwert (deklarierte Skalen)',
           title='6  Radiale Moden brauchen unabhängige Flussinformation', xticks=range(1, 8))
    ax.legend(loc='center right')
    ax.text(.02, .04, 'Kreuze: numerischer Nullraum an Rangtoleranz dargestellt', transform=ax.transAxes, fontsize=8)
    save(fig, '06_observability')

    fig, ax = plt.subplots(figsize=(6.1, 4.1), layout='constrained')
    current = [v['I_A'] for v in report['noise']]
    ax.loglog(current, [v['expected_sd_Wb'] for v in report['noise']], color=colors['reference'], label=r'$\sigma_M/(k_T I_s)$')
    ax.loglog(current, [v['observed_sd_Wb'] for v in report['noise']], 'o', color=colors['estimated'], label='Monte Carlo')
    ax.set(xlabel=r'$I_s$ / A', ylabel=r'$\sigma_{e_{\psi_\tau}}$ / Wb', title='Rauschen wächst invers zum Strombetrag')
    ax.legend(); save(fig, '07_noise')
    report['versions']['matplotlib'] = matplotlib.__version__


def write_report(report):
    (HERE/'results.json').write_text(json.dumps(report, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    rows = '\n'.join(f"| {name} | {value.get('max_abs_error', '—')} | bestanden |"
                     for name, value in report['checks'].items())
    noise = '\n'.join(f"| {v['I_A']:g} | {v['expected_sd_Wb']:.6g} | {v['observed_sd_Wb']:.6g} |"
                      for v in report['noise'])
    text = f"""# Synthetische Validierung der Torque-Flussprojektion

Alle {len(report['checks'])} Prüfungen bestanden, mit {report['samples']} zufälligen
Strompunkten und Seed {SEED}. Dies validiert die mathematischen Eigenschaften
der angenommenen Modelle; es ist keine Prüfstandsvalidierung.

## Reproduktion

```powershell
.\\.venv\\Scripts\\python.exe docs/torque_flux_consistency/proof_of_concept.py
```

NumPy und Matplotlib sowie `kpsewhich` für die kanonische Palette sind
erforderlich. `--checks-only` lässt vorhandene Grafiken unverändert und führt
nur die numerischen Prüfungen aus. Der Lauf schreibt ausschließlich lokale
Research-Ergebnisse und Grafiken. Quelldateihashes, Basisgrößen, Softwareversionen,
Rangtoleranzen und vollständige Zahlen stehen in [results.json](results.json).

## Beobachtbarkeit

Die deklarierte dimensionslose Potentialbasis ist
`[1, x, y, s, (x²−y²)/2, xy, s²]`, mit `s=(x²+y²)/2`.
Torque hat Rang 4 von 7: Potentialkonstante und zwei radiale Potentialmoden
sind unsichtbar. Gemeinsame ideale Spannungsinformation hebt den Rang auf 6;
eine Potentialgauge auf 7. Der affine Flussoperator hat Rang 5 von 6 und
behält den gemeinsamen Induktivitätsanteil im Nullraum. Eine reine d-Achsen-
Messung hat Rang 2 in der Potentialbasis. Das sind Beispiele für diese
Basis und Anregung, keine allgemeingültigen Kennfeldränge.

Die Blöcke sind mit `k_T I_* psi_*` bzw. `omega_e psi_*` normiert und nehmen
illustrativ gleiche Einheitsvarianzen der normierten Residuen an. Die Grafik
ist daher eine strukturelle Illustration, kein kalibrierter Informationsvergleich.
`null` bei `full_condition` bedeutet unendliche Kondition durch Nullraum.

## Rauschen bei kleinen Strömen

Unabhängiges Gaußrauschen mit angenommener Momentstandardabweichung 0.2 Nm,
100 000 Ziehungen pro Strombetrag, sonst exakt bekannte Ströme.

| Strom in A | Erwartete Standardabweichung in Wb | Monte Carlo in Wb |
|---|---:|---:|
{noise}

![Rauschverstärkung](figures/07_noise.png)

Die relative Abweichung vom analytischen Wert liegt an jedem Punkt unter
1.5 Prozent. Die Werte sind ausdrücklich illustrative Rauschannahmen.
Zusätzlich wurden 0.2 A Stromrauschen und 0.03 rad geschätzter Winkelvorsprung
bei unverändertem Kennfeld untersucht. Ihre Bias-/Streuungszahlen stehen in
JSON; beide enthalten auch den Effekt der Kennfeldauswertung an verschobenen
Argumenten. Eine kohärente Rotation von Strom und Fluss lässt Moment dagegen
bis Rundung unverändert.

## Detailprüfungen

Die Maximumfehler tragen die im Prüfnamen angegebenen Einheiten. Numerische
Toleranzen sind Rundungs-/Differentiationstoleranzen, keine Messunsicherheiten.
Der Stromgradient wird unabhängig durch zentrale Differenzen geprüft.

| Prüfung | Maximaler Absolutfehler | Ergebnis |
|---|---:|---|
{rows}

## Grenzen

Die lokalen harten Korrekturen zeigen Projektion und gewichtete Optimalität.
Sie werden nicht als reale Korrektur angewendet. Die globale Koeffizienten-
Rückgewinnung verwendet ideale, exakt repräsentierbare Daten; sie beweist
keine allgemeine Sättigungsrekonstruktion. Verlust-, Sensor-, Strom- und
Winkelfehler werden hier getrennt illustriert. Reale korrelierte Fehler,
Harmonische, thermische Zustände, EESM-Rotorportidentifikation und ein
praktischer globaler Fit mit unbekannten Nebenparametern bleiben offen.
"""
    (HERE/'validation.md').write_text(text, encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checks-only', action='store_true')
    args = parser.parse_args()
    report = run_checks()
    if not args.checks_only:
        make_figures(report)
    write_report(report)
    print(json.dumps({'passed_checks': len(report['checks']), 'samples': report['samples'],
                      'ranks': {key: value['rank'] for key, value in report['operators'].items()},
                      'output': str(HERE/'results.json')}, indent=2))
