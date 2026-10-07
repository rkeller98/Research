"""Reproduce the split papers using only portable research fixtures.

No raw MAT, external repository, GUI, or absolute local data path is required.
"""
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
from scipy.interpolate import LinearNDInterpolator
from scipy.spatial import Delaunay

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared/python"))
from canonical_dataset import load_dataset
from coenergy_mesh import AffineMesh
from potential_splines import solve, predict, design, Z
from publication_plotting import configure


def save_report(paper, result):
    path = ROOT / "papers" / paper / "numerics/real_evaluation.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    table = None
    if paper == "flux_correction_symmetry":
        table = [r"\begin{tabular}{rrrrr}",r"\toprule",r"Reference / $^\circ$C & Candidates & Supported & $r_d$ RMS & $r_q$ RMS\\",r"\midrule"]
        for s in result["slices"]:
            table.append(f'{s["source"]["temp"]} & {s["candidate_pairs"]} & {s["supported_pairs"]} & {s["forbidden_rms_mWb"][0]:.3f} & {s["forbidden_rms_mWb"][1]:.3f} '+r"\\")
    elif paper == "magnetic_coenergy_consistency":
        table = [r"\begin{tabular}{rrrrrr}",r"\toprule",r"Ref. / $^\circ$C & Curl all & Curl cond.$\le10$ & Paths & Path RMS & Green error\\",r"\midrule"]
        for s in result["slices"]:
            table.append(f'{s["source"]["temp"]} & {s["curl_area_weighted_rms_mH"]:.3f} & {s["curl_condition10_rms_mH"]:.3f} & {s["path_count"]} & {s["path_rms_J"]:.3f} & {s["green_max_error_J"]:.1e} '+r"\\")
    elif paper == "flux_correction_coenergy":
        table = [r"\begin{tabular}{lrrrr}",r"\toprule",r"Fit & Tuning RMS & Sample RMS & Parity RMS & Curl RMS\\",r"\midrule"]
        for s in result["results"]:
            table.append(f'{s["mode"]} & {s["spatial_holdout_rms_mWb"]:.3f} & {s["raw_sample_fit_rms_mWb"]:.3f} & {s["parity_rms_mWb"]:.3f} & {s["curl_rms_mH"]:.3f} '+r"\\")
    elif paper == "torque_flux_consistency":
        table = [r"\begin{tabular}{rrrrr}",r"\toprule",r"Speed / rpm & OPs & Torque RMS & Flux RMS & Median torque SD\\",r"\midrule"]
        for s in result["slices"]:
            table.append(f'{s["rpm"]} & {s["points"]} & {s["torque_rms_Nm"]:.3f} & {s["normalized_flux_rms_mWb"]:.3f} & {s["median_torque_std_Nm"]:.3f} '+r"\\")
    if table:
        table += [r"\bottomrule",r"\end{tabular}"]
        output = ROOT / "papers" / paper / "figures/data/real_metrics.tex"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text("\n".join(table)+"\n", encoding="utf-8")


def fixture(dataset, temp=None, rpm=None):
    d, m = load_dataset(dataset)
    mask = np.ones(len(d["id"]), dtype=bool)
    if temp is not None:
        mask &= d["rotor_temp_ref"] == temp
    if rpm is not None:
        mask &= d["rpm_req"] == rpm
    return {k: v[mask] for k, v in d.items()}, dict(dataset=dataset, csv_sha256=m["csv_sha256"], temp=temp, rpm=rpm)


def points(d):
    p = np.column_stack([d["id"], d["iq"]])
    f = np.column_stack([d["psi_d"], d["psi_q"]])
    return p, f


def figure(fig, paper, name):
    import matplotlib.pyplot as plt
    path = ROOT / "papers" / paper / "figures" / name
    path.parent.mkdir(exist_ok=True)
    fig.savefig(path.with_suffix(".pdf"), bbox_inches="tight", metadata={"CreationDate": None, "ModDate": None})
    preview = ROOT / "tmp/portfolio_figures"
    preview.mkdir(parents=True, exist_ok=True)
    fig.savefig(preview / f"{paper}_{name}.png", bbox_inches="tight")
    plt.close(fig)


