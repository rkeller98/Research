# Historical DAT exports

These five files were moved byte-for-byte from `sandbox/` on 8 October 2026.
They are preserved research inputs/results, separate from the eight canonical
operating-point CSV/JSON fixtures described in [the catalog](../README.md).
They have no canonical manifest and must not be loaded as v1 fixtures.

| File | Rows | Original columns | Known consumer / preservation reason |
|---|---:|---|---|
| `Dataset_for_ASM_torque_fitting.dat` | 2368 | id, iq, torque | No repository consumer found; raw grouping/source/calibration unknown |
| `Dataset_for_EESM_Fitting.dat` | 28875 | id, iq, iexc, torque | Excitation extends to 30 A, whereas the reduced canonical fixture covers requests 3/6 A; export recipe unknown |
| `Dataset_for_Inductance_Calculation.dat` | 10201 | id, iq, psi_d, psi_q, L_dd, L_dq, L_qd, L_qq | Contains differential-inductance results absent from canonical columns; derivation/fit recipe unknown |
| `Dataset_for_Outlier_Detection.dat` | 12882 | id, iq, torque | Full export differs from the reduced 320-OP stress fixture; grouping/source unknown |
| `Dataset_Raw_vs_Fitted_Flux.dat` | 8012 | id, iq, psi_d_raw, psi_d_fit, psi_q_raw, psi_q_fit | Input to archived `PY_RBF.py`; fitted fields have no documented regeneration recipe |

All five were compared with all eight canonical fixtures using their shared
numeric columns, including raw flux columns where applicable. No exported row
matched a canonical row within absolute Euclidean distance 1e-9 over all shared
finite columns. This is a comparison of stored observations, not a scientific
accuracy tolerance or proof of unrelated campaigns. Different grouping,
rounding, support and fitted quantities prevent a safe equivalence claim.
None is deleted or relabeled as calibrated evidence. No exporter or original
source hash establishing complete reproduction was found. Rights and original
provenance are not inferred from filenames.

Original paths and SHA-256 hashes are recorded in
[`docs/final_cleanup_manifest.json`](../../docs/final_cleanup_manifest.json).
The earlier column/evidence audit remains unchanged in
[`torque_consistency_integration.md`](../../_archive/composite_papers/physics_constrained_flux_maps/docs/torque_consistency_integration.md).
