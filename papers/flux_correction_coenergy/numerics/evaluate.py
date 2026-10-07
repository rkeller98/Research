"""Small structural fitting experiment. NumPy only; no external paper imports."""
from pathlib import Path
import json
import numpy as np
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "shared/python"))
from magnetic_model import flux, hessian, coenergy

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT/"figures"/"data"
DATA.mkdir(exist_ok=True)
from potential_splines import *

# Meaningful basis checks independent of fitted examples.
zz = np.linspace(-.97, .97, 101)
assert np.max(abs(bsplines(zz).sum(axis=1)-1)) < 1e-13
assert np.max(abs(bsplines(zz, derivative=1).sum(axis=1))) < 1e-12
assert np.max(abs((bsplines(zz+1e-6)-bsplines(zz-1e-6))/2e-6
                  -bsplines(zz, derivative=1))) < 1e-8
assert np.max(abs(design(np.zeros((1, 2)), parity=1)@Z)) < 1e-13
cleanpoints = grid(13, .99)
cleanfit = solve(cleanpoints, flux(cleanpoints), "Potential", 0.)
testpoints = grid(25)
cleanmetrics = metrics(cleanfit, testpoints, 1.)
assert cleanmetrics["flux_rmse"] < 1e-10
assert cleanmetrics["hessian_rmse"] < 1e-9
assert cleanmetrics["curl_rmse"] == 0
assert np.linalg.matrix_rank(np.vstack([design(cleanpoints, 1, 0, 1),
                                       design(cleanpoints, 0, 1, 1)])@Z) == Z.shape[1]
# Check the two axis-ordered paths independently with Gaussian quadrature.
# Four Gauss points integrate the polynomial flux on each straight edge exactly.
abscissa, weights = np.polynomial.legendre.leggauss(4)
def edge_integral(start, end, field):
    delta = end-start
    locations = start[None, :]+(abscissa[:, None]+1)*delta[None, :]/2
    return float(np.sum(weights*(field(locations)@delta))/2)

origin = np.zeros(2)
path_disagreement = 0.
for endpoint in testpoints[::31]:
    dcorner = np.array([endpoint[0], 0.])
    qcorner = np.array([0., endpoint[1]])
    first = edge_integral(origin, dcorner, flux)+edge_integral(dcorner, endpoint, flux)
    second = edge_integral(origin, qcorner, flux)+edge_integral(qcorner, endpoint, flux)
    expected = endpoint[0]+.3*endpoint[0]**2+.5*endpoint[1]**2-.01*endpoint[0]**4-.02*endpoint[1]**4-.03*np.prod(endpoint**2)+.02*endpoint[0]*endpoint[1]**2
    assert abs(first-expected) < 1e-12
    assert abs(second-expected) < 1e-12
    path_disagreement = max(path_disagreement, abs(first-second))

# A parity-only field [1+.6x+y^2, y] has curl=-2y, despite d-even/q-odd parity.
def nonconservative_field(locations):
    x, y = locations.T
    return np.column_stack([1+.6*x+y*y, y])
endpoint = np.array([.6, .7])
dcorner, qcorner = np.array([.6, 0.]), np.array([0., .7])
first = edge_integral(origin, dcorner, nonconservative_field)+edge_integral(dcorner, endpoint, nonconservative_field)
second = edge_integral(origin, qcorner, nonconservative_field)+edge_integral(qcorner, endpoint, nonconservative_field)
assert abs((first-second)+endpoint[0]*endpoint[1]**2) < 1e-12
assert np.allclose(flux(testpoints)[:, 0], flux(testpoints*np.array([1., -1.]))[:, 0])

rng = np.random.default_rng(20261006)
results = []
baseline = None
experiments = [("Noisy", 200, 1., False), ("Sparse", 50, 1., False),
               ("Outliers", 200, 1., True), ("Strong saturation", 200, 3., False)]
for case, count, saturation, outliers in experiments:
    points = rng.uniform(-1, 1, (count, 2))
    values = flux(points, saturation)+rng.normal(0, .005, (count, 2))
    if outliers:
        idx = rng.choice(count, count//20, replace=False)
        values[idx] += rng.normal(0, .1, (len(idx), 2))
    perm = rng.permutation(count)
    ntrain = int(.8*count)
    ti, vi = perm[:ntrain], perm[ntrain:]
    modes = [(mode, False) for mode in ("Independent", "Parity", "Potential")]
    if outliers:
        modes.append(("Potential", True))
    for mode, robust in modes:
        candidates = []
        for lam in (0., 1e-6, 1e-5, 1e-4, 1e-3):
            fit = solve(points[ti], values[ti], mode, lam, robust)
            prediction, _ = predict(fit, points[vi])
            err = np.mean((prediction-values[vi])**2)
            candidates.append((err, lam))
        lam = min(candidates)[1]
        fit = solve(points, values, mode, lam, robust)
        report = metrics(fit, testpoints, saturation)
        report.update(case=case, mode=mode+(" robust" if robust else ""),
                      sample_count=count, penalty=lam)
        if mode != "Independent":
            assert report["parity_rmse"] < 1e-12
        if mode == "Potential":
            assert report["curl_rmse"] == 0
        results.append(report)
        if case == "Noisy" and mode == "Potential":
            baseline = fit

slicepts = np.column_stack([np.full(101, -.4), np.linspace(-.95, .95, 101)])
f, H = predict(baseline, slicepts)
truth, ht = flux(slicepts), hessian(slicepts)
table = np.column_stack([slicepts[:, 1], truth[:, 0], f[:, 0], truth[:, 1], f[:, 1],
                         ht[:, 0, 0], H[:, 0, 0], ht[:, 0, 1], H[:, 0, 1]])
np.savetxt(DATA/"fit_slice.dat", table, fmt="%.12g", comments="",
           header="y dtrue dfit qtrue qfit ddtrue ddfit dqtrue dqfit")
tex = [r"\begin{tabular}{llrrrr}", r"\toprule",
       r"Case & Fit & Flux RMSE & Hessian RMSE & Parity RMS & Curl RMS\\", r"\midrule"]
for row in results:
    tex.append(f'{row["case"]} & {row["mode"]} & {row["flux_rmse"]:.2e} & '
               f'{row["hessian_rmse"]:.2e} & {row["parity_rmse"]:.1e} & '
               f'{row["curl_rmse"]:.1e} '+r"\\")
tex += [r"\bottomrule", r"\end{tabular}"]
(DATA/"fit_metrics.tex").write_text("\n".join(tex)+"\n", encoding="utf-8")
report = dict(seed=20261006, spline_degree=DEGREE, knots=KNOTS.tolist(),
              potential_coefficients=N*N//2, gauge_fixed_coefficients=Z.shape[1],
              noiseless_metrics=cleanmetrics, results=results,
              exact_path_disagreement=path_disagreement,
              parity_only_path_disagreement=first-second,
              strong_saturation_min_eigenvalue=float(np.linalg.eigvalsh(hessian(grid(41, 1.), 3.)).min()))
(ROOT/"numerics"/"evaluation.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
print(json.dumps(report, indent=2))