def parity():
    import matplotlib.pyplot as plt
    colors = configure()
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 2.7), layout="constrained")
    report = []
    for temp, role in [(30, "reference"), (70, "estimated")]:
        d, source = fixture("psm_temperature_2500", temp)
        p, f = points(d)
        interp = LinearNDInterpolator(p, f)
        # Only positive q is an independent representative; reflected arguments
        # use actually measured coordinates. No requested-key geometry is assumed.
        candidate = p[:, 1] > .1 * np.max(abs(p[:, 1]))
        pm = p[candidate] * [1, -1]
        fm = interp(pm)
        valid = np.isfinite(fm).all(axis=1)
        pp, ff, fm = p[candidate][valid], f[candidate][valid], fm[valid]
        forbidden = .5*np.column_stack([ff[:, 0]-fm[:, 0], ff[:, 1]+fm[:, 1]])
        projected = ff - forbidden
        projected_mirror = fm - forbidden*np.array([-1, 1])
        assert np.max(abs(projected[:, 0]-projected_mirror[:, 0])) < 1e-12
        assert np.max(abs(projected[:, 1]+projected_mirror[:, 1])) < 1e-12
        output = ROOT / "papers/flux_correction_symmetry/figures/data" / f"real_projection_{temp}.csv"
        values = np.column_stack([pp, ff, fm, projected, projected_mirror, forbidden])
        np.savetxt(output, values, delimiter=",", fmt="%.17g", comments="",
                   header="id_A,iq_A,raw_psi_d_Wb,raw_psi_q_Wb,mirror_psi_d_Wb,mirror_psi_q_Wb,projected_psi_d_Wb,projected_psi_q_Wb,projected_mirror_psi_d_Wb,projected_mirror_psi_q_Wb,removed_psi_d_Wb,removed_psi_q_Wb")
        entry = dict(source=source, points=len(p), candidate_pairs=int(candidate.sum()),
                     supported_pairs=len(pp), forbidden_rms_mWb=(1000*np.sqrt(np.mean(forbidden**2, axis=0))).tolist(),
                     method="P1 mirror interpolation on measured-current hull; positive q representatives",
                     pointwise_output=output.relative_to(ROOT).as_posix())
        report.append(entry)
        for j, ax in enumerate(axes):
            ax.scatter(pp[:, 1], forbidden[:, j]*1000, s=10, alpha=.7, color=colors[role], label=f"{temp} °C reference")
            ax.set(xlabel="$i_q$ / A", ylabel=("$r_d$" if j == 0 else "$r_q$")+" / mWb")
            ax.axhline(0, color=colors["guide"], lw=.8)
    axes[0].legend()
    figure(fig, "flux_correction_symmetry", "real_projection")
    save_report("flux_correction_symmetry", dict(slices=report, limitation="Interpolation errors are correlated; zero projected residual is structural"))


def coenergy():
    import matplotlib.pyplot as plt
    colors = configure()
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 2.7), layout="constrained")
    reports = []
    for temp, role in [(30, "reference"), (70, "estimated")]:
        d, source = fixture("psm_temperature_2500", temp)
        p, f = points(d)
        anchor = p[np.argsort(np.linalg.norm(p, axis=1))[:5]].mean(axis=0)
        mesh = AffineMesh(p-anchor, f)
        condition = np.linalg.cond(mesh.vertices[:, :2]-mesh.vertices[:, 2, None])
        good = condition <= 10
        weighted_rms = lambda mask: float(np.sqrt(np.sum(mesh.area[mask]*mesh.curl[mask]**2)/np.sum(mesh.area[mask])))
        path_values = []
        green_error = 0.
        for location in (p-anchor)[::3]:
            if np.any(abs(location) < .1*np.max(abs(p-anchor), axis=0)):
                continue
            try:
                wa, wb = mesh.paths(*location)
                green = mesh.rectangle_curl(*location)
                green_error = max(green_error, abs(wa-wb-green))
                assert abs(wa-wb-green) < 2e-9
                path_values.append([*location, wa-wb])
            except ValueError:
                continue
        v = np.asarray(path_values)
        if not len(v):
            raise AssertionError("No supported closed path")
        entry = dict(source=source, points=len(p), triangles=len(mesh.area),
                     retained_condition10_triangles=int(good.sum()),
                     curl_area_weighted_rms_mH=weighted_rms(np.ones(len(good), bool))*1000,
                     curl_condition10_rms_mH=weighted_rms(good)*1000,
                     path_count=len(v), path_rms_J=float(np.sqrt(np.mean(v[:, 2]**2))),
                     path_median_abs_J=float(np.median(abs(v[:, 2]))),
                     green_max_error_J=green_error, anchor_A=anchor.tolist())
        reports.append(entry)
        axes[0].scatter(v[:, 0], v[:, 2], s=12, color=colors[role], label=f"{temp} °C reference")
        axes[1].scatter(condition, mesh.curl*1000, s=8, alpha=.5, color=colors[role])
    axes[0].set(xlabel="$i_d-i_{d,0}$ / A", ylabel="$W'_1-W'_2$ / J")
    axes[0].legend()
    axes[1].set(xscale="log", xlabel="Triangle condition", ylabel="$r_{curl}$ / mH")
    axes[1].axvline(10, color=colors["guide"], linestyle="--")
    figure(fig, "magnetic_coenergy_consistency", "real_integrability")
    # Independent analytic reference: affine conservative field and parity-only
    # counterexample. Exact P1 interpolation reproduces affine fields.
    grid = np.array([(x,y) for x in np.linspace(-1,1,9) for y in np.linspace(-1,1,9)])
    affine = AffineMesh(grid, np.column_stack([1+.6*grid[:,0], grid[:,1]]))
    assert np.max(abs(affine.curl)) < 1e-12
    assert abs(np.subtract(*affine.paths(.6, .7))) < 1e-12
    save_report("magnetic_coenergy_consistency", dict(slices=reports, affine_reference="passed", interpretation="Measured terminal-current P1 reconstruction is inconsistent; no cause or continuum error bound inferred"))


