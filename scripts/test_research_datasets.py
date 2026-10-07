"""Transport, schema, scientific identities and deterministic-export checks."""
from pathlib import Path
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import numpy as np
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared/python"))
from canonical_dataset import import_canonical_dataset, export_canonical_dataset


def run():
    checks = []
    schema = json.loads((ROOT / "datasets/schema/operating_points_v1.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    with tempfile.TemporaryDirectory(prefix="research-datasets-") as directory:
        for path in sorted((ROOT / "datasets").glob("*.csv")):
            columns, values, manifest = import_canonical_dataset(path.with_suffix(""))
            validator.validate(manifest)
            out = Path(directory) / path.stem
            export_canonical_dataset(out, columns, values, manifest)
            assert out.with_suffix(".csv").read_bytes() == path.read_bytes()
            assert out.with_suffix(".json").read_bytes() == path.with_suffix(".json").read_bytes()
            d = dict(zip(columns, values.T))
            assert np.all(d["sample_count"] >= 1)
            assert np.allclose(d["psi_d"], (d["uq"]-d["rs_used"]*d["iq"])/d["omega_e"], rtol=1e-14)
            assert np.allclose(d["psi_q"], (d["rs_used"]*d["id"]-d["ud"])/d["omega_e"], rtol=1e-14)
            assert np.allclose(d["torque_map"],d["kt"]*(d["psi_d"]*d["iq"]-d["psi_q"]*d["id"]),equal_nan=True)
            bad = copy.deepcopy(manifest)
            bad["provenance"]["sources"][0]["path"] = "C:/private/raw.mat"
            try:
                export_canonical_dataset(out, columns, values, bad)
            except ValueError:
                pass
            else:
                raise AssertionError("Absolute provenance path accepted")
            out.with_suffix(".csv").write_bytes(out.with_suffix(".csv").read_bytes()+b"0")
            try:
                import_canonical_dataset(out)
            except ValueError:
                pass
            else:
                raise AssertionError("Corrupt data accepted")
            checks.append(dict(dataset=path.stem, exact_roundtrip=True, flux_and_torque_identities=True,
                               corruption_rejected=True, private_absolute_path_rejected=True))
    # Scientific reports and publication figures must reproduce byte-for-byte.
    paths = []
    for paper in ["flux_correction_symmetry","magnetic_coenergy_consistency","flux_correction_coenergy","torque_flux_consistency","flux_error_identifiability"]:
        paths.extend((ROOT/"papers"/paper/"numerics").glob("real_evaluation.json"))
        paths.extend((ROOT/"papers"/paper/"figures").glob("real_*.pdf"))
        paths.extend((ROOT/"papers"/paper/"figures/data").glob("real_*.tex"))
        paths.extend((ROOT/"papers"/paper/"figures/data").glob("real_*.csv"))
    before = {p:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    subprocess.run([sys.executable,str(ROOT/"scripts/evaluate_portfolio.py")],check=True)
    assert before == {p:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    report = dict(dataset_checks=checks, portable_evaluation_byte_identical_files=len(paths))
    (ROOT/"datasets/verification.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(f"{len(checks)} fixtures and {len(paths)} reproducible scientific artifacts verified.")


if __name__ == "__main__":
    run()
