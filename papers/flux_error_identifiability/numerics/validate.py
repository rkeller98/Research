"""Reproduce manuscript tables/data and check the derivations (NumPy, SymPy)."""
from pathlib import Path
import json
import numpy as np
import sympy as sp
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "shared/python"))
from magnetic_model import flux as model_flux, hessian as model_hessian

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "figures" / "data"
DATA.mkdir(exist_ok=True)
J = np.array([[0., -1.], [1., 0.]])


def rotation(a):
    return np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])


x, y = sp.symbols("x y", real=True)
w = x + sp.Rational(3, 10)*x**2 + y**2/2 - x**4/100 - y**4/50 \
    - sp.Rational(3, 100)*x**2*y**2 + x*y**2/50
f = sp.Matrix([sp.diff(w, z) for z in (x, y)])
H = f.jacobian([x, y])
assert sp.simplify(w-w.subs(y, -y)) == 0
assert sp.simplify(f[0]-f[0].subs(y, -y)) == 0
assert sp.simplify(f[1]+f[1].subs(y, -y)) == 0
assert H[0, 1] == H[1, 0]
for row, col, sign in ((0, 0, 1), (1, 1, 1), (0, 1, -1), (1, 0, -1)):
    assert sp.simplify(H[row, col]-sign*H[row, col].subs(y, -y)) == 0
fn = sp.lambdify((x, y), f, "numpy")
hn = sp.lambdify((x, y), H, "numpy")


def flux(i):
    result = model_flux(i)
    assert np.allclose(result, np.asarray(fn(*i), dtype=float).reshape(2), atol=1e-14)
    return result


def hessian(i):
    result = model_hessian(i)
    assert np.allclose(result, np.asarray(hn(*i), dtype=float).reshape(2, 2), atol=1e-14)
    return result


def sensitivity(i):
    return hessian(i) @ J @ i - J @ flux(i)


def observed(i, speed=1., er=0., angle=0., voltage_bias=None):
    """Generate true voltages, rotate signals, reconstruct with used R."""
    true_i = rotation(angle) @ i
    true_u = .08*true_i + speed*J @ flux(true_i)
    measured_u = rotation(-angle) @ true_u
    if voltage_bias is not None:
        measured_u += voltage_bias(i)
    return -J @ (measured_u-(.08+er)*i)/speed


def residual(i, speed=1., er=0., angle=0., voltage_bias=None):
    pos = observed(i, speed, er, angle, voltage_bias)
    neg = observed(i*np.array([1., -1.]), speed, er, angle, voltage_bias)
    return np.array([(pos[0]-neg[0])/2, (pos[1]+neg[1])/2])


# Symbolic reconstruction derivatives and exact angle derivative.
ud, uq, d, q, rs, om = sp.symbols("ud uq d q rs om", nonzero=True)
js = sp.Matrix([[0, -1], [1, 0]])
ii = sp.Matrix([d, q])
rec = -js*(sp.Matrix([ud, uq])-rs*ii)/om
expected = [-js[:, 0]/om, -js[:, 1]/om,
            rs*js[:, 0]/om, rs*js[:, 1]/om, js*ii/om, -rec/om]
for variable, column in zip((ud, uq, d, q, rs, om), expected):
    assert sp.simplify(rec.diff(variable)-column) == sp.zeros(2, 1)