def reconstruction():
    import matplotlib.pyplot as plt
    colors = configure()
    d, source = fixture("psm_temperature_2500", 30)
    p, f = points(d)
    center = np.array([.5*(p[:,0].min()+p[:,0].max()), 0.])
    scales = np.array([.5*np.ptp(p[:,0]), np.max(abs(p[:,1]))])*1.001
    ibase = float(np.max(scales))
    psibase = .1
    # Cover the basis domain in both axes. Derivatives must include the
    # anisotropic coordinate chain rule: Wbase = psibase*ibase.
    x, z = (p-center)/scales, f*scales/(psibase*ibase)
    # A deterministic spatial holdout removes complete reflection-related bins,
    # keeping mirrored measurements in the same fold. No raw time-record split.
    bins = np.floor((x[:,0]+1)*8).astype(int)+3*np.floor(abs(x[:,1])*8).astype(int)
    test = bins % 5 == 0
    train = ~test
    hull = Delaunay(x[train])
    supported = test & (hull.find_simplex(x) >= 0)
    assert supported.sum() >= 10
    results, fits = [], {}
    for mode in ["Independent", "Parity", "Potential"]:
        candidates = []
        for lam in [0., 1e-6, 1e-5, 1e-4, 1e-3]:
            fit = solve(x[train], z[train], mode, lam)
            pred, _ = predict(fit, x[supported])
            candidates.append((float(np.sqrt(np.mean(((pred-z[supported])*psibase*ibase/scales)**2))), lam))
        score, lam = min(candidates)
        fit = solve(x, z, mode, lam)
        pred, hessian = predict(fit, x)
        mirror, _ = predict(fit, x*[1,-1])
        parity = .5*np.column_stack([pred[:,0]-mirror[:,0],pred[:,1]+mirror[:,1]])
        curl = hessian[:,1,0]-hessian[:,0,1]
        results.append(dict(mode=mode, penalty=lam, spatial_holdout_rms_mWb=score*1000,
            raw_sample_fit_rms_mWb=float(np.sqrt(np.mean(((pred-z)*psibase*ibase/scales)**2))*1000),
            parity_rms_mWb=float(np.sqrt(np.mean((parity*psibase*ibase/scales)**2))*1000),
            curl_rms_mH=float(np.sqrt(np.mean(curl**2))*psibase*ibase/np.prod(scales)*1000)))
        fits[mode] = pred*psibase*ibase/scales
        if mode == "Potential":
            assert np.max(abs(curl)) == 0 and np.max(abs(parity)) < 1e-12
    gradient = np.vstack([design(x,1,0,1),design(x,0,1,1)])@Z
    rank = int(np.linalg.matrix_rank(gradient))
    assert rank == Z.shape[1]
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 2.7), layout="constrained")
    for j, ax in enumerate(axes):
        ax.scatter(p[:,1], f[:,j]*1000, s=12, color=colors["reference"], alpha=.45, label="raw")
        ax.scatter(p[:,1], fits["Potential"][:,j]*1000, s=9, color=colors["estimated"], label="potential fit")
        ax.set(xlabel="$i_q$ / A", ylabel=("$\\psi_d$" if j==0 else "$\\psi_q$")+" / mWb")
    axes[0].legend()
    figure(fig, "flux_correction_coenergy", "real_reconstruction")
    save_report("flux_correction_coenergy", dict(source=source, points=len(p), train_count=int(train.sum()),
        holdout_count=int(test.sum()), supported_holdout_count=int(supported.sum()),
        current_base_A=ibase, current_axis_scales_A=scales.tolist(), current_center_A=center.tolist(),
        flux_base_Wb=psibase, rank=rank, gauge_fixed_columns=Z.shape[1],
        results=results, selection="spatial holdout selects lambda; score is tuning error, not an independent final test",
        limit="No true flux reference; discarded residual is not identified measurement error"))
    # Raw and reconstructed values remain available separately at every OP.
    path = ROOT / "papers/flux_correction_coenergy/figures/data/real_fit.csv"
    np.savetxt(path, np.column_stack([p,f,fits["Potential"],f-fits["Potential"]]), delimiter=",", fmt="%.17g", comments="",
               header="id,iq,psi_d_raw,psi_q_raw,psi_d_fit,psi_q_fit,residual_d,residual_q")


