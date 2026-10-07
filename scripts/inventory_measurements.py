"""Inspect local raw files; only compact metadata enters the research catalog."""
import argparse
import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared/python"))
from measurement_io import read_measurement, sha256

FIELDS = {
    "Machine_type", "Const_Machine_pole_pairs", "Const_Machine_R_s",
    "Const_Machine_R_exc", "MultiPhase_control_request_sel", "PE_Request_Modus",
    "PE_Rpm_req", "PE_speed_rpm", "PE_w_el_rad", "CAN_RPM_meas",
    "Rotor_temp_ref", "CAN_T_Rot_max", "PE_Char_Temp_Stator_ref_DegCel",
    "I_exc_req", "I_exc_meas_avg", "PE_Id_meas_avg", "PE_Iq_meas_avg",
    "PE_Ud_meas_avg", "PE_Uq_meas_avg", "CAN_Torque_meas", "Yok_M",
    "PE_I_AC_meas_Arms", "PE_U_AC_meas_Vrms", "PE_Index_meas",
    "PE_Index_Flx_Char_StatorCurrent_OP_param_none", "PE_Id_req_meas", "PE_Iq_req_meas",
    "CAN_P_AC_meas_W", "CAN_P_mech_meas_W", "PE_P_AC_meas_W", "Yok_P_Sum",
}


def inventory(raw_root):
    rows = []
    for path in sorted(raw_root.rglob("*.mat")):
        row = {"source": path.relative_to(raw_root).as_posix(), "bytes": path.stat().st_size,
               "sha256": sha256(path)}
        try:
            signals, metadata, description = read_measurement(path, FIELDS)
            row.update(description_keys=sorted(description) if isinstance(description, dict) else [], channel_count=len(metadata),
                       channel_names=sorted(metadata), fields={})
            for name, values in signals.items():
                finite = values[np.isfinite(values)]
                unique = np.unique(finite)
                row["fields"][name] = dict(n=len(values), missing=int(np.sum(~np.isfinite(values))),
                    min=float(finite.min()) if len(finite) else None,
                    max=float(finite.max()) if len(finite) else None,
                    unique=unique.tolist() if len(unique) <= 20 else None,
                    metadata=metadata[name])
            machine = signals.get("Machine_type", [])
            codes = np.unique(machine).tolist()
            row["machine_type"] = {1: "PSM", 2: "ASM", 6: "EESM"}.get(codes[0], "unknown") if len(codes) == 1 else "unknown"
            row["classification_evidence"] = "Machine_type channel + MeasEval eMachineType" if len(codes) == 1 else "missing/mixed Machine_type; no filename inference"
        except Exception as exc:
            row["error"] = str(exc)
        rows.append(row)
        print(row["source"], row.get("machine_type", "unread"), row.get("error", ""), flush=True)
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_root", type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "datasets/raw_inventory.json")
    args = parser.parse_args()
    rows = inventory(args.raw_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(rows, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
