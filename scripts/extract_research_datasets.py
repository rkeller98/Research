"""Deterministically extract stationary logger groups; never calibrate torque.

Run with the root containing Flux/ and Trq/. Research reproduction needs only
the resulting fixtures, not this local raw folder or a MeasEval installation.
"""
import argparse
import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared/python"))
from measurement_io import read_measurement, sha256
from canonical_dataset import VERSION, export_canonical_dataset, import_canonical_dataset

SELECTION = {
    "psm_dual_system_multirpm": ("Flux/WW_Dataset_Multi_RPM.mat", None, None),
    "psm_temperature_2500": ("Flux/PSM_Measdata.mat", None, None),
    "eesm_excitation_reduced": ("Flux/EESM_Measdata_Reduced.mat", None, None),
    "asm_500rpm_set1": ("Flux/ASM/Set_01/Matlab_005.mat", None, None),
    "asm_500rpm_set2": ("Flux/ASM/Set_01/Matlab_006.mat", None, None),
    "psm_merge_4000_part1": ("Flux/WW_Dataset_Merge_1.mat", None, None),
    "psm_merge_4000_part2": ("Flux/WW_Dataset_Merge_2.mat", None, None),
    "psm_outlier_stress_60c": ("Flux/WW_Dataset_Outlier.mat", 60, 320),
}
FIELDS = {
    "id": ("PE_Id_meas_avg", "A"), "iq": ("PE_Iq_meas_avg", "A"),
    "ud": ("PE_Ud_meas_avg", "V"), "uq": ("PE_Uq_meas_avg", "V"),
    "iexc": ("I_exc_meas_avg", "A"), "id_req": ("PE_Id_req_meas", "A"),
    "iq_req": ("PE_Iq_req_meas", "A"), "iexc_req": ("I_exc_req", "A"),
    "rpm_req": ("PE_Rpm_req", "rpm"), "rpm_meas": ("PE_speed_rpm", "rpm"),
    "omega_e": ("PE_w_el_rad_avg", "rad/s"), "rotor_temp_ref": ("Rotor_temp_ref", "degC"),
    "rotor_temp_meas": ("CAN_T_Rot_max", "degC"),
    "stator_temp_ref": ("PE_Char_Temp_Stator_ref_DegCel", "degC"),
    "rs_used": ("Const_Machine_R_s", "ohm"), "pole_pairs": ("Const_Machine_pole_pairs", "1"),
    "phase_selector": ("MultiPhase_control_request_sel", "1"),
    "torque": ("CAN_Torque_meas", "Nm"), "phase_current_rms": ("PE_I_AC_meas_Arms", "A"),
    "phase_voltage_rms": ("PE_U_AC_meas_Vrms", "V"),
}
STAT_FIELDS = {"id", "iq", "iexc", "ud", "uq", "rpm_meas", "torque"}


def operating_points(path, temperature=None, limit=None):
    raw, metadata, description = read_measurement(path)
    n = len(raw["PE_Id_meas_avg"])
    def get(field, default=np.nan):
        value = raw.get(field)
        return value if value is not None and len(value) == n else np.full(n, default)
    # Never combine equal measurement counters across excitation/state slices.
    counter = get("PE_Index_meas")
    if not np.isfinite(counter).all():
        raise ValueError("Missing/invalid measurement-group counter")
    secondary = get("I_exc_req", 0)
    temp = get("Rotor_temp_ref", 0)
    keys = np.column_stack([get("PE_Rpm_req"), secondary, temp, counter])
    columns = ["op_index", "sample_count"]
    spec = {"op_index": {"unit": "1", "source": "PE_Index_meas"},
            "sample_count": {"unit": "1", "source": "retained logger records"}}
    for name, (source, unit) in FIELDS.items():
        columns.append(name)
        spec[name] = {"unit": unit, "source": source, "raw_unit": metadata.get(source, {}).get("unit", "")}
        if name in STAT_FIELDS:
            for suffix in ("median", "std", "count"):
                key = name + "_" + suffix
                columns.append(key)
                spec[key] = {"unit": "1" if suffix == "count" else unit,
                             "source": source + ": " + suffix}
    columns.extend(["psi_d", "psi_q", "kt", "torque_map"])
    for name, unit, source in [("psi_d", "Wb", "(uq-rs_used*iq)/omega_e"),
                               ("psi_q", "Wb", "(rs_used*id-ud)/omega_e"),
                               ("kt", "1", "phase-system configuration; no sensor gain fit"),
                               ("torque_map", "Nm", "kt*(psi_d*iq-psi_q*id)")]:
        spec[name] = {"unit": unit, "source": source}
    records = []
    rejected = 0
    for key in np.unique(keys, axis=0):
        if key[3] <= 0 or not np.isfinite(key).all():
            continue
        if temperature is not None and key[2] != temperature:
            continue
        mask = np.all(keys == key, axis=1)
        for field in ["PE_Id_meas_avg", "PE_Iq_meas_avg", "PE_Ud_meas_avg", "PE_Uq_meas_avg", "PE_w_el_rad_avg"]:
            mask &= np.isfinite(get(field))
        count = int(mask.sum())
        rejected += int(np.sum(np.all(keys == key, axis=1))) - count
        if not count:
            continue
        row = [key[3], count]
        means = {}
        for name, (source, _) in FIELDS.items():
            values = get(source)[mask]
            values = values[np.isfinite(values)]
            mean = float(np.mean(values)) if len(values) else np.nan
            # Zero-only temperature channels are disconnected placeholders.
            if name == "rotor_temp_meas" and len(values) and np.all(values == 0):
                mean = np.nan
            means[name] = mean
            row.append(mean)
            if name in STAT_FIELDS:
                row.extend([float(np.median(values)) if len(values) else np.nan,
                            float(np.std(values, ddof=1)) if len(values) > 1 else np.nan, len(values)])
        omega = means["omega_e"]
        pd = (means["uq"] - means["rs_used"] * means["iq"]) / omega if abs(omega) > 1e-8 else np.nan
        pq = (means["rs_used"] * means["id"] - means["ud"]) / omega if abs(omega) > 1e-8 else np.nan
        selector, p = means["phase_selector"], means["pole_pairs"]
        kt = {0: 1.5, 1: 3.0, 3: 2.5}.get(selector, np.nan) * p
        row.extend([pd, pq, kt, kt * (pd * means["iq"] - pq * means["id"])])
        records.append(row)
    values = np.asarray(records, dtype=float)
    total = len(values)
    if limit and total > limit:
        values = values[np.unique(np.linspace(0, total - 1, limit).round().astype(int))]
    codes = np.unique(get("Machine_type"))
    machine = {1: "PSM", 2: "ASM", 6: "EESM"}.get(codes[0], "unknown") if len(codes) == 1 else "unknown"
    return columns, values, spec, machine, dict(source_groups=total, retained_groups=len(values), invalid_records_rejected=rejected)


