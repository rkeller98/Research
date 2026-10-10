"""Portable operating-point CSV + JSON contract, version 1.

CSV uses UTF-8, LF, comma separator, .17g IEEE-double precision, empty missing
values. The manifest is sorted JSON and binds the CSV with SHA-256.
"""

import csv
import hashlib
import io
import json
from pathlib import Path

import numpy as np

VERSION = "research-operating-points-v1"
REQUIRED = {
    "schema_version",
    "dataset_id",
    "machine_type",
    "provenance",
    "columns",
    "dq_convention",
    "torque",
    "aggregation",
    "known_limitations",
    "data_rights",
}


def validate(manifest, columns, values):
    if not REQUIRED <= manifest.keys() or manifest["schema_version"] != VERSION:
        raise ValueError("Missing manifest fields or unsupported schema")
    if manifest["machine_type"] not in {"PSM", "EESM", "ASM", "unknown"}:
        raise ValueError("Unsupported machine type")
    if len(set(columns)) != len(columns) or columns != list(manifest["columns"]):
        raise ValueError("Column order/identity differs from manifest")
    if values.ndim != 2 or values.shape[1] != len(columns) or np.isinf(values).any():
        raise ValueError("Invalid matrix shape or infinite value")
    if any(
        not entry.get("unit") or "source" not in entry
        for entry in manifest["columns"].values()
    ):
        raise ValueError("Each column needs a unit and source")
    for source in manifest["provenance"]["sources"]:
        path = Path(source["path"])
        if path.is_absolute() or ":" in source["path"] or ".." in path.parts:
            raise ValueError("Provenance must use relative paths")
        if len(source["sha256"]) != 64:
            raise ValueError("Invalid source SHA-256")


def export_canonical_dataset(stem, columns, values, manifest):
    stem = Path(stem)
    values = np.asarray(values, dtype=float)
    validate(manifest, columns, values)
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(columns)
    writer.writerows(
        [["" if np.isnan(x) else format(x, ".17g") for x in row] for row in values]
    )
    payload = buffer.getvalue().encode("utf-8")
    manifest = dict(
        manifest,
        csv_file=stem.name + ".csv",
        row_count=len(values),
        csv_sha256=hashlib.sha256(payload).hexdigest(),
    )
    stem.parent.mkdir(parents=True, exist_ok=True)
    stem.with_suffix(".csv").write_bytes(payload)
    # Insertion order of columns is meaningful; sort all other manifest keys.
    ordered = {key: manifest[key] for key in sorted(manifest)}
    stem.with_suffix(".json").write_text(
        json.dumps(ordered, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return ordered


def import_canonical_dataset(stem):
    stem = Path(stem)
    manifest = json.loads(stem.with_suffix(".json").read_text(encoding="utf-8"))
    if manifest["csv_file"] != stem.name + ".csv":
        raise ValueError("Manifest CSV filename mismatch")
    payload = stem.with_suffix(".csv").read_bytes()
    if hashlib.sha256(payload).hexdigest() != manifest["csv_sha256"]:
        raise ValueError("CSV checksum mismatch")
    records = list(csv.reader(io.StringIO(payload.decode("utf-8"))))
    columns = records[0]
    values = np.asarray(
        [[float(x) if x else np.nan for x in row] for row in records[1:]], dtype=float
    )
    if len(values) != manifest["row_count"]:
        raise ValueError("Row count mismatch")
    validate(manifest, columns, values)
    return columns, values, manifest


def load_dataset(dataset_id, root=None):
    root = Path(root) if root else Path(__file__).resolve().parents[2] / "datasets"
    columns, values, manifest = import_canonical_dataset(root / dataset_id)
    return {name: values[:, n] for n, name in enumerate(columns)}, manifest
