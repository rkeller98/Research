from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from shared.python.raw_ww_data_importer import RawDataImporter

# ============================================================
# Modellparameter
# ============================================================

PSI_PM = 0.08  # Permanentmagnetfluss [Vs]
LD = 0.0005  # d-Induktivität [H]
LQ = 0.0008  # q-Induktivität [H]

F_E = 100  # Elektrische Frequenz [Hz]
OMEGA_E = 2 * np.pi * F_E  # Elektrische Kreisfrequenz [rad/s]

R_FE = 10.0  # Eisenverlustwiderstand [Ohm]


# ============================================================
# Magnetisches Modell
# ============================================================


def get_magnetic_coenergy(id_m, iq_m):
    coenergy = PSI_PM * id_m + 0.5 * LD * id_m**2 + 0.5 * LQ * iq_m**2
    return coenergy


def get_magnetic_flux(id_m, iq_m):
    psi_d = PSI_PM + LD * id_m
    psi_q = LQ * iq_m

    return psi_d, psi_q


def get_numeric_flux(id_m, iq_m, coenergy):
    id_values = id_m[0, :]
    iq_values = iq_m[:, 0]

    psi_q, psi_d = np.gradient(coenergy, iq_values, id_values, edge_order=2)

    return psi_d, psi_q


# ============================================================
# Eisenverlustmodell
# ============================================================


def get_induced_voltage(psi_d, psi_q, omega_e):
    e_d = -omega_e * psi_q
    e_q = omega_e * psi_d

    return e_d, e_q


def get_iron_loss_currents(e_d, e_q, r_fe):
    i_fe_d = e_d / r_fe
    i_fe_q = e_q / r_fe

    return i_fe_d, i_fe_q


def get_stator_currents(id_m, iq_m, i_fe_d, i_fe_q):
    id_s = id_m + i_fe_d
    iq_s = iq_m + i_fe_q

    return id_s, iq_s


# ============================================================
# Numerische Diagnose
# ============================================================


def print_flux_errors(psi_d, psi_q, psi_d_num, psi_q_num):
    error_d = np.max(np.abs(psi_d_num - psi_d))
    error_q = np.max(np.abs(psi_q_num - psi_q))

    print(f"Max. d-Flussfehler: {error_d:.3e} Vs")
    print(f"Max. q-Flussfehler: {error_q:.3e} Vs")


# ============================================================
# Visualisierung
# ============================================================


def plot_results(id_m, iq_m, psi_d, psi_q, coenergy):
    fig = plt.figure(figsize=(16, 5))

    # d-Flusskennfeld
    ax_d = fig.add_subplot(131, projection="3d")
    ax_d.plot_surface(id_m, iq_m, psi_d)

    ax_d.set_title("d-Flusskennfeld")
    ax_d.set_xlabel(r"$i_d$ in A")
    ax_d.set_ylabel(r"$i_q$ in A")
    ax_d.set_zlabel(r"$\psi_d$ in Vs")

    # q-Flusskennfeld
    ax_q = fig.add_subplot(132, projection="3d")
    ax_q.plot_surface(id_m, iq_m, psi_q)

    ax_q.set_title("q-Flusskennfeld")
    ax_q.set_xlabel(r"$i_d$ in A")
    ax_q.set_ylabel(r"$i_q$ in A")
    ax_q.set_zlabel(r"$\psi_q$ in Vs")

    # Magnetische Coenergy
    ax_coenergy = fig.add_subplot(133, projection="3d")
    ax_coenergy.plot_surface(id_m, iq_m, coenergy)

    ax_coenergy.set_title("Magnetische Coenergy")
    ax_coenergy.set_xlabel(r"$i_d$ in A")
    ax_coenergy.set_ylabel(r"$i_q$ in A")
    ax_coenergy.set_zlabel(r"$W'$ in J")

    fig.tight_layout()


def plot_current_mapping(id_m, iq_m, id_s, iq_s, i_fe_d, i_fe_q):
    fig, (ax_grid, ax_vectors) = plt.subplots(1, 2, figsize=(13, 5))

    # Magnetisierungsstrom vs. Statorstrom
    ax_grid.scatter(id_m[::5, ::5], iq_m[::5, ::5], label="Magnetisierungsstrom")

    ax_grid.scatter(id_s[::5, ::5], iq_s[::5, ::5], label="Statorstrom")

    ax_grid.set_title("Stromraumtransformation")
    ax_grid.legend()

    # Eisenverluststrom als Vektorfeld
    ax_vectors.quiver(
        id_m[::5, ::5],
        iq_m[::5, ::5],
        i_fe_d[::5, ::5],
        i_fe_q[::5, ::5],
        angles="xy",
        scale_units="xy",
        scale=1,
    )

    ax_vectors.set_title("Eisenverluststromfeld")

    # Gemeinsame Achseneinstellungen
    for ax in (ax_grid, ax_vectors):
        ax.set_xlabel(r"$i_d$ in A")
        ax.set_ylabel(r"$i_q$ in A")
        ax.set_aspect("equal")
        ax.grid(True)

    fig.tight_layout()