def extract(raw_root, output):
    report = []
    for dataset_id, (relative, temperature, limit) in SELECTION.items():
        path = raw_root / relative
        columns, values, spec, machine, counts = operating_points(path, temperature, limit)
        manifest = dict(schema_version=VERSION, dataset_id=dataset_id, machine_type=machine,
            provenance=dict(sources=[dict(path=relative, sha256=sha256(path))],
                            exporter="scripts/extract_research_datasets.py", exporter_version="1.0",
                            machine_type_evidence="Machine_type channel; MeasEval eMachineType: 1=PSM, 2=IM/ASM, 6=EESM"),
            columns=spec,
            dq_convention=dict(name="amplitude-invariant per three-phase system",
                evidence="MeasEval grid.calculate RMS=norm(dq)/sqrt(2); phase selector is retained",
                status="implementation-declared, not a transducer calibration",
                axes="d rotor-reference axis; q positive CCW; J=[[0,-1],[1,0]]",
                electrical_speed="mean PE_w_el_rad_avg, not requested rpm*p; ASM includes slip"),
            torque=dict(source_field="CAN_Torque_meas", status="CAN indicator, calibration and shaft-loss relation unverified",
                unit="Nm", unit_evidence="MeasEval typed torque semantics; raw Unit may be empty",
                gain_applied=1, sign="stored signed signal, compared against positive electromagnetic motor convention",
                kt="selector 0: 3p/2; selector 1: 3p (two three-phase systems); selector 3: 5p/2; other/missing: absent",
                warning="No arbitrary factor-2 calibration. Equal system currents assumed for selector 1 total torque."),
            aggregation=dict(group_by=["PE_Rpm_req", "I_exc_req", "Rotor_temp_ref", "PE_Index_meas"],
                estimator="arithmetic mean; median and sample standard deviation ddof=1 retained for selected channels",
                flux="invert group means; no averaging of products; stored voltage/current average channels",
                settling="no additional exclusion; acquisition-window/settling timing is unavailable",
                outliers="no residual-based deletion", temperature_filter=temperature,
                reduction="none" if limit is None else f"{limit} equally spaced indices in lexicographically sorted group list",
                **counts),
            known_limitations=["No true flux or Rs ground truth", "Record count is not independent sensor replicate count",
                "Requested temperatures differ from measured state; zero-only rotor temperature means missing",
                "No excitation flux for EESM: full three-current reciprocity cannot be tested",
                "ASM stator field depends on rotor/slip state; PSM current-only coenergy inference is not transferable",
                "Missing phase selector is not silently assigned 3-phase torque", "CAN calibration, gear ratio and mechanical losses unavailable"],
            data_rights=dict(derived_data_publication="authorized by repository owner on 2026-10-07", raw_data="local, excluded from Git", license="not specified; authorization is not an invented third-party license"))
        stem = output / dataset_id
        result = export_canonical_dataset(stem, columns, values, manifest)
        cols2, values2, manifest2 = import_canonical_dataset(stem)
        assert cols2 == columns and np.array_equal(values, values2, equal_nan=True)
        before = (stem.with_suffix(".csv").read_bytes(), stem.with_suffix(".json").read_bytes())
        export_canonical_dataset(stem, cols2, values2, manifest2)
        assert before == (stem.with_suffix(".csv").read_bytes(), stem.with_suffix(".json").read_bytes())
        report.append(dict(dataset_id=dataset_id, rows=len(values), csv_bytes=len(before[0]), manifest_bytes=len(before[1]), csv_sha256=result["csv_sha256"], roundtrip="exact double values and byte-identical re-export"))
        print(report[-1], flush=True)
    (output / "extraction_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_root", type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "datasets")
    args = parser.parse_args()
    extract(args.raw_root, args.output)
