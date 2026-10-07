"""Synthetic observability checks and figures; portable real study is separate."""
from pathlib import Path
import importlib.util
import json
import sys
import numpy as np
PAPER=Path(__file__).resolve().parents[1]
ROOT=PAPER.parents[1]
spec=importlib.util.spec_from_file_location("torque_poc", ROOT/"docs/torque_flux_consistency/proof_of_concept.py")
poc=importlib.util.module_from_spec(spec)
spec.loader.exec_module(poc)

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

def figures():
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

if __name__ == "__main__":
    report=synthetic()
    (PAPER/"numerics/torque_synthetic.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    figures()
    print(f"{report['total_passed']} torque checks passed.")
