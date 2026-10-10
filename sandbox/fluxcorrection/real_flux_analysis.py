# %% Daten laden
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import RBFInterpolator

repo_root = Path("/Users/raphaelkeller/Development/Research")
sys.path.insert(0, str(repo_root))

from shared.python.canonical_dataset import load_dataset

data, metadata = load_dataset("psm_temperature_2500")

mask = np.isclose(data["rotor_temp_ref"], 70.0)

# %% Flussverkettungen rekonstruieren
i_d = data["id"][mask]
i_q = data["iq"][mask]

u_d = data["ud"][mask]
u_q = data["uq"][mask]

omega_e = data["omega_e"][mask]
rs = data["rs_used"][mask] * 0.265

psi_d = (u_q - rs * i_q) / omega_e
psi_q = (rs * i_d - u_d) / omega_e

# %% Split data for training and fit check
numel = len(i_d)
index = np.arange(numel)
rng = np.random.default_rng(42)
idx_random = rng.permutation(index)
idx_split = int(np.floor(numel * 0.8))
idx_training = idx_random[:idx_split]
idx_test = idx_random[idx_split:]

i_d_train = i_d[idx_training]
i_q_train = i_q[idx_training]
psi_d_train = psi_d[idx_training]
psi_q_train = psi_q[idx_training]

i_d_test = i_d[idx_test]
i_q_test = i_q[idx_test]
psi_d_test = psi_d[idx_test]
psi_q_test = psi_q[idx_test]

# %% Prepare for Approximation
Iref = np.max(np.sqrt(i_d_train**2 + i_q_train**2))
y_train = np.column_stack((i_d_train, i_q_train)) / Iref
y_test = np.column_stack((i_d_test, i_q_test)) / Iref

psi_d_rbf_handle = RBFInterpolator(
    y_train, psi_d_train, smoothing=0.01, epsilon=1, kernel="inverse_multiquadric"
)
psi_q_rbf_handle = RBFInterpolator(
    y_train, psi_q_train, smoothing=0.01, epsilon=1, kernel="inverse_multiquadric"
)

psi_d_rbf_train = psi_d_rbf_handle(y_train)
psi_q_rbf_train = psi_q_rbf_handle(y_train)

psi_d_rbf_test = psi_d_rbf_handle(y_test)
psi_q_rbf_test = psi_q_rbf_handle(y_test)


# %% Fit quality
d_psi_d_train = psi_d_rbf_train - psi_d_train
d_psi_q_train = psi_q_rbf_train - psi_q_train

rms_d_train = np.sqrt(np.mean(d_psi_d_train**2))
rms_q_train = np.sqrt(np.mean(d_psi_q_train**2))

norm_d = np.ptp(psi_d_train)
norm_q = np.ptp(psi_q_train)

nrms_d_train = rms_d_train / norm_d * 100
nrms_q_train = rms_q_train / norm_q * 100

print(f"RMS e_psi_d_train = {rms_d_train}, NRMS = {nrms_d_train} %")
print(f"RMS e_psi_q_train = {rms_q_train}, NRMS = {nrms_q_train} %")

# %% Validate with test data
d_psi_d_test = psi_d_rbf_test - psi_d_test
d_psi_q_test = psi_q_rbf_test - psi_q_test

rms_d_test = np.sqrt(np.mean(d_psi_d_test**2))
rms_q_test = np.sqrt(np.mean(d_psi_q_test**2))

nrms_d_test = rms_d_test / norm_d * 100
nrms_q_test = rms_q_test / norm_q * 100

print(f"RMS e_psi_d_test = {rms_d_test}, NRMS = {nrms_d_test} %")
print(f"RMS e_psi_q_test = {rms_q_test}, NRMS = {nrms_q_test} %")

# %% Check integrability
N_vec = 100
id_vec = np.linspace(np.min(i_d), np.max(i_d), N_vec)
iq_vec = np.linspace(np.min(i_q), np.max(i_q), N_vec)

id_grid, iq_grid = np.meshgrid(id_vec, iq_vec)

y = np.column_stack((np.ravel(id_grid), np.ravel(iq_grid))) / Iref
psi_d_grid = np.array(psi_d_rbf_handle(y)).reshape(N_vec, -1)
psi_q_grid = np.array(psi_q_rbf_handle(y)).reshape(N_vec, -1)

Ldq_grid, Ldd_grid = np.gradient(psi_d_grid, iq_vec, id_vec)
Lqq_grid, Lqd_grid = np.gradient(psi_q_grid, iq_vec, id_vec)

I_max = np.max(i_d**2 + i_q**2) ** 0.5
valid_mask = (id_grid**2 + iq_grid**2) <= I_max**2

Ldd_valid = np.where(valid_mask, Ldd_grid, np.nan)
Ldq_valid = np.where(valid_mask, Ldq_grid, np.nan)
Lqd_valid = np.where(valid_mask, Lqd_grid, np.nan)
Lqq_valid = np.where(valid_mask, Lqq_grid, np.nan)

r_int = Ldq_valid - Lqd_valid

min_int = np.nanmin(r_int)
max_int = np.nanmax(r_int)
mean_int = np.nanmean(r_int)
rms_int = np.sqrt(np.nanmean(r_int**2))
std_int = np.nanstd(r_int)

print(f"MIN int: {min_int}")
print(f"MAX int: {max_int}")
print(f"AVG int: {mean_int}")
print(f"RMS int: {rms_int}")
print(f"STD int: {std_int}")

# %% Plot
fig, ((ax_dd, ax_dq), (ax_qd, ax_qq)) = plt.subplots(
    2, 2, subplot_kw={"projection": "3d"}
)
for ax, L_val, index in (
    (ax_dd, Ldd_valid, "dd"),
    (ax_dq, Ldq_valid, "dq"),
    (ax_qd, Lqd_valid, "qd"),
    (ax_qq, Lqq_valid, "qq"),
):
    ax.scatter(
        id_grid[valid_mask],
        iq_grid[valid_mask],
        L_val[valid_mask] * 1000,
        c=L_val[valid_mask],
    )
    ax.set_title(rf"$L_{{{index}}}$")
    ax.set_xlabel(r"$i_d$ in A")
    ax.set_ylabel(r"$i_q$ in A")
    ax.set_zlabel(rf"$L_{{{index}}}$ in mH")

fig, ax = plt.subplots(1, 1, subplot_kw={"projection": "3d"})
ax.scatter(
    id_grid[valid_mask],
    iq_grid[valid_mask],
    r_int[valid_mask] * 1000,
    c=r_int[valid_mask],
)
ax.set_xlabel(r"$i_d$ in A")
ax.set_ylabel(r"$i_q$ in A")
ax.set_zlabel("r_int in mH")

fig, (ax1, ax2) = plt.subplots(1, 2, subplot_kw={"projection": "3d"})
ax1.scatter(i_d_train, i_q_train, psi_d_rbf_train, label="fit")
ax1.scatter(i_d, i_q, psi_d, label="real")
ax1.legend()

ax2.scatter(i_d_train, i_q_train, psi_q_rbf_train, label="fit")
ax2.scatter(i_d, i_q, psi_q, label="real")
ax2.legend()

fig, (ax1, ax2) = plt.subplots(1, 2, layout="constrained")
cbar1 = ax1.scatter(i_d, i_q, c=psi_d)
ax1.set_aspect("equal")

cbar2 = ax2.scatter(i_d, i_q, c=psi_q)
ax2.set_aspect("equal")

fig.colorbar(cbar1, ax=ax1)
fig.colorbar(cbar2, ax=ax2)
plt.show()

# %%