def torque():
    import matplotlib.pyplot as plt
    colors = configure()
    d, source = fixture("psm_dual_system_multirpm")
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 2.7), layout="constrained")
    reports = []
    for rpm, role in [(1000,"reference"),(3000,"estimated")]:
        mask = d["rpm_req"] == rpm
        v = {k:a[mask] for k,a in d.items()}
        mag = np.hypot(v["id"],v["iq"])
        selected = mag >= .1*np.max(mag)
        em = v["torque_map"]-v["torque"]
        epsi = em[selected]/(v["kt"][selected]*mag[selected])
        assert np.all(v["kt"] == 12)
        reports.append(dict(rpm=rpm, points=len(mag), normalized_points=int(selected.sum()),
            torque_bias_Nm=float(em.mean()), torque_rms_Nm=float(np.sqrt(np.mean(em**2))),
            normalized_flux_rms_mWb=float(np.sqrt(np.mean(epsi**2))*1000),
            median_torque_std_Nm=float(np.median(v["torque_std"]))))
        axes[0].scatter(v["torque_map"],v["torque"],s=12,color=colors[role],label=f"{rpm} rpm")
        axes[1].scatter(mag[selected],epsi*1000,s=12,color=colors[role])
    axes[0].plot([-75,75],[-75,75],color=colors["guide"],linestyle="--",label="equal values")
    axes[0].set(xlabel="$M_{map}$ / Nm, $k_T=3p$",ylabel="$M_{CAN}$ / Nm")
    axes[0].legend()
    axes[1].set(xlabel="$I_s$ / A",ylabel="$e_\\psi$ / mWb")
    figure(fig,"torque_flux_consistency","real_torque")
    save_report("torque_flux_consistency",dict(source=source,slices=reports,
        phase_selector=1,systems=2,kt=12,nominal_pole_pairs=4,
        evidence="Recorded selector and MeasEval phase-system interpretation; unity CAN gain retained",
        limit="CAN indication is not calibrated electromagnetic truth; equal represented system currents assumed"))


def identifiability():
    d, source = fixture("psm_dual_system_multirpm")
    i = np.column_stack([d["id"],d["iq"]])
    J = np.array([[0.,-1.],[1.,0.]])
    resistance_column = (i@J.T/d["omega_e"][:,None]).reshape(-1)
    # A nuisance voltage error -a*i has exactly the same reconstruction
    # sensitivity as a used-minus-true resistance error, on measured support.
    nuisance_column = resistance_column.copy()
    S = np.column_stack([resistance_column,nuisance_column])
    assert np.linalg.matrix_rank(S) == 1
    offset_columns = np.column_stack([
        np.tile([0.,-1.],(len(i),1))/d["omega_e"][:,None],
        np.tile([1.,0.],(len(i),1))/d["omega_e"][:,None]])
    offset_columns = np.stack([offset_columns[:,:2].reshape(-1),offset_columns[:,2:].reshape(-1)],axis=1)
    augmented = np.column_stack([S,offset_columns])
    assert np.linalg.matrix_rank(augmented) == 3
    save_report("flux_error_identifiability",dict(source=source,points=len(i),
        resistance_voltage_nuisance_rank=1, columns=2, offset_augmented_rank=3,
        augmented_columns=4, singular_values=np.linalg.svd(S,compute_uv=False).tolist(),
        interpretation="Real support checks a mathematical exact confounder; no sensor error is estimated"))


if __name__ == "__main__":
    parity()
    coenergy()
    reconstruction()
    torque()
    identifiability()
    print("Portable parity, Green, potential-fit and torque evaluations passed.")
