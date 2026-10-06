"""Reproducible audit of the existing path experiment; no magnetic fitter.

Run from the repository root: python papers/physics_constrained_flux_maps/python/audit_coenergy.py
The original importer, reconstruction and path experiment are imported unchanged.
All outputs go to ../docs/audit_data. Data files are read-only.
"""
from pathlib import Path
import hashlib
import importlib.metadata
import json
import platform

import numpy as np
import pandas as pd
from scipy.interpolate import LinearNDInterpolator
from scipy.spatial import Delaunay, cKDTree

import coenergy_path_test as original
from flux_correction import FluxMapSymmetryAnalyzer, MeasurementSlice, build_ww_measurement_slice
from raw_ww_data_importer import RawDataImporter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "audit_data"
EPSILON = 0.002  # ohm; used minus true


def stats(values):
    a = np.asarray(values, dtype=float)
    assert np.isfinite(a).all() and a.size
    m = float(np.median(a))
    return {"n": int(a.size), "median": m, "raw_mad": float(np.median(abs(a-m))),
            "rms": float(np.sqrt(np.mean(a*a))), "min": float(a.min()),
            "max": float(a.max()), "p05": float(np.quantile(a, .05)),
            "p95": float(np.quantile(a, .95))}


class AffineMesh:
    """Independent triangle gradients and exact integrals of a P1 vector field.

    A path is split at ALL mesh-edge crossings. The midpoint rule is exact
    on each affine segment. This removes quadrature error, not interpolation
    error. Curl is piecewise constant and undefined classically on edges.
    """
    def __init__(self, coordinates, flux):
        self.coordinates = np.asarray(coordinates)
        self.flux = np.asarray(flux)
        self.tri = Delaunay(self.coordinates)
        self.interp = LinearNDInterpolator(self.tri, self.flux)
        vertices = self.coordinates[self.tri.simplices]
        delta = self.flux[self.tri.simplices[:, :2]] - self.flux[self.tri.simplices[:, 2]][:, None, :]
        self.gradient = np.einsum("nvc,nvk->nck", delta, self.tri.transform[:, :2, :])
        self.curl = self.gradient[:, 1, 0] - self.gradient[:, 0, 1]
        side1, side2 = vertices[:, 1]-vertices[:, 0], vertices[:, 2]-vertices[:, 0]
        self.area = abs(side1[:, 0]*side2[:, 1]-side1[:, 1]*side2[:, 0])/2
        self.vertices = vertices
        edges = np.concatenate([self.tri.simplices[:, [0, 1]], self.tri.simplices[:, [1, 2]],
                                self.tri.simplices[:, [2, 0]]])
        edges = np.unique(np.sort(edges, axis=1), axis=0)
        self.edge_a, self.edge_b = self.coordinates[edges[:, 0]], self.coordinates[edges[:, 1]]

    def segment(self, start, end):
        start, end = np.asarray(start, dtype=float), np.asarray(end, dtype=float)
        if (self.tri.find_simplex(np.array([start, end]), tol=1e-10) < 0).any():
            raise ValueError("Segment outside convex hull")
        r, s = end-start, self.edge_b-self.edge_a
        a = self.edge_a-start
        denom = r[0]*s[:, 1]-r[1]*s[:, 0]
        good = abs(denom) > 1e-14
        t = np.full(len(s), np.nan)
        u = t.copy()
        t[good] = (a[good, 0]*s[good, 1]-a[good, 1]*s[good, 0])/denom[good]
        u[good] = (a[good, 0]*r[1]-a[good, 1]*r[0])/denom[good]
        valid = good & (t > 0) & (t < 1) & (u >= -1e-12) & (u <= 1+1e-12)
        breaks = np.unique(np.r_[0., t[valid], 1.])
        middle = start + ((breaks[:-1]+breaks[1:])/2)[:, None]*r
        values = self.interp(middle)
        if not np.isfinite(values).all():
            raise ValueError("Nonfinite interpolated segment")
        return float(np.sum((values@r)*np.diff(breaks)))

    def paths(self, x, y):
        wa = self.segment((0, 0), (x, 0)) + self.segment((x, 0), (x, y))
        wb = self.segment((0, 0), (0, y)) + self.segment((0, y), (x, y))
        return wa, wb

    def rectangle_curl(self, x, y):
        """Independent Green check by clipping every intersecting triangle."""
        lo, hi = np.minimum([0, 0], [x, y]), np.maximum([0, 0], [x, y])
        candidates = ((self.vertices.max(axis=1) >= lo).all(axis=1) &
                      (self.vertices.min(axis=1) <= hi).all(axis=1))
        total, covered = 0., 0.
        for index in np.flatnonzero(candidates):
            polygon = list(self.vertices[index])
            for axis, boundary, direction in ((0, lo[0], 1), (0, hi[0], -1),
                                               (1, lo[1], 1), (1, hi[1], -1)):
                if not polygon:
                    break
                clipped = []
                previous = polygon[-1]
                was_inside = direction*(previous[axis]-boundary) >= 0
                for point in polygon:
                    inside = direction*(point[axis]-boundary) >= 0
                    if inside != was_inside:
                        fraction = (boundary-previous[axis])/(point[axis]-previous[axis])
                        clipped.append(previous+fraction*(point-previous))
                    if inside:
                        clipped.append(point)
                    previous, was_inside = point, inside
                polygon = clipped
            if len(polygon) >= 3:
                v = np.asarray(polygon)
                # Shift before the shoelace sum to avoid cancellation.
                v = v-v[0]
                area = abs(np.sum(v[:, 0]*np.roll(v[:, 1], -1)-v[:, 1]*np.roll(v[:, 0], -1)))/2
                total += self.curl[index]*area
                covered += area
        assert np.isclose(covered, abs(x*y), rtol=2e-10, atol=1e-8)
        return np.sign(x*y)*total

    def table(self, omega):
        center = self.vertices.mean(axis=1)
        lengths = np.stack([np.linalg.norm(self.vertices[:, a]-self.vertices[:, b], axis=1)
                            for a, b in ((0, 1), (1, 2), (2, 0))], axis=1)
        circumradius = np.prod(lengths, axis=1)/(4*self.area)
        return pd.DataFrame({"id_center_A": center[:, 0], "iq_center_A": center[:, 1],
                             "area_A2": self.area, "curl_Wb_per_A": self.curl,
                             "delta_R_eq_curl_ohm": omega*self.curl/2,
                             "circumradius_A": circumradius,
                             "edge_condition": np.linalg.cond(self.vertices[:, :2]-self.vertices[:, 2, None]),
                             "L_dq_H": self.gradient[:, 0, 1], "L_qd_H": self.gradient[:, 1, 0]})


