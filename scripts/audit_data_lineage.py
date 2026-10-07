"""Verify duplicate files and numeric signal lineage across raw formats."""
from collections import defaultdict
import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared/python"))
from measurement_io import read_measurement


def audit(raw_root):
    inventory = json.loads((ROOT / "datasets/raw_inventory.json").read_text(encoding="utf-8"))
    by_hash = defaultdict(list)
    for entry in inventory:
        by_hash[entry["sha256"]].append(entry["source"])
    comparisons = []
    base, _, _ = read_measurement(raw_root / "Flux/PSM_Measdata.mat")
    for relative in ["Flux/PSM_Measdata_2500rpm.mat", "Flux/PSM_Measdata_1500rpm.mat"]:
        signals, _, _ = read_measurement(raw_root / relative)
        equal = [k for k in base if k in signals and np.array_equal(base[k], signals[k], equal_nan=True)]
        changed = [k for k in base if k not in equal]
        comparisons.append(dict(base="Flux/PSM_Measdata.mat", variant=relative,
                                equal_signal_count=len(equal), changed_signals=changed))
    # These variants also occur in torque and merge regression fixtures.
    for original, variant in [
        ("Flux/Porsche/Matlab_033.mat", "Flux/Porsche/Matlab_033_MultiTempButDeactivated.mat"),
        ("Flux/Matlab_201_Mahle.mat", "Flux/WW_Dataset_neg_rpm_1.mat"),
        ("Flux/Matlab_200_Mahle.mat", "Flux/WW_Dataset_neg_rpm_2.mat"),
        ("Trq/Matlab_MnChar_PM2315_200521_028.mat", "Trq/Matlab_MnChar_PM2315_200521_028_neg_rpm.mat")]:
        a, _, _ = read_measurement(raw_root / original)
        b, _, _ = read_measurement(raw_root / variant)
        equal = [k for k in a if k in b and np.array_equal(a[k], b[k], equal_nan=True)]
        comparisons.append(dict(base=original, variant=variant, equal_signal_count=len(equal),
                                changed_signals=[k for k in a if k not in equal]))
    result = dict(exact_duplicate_groups=[v for v in by_hash.values() if len(v) > 1],
                  numeric_comparisons=comparisons,
                  policy="CI copies and edited speed/temperature variants are not independent experiments")
    (ROOT / "datasets/lineage.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    audit(Path(sys.argv[1]))
