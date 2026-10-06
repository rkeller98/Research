from pathlib import Path

import h5py
import numpy as np
from numpy.typing import NDArray


class RawDataImporter:
    """Minimal reader for the MATLAB v7.3 measurement files used in this paper."""

    def __init__(self, file_path: str | Path):
        path = Path(file_path)

        if not path.is_file():
            raise FileNotFoundError(f"{path} was not found or is not a file.")

        self._file_path = path

    def __repr__(self) -> str:
        return f"{type(self).__name__}(file_path={self._file_path!r})"

    def __str__(self) -> str:
        return "\n".join(self.get_signal_names())

    def _find_measurement_group(self, file: h5py.File) -> h5py.Group:
        groups = [
            file[name]
            for name in file.keys()
            if name != "#refs#"
            and isinstance(file[name], h5py.Group)
            and "Y" in file[name]
        ]

        if len(groups) != 1:
            raise ValueError(
                "Expected exactly one MATLAB measurement group containing 'Y', "
                f"found {len(groups)}."
            )

        return groups[0]["Y"]

    @staticmethod
    def _read_matlab_string(file: h5py.File, ref) -> str:
        values = file[ref][()].reshape(-1)
        return "".join(chr(int(value)) for value in values).strip()

    def get_signal_names(self) -> list[str]:
        with h5py.File(self._file_path, "r") as file:
            y = self._find_measurement_group(file)
            return [self._read_matlab_string(file, ref) for ref in y["Name"][:, 0]]

    def get_signal(self, name: str) -> NDArray[np.float64]:
        with h5py.File(self._file_path, "r") as file:
            y = self._find_measurement_group(file)

            for index, name_ref in enumerate(y["Name"][:, 0]):
                signal_name = self._read_matlab_string(file, name_ref)

                if signal_name == name:
                    data_ref = y["Data"][index, 0]
                    return np.asarray(
                        file[data_ref][()],
                        dtype=np.float64,
                    ).reshape(-1)

        raise KeyError(f"Signal '{name}' was not found.")