def local_regression(coordinates, flux, k):
    """Independent unconstrained local-linear diagnostic; never a final fit.

    k-nearest neighbours in measured A coordinates, radius-scaled design,
    weights 1/(1+(distance/radius)^2); no reciprocity constraint imposed.
    """
    distance, indices = cKDTree(coordinates).query(coordinates, k=k)
    result = []
    for point, dist, index in zip(coordinates, distance, indices):
        radius = max(float(dist[-1]), 1e-12)
        design = np.column_stack([np.ones(k), (coordinates[index]-point)/radius])
        weight = np.sqrt(1/(1+(dist/radius)**2))
        coefficient, _, rank, singular = np.linalg.lstsq(design*weight[:, None], flux[index]*weight[:, None], rcond=None)
        assert rank == 3
        result.append([coefficient[1, 1]/radius-coefficient[2, 0]/radius,
                       radius, singular[0]/singular[-1]])
    return np.asarray(result)


def conservative_flux(coordinates, scale, nonlinear=False, angle=0.):
    """Explicit analytic polynomial potential, fixed before inspecting results.

    W/(.2*scale)=.8*x+.5*x^2+.65*y^2
      -.02*x^4-.025*y^4-.03*x^2*y^2+.02*x*y^2 (nonlinear case).
    Its Hessian is positive on |x|,|y|<=1.1; no saturation-induced curl.
    Coherent angle rotation transforms both argument and output.
    """
    c, s = np.cos(angle), np.sin(angle)
    rotation = np.array([[c, -s], [s, c]])
    physical = np.asarray(coordinates)@rotation.T
    x, y = (physical/scale).T
    pd_, pq = .8+x, 1.3*y
    if nonlinear:
        pd_ = pd_-.08*x**3-.06*x*y**2+.02*y**2
        pq = pq-.1*y**3-.06*x*x*y+.04*x*y
    return (.2*np.column_stack([pd_, pq]))@rotation


def analytic_loop(function, x, y):
    node, weight = np.polynomial.legendre.leggauss(8)
    t, weight = (node+1)/2, weight/2
    def segment(a, b):
        a, b = np.asarray(a), np.asarray(b)
        return float(weight@(function(a+t[:, None]*(b-a))@(b-a)))
    return (segment((0, 0), (x, 0))+segment((x, 0), (x, y))-
            segment((0, 0), (0, y))-segment((0, y), (x, y)))


