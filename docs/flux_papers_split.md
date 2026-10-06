# Two flux-map papers: current scope, evidence, and reproducibility

Updated 6 October 2026 after integration of the completed co-energy audit.
The combined `dq_flux_symmetry_diagnostics` draft was split incrementally;
correct derivations, sources, synthetic checks and figures were reused. It is
not an active third publication. Ignored snapshots under `tmp/` are recovery
material only. There is no MeasEval implementation or product workflow here.

## Scientific allocation

| Subject | Paper 1: reconstruction | Paper 2: diagnostics |
|---|---|---|
| Measurements to flux | Full voltage inversion and assumptions | Independent compact foundation and input sensitivities |
| Co-energy | Latent potential, normalization, gauge, topology, paths | Compact conservation baseline and independent cross-check |
| Reflection parity | Full magnetic symmetry derivation; distinct from conservation | Forbidden channels and observed spatial/thermal/speed structure |
| Saturation | Hessian, differential inductance, reciprocal cross-saturation | Operating-point-dependent angle sensitivity |
| Gradient fitting | Weights, regularization, rank, robust fitting and residuals | Diagnostic implications; no second fitter |
| B-splines/RBF | Existing spline illustration; conceptual RBF comparison | No experimental magnetic field fit |
| Resistance/voltage error | Admissibility boundary; real-data hypothetical adjustment | Conditional fingerprints and exact voltage-error confounding |
| Angle | Conservative rotations can change parity | Exact argument/vector rotation; reciprocity retained |
| Real-data audit | Full admissibility stress test, interpolation, coordinates and scaling | Compact symmetry/conservation cross-check and correction boundary |
| Multi-speed | Different rectangle support limits comparisons | Direct 36-common-pair check and conditional identifiability |
| Correction | No demonstrated physical correction or real-data reconstruction | Inverse operation checked synthetically; no automatic experimental correction |

Both manuscripts carry the minimum equations and assumptions needed for
independent reading. Neither includes the other's sections or table files.
Notation, glossary and semantic styles remain canonical in `shared/`; content,
figures, generated tables and literature remain paper-local. Companions are
explicitly unpublished working drafts, not published evidence.

## Paper 1

**Physics-Constrained Reconstruction of Saturated dq Flux-Linkage Maps from
Magnetic Co-Energy**, in `papers/physics_constrained_flux_maps/`.

Eleven sections cover introduction; measurements to flux; latent co-energy;
reflection/reciprocity; saturation/differential inductance; gradient fitting;
numerical representations; synthetic evaluation; real-data admissibility;
discussion; conclusions. Five existing figures remain.

For amplitude-invariant dq, the declared potential is physical three-phase
co-energy divided by 3/2; its gradient is flux and its Hessian differential
inductance. This normalization does not verify the actual measurement system.
The existing degree-four B-spline illustration has 32 coefficients, 31 after
gauge fixing. Gradient fitting avoids arbitrary integration paths. Flux accuracy,
derivative quality, parity, reciprocity and curvature are assessed separately.
The unchanged seeded `numerics/evaluation.json` gives exact flux/Hessian recovery
RMSE 1.12e-15/6.34e-15, and noisy independent/parity/potential flux RMSE
0.00243/0.00181/0.00150. The potential's Hessian RMSE (0.0124) is slightly worse
than the parity fit's (0.0111). Ordinary outlier fitting retains structural
parity/conservation yet develops a negative sampled Hessian eigenvalue (-0.0764).
Robust fitting improves that realization; no global positivity or universal
method ranking follows. RBFs have not been benchmarked.

The new real-data study is a **stress test of admissibility**, not demonstrated
real-data co-energy recovery. At 2000 rpm/60 C the high-current symmetry
resistance equivalent is 8.274010 mOhm, while the path median is 5.885553 mOhm
and exact-P1 median 5.885512 mOhm. The latter integrates the chosen interpolator
exactly, without establishing physical truth. Over all 2869 rectangles, the
500-point quadrature error is only 0.0000766 mOhm RMS. The gap survives it.

The path quantity averages curl over an oriented origin-to-target rectangle;
the endpoint does not identify a local material resistance. Its invariance
under arbitrary used-resistance shifts is algebraic, not a true-resistance
calibration. High-current parity improves under the tested scalar adjustment,
but all-pair d/vector RMS and median relative path disagreement increase.
Parity and integrability are independent. Componentwise C0 P1 interpolation
can break integrability of conservative nonlinear samples; skinny triangles
make local derivatives fragile. Terminal versus magnetizing coordinates require
a full differential-form transformation. RMS evidence suggests amplitude-
invariant currents but does not verify the Park transform or voltage/power
scale. No iron-loss cause is identified. A potential fit would project onto a
chosen model class; raw-to-model residuals must remain visible.

