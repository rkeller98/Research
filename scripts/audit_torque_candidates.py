"""Rank measured torque candidates and diagnose configuration, without gain fitting."""
import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared/python"))
from canonical_dataset import load_dataset
from extract_research_datasets import operating_points


def summarize(columns, values):
    d = dict(zip(columns, values.T))
    mag = np.hypot(d["id"], d["iq"])
    mask = (mag >= .1 * np.max(mag)) & np.isfinite(d["torque"]) & np.isfinite(d["torque_map"])
    residual = d["torque_map"][mask] - d["torque"][mask]
    ratio_mask = mask & (np.abs(d["torque_map"]) >= .2 * np.nanmax(np.abs(d["torque_map"])))
    sd = d["torque_std"]
    with np.errstate(invalid="ignore", divide="ignore"):
        iratio = d["phase_current_rms"] / mag
        uratio = d["phase_voltage_rms"] / np.hypot(d["ud"], d["uq"])
    finite = lambda v: v[np.isfinite(v)]
    def med(v):
        v = finite(v)
        return float(np.median(v)) if len(v) else None
    return dict(groups=len(values), normalized_groups=int(mask.sum()),
        missing_torque_groups=int(np.sum(~np.isfinite(d["torque"]))),
        median_logger_count=med(d["sample_count"]), median_torque_std=med(sd),
        p95_torque_std=float(np.nanquantile(sd, .95)) if len(finite(sd)) else None,
        torque_range=[float(np.nanmin(d["torque"])), float(np.nanmax(d["torque"]))],
        current_direction_rank=int(np.linalg.matrix_rank(np.column_stack([d["id"], d["iq"]]))),
        rpm_references=np.unique(d["rpm_req"]).tolist(),
        temperature_references=finite(np.unique(d["rotor_temp_ref"])).tolist(),
        kt_values=finite(np.unique(d["kt"])).tolist(),
        mean_vs_median_torque_rms=float(np.sqrt(np.nanmean((d["torque"]-d["torque_median"])**2))),
        residual_bias=float(np.mean(residual)) if len(residual) else None,
        residual_rms=float(np.sqrt(np.mean(residual**2))) if len(residual) else None,
        can_over_map_median=med(d["torque"][ratio_mask]/d["torque_map"][ratio_mask]),
        rms_over_dq_current_median=med(iratio[mag > .1 * np.max(mag)]),
        rms_over_dq_voltage_median=med(uratio),
        status="configuration-consistent comparison; CAN calibration and loss mapping unverified")


def run(raw_root=None):
    result = {"portable_datasets": {}}
    for path in sorted((ROOT / "datasets").glob("*.json")):
        if not path.with_suffix(".csv").is_file():
            continue
        d, m = load_dataset(path.stem)
        result["portable_datasets"][path.stem] = summarize(list(d), np.column_stack(list(d.values())))
    if raw_root:
        result["additional_raw_candidates"] = {}
        for relative in [
            "Flux/Matlab_008.mat", "Flux/Matlab_034 Toufic.mat", "Flux/Matlab_038 Toufic.mat",
            "Flux/Matlab_200_Mahle.mat", "Flux/PSM_Measdata_1500rpm.mat",
            "Trq/Matlab_014_Mn_complete_active_fieldweakeningctrl.mat",
            "Flux/2025-07-09_UPI1000-ZF02_STLA_Gen2_800V_350kW_DS30a_FC09_080degC_00000-03121.mat"]:
            columns, values, *_ = operating_points(raw_root / relative)
            result["additional_raw_candidates"][relative] = summarize(columns, values)
    dual, _ = load_dataset("psm_dual_system_multirpm")
    old = dual["torque_map"] / 2
    mask = np.hypot(dual["id"], dual["iq"]) >= .1 * np.max(np.hypot(dual["id"], dual["iq"]))
    result["factor_two"] = dict(phase_selector=1, configured_systems=2, pole_pairs=4,
        old_kt=6, configured_total_kt=12,
        old_residual_rms=float(np.sqrt(np.mean((old[mask]-dual["torque"][mask])**2))),
        configured_residual_rms=float(np.sqrt(np.mean((dual["torque_map"][mask]-dual["torque"][mask])**2))),
        interpretation="Missing second three-phase-system contribution explains the leading factor; no CAN gain fitted",
        open="Equal per-system currents/fluxes assumed; independent sensor calibration and losses not established")
    (ROOT / "datasets/torque_candidate_audit.json").write_text(json.dumps(result, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run(Path(sys.argv[1]) if len(sys.argv)>1 else None)
