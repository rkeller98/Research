"""Recheck CI fixture hashes and the edited torque workspace's lineage.

The optional MeasEval root is an explicit input; portable evaluations do not
depend on that checkout. No private absolute paths are exported.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import numpy as np
from scipy.io import loadmat

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared/python"))
from measurement_io import read_measurement, sha256


def audit(raw_root, measeval_root=None):
    parent_path = "Trq/Matlab_MnChar_PM2315_200521_028.mat"
    candidates = sorted((raw_root / "Trq").glob("*FakeForTesting*.mat"))
    if len(candidates) != 1:
        raise ValueError("Expected the single documented artificial torque fixture")
    fake = candidates[0]
    parent, _, _ = read_measurement(raw_root / parent_path)
    signals, _, _ = read_measurement(fake)
    workspace = loadmat(fake, simplify_cells=True)
    roots = [v for k, v in workspace.items() if k.startswith("Matlab") and isinstance(v, dict) and "Y" in v]
    alias = workspace["raw_data"]["Y"]
    original = roots[0]["Y"]
    assert [v["Name"] for v in alias] == [v["Name"] for v in original]
    same = all(np.array_equal(a["Data"], b["Data"], equal_nan=True) for a, b in zip(alias, original))
    assert same
    repeated = [k for k in parent if k in signals and np.array_equal(np.tile(parent[k], 2), signals[k], equal_nan=True)]
    result = dict(source=fake.relative_to(raw_root).as_posix(), same_workspace_alias=same,
                  records=len(signals["PE_Index_meas"]), parent_records=len(parent["PE_Index_meas"]),
                  exactly_repeated_parent_signals=repeated, classification="unknown: Machine_type missing",
                  policy="synthetically edited workspace fixture; excluded from independent experimental evidence")
    (ROOT / "datasets/artificial_fixture_audit.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    if measeval_root is None:
        return
    recipes = [("Test1", "EESM_Measdata_Reduced.mat"), ("Test2", "WW_Dataset_Merge_1.mat"),
               ("Test2", "WW_Dataset_Merge_2.mat"), ("Test3", "PSM_Measdata.mat"),
               ("Test4", "Matlab_005.mat"), ("Test4", "Matlab_006.mat")]
    fixtures = []
    for test, filename in recipes:
        local = raw_root / "Flux/CI_Test" / test / filename
        external = measeval_root / "SourceCode/tests" / test / filename
        checksum = sha256(local)
        assert checksum == sha256(external), f"Fixture differs: {test}/{filename}"
        fixtures.append(dict(test=test, file=filename, sha256=checksum, external_copy_verified=True))
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=measeval_root, text=True).strip()
    evidence = dict(commit=commit, fixtures=fixtures,
        classification="Test1 EESM; Test2 PSM two-system merge; Test3 PSM; Test4 ASM",
        enum_source="SourceCode/+backend/+enums/eMachineType.m",
        loader_source="SourceCode/+adapter/+matfile/inspect_measurement_files.m",
        assertions=["SourceCode/tests/test_data_check_test1_characterization.m", "SourceCode/tests/test_data_check_test2_characterization.m"],
        grouping_source="SourceCode/+backend/+product/+motor/+calculation/+input/DataConversion.m")
    (ROOT / "datasets/measeval_test_evidence.json").write_text(json.dumps(evidence, indent=2)+"\n", encoding="utf-8")
    print("Artificial lineage and all six external fixture hashes verified.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_root", type=Path)
    parser.add_argument("--measeval-root", type=Path)
    args = parser.parse_args()
    audit(args.raw_root, args.measeval_root)
