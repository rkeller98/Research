"""Read MATLAB measurement exports without MeasEval or a MATLAB runtime.

The reader preserves channel metadata. It performs no scaling, imputation,
outlier removal, or machine-type fallback. Both v5 and v7.3 are supported.
"""

import hashlib
from pathlib import Path

import h5py
import numpy as np
from scipy.io import loadmat


def sha256(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def _text(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return "".join(str(x) for x in np.asarray(value).reshape(-1)).strip()


def read_measurement(path, selected=None):
    """Return signals, channel metadata, and recording description.

    selected=None reads all numeric channels; a set reads only those channels.
    Channel names/metadata are always inspected, including absent selections.
    """
    signals, metadata = {}, {}
    if h5py.is_hdf5(path):
        with h5py.File(path, "r") as file:
            roots = [
                file[k]
                for k in file
                if k != "#refs#" and isinstance(file[k], h5py.Group) and "Y" in file[k]
            ]
            if len(roots) != 1:
                raise ValueError(f"Expected one measurement root; found {len(roots)}")
            root, y = roots[0], roots[0]["Y"]

            def read_text(node):
                if isinstance(node, h5py.Group):
                    return {key: read_text(node[key]) for key in sorted(node)}
                if node.attrs.get("MATLAB_empty", 0):
                    return ""
                if h5py.check_dtype(ref=node.dtype) is not None:
                    return [read_text(file[ref]) for ref in node[()].reshape(-1)]
                if node.attrs.get("MATLAB_class", b"") != b"char":
                    return node[()].reshape(-1).tolist()
                return "".join(chr(int(x)) for x in node[()].reshape(-1)).strip("\0 ")

            names = y["Name"][()].reshape(-1)
            for n, ref in enumerate(names):
                name = read_text(file[ref])
                if name in metadata:
                    raise ValueError(f"Duplicate signal name: {name}")
                metadata[name] = {}
                for key in ("Unit", "Description", "Path", "Device"):
                    if key in y:
                        metadata[name][key.lower()] = read_text(
                            file[y[key][()].reshape(-1)[n]]
                        )
                if selected is None or name in selected:
                    node = file[y["Data"][()].reshape(-1)[n]]
                    if not node.attrs.get("MATLAB_empty", 0):
                        signals[name] = np.asarray(node[()], dtype=float).reshape(-1)
            description = (
                read_text(root["Description"]) if "Description" in root else ""
            )
            return signals, metadata, description
    loaded = loadmat(path, simplify_cells=True)
    named_roots = [
        (k, v)
        for k, v in loaded.items()
        if not k.startswith("__") and isinstance(v, dict) and "Y" in v
    ]
    # MeasEval selects the Matlab* measurement variable, not a saved workspace
    # alias named raw_data. Ambiguous independently named recordings still fail.
    matlab_roots = [v for k, v in named_roots if k.startswith("Matlab")]
    roots = matlab_roots if len(matlab_roots) == 1 else [v for _, v in named_roots]
    if len(roots) != 1:
        raise ValueError(f"Expected one measurement root; found {len(roots)}")
    root = roots[0]
    channels = root["Y"]
    if isinstance(channels, dict):
        channels = [channels]
    for channel in channels:
        name = _text(channel.get("Name"))
        if name in metadata:
            raise ValueError(f"Duplicate signal name: {name}")
        metadata[name] = {
            k.lower(): _text(channel.get(k))
            for k in ("Unit", "Description", "Path", "Device")
        }
        if selected is None or name in selected:
            signals[name] = np.asarray(channel.get("Data", []), dtype=float).reshape(-1)
    description = root.get("Description", "")
    return (
        signals,
        metadata,
        description if isinstance(description, dict) else _text(description),
    )
