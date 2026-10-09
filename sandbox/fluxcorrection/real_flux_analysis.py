from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from shared.python.raw_ww_data_importer import RawDataImporter


DATA_PATH = Path(
    r"C:\Git\Research\Test_Daten\Test_Daten\Flux\PSM_Measdata.mat"
)


if __name__ == "__main__":

    importer = RawDataImporter(str(DATA_PATH))

    op_index = importer.get_signal("PE_Index_meas")
    id_meas = importer.get_signal("PE_Id_meas_avg")
    iq_meas = importer.get_signal("PE_Iq_meas_avg")
    ud_meas = importer.get_signal("PE_Ud_meas_avg")
    uq_meas = importer.get_signal("PE_Uq_meas_avg")
    temp_ref = importer.get_signal("Rotor_temp_ref")  

    # Zunächst nur die 70-°C-Referenzmessung
    mask = np.isclose(temp_ref, 30.0)

    id_70 = id_meas[mask]
    iq_70 = iq_meas[mask]
    
    indices, counts = np.unique(
        op_index[mask],
        return_counts=True
    )
    
    print("Anzahl Messdatensätze:", len(id_70))
    print("Anzahl Betriebspunkte:", len(indices))
    print("Messwerte pro Betriebspunkt:", np.unique(counts))

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.scatter(id_70, iq_70, s=10, alpha=0.5)

    ax.set_xlabel(r"$i_d$ [A]")
    ax.set_ylabel(r"$i_q$ [A]")
    ax.set_title("Strombetriebspunkte bei 70 °C")

    ax.set_aspect("equal")
    ax.grid(True)

    plt.show()