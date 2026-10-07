# Torque consistency: manuscript integration and evidence audit

Status: integrated into the existing physics-constrained manuscript.
This record accompanies the paper; the paper itself owns the derivation and
interpretation. The research note and its forty checks remain intact.

## Manuscript changes

- Abstract and introduction pose the observability question and distinguish
  known-field tests from conditional real observations.
- Section 05b, between differential inductance and fitting, derives the
  projection, local rank-one kernel, solution line, minimum-change and
  weighted representatives, smooth reciprocal radial ambiguity, polar
  co-energy interpretation, voltage/torque rank and power identity.
- Section 06 adds covariance-whitened electrical and torque observation
  blocks for a common potential with explicit nuisance parameters.
  Reconstructed flux replaces voltage; it is not counted as an additional
  independent observation. No arbitrary empirical weights or real estimator
  are claimed.
- Section 08 retains the original fitting experiments and adds normal,
  radial and mixed perturbations, inverse-current noise amplification and
  an even reciprocal five-column rank example.
- Section 08c presents the actual Multi_RPM channel inventory, qualification
  failure, matched OP reduction, residual maps, statistics and sensitivities.
- Discussion and conclusion distinguish electromagnetic, shaft, loss and
  acceleration terms and state what is still needed for identification.
- The diagnostic companion gets one compact cross-reference, not another
  torque derivation or repeated dataset analysis.

The title retains co-energy as the central framework. No separate paper
is created. Torque is a complementary observation of the same unknown field.

## Data inventory and selection

The script inventories every non-temporary MAT file and deduplicates copies
by SHA-256. There are two unique originals, with copies in both papers and
an additional Outlier copy in sandbox. Existing CSVs are derived exports,
not independent flux references. No raw dq flux signal is present.

The five sandbox DAT exports were also inspected by actual column headers:
ASM and Outlier fitting exports have id/iq/torque; the EESM export adds
iexc; the inductance export has flux components and differential inductances;
Raw_vs_Fitted_Flux has raw/fitted flux components. None combines CAN torque,
flux/voltage, speed and thermal metadata with a traceable common observation
definition. They cannot be joined into a qualified torque/flux reference
merely because current-column names match. They are not the chosen evidence.

Primary source: python/WW_Dataset_Multi_RPM.mat.
Selection: requested speed 1000/3000 rpm and Rotor_temp_ref=70.
Each slice contains 327 finite records, 109 OP groups with three records
each, and 104 distinct requested-current keys. All OP groups are retained.

Electrical fields:
PE_Id_meas_avg, PE_Iq_meas_avg, PE_Ud_meas_avg, PE_Uq_meas_avg.
Selection and alignment:
PE_Rpm_req, Rotor_temp_ref,
PE_Index_Flx_Char_StatorCurrent_OP_param_none.
Configuration: Const_Machine_R_s and Const_Machine_pole_pairs.
Additional observations: CAN_Torque_meas, PE_speed_rpm, I_exc_meas.
Requested currents define matched-speed labels only; no measured current
or voltage is rounded before reconstructing flux.

The existing build_ww_measurement_slice and
FluxMapSymmetryAnalyzer.flux_points supply the flux inversion unchanged.
CAN and speed use the same OP indices. Equal OP weight is used for slice
metrics; repeated requested labels are averaged only for the separate
matched-speed comparison. There is no residual-dependent filter,
interpolation, inferred gain, sign reversal, or resistance adjustment.

Multi_RPM supplies quiet repeat observations relative to the large spatial
disagreement, two speed slices and repeated directional coverage.
Outlier has a much broader numeric CAN range and is not the primary torque
reference. No noise distribution is inferred from that range alone.

## CAN qualification gate

Checked raw Y fields: Unit, Description, Device, Path, Raster and XIndex;
also raw X, root recording description and signal lists. Repository text
searches for CAN_Torque_meas, Torque_meas, torque, moment, loss torque and
friction provide no sensor definition or calibration. The recording origin
names software_standard_002_005_001_030.sdf/.rta and the DS1202 MicroLabBox,
but those defining files and a DBC/A2L sensor definition are absent.

Unit and Description are empty; Device is Platform; Path ends in a generic
recorder-values path. Root metadata identify ControlDesk 6.4 and a recording
date, not a torque transducer. The CAN speed channel and torque requests
are zero. PE_speed_rpm is nonzero and close to requested speed.
The X array increases but its unit and measurement-window interpretation
are unspecified; averaging synchronization and acceleration are unverified.
Temperature references are constant and there is no excitation sweep.

Outcome: no proven torque unit, sensor location/source, sign calibration,
gain, offset or loss compensation. Neither electromagnetic torque nor
measured shaft torque is established. For illustration only, CAN numbers
are interpreted as Nm with unity gain and their recorded sign.
Superscript CAN labels the conditional residuals. No electromagnetic
reference, real flux error, loss model or corrected map is identified.

## Conditioning and interpretation

Only normalized residuals require I_s > 0.10*max(I_s) per slice. This caps
torque-to-flux noise conversion relative to full current at a factor ten;
it is not a calibrated noise threshold. The unnormalized residual retains
all groups. Fractions .05/.15/.20 and complete quantiles are exported.
One near-origin OP is omitted at the primary threshold per speed.