def plot_flux_comparison(id_m, iq_m, id_s, iq_s, psi_d):
    fig = plt.figure(figsize=(12, 5))

    ax_m = fig.add_subplot(121, projection="3d")
    ax_s = fig.add_subplot(122, projection="3d")

    # Fluss über Magnetisierungsströmen
    ax_m.plot_surface(id_m, iq_m, psi_d)

    # Derselbe Fluss über Statorströmen
    ax_s.plot_surface(id_s, iq_s, psi_d)

    ax_m.set_title("Magnetisierungsstromraum")
    ax_s.set_title("Statorstromraum")

    for ax in (ax_m, ax_s):
        ax.set_xlabel(r"$i_d$ [A]")
        ax.set_ylabel(r"$i_q$ [A]")
        ax.set_zlabel(r"$\psi_d$ [Vs]")

        ax.view_init(elev=25, azim=-60)

    fig.tight_layout()


def plot_coenergy_risiduum():
    omg = np.linspace(-100, 1e5, 10000)

    rint = 2 * omg * LD * LQ * R_FE / (R_FE**2 + omg**2 * LD * LQ)

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(omg, rint)
    ax.set_xlabel(r"$\omega_e$ [rad/s]")
    ax.set_ylabel(r"$r_{\mathrm{int}}$ [H]")
    ax.grid(True)


# ============================================================
# Hauptprogramm
# ============================================================

if __name__ == "__main__":
    data_path = Path(r"C:\Git\Research\Test_Daten\Test_Daten\Flux\PSM_Measdata.mat")

    importer = RawDataImporter(str(data_path))

    id_meas = importer.get_signal("PE_Id_meas_avg")
    iq_meas = importer.get_signal("PE_Iq_meas_avg")
    ud_meas = importer.get_signal("PE_Ud_meas_avg")
    uq_meas = importer.get_signal("PE_Uq_meas_avg")

    omega_e = importer.get_signal("PE_w_el_rad_avg")
    rs = importer.get_signal("Const_Machine_R_s")
    temp_ref = importer.get_signal("Rotor_temp_ref")

    print(f"Messdatensätze: {len(id_meas)}")
    print(f"Temperaturreferenzen: {np.unique(temp_ref)}")

    # Magnetisierungsstromgitter erzeugen
    i = np.linspace(-100, 100, 51)
    id_m_grid, iq_m_grid = np.meshgrid(i, i)

    # Magnetisches Modell berechnen
    psi_d_grid, psi_q_grid = get_magnetic_flux(id_m_grid, iq_m_grid)

    coenergy = get_magnetic_coenergy(id_m_grid, iq_m_grid)

    # Fluss numerisch aus Coenergy ableiten
    psi_d_numeric_grid, psi_q_numeric_grid = get_numeric_flux(
        id_m_grid, iq_m_grid, coenergy
    )

    # Induzierte Spannungen berechnen
    e_d_grid, e_q_grid = get_induced_voltage(psi_d_grid, psi_q_grid, OMEGA_E)

    # Eisenverlustströme berechnen
    i_fe_d_grid, i_fe_q_grid = get_iron_loss_currents(e_d_grid, e_q_grid, R_FE)

    # Gesamte Statorströme berechnen
    id_s_grid, iq_s_grid = get_stator_currents(
        id_m_grid, iq_m_grid, i_fe_d_grid, i_fe_q_grid
    )

    # Numerische Validierung
    print_flux_errors(psi_d_grid, psi_q_grid, psi_d_numeric_grid, psi_q_numeric_grid)

    # Visualisierung
    plot_results(id_m_grid, iq_m_grid, psi_d_grid, psi_q_grid, coenergy)

    plot_current_mapping(
        id_m_grid, iq_m_grid, id_s_grid, iq_s_grid, i_fe_d_grid, i_fe_q_grid
    )

    plot_flux_comparison(id_m_grid, iq_m_grid, id_s_grid, iq_s_grid, psi_d_grid)
    plot_flux_comparison(id_m_grid, iq_m_grid, id_s_grid, iq_s_grid, psi_q_grid)

    plot_coenergy_risiduum()

    a = OMEGA_E * LQ / R_FE
    b = OMEGA_E * LD / R_FE

    A = np.array([[1, -a], [b, 1]])

    J_psi_m = np.diag([LD, LQ])
    J_psi_s = J_psi_m @ np.linalg.inv(A)
    print(J_psi_s)

    plt.show()