a = sp.symbols("a", real=True)
rot = sp.Matrix([[sp.cos(a), -sp.sin(a)], [sp.sin(a), sp.cos(a)]])
zi = rot*sp.Matrix([x, y])
exact_symbolic = rot.T*f.subs({x: zi[0], y: zi[1]}, simultaneous=True)
sa = H*js*sp.Matrix([x, y])-js*f
assert sp.simplify(exact_symbolic.diff(a).subs(a, 0)-sa) == sp.zeros(2, 1)
exact_hessian = exact_symbolic.jacobian([x, y])
assert sp.simplify(exact_hessian-exact_hessian.T) == sp.zeros(2, 2)
assert sp.diff((js*sp.Matrix([x, y]))[1], x)-sp.diff((js*sp.Matrix([x, y]))[0], y) == 2
pm, ld, lq = sp.symbols("pm ld lq")
fl = sp.Matrix([pm+ld*x, lq*y])
sl = fl.jacobian([x, y])*js*sp.Matrix([x, y])-js*fl
assert sp.simplify(sl-sp.Matrix([(lq-ld)*y, (lq-ld)*x-pm])) == sp.zeros(2, 1)
assert sp.simplify(sl.subs({x: 0, ld: lq})-sp.Matrix([0, -pm])) == sp.zeros(2, 1)
# Remove nonlinear terms; remove only cross terms as distinct limiting checks.
independent_w = w + sp.Rational(3, 100)*x**2*y**2-x*y**2/50
assert sp.diff(independent_w, x, y) == 0
linear_w = x+sp.Rational(3, 10)*x**2+y**2/2
assert sp.hessian(linear_w, (x, y)) == sp.diag(sp.Rational(3, 5), 1)

grid = [np.array([xx, yy]) for xx in np.linspace(-1, 1, 41)
        for yy in np.linspace(-1, 1, 81)]
parity = max(np.linalg.norm(flux(i)-np.array([1., -1.])*flux(i*np.array([1., -1.])))
             for i in grid)
mineig = min(np.linalg.eigvalsh(hessian(i))[0] for i in grid)
assert parity < 1e-13 and mineig > 0
derivative_error = max(np.linalg.norm((observed(i, angle=1e-6)-observed(i, angle=-1e-6))
                                     /2e-6-sensitivity(i)) for i in grid)
assert derivative_error < 1e-8
assert max(np.linalg.norm(observed(i)-flux(i)) for i in grid) < 1e-13
assert max(np.linalg.norm(observed(i, er=.025)-flux(i)-.025*J@i) for i in grid) < 1e-13
assert max(np.linalg.norm(observed(i, angle=.02)-rotation(-.02)@flux(rotation(.02)@i))
           for i in grid) < 1e-13

points = [(np.array([xx, yy]), speed) for xx in (-.6, 0., .6)
          for yy in np.linspace(.1, 1., 10) for speed in (.5, 1., 2.)]
S = np.vstack([np.column_stack((J@i/speed, sensitivity(i))) for i, speed in points])
scaled_S = S @ np.diag([.025, .02])
assert np.linalg.matrix_rank(S) == 2
scenarios = [("No error", 0., 0.), ("Resistance only", .025, 0.),
             ("Angle only", 0., .02), ("Both errors", .025, .02)]
fitted = []
for name, er, angle in scenarios:
    r = np.concatenate([residual(i, speed, er, angle) for i, speed in points])
    estimate = np.linalg.lstsq(S, r, rcond=None)[0]
    mismatch = np.sqrt(np.mean((r-S@estimate)**2))
    assert abs(estimate[0]-er) < 1e-5 and abs(estimate[1]-angle) < 1e-5
    fitted.append(dict(case=name, er=er, angle=angle, estimated_er=float(estimate[0]),
                       estimated_angle=float(estimate[1]), residual_rms=float(mismatch)))
# Exact counterexample: current-proportional voltage error mimics resistance.
confounding = max(np.linalg.norm(residual(i, speed, er=.025)
                                -residual(i, speed, voltage_bias=lambda z: -.025*z))
                  for i, speed in points)
assert confounding < 1e-13
# Positive correction sign recovers true used value .08 after subtracting .025.
assert abs((.105-fitted[1]["estimated_er"])-.08) < 1e-13

# Reconstruct with proposed R and correct the coordinate axes, then pair anew.
estimated_er = fitted[3]["estimated_er"]
estimated_angle = fitted[3]["estimated_angle"]
def corrected_map(target, speed):
    label = rotation(-estimated_angle) @ target
    return rotation(estimated_angle) @ (observed(label, speed, .025, .02)
                                        -estimated_er*J@label/speed)