## Paper 2

**On the Interpretation of Symmetry Residuals in Experimental dq Flux-Linkage
Maps**, in `papers/flux_map_error_diagnostics/`.

Its research question concerns information in forbidden components and the
extent to which a sole constant-resistance mismatch explains their spatial,
thermal-reference and speed structure. Existing error derivations and synthetic
checks remain; twelve analytical/experimental figures remain. A new compact
conservation section follows the measured symmetry results and precedes
conditional identification. It reproduces the all-slice equivalent comparison
and the 60-C high-current/global/path contrast without duplicating fitting theory.

The real experiment does not identify true winding resistance, iron loss,
inverter, angle or sensor contributions. Rotor/stator reference temperatures
are not verified conductor temperatures. Constant coherent frame rotation
preserves reciprocity while rotating the symmetry axis. A current-proportional
voltage error exactly imitates resistance reconstruction bias, even across
multiple speeds. The retained direct 1000/3000-rpm comparison has 36 valid common
pairs; inverse-speed residual discrepancy is 0.157316 mWb RMS (0.157112 mWb
with measured-current ratio correction). Path supports of 65/45 rectangles
cannot substitute for that matched comparison.

Conditional identification and inverse correction remain known-model
analytical/synthetic results. They are not recovery or correction of either
measured machine. No automatic correction follows from smaller selected parity.

## Evidence, reuse and reproduction

The detailed [co-energy audit](../papers/physics_constrained_flux_maps/docs/coenergy_analysis_audit.md)
remains the evidence report. Its JSON/CSV and three scripts retain full measured
and synthetic results, source/input hashes, oriented-path/Green checks,
quadrature, geometry sensitivity and observable checks. It is not replaced by
manuscript prose. [The experimental report](flux_map_experimental_validation.md)
retains the original pairing and direct-speed evidence and records integration.

`magnetic_model.py`, importers, reconstruction modules and the two MAT inputs
remain unchanged. Each numerical experiment has its own local helper. The
standard-library `papers/physics_constrained_flux_maps/numerics/export_audit_tables.py`
reads existing audit JSON and exports identical concrete TeX tables plus
provenance hashes into each paper's `figures/data/audit/`. Neither build depends
on the other paper at LaTeX time. This intentional content reuse does not create
competing mathematical/visual infrastructure.

From the repository root, with the scientific Python dependencies installed:

```powershell
$env:MPLBACKEND='Agg'
python papers/physics_constrained_flux_maps/python/audit_coenergy.py
python papers/physics_constrained_flux_maps/python/audit_observables.py
python papers/physics_constrained_flux_maps/python/audit_symbolic.py
python papers/physics_constrained_flux_maps/numerics/export_audit_tables.py
python scripts/check_architecture.py
git diff --check
./scripts/build.ps1 physics_constrained_flux_maps
./scripts/build.ps1 flux_map_error_diagnostics
./scripts/build_all.ps1
```

Sources are used within verified scope: Haus/Melcher for nonlinear lossless
storage reciprocity; Jebai for energy/construction symmetry; Sun/Xiao for
separate parity/reciprocity/continuity requirements with losses excluded;
Richter et al. for magnetic versus terminal current; Liu et al. for competing
resistance/inverter uncertainties. Kullick/Hackl's journal result concerns
**induction machines**, not validation of a PMSM terminal-current potential.

## Remaining scientific work

Verify machine/acquisition provenance, actual conductor temperature, abc-to-dq
and voltage/power normalization, current/angle/timing calibration, and the
subsystem represented by a potential. Bound pairing/interpolation uncertainty
and obtain independent loss/voltage/thermal observables and repeat measurements.
Real-data potential recovery, causal correction, Monte Carlo uncertainty, an
RBF benchmark and convexity-constrained fitting remain research work. These
limits are explicit in the closed drafts; they are not omitted production tasks.

## Latest evidence-boundary revision

The storage/terminal distinction is now explicit throughout the reconstruction
paper, including the abstract and early measurement/potential/fitting sections.
Its coherent-rotation proof is locally readable. Apparent tilt is preserved as
possible loss/measurement information; a future joint speed/temperature study
requires independently measured winding state, calibrated added observables,
and an identifiable storage/loss/measurement model. The compact diagnostics
outlook agrees with this scope. See
[the section-by-section revision report](flux_paper_evidence_revision.md).
