"""Supplementary observable, orientation and arbitrary-resistance audit checks.

Run after audit_coenergy.py; does not modify original scripts or measurements.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd

import coenergy_path_test as original
from audit_coenergy import AffineMesh, OUT, stats, conservative_flux
from flux_correction import FluxMapSymmetryAnalyzer, build_ww_measurement_slice
from raw_ww_data_importer import RawDataImporter


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report = {"checks": [], "normalization": [], "symmetry_region": []}
    # All four quadrants, both resistance signs, arbitrary resistance changes.
    grid = np.array([(x, y) for x in np.linspace(-2, 2, 5) for y in np.linspace(-2, 2, 5)])
    omega, base_R = 400., .01
    for epsilon in (-.002, 0., .002):
        flux = np.column_stack([.15+.001*grid[:, 0]-epsilon/omega*grid[:, 1],
                                .002*grid[:, 1]+epsilon/omega*grid[:, 0]])
        mesh = AffineMesh(grid, flux)
        for x, y in ((1., 1.), (-1., 1.), (1., -1.), (-1., -1.)):
            wa, wb = mesh.paths(x, y)
            assert abs(wa-wb-2*epsilon*x*y/omega) < 1e-14
            assert abs(mesh.rectangle_curl(x, y)-(wa-wb)) < 1e-14
            for shift in (-.0031, .0047):
                shifted = AffineMesh(grid, flux+shift/omega*np.column_stack([-grid[:, 1], grid[:, 0]]))
                ca, cb = shifted.paths(x, y)
                req = base_R-omega*(wa-wb)/(2*x*y)
                req_changed = base_R+shift-omega*(ca-cb)/(2*x*y)
                assert abs(req_changed-req) < 1e-13
            report["checks"].append({"epsilon_R_ohm": epsilon, "id_A": x, "iq_A": y,
                                     "delta_W_Weber_A": wa-wb})
    # Provisional scaling evidence from recorded observables, not names alone.
    for filename, slices in (("WW_Dataset_Outlier.mat", [(2000., 40.), (2000., 60.), (2000., 80.)]),
                             ("WW_Dataset_Multi_RPM.mat", [(1000., 70.), (3000., 70.)])):
        raw = RawDataImporter(Path(__file__).parent/filename)
        names = raw.get_signal_names()
        for rpm, temp in slices:
            analyzer = FluxMapSymmetryAnalyzer(build_ww_measurement_slice(raw, rpm, temp))
            corrected = analyzer.with_stator_resistance(analyzer.estimate_high_current_resistance().resistance_equivalent)
            pair = analyzer.symmetric_pairs
            high = pair.valid_delta_R_eq & (pair.iq_mag >= .85*pair.iq_mag.max())
            high_raw, high_corrected = pair[high], corrected.symmetric_pairs[high]
            def metrics(p):
                return {"rd_rms_Wb": float(np.sqrt(np.mean(p.r_d**2))),
                        "rq_rms_Wb": float(np.sqrt(np.mean(p.r_q**2))),
                        "vector_rms_Wb": float(np.sqrt(np.mean(p.r_d**2+p.r_q**2)))}
            report["symmetry_region"].append({"file": filename, "rpm": rpm, "temp_C": temp,
                "high_raw": metrics(high_raw), "high_changed_R": metrics(high_corrected),
                "all_raw": metrics(pair), "all_changed_R": metrics(corrected.symmetric_pairs)})
            mask = np.isclose(raw.get_signal("PE_Rpm_req"), rpm)&np.isclose(raw.get_signal("Rotor_temp_ref"), temp)
            signals = {n: raw.get_signal(n)[mask] for n in ("PE_Id_meas_avg", "PE_Iq_meas_avg", "PE_Ud_meas_avg", "PE_Uq_meas_avg")}
            id_, iq = signals["PE_Id_meas_avg"], signals["PE_Iq_meas_avg"]
            ud, uq = signals["PE_Ud_meas_avg"], signals["PE_Uq_meas_avg"]
            current_norm, voltage_norm = np.hypot(id_, iq), np.hypot(ud, uq)
            dot = ud*id_+uq*iq
            row = {"file": filename, "rpm": rpm, "temp_C": temp, "ratios": {}}
            for n, denominator in (("PE_I_AC_meas_Arms", current_norm), ("CAN_I_AC_meas_Arms", current_norm),
                                   ("Yok_IAC_U", current_norm), ("Yok_IAC_V", current_norm), ("Yok_IAC_W", current_norm),
                                   ("PE_U_AC_meas_Vrms", voltage_norm), ("Yok_P_Sum", dot), ("Yok_P_XYZ_Sum", dot)):
                if n not in names:
                    continue
                v = raw.get_signal(n)[mask]
                valid = (abs(denominator) > .1*abs(denominator).max())&np.isfinite(v)
                if valid.any():
                    row["ratios"][n] = stats(v[valid]/denominator[valid])
            report["normalization"].append(row)
    # Unfiltered triangle statistics remain exported. Geometry sensitivity is
    # reported additionally and never silently substituted for the full map.
    tri = pd.read_csv(OUT/"outlier60_triangle_curl.csv")
    report["geometry_sensitivity"] = {}
    for bound in (5., 10., 100.):
        selected = tri.edge_condition <= bound
        report["geometry_sensitivity"][str(bound)] = {"triangles": int(selected.sum()),
            "retained_area_fraction": float(tri.loc[selected, "area_A2"].sum()/tri.area_A2.sum()),
            "curl_equivalent_ohm": stats(tri.loc[selected, "delta_R_eq_curl_ohm"])}
    # Separate interpolation from nonlinear averaging at repeated requested keys.
    raw = RawDataImporter(Path(__file__).parent/"WW_Dataset_Outlier.mat")
    analyzer = FluxMapSymmetryAnalyzer(build_ww_measurement_slice(raw, 2000., 60.))
    points = original.prepare_points(analyzer)
    scale = float(abs(analyzer.measurement.operating_points[["id", "iq"]].to_numpy()).max())
    coordinates = points[["id", "iq"]].to_numpy()
    direct_mesh = AffineMesh(coordinates, conservative_flux(coordinates, scale, True))
    saved = pd.read_csv(OUT/"synthetic_B_saturated.csv")
    loops = np.array([a-b for a,b in [direct_mesh.paths(x,y) for x,y in saved[["id_A","iq_A"]].to_numpy()]])
    equivalent = analyzer.omega_e*loops/(2*saved.id_A.to_numpy()*saved.iq_A.to_numpy())
    report["nonlinear_averaging_separation"] = {
        "direct_samples_at_aggregated_coordinates_equivalent_ohm": stats(equivalent),
        "OP_then_key_average_minus_direct_equivalent_ohm": stats(saved.path_equivalent_ohm-equivalent)}
    report["source_sha256"] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob("*.py")}
    (OUT/"observable_checks.json").write_text(json.dumps(report, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    print("All quadrant/orientation/resistance-invariance checks passed.")
    print(json.dumps(report["normalization"], indent=2))


if __name__ == "__main__":
    main()