The generated tables report bias, MAE, RMSE, median and 5/95% quantiles.
JSON additionally reports 25/75% quantiles, repeat scatter, support and
current/angle bins. A small signed bias conceals large opposite-sign
directional contributions. Residual maps preserve measured coordinates
and avoid an interpolated appearance of unsupported coverage.
Under the conversion hypothesis, CAN is approximately twice the calculated
moment; the descriptive ratio is exported on |M_map|>=10 Nm without
calibrating anything. Requested-to-recorded speed replacement and mean-product
sensitivity are much smaller than the discrepancy. A fixed resistance
error alone would have a different speed scaling on matched current.
Configured pole pairs cancel between kT and requested electrical speed
when flux is voltage-inverted; changing p alone cannot explain this ratio.

Possible explanations remain torque or dq scaling, sensor gain/offset,
voltage reconstruction, current/coordinate error, loss, dynamic averaging,
temperature, and magnetic map error. A common proper rotation of current
and flux preserves torque; inconsistent coordinates do not. No causal
selection is made from low residual or ideal matrix rank.

## Seven research figures reviewed

| Research figure | Manuscript decision |
|---|---|
| 01 directions | Redrawn in English, combined with projection in geometry panel (a). |
| 02 projection | Combined into geometry panel (a); no redundant standalone plot. |
| 03 solution line | Redrawn as geometry panel (b), with radial alternative. |
| 04 correction | Combined into geometry panel (b); explicitly one representative. |
| 05 synthetic residual map | Replaced by a known-current-angle perturbation test; the main spatial maps use actual real support. |
| 06 observability spectrum | Replaced by a generated rank/nullity table for an even reciprocal basis; log-floor singular values do not add needed information. Original broader checks remain. |
| 07 noise | Redrawn in English and combined with the perturbation test; mWb units and analytic/Monte Carlo distinction. |

Four paper-owned vector PDFs are generated by the local script. Fonts and
semantic colors come from shared/python/publication_plotting.py and its
canonical TeX palette. Geometry markers, curve patterns, open/filled shapes
and size encode distinctions independently of color. Real plots label the
CAN conversion hypothesis and actual support; no map is corrected.
The measurement pipeline now shows the three consistency channels.
Only these four generated figure PDFs are exempted from the global PDF ignore.
QA rasters and temporary scripts stay under ignored tmp.

## Mathematical sanity and limits

The local torque row has units A, its flux input Wb and output Nm/kT.
The residual normalization is Wb; radial coefficients and f'(I_s^2/2)
have units H. Co-energy uses the established Wb A dq normalization.
Clockwise normal is -J i_s, so normal residual correction is -e_psi n_tau.
Resistance error retains used-minus-true and its torque equivalent has
the minus sign required by that convention.

The origin has rank zero and undefined normalized projection. The two
axes, all four quadrants, both torque signs and signed speeds are checked.
EESM uses stator magnitude only at fixed excitation; full three-current
reciprocity can retain f(s,i_e). A constant positive isotropic inductance
is reciprocal, even, positive in curvature and torque-invisible.
Pointwise minimum-change projection need not preserve curl.
Torque plus reciprocity never supports a full-flux-recovery claim.
Gauge fixing and regularization uniqueness are distinct from observation rank.

## Reproduction and QA

Run from the repository root with the existing Python environment:

    python papers/physics_constrained_flux_maps/numerics/torque_consistency.py
    python papers/physics_constrained_flux_maps/numerics/evaluate.py
    python papers/physics_constrained_flux_maps/python/audit_coenergy.py
    python papers/physics_constrained_flux_maps/python/audit_observables.py
    python papers/physics_constrained_flux_maps/python/audit_symbolic.py
    pwsh -File scripts/build_all.ps1

The torque pipeline preserves 40 checks and adds 18, all passing.
CSV/TeX/JSON and four timestamp-free vector PDFs reproduced byte-for-byte
in a second run (15 generated files). Both original input hashes match.
The original gradient-fitting and full real co-energy audit, quadrant
orientation/resistance-invariance and independent symbolic checks pass.
Repeated fitting results differ from checked-in exports only at numerical
roundoff; those unrelated exports are retained instead of introducing noise.
No original data or production/measurement-evaluation code is edited.

The target and all nine manuscripts are built through the architecture gate.
All pages of the target are rendered for review, new math/figures/tables and
glossary pages inspected at full size, and new figures reviewed in grayscale.
Float boundaries keep the two evaluation studies before the next sections.
The pre-existing diagnostic-paper overfull vbox of 1.1203pt in its angle
section is recorded separately; no blanket warning suppression is used.
The writing guide is rechecked for canonical notation/style, explicit
assumptions, dimensional signs, limiting cases and evidence level.

## Split decision and next experimental evidence

Keep this contribution in physics_constrained_flux_maps. Projection and
radial-null analysis strengthen its physical-information argument, but the
present real comparison is unqualified and no calibrated improvement over
existing validation methods or identified global reconstruction is shown.
A separate experimental paper is not yet justified.

Needed next: source model/DBC or sensor documentation; verified torque
unit/sign/gain/offset and transducer location; synchronized averages and
mechanical-speed timing; inertia/loss evidence if shaft torque is used;
independent winding temperature and dq voltage/current scaling; and
electrical/magnetic information to constrain remaining radial modes.