def synthetic_analyzer(measurement, coordinates, flux):
    points = measurement.operating_points.copy()
    points["ud"] = measurement.stator_resistance*coordinates[:, 0]-measurement.omega_e*flux[:, 1]
    points["uq"] = measurement.stator_resistance*coordinates[:, 1]+measurement.omega_e*flux[:, 0]
    synthetic = MeasurementSlice(points, measurement.stator_resistance, measurement.pole_pairs,
                                 measurement.rpm, measurement.rotor_temperature)
    return FluxMapSymmetryAnalyzer(synthetic)


def synthetic_tests(analyzer, targets):
    coordinates = analyzer.measurement.operating_points[["id", "iq"]].to_numpy()
    scale = float(abs(coordinates).max())
    omega = analyzer.omega_e
    report = {"coordinate_scale_A": scale, "flux_scale_Wb": .2, "injected_epsilon_R_ohm": EPSILON,
              "angle_rad": .04, "cases": {}}
    cases = (("A_linear", False, 0., 0.), ("B_saturated", True, 0., 0.),
             ("C_linear_resistance", False, 0., EPSILON),
             ("C_saturated_resistance", True, 0., EPSILON),
             ("D_coherent_angle", True, .04, 0.))
    base_pairs = {}
    mesh_curls, mesh_paths = {}, {}
    for name, nonlinear, angle, epsilon in cases:
        def function(c):
            bias = epsilon/omega*np.column_stack([-c[:, 1], c[:, 0]])
            return conservative_flux(c, scale, nonlinear, angle)+bias
        sampled = synthetic_analyzer(analyzer.measurement, coordinates, function(coordinates))
        points = original.prepare_points(sampled)
        mesh = AffineMesh(points[["id", "iq"]].to_numpy(), points[["psi_d", "psi_q"]].to_numpy())
        path_values = np.array([mesh.paths(x, y) for x, y in targets])
        loops = path_values[:, 0]-path_values[:, 1]
        equivalents = omega*loops/(2*targets[:, 0]*targets[:, 1])
        analytic = np.array([analytic_loop(function, x, y) for x, y in targets])
        analytic_expected = 2*epsilon/omega*targets[:, 0]*targets[:, 1]
        assert np.max(abs(analytic-analytic_expected)) < 1e-10
        valid = sampled.symmetric_pairs.query("valid_delta_R_eq")
        pairs = valid.delta_R_eq.to_numpy()
        exact_pair_coordinates = np.column_stack([valid.id_key, valid.iq_key])
        mirror = exact_pair_coordinates*np.array([1, -1])
        rd_exact = (function(exact_pair_coordinates)[:, 0]-function(mirror)[:, 0])/2
        ideal_pair_equivalent = -omega*rd_exact/exact_pair_coordinates[:, 1]
        expected_name = "B_saturated" if nonlinear else "A_linear"
        if epsilon:
            # Actual measured pairing has baseline leakage; the increment must be exact.
            assert np.max(abs((pairs-base_pairs[expected_name])-EPSILON)) < 1e-12
            assert np.max(abs((mesh.curl-mesh_curls[expected_name])-2*EPSILON/omega)) < 1e-12
            assert np.max(abs((equivalents-mesh_paths[expected_name])-EPSILON)) < 1e-12
        else:
            base_pairs[name] = pairs
        mesh_curls[name], mesh_paths[name] = mesh.curl.copy(), equivalents.copy()
        regression = {}
        for k in (12, 24, 48):
            regression[str(k)] = stats(omega*local_regression(mesh.coordinates, mesh.flux, k)[:, 0]/2)
        if name in ("A_linear", "C_linear_resistance"):
            assert np.max(abs(equivalents-epsilon)) < 1e-12
            assert np.max(abs(omega*mesh.curl/2-epsilon)) < 1e-10
        if not angle:
            assert np.max(abs(ideal_pair_equivalent-epsilon)) < 1e-12
        green_errors = [mesh.rectangle_curl(x, y)-(wa-wb)
                        for (x, y), (wa, wb) in zip(targets[::8], path_values[::8])]
        assert np.max(np.abs(green_errors)) < 1e-9
        report["cases"][name] = {"analytic_loop_error_Weber_A": stats(analytic-analytic_expected),
            "interpolated_loop_Weber_A": stats(loops), "interpolated_path_equivalent_ohm": stats(equivalents),
            "triangle_curl_equivalent_ohm": stats(omega*mesh.curl/2),
            "requested_pair_equivalent_ohm": stats(pairs),
            "exact_mirror_equivalent_ohm": stats(ideal_pair_equivalent),
            "local_regression_equivalent_ohm": regression,
            "green_error_Weber_A": stats(green_errors)}
        pd.DataFrame({"id_A": targets[:, 0], "iq_A": targets[:, 1], "analytic_loop_Weber_A": analytic,
                      "interpolated_loop_Weber_A": loops, "path_equivalent_ohm": equivalents}).to_csv(OUT/f"synthetic_{name}.csv", index=False)
    # A parity-respecting but nonconservative field is a direct counterexample.
    report["parity_without_conservation"] = {"field": "psi_d=1+y^2, psi_q=y", "curl": "-2*y"}
    return report


