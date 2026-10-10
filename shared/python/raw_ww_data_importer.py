from pathlib import Path

import h5py
import numpy as np
import pandas as pd
from numpy.typing import NDArray
from scipy import stats


class RawDataImporter:
    def __init__(self, file_path: str):
        path = Path(file_path)

        if not path.is_file():
            raise FileNotFoundError(f"{path} was not found or is not a file.")

        self._file_path = path

    def _find_measurement_group(self, file):
        groups = [
            file[name]
            for name in file.keys()
            if name != "#refs#"
            and isinstance(file[name], h5py.Group)
            and "Y" in file[name]
        ]

        if len(groups) != 1:
            raise ValueError(
                f"Expected exactly one MATLAB measurement group, found {len(groups)}."
            )

        return groups[0]["Y"]

    def __str__(self) -> str:
        with h5py.File(self._file_path, "r") as file:
            y = self._find_measurement_group(file)

            names = [self._read_matlab_string(file, ref) for ref in y["Name"][:, 0]]

        return "\n".join(names)

    def _read_matlab_string(self, file, ref) -> str:
        values = file[ref][()].reshape(-1)
        return "".join(chr(value) for value in values).strip()

    def get_signal(self, name: str) -> NDArray[np.float64]:
        with h5py.File(self._file_path, "r") as file:
            y = self._find_measurement_group(file)

            for index, name_ref in enumerate(y["Name"][:, 0]):
                signal_name = self._read_matlab_string(file, name_ref)

                if signal_name == name:
                    data_ref = y["Data"][index, 0]
                    return np.asarray(file[data_ref][()], dtype=np.float64).reshape(-1)

        raise KeyError(f"Signal '{name}' was not found.")
