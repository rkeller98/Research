"""Torque observability and conditional CAN comparison; never changes input data.

Run with the repository Python environment from any working directory.
The CAN channel has no verified unit/sensor definition. All real torque numbers
assume its recorded sign, unity gain, and Nm; they are not electromagnetic truth.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

import h5py
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
ROOT = PAPER.parents[1]
OUT = PAPER / "figures/data/torque"
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(PAPER / "python"))
from raw_ww_data_importer import RawDataImporter
from flux_correction import build_ww_measurement_slice, FluxMapSymmetryAnalyzer


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


POC_PATH = ROOT / "docs/torque_flux_consistency/proof_of_concept.py"
poc = load_module(POC_PATH, "torque_poc")


def stats(v):
    v = np.asarray(v, dtype=float)
    v = v[np.isfinite(v)]
    return dict(n=len(v), bias=float(v.mean()), mae=float(abs(v).mean()),
                rmse=float(np.sqrt(np.mean(v*v))), median=float(np.median(v)),
                q05=float(np.quantile(v, .05)), q25=float(np.quantile(v, .25)),
                q75=float(np.quantile(v, .75)), q95=float(np.quantile(v, .95)))


def metadata(path):
    raw = RawDataImporter(path)
    names = raw.get_signal_names()
    with h5py.File(path) as f:
        y = raw._find_measurement_group(f)
        selected = {}
        for name in names:
            if not any(s in name.lower() for s in ("torque", "temp", "exc", "rpm", "speed")):
                continue
            idx = names.index(name)
            a = raw.get_signal(name)
            fields = {}
            for key in ("Unit", "Description", "Device", "Path", "Raster", "XIndex"):
                data = f[y[key][idx, 0]][()]
                if key == "XIndex":
                    fields[key] = np.asarray(data).reshape(-1).tolist()
                else:
                    fields[key] = "".join(chr(int(v)) for v in data.reshape(-1)).strip("\x00 ")
            selected[name] = dict(fields=fields, n=len(a), finite=int(np.isfinite(a).sum()),
                                  minimum=float(a.min()), maximum=float(a.max()),
                                  unique=len(np.unique(a)))
        group = y.parent
        clock = group["X/Data"][()].reshape(-1)
        clock_unit = "".join(chr(int(v)) for v in group["X/Unit"][()].reshape(-1)).strip("\x00 ")
        general = {}
        def collect(name, node):
            if isinstance(node, h5py.Dataset):
                values = node[()].reshape(-1)
                if values.dtype.kind in "ui" and len(values) > 1:
                    general[name] = "".join(chr(int(v)) for v in values).strip("\x00 ")
                else:
                    general[name] = str(values.tolist())
        group["Description"].visititems(collect)
    return dict(sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                signal_names=names, selected=selected, recording_description=general,
                clock=dict(unit=clock_unit, n=len(clock), increasing=bool(np.all(np.diff(clock)>0)),
                           minimum_step=float(np.diff(clock).min()),
                           maximum_step=float(np.diff(clock).max())))


def analyze(path, rpm, temp):
    raw = RawDataImporter(path)
    measurement = build_ww_measurement_slice(raw, rpm, temp)
    mask = np.isclose(raw.get_signal("PE_Rpm_req"), rpm) & np.isclose(raw.get_signal("Rotor_temp_ref"), temp)
    samples = pd.DataFrame({
        "op_index": raw.get_signal("PE_Index_Flx_Char_StatorCurrent_OP_param_none")[mask],
        "can": raw.get_signal("CAN_Torque_meas")[mask],
        "speed": raw.get_signal("PE_speed_rpm")[mask],
        "exc": raw.get_signal("I_exc_meas")[mask],
        "id": raw.get_signal("PE_Id_meas_avg")[mask], "iq": raw.get_signal("PE_Iq_meas_avg")[mask],
        "ud": raw.get_signal("PE_Ud_meas_avg")[mask], "uq": raw.get_signal("PE_Uq_meas_avg")[mask],
    })
    assert np.isfinite(samples.to_numpy()).all()
    grouped = samples.groupby("op_index")
    extra = grouped[["can", "speed", "exc"]].mean()
    extra["can_sd"] = grouped["can"].std()
    extra["speed_sd"] = grouped["speed"].std()
    extra["n_raw"] = grouped.size()
    pts = FluxMapSymmetryAnalyzer(measurement).flux_points.merge(extra, on="op_index", validate="one_to_one")
    kt = 1.5*measurement.pole_pairs
    pts["I"] = np.hypot(pts.id, pts.iq)
    pts["angle_deg"] = np.degrees(np.arctan2(pts.iq, pts.id))
    pts["map"] = kt*(pts.psi_d*pts.iq-pts.psi_q*pts.id)
    pts["eM"] = pts["map"]-pts.can
    threshold = .10*pts.I.max()
    pts["valid"] = pts.I > threshold
    pts["epsi_mWb"] = np.nan
    pts.loc[pts.valid, "epsi_mWb"] = 1000*pts.loc[pts.valid, "eM"]/(kt*pts.loc[pts.valid, "I"])
    # Requested labels only for the matched-speed descriptive comparison.
    pts["id_key"], pts["iq_key"] = pts.id_req.round(2), pts.iq_req.round(2)
    # Sensitivities preserve signs, resistance and all OP groups.
    sample_map = kt*(samples.ud*samples.id + samples.uq*samples.iq
                     -measurement.stator_resistance*(samples.id**2+samples.iq**2))/measurement.omega_e
    mean_product = sample_map.groupby(samples.op_index).mean()
    product_difference = mean_product.loc[pts.op_index].to_numpy()-pts["map"].to_numpy()
    actual_omega = 2*np.pi*measurement.pole_pairs*pts.speed/60
    pts["map_actual_speed"] = pts["map"]*measurement.omega_e/actual_omega
    metrics = dict(rpm=rpm, rotor_reference_C=temp, raw_samples=len(samples), operating_points=len(pts),
                   unique_requested_keys=len(pts.groupby(["id_key", "iq_key"])),
                   p=measurement.pole_pairs, used_resistance_ohm=measurement.stator_resistance,
                   Imax_A=float(pts.I.max()), Imin_A=float(threshold), normalized_retained=int(pts.valid.sum()),
                   eM_conditional_Nm=stats(pts.eM), epsi_conditional_mWb=stats(pts.epsi_mWb),
                   recorded_speed_rpm=stats(samples.speed), speed_deviation_rpm=stats(samples.speed-rpm),
                   within_OP_CAN_sd_conditional_Nm=stats(extra.can_sd),
                   within_OP_speed_sd_rpm=stats(extra.speed_sd),
                   excitation_numeric_range=[float(samples.exc.min()), float(samples.exc.max())],
                   mean_product_difference_conditional_Nm=stats(product_difference),
                   actual_speed_change_conditional_Nm=stats(pts.map_actual_speed-pts["map"]),
                   sensitivity_thresholds={str(r):stats(1000*pts.loc[pts.I>r*pts.I.max(), "eM"]/
                                                        (kt*pts.loc[pts.I>r*pts.I.max(), "I"]))
                                           for r in (.05, .10, .15, .20)},
                   signs={"map_positive":int((pts["map"]>0).sum()), "map_negative":int((pts["map"]<0).sum()),
                          "CAN_positive":int((pts.can>0).sum()), "CAN_negative":int((pts.can<0).sum())})
    ratio_support=abs(pts["map"])>=10.
    metrics["descriptive_CAN_over_map"] = dict(min_abs_map_Nm=10., **stats(pts.loc[ratio_support,"can"]/pts.loc[ratio_support,"map"]))
    pts.to_csv(OUT/f"points_{rpm}.csv", index=False, float_format="%.12g")
    return pts, metrics


def synthetic():
    report = poc.run_checks()  # All forty original checks, unchanged.
    extra = {}
    def check(name, condition):
        assert condition, name
        extra[name] = {"passed": True}
    i = np.array([[0.,100.],[0.,-100.],[100.,0.],[-100.,0.],
                  [60.,80.],[-60.,80.],[-60.,-80.],[60.,-80.]])
    I, ni, nt = poc.directions(i)
    psi = poc.flux(i)
    check("axis_id_zero", np.allclose(poc.torque(i[:2],psi[:2]), poc.KT*i[:2,1]*psi[:2,0]))
    check("axis_iq_zero", np.allclose(poc.torque(i[2:4],psi[2:4]), -poc.KT*i[2:4,0]*psi[2:4,1]))
    normal = poc.torque(i,psi+.005*nt)-poc.torque(i,psi)
    radial = poc.torque(i,psi+.008*ni)-poc.torque(i,psi)
    mixed = poc.torque(i,psi+.008*ni+.005*nt)-poc.torque(i,psi)
    check("four_quadrants_normal_observable", np.allclose(normal,poc.KT*I*.005))
    check("four_quadrants_radial_invisible", np.allclose(radial,0,atol=1e-12))
    check("four_quadrants_mixed_projection", np.allclose(mixed,normal))
    check("positive_negative_torque", np.any(poc.torque(i,psi)>0) and np.any(poc.torque(i,psi)<0))
    tiny = np.array([[1e-9,0.],[0.,1e-9]])
    check("small_current_torque_continuous", np.max(abs(poc.torque(tiny,poc.flux(tiny))))<1e-8)
    check("origin_torque_zero", float(poc.torque(np.zeros(2),poc.flux(np.zeros(2))))==0)
    # Positive isotropic inductance perturbation: reciprocal, parity-preserving,
    # positive semidefinite added Hessian, but globally invisible to torque.
    L0 = .0001
    check("reciprocal_isotropic_radial_null", np.allclose(poc.torque(i,psi+L0*i),poc.torque(i,psi)))
    check("radial_even_potential_and_positive_curvature", np.allclose(np.diag([L0,L0]),np.diag([L0,L0]).T)
          and np.all(np.linalg.eigvalsh(np.diag([L0,L0]))>0))
    # A conservative constant d-flux error has a nonconservative normal-only
    # representative; finite differences independently test the manuscript caveat.
    def normal_projection(z):
        a=np.array([z[1],-z[0]])
        return a*z[1]/np.dot(z,z)
    z=np.array([.6,.8]); h=1e-5
    dq=(normal_projection(z+[0,h])-normal_projection(z-[0,h]))/(2*h)
    dd=(normal_projection(z+[h,0])-normal_projection(z-[h,0]))/(2*h)
    check("pointwise_minimum_change_need_not_preserve_curl",abs(dd[1]-dq[0])>.1)
    # f(s,e)=e*s: symmetric 3-current Hessian including cross derivatives.
    xd,xq,exc=.6,.8,2.
    Hessian=np.array([[exc,0.,xd],[0.,exc,xq],[xd,xq,0.]])
    check("three_current_reciprocity_radial_excitation_family",
          np.allclose(Hessian,Hessian.T) and np.isclose(xq*(exc*xd)-xd*(exc*xq),0.))
    grid = np.array([(x,y) for x in np.linspace(-1,1,13) for y in np.linspace(-1,1,13)])
    hm, gu, gauge = poc.potential_operators(grid)
    columns = [0,1,3,4,6]  # Even in q: [1,x,s,(x²-y²)/2,s²].
    ops = {"torque":poc.spectrum(hm[:,columns]),
           "torque_voltage":poc.spectrum(np.vstack([hm[:,columns],gu[:,columns]])),
           "torque_voltage_gauge":poc.spectrum(np.vstack([hm[:,columns],gu[:,columns],gauge[:,columns]]))}
    check("even_reciprocal_torque_rank_two_of_five",ops["torque"]["rank"]==2)
    check("even_reciprocal_joint_rank_four_gauge_five",ops["torque_voltage"]["rank"]==4
          and ops["torque_voltage_gauge"]["rank"]==5)
    for omega in (-100.,100.):
        x,y=i[-1]
        A=np.array([[0.,-omega,x],[omega,0.,y],[poc.KT*y,-poc.KT*x,0.]])
        check(f"joint_local_rank_signed_speed_{omega:g}",
              np.isclose(np.linalg.det(A),-poc.KT*omega*(x*x+y*y)) and np.linalg.matrix_rank(A)==3)
    # Excitation may change both stator fluxes; it does not enter stator I_s.
    for excitation in (0.,2.):
        esm=psi+np.column_stack([np.full(len(i),.01*excitation),np.zeros(len(i))])
        check(f"excitation_slice_radial_null_{excitation:g}",
              np.allclose(poc.torque(i,esm+L0*i),poc.torque(i,esm)))
    report["additional_checks"]=extra
    report["even_potential_operators"]=ops
    report["total_passed"]=len(report["checks"])+len(extra)
    return report


def figures(points, matched):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    sys.path.insert(0,str(ROOT/"shared/python"))
    from publication_plotting import configure
    c=configure()
    def save(fig,name):
        fig.savefig(PAPER/f"figures/{name}.pdf",bbox_inches="tight",
                    metadata={"CreationDate":None,"ModDate":None})
        qa=ROOT/"tmp/torque_paper_figures"
        qa.mkdir(parents=True,exist_ok=True)
        fig.savefig(qa/f"{name}.png",bbox_inches="tight",dpi=180)
        plt.close(fig)
    # Dimensionless local geometry; figure content generated rather than exported.
    fig,axes=plt.subplots(1,2,figsize=(7.0,3.2),layout="constrained")
    ni=np.array([.6,.8]); nt=np.array([.8,-.6])
    ax=axes[0]
    for v,label,color in [(ni,r"$n_i$",c["reference"]),(nt,r"$n_\tau$",c["torque"])]:
        ax.annotate("",xy=v,xytext=(0,0),arrowprops=dict(arrowstyle="->",color=color,lw=1.8))
        ax.text(*(1.1*v),label)
    psi=.8*ni+.5*nt
    ax.plot([0,psi[0]],[0,psi[1]],color=c["derived"])
    ax.plot([psi[0],.5*nt[0]],[psi[1],.5*nt[1]],"--",color=c["guide"])
    ax.scatter(*psi,color=c["derived"],marker="s"); ax.text(*(psi+[-.1,.1]),r"$\psi$")
    ax.text(*(.5*nt+[.05,0]),r"$\psi_\tau n_\tau$")
    ax.set(xlim=(-.15,1.2),ylim=(-.85,1.1),title="(a) Current-dependent projection",
           xlabel="d component / chosen base",ylabel="q component / chosen base")
    ax=axes[1]
    old=.8*ni+.5*nt; closest=.8*ni+.2*nt
    t=np.linspace(-.4,1.3,100); line=t[:,None]*ni+.2*nt
    ax.plot(*line.T,"--",color=c["reference"],label="Equal reference torque")
    ax.scatter(*old,marker="s",color=c["estimated"],label="Map flux")
    ax.scatter(*closest,marker="o",facecolors="none",edgecolors=c["derived"],label="Minimum change")
    ax.annotate("",xy=closest,xytext=old,arrowprops=dict(arrowstyle="->",color=c["torque"],lw=1.8))
    other=closest+.3*ni
    ax.scatter(*other,marker="^",color=c["highlight"],label="Radial alternative")
    ax.plot([closest[0],other[0]],[closest[1],other[1]],":",color=c["highlight"])
    ax.set(xlim=(-.3,1.3),ylim=(-.65,1.2),title="(b) Underdetermined correction",
           xlabel="d flux / chosen base",ylabel="q flux / chosen base")
    ax.legend(loc="upper left",bbox_to_anchor=(0,-.22),ncols=2,fontsize=7)
    for ax in axes: ax.set_aspect("equal",adjustable="box")
    save(fig,"06_torque_geometry")
    fig,axes=plt.subplots(1,2,figsize=(7.0,3.1),layout="constrained")
    angle=np.linspace(-180,180,181); rad=np.radians(angle)
    i=100*np.column_stack([np.cos(rad),np.sin(rad)]); I,ni,nt=poc.directions(i)
    psi=poc.flux(i)
    normal=5*np.sin(2*rad)
    for error,label,style,color in [(8*ni,"Radial 8 mWb",":",c["reference"]),
                                  (normal[:,None]*nt,"Normal error","-",c["torque"]),
                                  (8*ni+normal[:,None]*nt,"Mixed error","--",c["derived"])]:
        residual=(poc.torque(i,psi+error/1000)-poc.torque(i,psi))/(poc.KT*I)*1000
        axes[0].plot(angle,residual,style,color=color,label=label)
    axes[0].set(xlabel="Current angle (deg)",ylabel=r"$e_{\psi_\tau}$ (mWb)",title="(a) Only the normal error survives")
    axes[0].legend(fontsize=7,loc="upper right")
    amps=np.geomspace(.1,100,100); sd=1000*.2/(poc.KT*amps)
    axes[1].loglog(amps,sd,color=c["reference"],label="Analytic conversion")
    report=poc.run_checks()
    noise=report["noise"]
    # Original Monte Carlo output uses a list of current/noise records.
    for row in noise:
        axes[1].plot(row["I_A"],1000*row["observed_sd_Wb"],"o",mfc="none",color=c["derived"])
    axes[1].plot([],[],"o",mfc="none",color=c["derived"],label="Monte Carlo")
    axes[1].set(xlabel=r"$I_s$ (A)",ylabel="Flux residual standard deviation (mWb)",
                title="(b) Torque noise 0.2 Nm, p = 3")
    axes[1].legend(fontsize=7)
    save(fig,"07_torque_synthetic")
    fig,axes=plt.subplots(2,2,figsize=(7.0,5.8),layout="constrained")
    limits={key:max(abs(p[key].dropna()).max() for p in points.values()) for key in ("eM","epsi_mWb")}
    (OUT/"map_scale.tex").write_text(
        f"The shared row maxima are {limits['eM']:.2f} conditional Nm and "
        f"{limits['epsi_mWb']:.2f} conditional mWb. ")
    for col,(rpm,p) in enumerate(points.items()):
        for row,key in enumerate(("eM","epsi_mWb")):
            ax=axes[row,col]; v=p.dropna(subset=[key])
            for positive,marker in [(True,"o"),(False,"^")]:
                z=v[v[key]>=0] if positive else v[v[key]<0]
                ax.scatter(z.id,z.iq,s=10+45*abs(z[key])/limits[key],marker=marker,
                           facecolors="none" if positive else c["estimated"],
                           edgecolors=c["reference"] if positive else c["estimated"],linewidths=.7)
            excluded=p[p[key].isna()]
            if len(excluded): ax.scatter(excluded.id,excluded.iq,marker="x",color=c["guide"],s=18)
            unit="Nm" if key=="eM" else "mWb"
            ax.set(title=f"{rpm} rpm: "+(r"$e_M^{CAN}$" if row==0 else r"$e_{\psi_\tau}^{CAN}$"),
                   xlabel=r"$i_d$ (A)",ylabel=r"$i_q$ (A)")
            ax.set_aspect("equal")
    handles=[Line2D([],[],marker="o",ls="",mfc="none",color=c["reference"],label="Positive"),
             Line2D([],[],marker="^",ls="",color=c["estimated"],label="Negative"),
             Line2D([],[],marker="x",ls="",color=c["guide"],label="Below current threshold")]
    fig.legend(handles=handles,loc="outside upper center",ncols=3,fontsize=8)
    save(fig,"08_torque_real_maps")
    fig,axes=plt.subplots(2,2,figsize=(7.0,5.2),layout="constrained")
    for rpm,p in points.items():
        marker="o" if rpm==1000 else "^"; color=c["reference"] if rpm==1000 else c["estimated"]
        for ax,x,y in [(axes[0,0],"can","map"),(axes[0,1],"I","eM"),(axes[1,0],"angle_deg","epsi_mWb")]:
            ax.scatter(p[x],p[y],marker=marker,s=15,facecolors="none",edgecolors=color,label=f"{rpm} rpm")
    axes[0,0].plot([-80,80],[-80,80],"--",color=c["guide"])
    axes[0,0].set(xlabel="CAN numeric value (assumed Nm)",ylabel=r"$M_{map}$ (Nm)",title="(a) Conditional comparison")
    axes[0,0].legend(fontsize=7)
    axes[0,1].set(xlabel=r"$I_s$ (A)",ylabel=r"$e_M^{CAN}$ (assumed Nm)",title="(b) Magnitude dependence")
    axes[1,0].set(xlabel="Current angle (deg)",ylabel=r"$e_{\psi_\tau}^{CAN}$ (conditional mWb)",title="(c) Direction dependence")
    axes[1,1].scatter(matched.I_1000,matched.delta_eM,s=15,facecolors="none",edgecolors=c["derived"])
    axes[1,1].set(xlabel=r"$I_s$ at 1000 rpm (A)",ylabel=r"$e_M^{CAN}(3000)-e_M^{CAN}(1000)$ (Nm)",
                  title="(d) Matched speed difference")
    for ax in axes.ravel(): ax.axhline(0,color=c["guide"],lw=.6)
    save(fig,"09_torque_real_trends")


def export_tables(summaries, report):
    lines=[r"\begin{tabular}{rrlrrrrrr}",r"\toprule",
           r"$n$ & $N$ & Residual & Bias & MAE & RMSE & Median & $q_{05}$ & $q_{95}$\\",r"\midrule"]
    for m in summaries:
        for key,label in [("eM_conditional_Nm",r"$e_M^{\rm CAN}$ (Nm)"),
                          ("epsi_conditional_mWb",r"$e_{\psi_\tau}^{\rm CAN}$ (mWb)")]:
            s=m[key]; vals=" & ".join(f"{s[k]:.3f}" for k in ("bias","mae","rmse","median","q05","q95"))
            lines.append(f"{m['rpm']} & {s['n']} & {label} & {vals}"+r"\\")
    lines += [r"\bottomrule",r"\end{tabular}"]
    (OUT/"metrics.tex").write_text("\n".join(lines)+"\n")
    lines=[r"\begin{tabular}{lrr}",r"\toprule",r"Observation block & Rank & Nullity\\",r"\midrule"]
    for key,label in [("torque","Torque"),("torque_voltage","Torque + voltage"),("torque_voltage_gauge","Torque + voltage + gauge")]:
        op=report["even_potential_operators"][key]
        lines.append(f"{label} & {op['rank']} & {op['nullity']}"+r"\\")
    lines += [r"\bottomrule",r"\end{tabular}"]
    (OUT/"ranks.tex").write_text("\n".join(lines)+"\n")
    lines=[r"\begin{tabular}{rrrrrr}",r"\toprule",
           r"$n$ & $I_{\min}$ (A) & Retained & CAN SD & Speed range (rpm) & OP speed SD\\",r"\midrule"]
    for m in summaries:
        s=m["recorded_speed_rpm"]
        # Complete speed range retained separately, not replaced by quantiles.
        lo,hi=m["speed_range_rpm"]
        lines.append(f"{m['rpm']} & {m['Imin_A']:.2f} & {m['normalized_retained']} & "
                     f"{m['within_OP_CAN_sd_conditional_Nm']['median']:.3f} & {lo:.2f}--{hi:.2f} & "
                     f"{m['within_OP_speed_sd_rpm']['median']:.3f}"+r"\\")
    lines += [r"\bottomrule",r"\end{tabular}"]
    (OUT/"support.tex").write_text("\n".join(lines)+"\n")
    # Small factual paragraphs, generated to prevent transcription drift.
    lo,hi=summaries
    text=(f"The median CAN-to-map ratio on $|M_{{\\rm map}}|\\ge\\SI{{10}}{{\\newton\\metre}}$ is "
          f"{lo['descriptive_CAN_over_map']['median']:.3f} at 1000 rpm and "
          f"{hi['descriptive_CAN_over_map']['median']:.3f} at 3000 rpm. "
          "This describes a scale-like disagreement; it is not an identified gain. "
          f"Replacing requested speed by the mean recorded speed changes $M_{{\\rm map}}$ by RMS "
          f"\\SI{{{lo['actual_speed_change_conditional_Nm']['rmse']:.3f}}}{{\\newton\\metre}} and "
          f"\\SI{{{hi['actual_speed_change_conditional_Nm']['rmse']:.3f}}}{{\\newton\\metre}}, respectively. "
          "The RMS difference between torque of mean inputs and mean torque of sample inputs is "
          f"$ {lo['mean_product_difference_conditional_Nm']['rmse']:.2e}$ and "
          f"$ {hi['mean_product_difference_conditional_Nm']['rmse']:.2e}$ Nm, respectively. "
          "Neither sensitivity accounts for the conditional discrepancy.\n")
    (OUT/"sensitivities.tex").write_text(text.replace("e-05",r"\cdot10^{-5}").replace("e-04",r"\cdot10^{-4}"))


def main():
    report=synthetic()
    paths=sorted(p for p in ROOT.rglob("*.mat") if not any(part in (".git",".venv","tmp","build") for part in p.relative_to(ROOT).parts))
    inventory={}
    for path in paths:
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        inventory.setdefault(digest,[]).append(path.relative_to(ROOT).as_posix())
    sources={name:metadata(PAPER/f"python/WW_Dataset_{name}.mat") for name in ("Multi_RPM","Outlier")}
    points={}; summaries=[]
    for rpm in (1000,3000):
        pts,m=analyze(PAPER/"python/WW_Dataset_Multi_RPM.mat",rpm,70.)
        raw=RawDataImporter(PAPER/"python/WW_Dataset_Multi_RPM.mat")
        speeds=raw.get_signal("PE_speed_rpm")[np.isclose(raw.get_signal("PE_Rpm_req"),rpm)]
        m["speed_range_rpm"]=[float(speeds.min()),float(speeds.max())]
        points[rpm]=pts; summaries.append(m)
    # One record per rounded requested key, equal OP weight; no interpolation.
    keys={rpm:p.groupby(["id_key","iq_key"],as_index=False).mean(numeric_only=True) for rpm,p in points.items()}
    matched=keys[1000].merge(keys[3000],on=["id_key","iq_key"],suffixes=("_1000","_3000"),validate="one_to_one")
    matched["delta_eM"]=matched.eM_3000-matched.eM_1000
    matched.to_csv(OUT/"matched_speeds.csv",index=False,float_format="%.12g")
    # Descriptive binned structure, support counts included. No causal regression.
    bins=[]
    for rpm,p in points.items():
        for variable,edges in [("I",np.linspace(0,p.I.max()*1.001,5)),("angle_deg",np.linspace(-180,180,9))]:
            for interval,g in p.groupby(pd.cut(p[variable],edges,include_lowest=True),observed=True):
                bins.append(dict(rpm=rpm,variable=variable,bin=str(interval),
                                 eM=stats(g.eM),epsi=stats(g.epsi_mWb)) if g.epsi_mWb.notna().any()
                            else dict(rpm=rpm,variable=variable,bin=str(interval),eM=stats(g.eM),epsi=None))
    data=dict(interpretation="conditional CAN comparison assuming Nm, recorded sign, unity gain; not qualified electromagnetic torque",
              inventory_unique_MAT=inventory, sources=sources, slices=summaries, bins=bins,
              matched_speed=dict(n=len(matched),delta_eM_conditional_Nm=stats(matched.delta_eM)),
              selection="Multi_RPM, requested 1000/3000 rpm and Rotor_temp_ref=70; all finite OP groups, no residual filters",
              normalization="amp-invariant assumed; kT=3p/2; requested speed in existing voltage inversion",
              grouping="raw signals averaged on same OP indices, flux of mean voltage/current; equal OP weight",
              threshold="I_s > 0.10*maximum measured OP I_s, sensitivity fractions .05/.15/.20; no epsilon denominator",
              qualification_gate="FAILED: CAN Unit/Description empty, Device Platform, generic recorder Path; sensor, gain, offset, loss, synchronization absent",
              script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              dependency_hashes={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in (PAPER/"python/raw_ww_data_importer.py",
                                           PAPER/"python/flux_correction.py",POC_PATH,
                                           poc.MODEL_PATH,ROOT/"shared/python/publication_plotting.py",
                                           ROOT/"shared/config/palette.tex")},
              versions=dict(python=sys.version.split()[0],numpy=np.__version__,pandas=pd.__version__,h5py=h5py.__version__))
    ms=data["matched_speed"]
    (OUT/"matched.tex").write_text(f"On {ms['n']} common requested-current keys, the 3000-minus-1000-rpm "
        f"conditional torque residual has mean \\SI{{{ms['delta_eM_conditional_Nm']['bias']:.3f}}}{{\\newton\\metre}} "
        f"and RMS \\SI{{{ms['delta_eM_conditional_Nm']['rmse']:.3f}}}{{\\newton\\metre}}. "
        "This is a comparison at matched requested labels, not identical measured current or magnetic state.\n")
    (HERE/"torque_synthetic.json").write_text(json.dumps(report,indent=2)+"\n")
    (HERE/"torque_real_data.json").write_text(json.dumps(data,indent=2)+"\n")
    export_tables(summaries,report)
    if "--checks-only" not in sys.argv:
        figures(points,matched)
    print(json.dumps(dict(total_checks=report["total_passed"],slices=summaries,
                          matched_speed=data["matched_speed"]),indent=2))


if __name__=="__main__":
    main()