def audit_slice(path, rpm, temperature, detailed=False):
    raw = RawDataImporter(path)
    analyzer = FluxMapSymmetryAnalyzer(build_ww_measurement_slice(raw, rpm, temperature))
    estimate = analyzer.estimate_high_current_resistance()
    corrected = analyzer.with_stator_resistance(estimate.resistance_equivalent)
    old_n = original.N_INTEGRATION_POINTS
    original.N_INTEGRATION_POINTS = 500
    baseline = original.calculate_path_resistance_field(analyzer)
    baseline_corr = original.calculate_path_resistance_field(corrected)
    comparison = original.compare_fields(baseline, baseline_corr)
    change = corrected.stator_resistance-analyzer.stator_resistance
    assert np.max(abs(comparison.R_eq_path_shift)) < 1e-12
    assert np.max(abs(comparison.delta_R_eq_path_shift-change)) < 1e-12
    points = original.prepare_points(analyzer)
    mesh = AffineMesh(points[["id", "iq"]].to_numpy(), points[["psi_d", "psi_q"]].to_numpy())
    exact_values = np.array([mesh.paths(x, y) for x, y in baseline[["id", "iq"]].to_numpy()])
    baseline["exact_W_A"] = exact_values[:, 0]
    baseline["exact_W_B"] = exact_values[:, 1]
    baseline["exact_delta_R_eq_path"] = analyzer.omega_e*(exact_values[:, 0]-exact_values[:, 1])/(2*baseline.id*baseline.iq)
    baseline["exact_R_eq_path"] = analyzer.stator_resistance-baseline.exact_delta_R_eq_path
    tag = f"{path.stem}_{rpm:g}_{temperature:g}"
    baseline.to_csv(OUT/f"{tag}_paths.csv", index=False)
    report = {"dataset": path.name, "rpm": rpm, "rotor_reference_C": temperature,
        "omega_e_rad_s": analyzer.omega_e, "used_R_ohm": analyzer.stator_resistance,
        "OP_groups": len(analyzer.flux_points), "requested_keys": len(points),
        "pairs": len(analyzer.symmetric_pairs), "high_pairs": estimate.n_points,
        "symmetry_R_ohm": estimate.resistance_equivalent,
        "raw_symmetry_Wb": analyzer.symmetry_metrics(), "corrected_symmetry_Wb": corrected.symmetry_metrics(),
        "raw_path_delta_R_ohm": stats(baseline.delta_R_eq_path),
        "raw_path_R_ohm": stats(baseline.R_eq_path),
        "corrected_path_delta_R_ohm": stats(baseline_corr.delta_R_eq_path),
        "raw_relative_difference": stats(baseline.relative_difference),
        "corrected_relative_difference": stats(baseline_corr.relative_difference),
        "relative_change": stats(comparison.path_difference_change),
        "R_invariance_max_ohm": float(abs(comparison.R_eq_path_shift).max()),
        "exact_path_R_ohm": stats(baseline.exact_R_eq_path),
        "quadrature_R_error_ohm": stats(baseline.delta_R_eq_path-baseline.exact_delta_R_eq_path),
        "triangle_curl_equivalent_ohm": stats(analyzer.omega_e*mesh.curl/2),
        "area_weighted_curl_equivalent_ohm": float(analyzer.omega_e*np.average(mesh.curl, weights=mesh.area)/2)}
    if detailed:
        mesh.table(analyzer.omega_e).to_csv(OUT/"outlier60_triangle_curl.csv", index=False)
        regression_table = points[["id", "iq"]].copy()
        regression_stats = {}
        for k in (12, 24, 48):
            reg = local_regression(mesh.coordinates, mesh.flux, k)
            regression_table[f"curl_k{k}_Wb_per_A"] = reg[:, 0]
            regression_table[f"radius_k{k}_A"] = reg[:, 1]
            regression_table[f"condition_k{k}"] = reg[:, 2]
            regression_stats[str(k)] = stats(analyzer.omega_e*reg[:, 0]/2)
        regression_table.to_csv(OUT/"outlier60_local_regression.csv", index=False)
        report["local_regression_equivalent_ohm"] = regression_stats
        report["triangle_geometry"] = {col: stats(mesh.table(analyzer.omega_e)[col])
                                       for col in ("edge_condition", "circumradius_A", "area_A2")}
        targets = baseline[["id", "iq"]].iloc[np.linspace(0, len(baseline)-1, 64, dtype=int)].to_numpy()
        convergence, green, local_vs_area = [], [], []
        interpolators = original.build_flux_interpolators(points)
        for n in (50, 100, 250, 500, 1000, 2000):
            original.N_INTEGRATION_POINTS = n
            for x, y in targets:
                wa, wb = mesh.paths(x, y)
                sampled = original.evaluate_target(*interpolators, analyzer.omega_e, x, y)
                exact = analyzer.omega_e*(wa-wb)/(2*x*y)
                convergence.append({"N": n, "id_A": x, "iq_A": y,
                                    "delta_R_error_ohm": sampled["delta_R_eq_path"]-exact})
        for x, y in targets[::8]:
            wa, wb = mesh.paths(x, y)
            integral = mesh.rectangle_curl(x, y)
            green.append({"id_A": x, "iq_A": y, "loop_Weber_A": wa-wb,
                          "area_curl_Weber_A": integral, "error_Weber_A": integral-(wa-wb)})
            assert abs(integral-(wa-wb)) < 1e-9
        # Deterministic target selection, both q signs retained, no outcome-based selection.
        indices = mesh.tri.find_simplex(targets)
        for (x, y), index in zip(targets, indices):
            wa, wb = mesh.paths(x, y)
            local_vs_area.append({"id_A": x, "iq_A": y,
                "endpoint_triangle_equivalent_ohm": analyzer.omega_e*mesh.curl[index]/2,
                "rectangle_average_equivalent_ohm": analyzer.omega_e*(wa-wb)/(2*x*y)})
        pd.DataFrame(convergence).to_csv(OUT/"quadrature_convergence.csv", index=False)
        pd.DataFrame(green).to_csv(OUT/"green_check.csv", index=False)
        pd.DataFrame(local_vs_area).to_csv(OUT/"local_vs_area.csv", index=False)
        report["quadrature_convergence"] = {str(n): stats([r["delta_R_error_ohm"] for r in convergence if r["N"] == n]) for n in (50, 100, 250, 500, 1000, 2000)}
        report["green_error_Weber_A"] = stats([r["error_Weber_A"] for r in green])
        report["synthetic"] = synthetic_tests(analyzer, targets)
        # Inventory only: names do not establish Park normalization or physical sensor meaning.
        names = raw.get_signal_names()
        report["normalization_candidate_signals"] = [n for n in names if any(token in n.lower() for token in ("park", "power", "p_el", "phase", "rms", "norm", "torque"))]
        (OUT/"outlier_signal_names.txt").write_text("\n".join(names)+"\n", encoding="utf-8")
    original.N_INTEGRATION_POINTS = old_n
    return report


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    summary = {"python": platform.python_version(), "packages": {p: importlib.metadata.version(p) for p in ("numpy", "scipy", "pandas", "h5py", "matplotlib")},
               "source_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob("*.py")},
               "dataset_sha256": {}, "slices": []}
    for filename, rpms, temperatures in (("WW_Dataset_Outlier.mat", [2000.], [40., 60., 80.]),
                                         ("WW_Dataset_Multi_RPM.mat", [1000., 3000.], [70.])):
        path = Path(__file__).parent/filename
        summary["dataset_sha256"][filename] = hashlib.sha256(path.read_bytes()).hexdigest()
        for rpm in rpms:
            for temperature in temperatures:
                print(f"Audit {filename} {rpm:g} rpm {temperature:g} C", flush=True)
                summary["slices"].append(audit_slice(path, rpm, temperature, detailed=(filename.endswith("Outlier.mat") and temperature == 60)))
    (OUT/"audit_results.json").write_text(json.dumps(summary, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    print(f"All audit assertions passed. Results: {OUT}", flush=True)


if __name__ == "__main__":
    main()