before = max(np.linalg.norm(residual(i, speed, .025, .02)) for i, speed in points)
after = 0.
for i, speed in points:
    fp = corrected_map(i, speed)
    fm = corrected_map(i*np.array([1., -1.]), speed)
    after = max(after, np.linalg.norm([(fp[0]-fm[0])/2, (fp[1]+fm[1])/2]))
assert after < 1e-5 and after < before/1000

errors = []
for angle in (.001, .005, .01, .02, .05, .1):
    maperr = max(np.linalg.norm(observed(i, angle=angle)-flux(i)-angle*sensitivity(i))
                 for i in grid)
    reserr = max(np.linalg.norm(residual(i, angle=angle)-angle*sensitivity(i))
                 for i in grid)
    errors.append(dict(angle=angle, full_map_max=maperr, parity_residual_max=reserr))
assert 3.9 < errors[3]["full_map_max"]/errors[2]["full_map_max"] < 4.1
assert 7.8 < errors[3]["parity_residual_max"]/errors[2]["parity_residual_max"] < 8.2

def write_table(name, headers, rows):
    np.savetxt(DATA/name, rows, header=" ".join(headers), comments="", fmt="%.12g")

rows = []
for yy in np.linspace(-1, 1, 101):
    i = np.array([0., yy])
    vals = [observed(i, 1., er, angle) for _, er, angle in scenarios]
    rsvals = [residual(i, 1., er, angle) for _, er, angle in scenarios]
    rows.append([yy, *[v for pair in vals for v in pair],
                 *[v for pair in rsvals for v in pair]])
write_table("synthetic.dat", ["y", "d0", "q0", "dR", "qR", "dg", "qg", "db", "qb",
                             "rd0", "rq0", "rdR", "rqR", "rdg", "rqg", "rdb", "rqb"], rows)
speedrows = []
for speed in np.linspace(.5, 2., 61):
    i = np.array([0., .8])
    rr = residual(i, speed, er=.025)
    rg = residual(i, speed, angle=.02)
    speedrows.append([speed, rr[0], rg[0], rg[1], speed*rr[0]])
write_table("speeds.dat", ["speed", "rdR", "rdg", "rqg", "scaledR"], speedrows)
report = dict(symbolic_checks="passed", parity_max=parity, minimum_hessian_eigenvalue=mineig,
              angle_derivative_max_error=derivative_error, nuisance_confounding_max=confounding,
              pair_count=len(points), rank=int(np.linalg.matrix_rank(S)),
              scaled_condition_number=float(np.linalg.cond(scaled_S)),
              estimates=fitted, linearization_errors=errors)
report["correction"] = dict(before_max_residual=before, after_max_residual=after,
                            proposed_resistance=.105-estimated_er)
(ROOT/"numerics"/"validation.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
tex = [r"\begin{tabular}{lrrr}", r"\toprule",
       r"Injected case & $\hat\varepsilon_R$ (\si{\ohm}) & $\widehat{\delta\gamma}$ (rad) & RMS$/\psi_*$\\",
       r"\midrule"]
for case in fitted:
    printed_er = 0. if abs(case["estimated_er"]) < .5e-6 else case["estimated_er"]
    printed_angle = 0. if abs(case["estimated_angle"]) < .5e-6 else case["estimated_angle"]
    tex.append(f'{case["case"]} & {printed_er:.6f} & '
               f'{printed_angle:.6f} & {case["residual_rms"]:.2e} '+r"\\")
tex += [r"\bottomrule", r"\end{tabular}"]
(DATA/"estimates.tex").write_text("\n".join(tex)+"\n", encoding="utf-8")
tex = [r"\begin{tabular}{rrr}", r"\toprule",
       r"$|\delta\gamma|$ (rad) & Max. map error$/\psi_*$ & Max. residual error$/\psi_*$\\",
       r"\midrule"]
for case in errors:
    tex.append(f'{case["angle"]:.3f} & {case["full_map_max"]:.3e} & '
               f'{case["parity_residual_max"]:.3e} '+r"\\")
tex += [r"\bottomrule", r"\end{tabular}"]
(DATA/"linearization.tex").write_text("\n".join(tex)+"\n", encoding="utf-8")
print(json.dumps(report, indent=2))
