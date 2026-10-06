# Two flux-map papers: scope, provenance, and validation

**Subsequent diagnostics revision (6 October 2026):** the diagnostics paper is
now titled *On the Interpretation of Symmetry Residuals in Experimental dq
Flux-Linkage Maps*. Its real-data analysis and current evidence boundaries
are documented in [the experimental report](flux_map_experimental_validation.md).
The allocation and synthetic-only validation below record the earlier split;
the former product correction workflow has since been removed from the paper.
The reconstruction paper is outside this subsequent task's implementation scope.

The combined `dq_flux_symmetry_diagnostics` working draft was divided
incrementally. Correct derivations, sources, numerical checks, and drawings
were reused; it is no longer an active third paper. The local pre-split snapshot
remains in the ignored `tmp/dq_split_snapshot/combined_draft/` for recovery.
Subsequent infrastructure backups under `tmp/` are also recovery material,
rather than additional publications.

## Scientific allocation

| Existing subject/result | Paper 1: reconstruction | Paper 2: diagnostics |
|---|---|---|
| Measurements and voltage balance | Measurement-to-flux route and assumptions | Compact foundation for error differentiation |
| Co-energy and gradient | Latent potential, normalization, PM tilt, gauge, paths, topology | Compact admissible-class foundation |
| Reflection and even/odd flux | Full conservative magnetic derivation | Reference structure and forbidden channels |
| Saturation and cross-saturation | Expansion, Hessian and differential gains | Operating-point-dependent angle sensitivity |
| Reciprocity | Integrability and fitting guarantee | Complementary test; does not identify angle by itself |
| Gradient fitting and regularization | Objective, weights, gauge and analytic derivatives | Brief bridge explaining residual information |
| B-spline/RBF representations | B-spline implementation; conceptual RBF comparison | No second fitting-method discussion |
| Measurement-input sensitivities | Reconstruction assumptions | Six sensitivities and nuisance alternatives |
| Resistance mismatch | Reconstruction bias boundary | Exact transverse field, parity and curl fingerprints |
| Rotor-angle offset | Companion boundary | Exact inner/outer rotations, sensitivity and limits |
| Speed and rank | Fitting coverage/rank | Speed separation, scaled rank, conditioning and delay |
| Correction/MeasEval | Corrected samples as a possible input | Map correction, relabeling, proposal/Apply workflow |
| Synthetic experiments | Noise, sparse sampling, outliers, stronger saturation | Injected resistance, angle, both, linearization and correction |

Necessary reconstruction equations appear in both drafts for independent
reading. Long magnetic theory and fitting theory belong to Paper 1. Paper 2
contains a compact foundation and cites the unpublished companion explicitly.
Both bibliographies are local. Neither companion is assigned a fictitious
published status, DOI, or measured accuracy.

## Paper 1

**Physics-Constrained Reconstruction of Saturated dq Flux-Linkage Maps from
Magnetic Co-Energy** lives in `papers/physics_constrained_flux_maps/`.

Its ten sections are introduction; measurement-to-flux; latent co-energy;
symmetry/reciprocity; saturation/differential inductance; physics-constrained
fitting; numerical realizations; synthetic evaluation; discussion; conclusion.
Five figures explain the measurement pipeline, reflection structure, potential
landscape, two paths, and fitted slopes/curvature.

For amplitude-invariant dq, the potential is physical three-phase co-energy
divided by 3/2. Its gradient is flux; its Hessian is differential inductance.
Data provide slopes, not independent energy heights. Gauge fixing removes
the constant ambiguity. Simply connected domains permit local curl equality
to establish a potential; domains with holes also require circulation checks.
Path integration explains the structure; the implementation fits gradients
jointly instead of integrating noisy samples into arbitrary energy data.

The candidate uses degree-four tensor B-splines, eight d bases and four even
q bases: 32 coefficients, 31 after gauge fixing. Analytic potential derivatives
provide flux and Hessian; a third-derivative penalty smooths flux curvature.
Independent/parity-only flux B-splines use second-derivative penalties. A shared
held-out flux split selects regularization within each case. These are related
but unequal optimization problems. Pointwise, derivative, parity, curl, and
eigenvalue metrics are assessed separately.

Results in `numerics/evaluation.json`:

| Check/illustration | Result in normalized units |
|---|---|
| Exact noiseless flux/Hessian recovery | RMSE 1.12e-15 / 6.34e-15 |
| Noisy independent / parity / potential flux RMSE | 0.00243 / 0.00181 / 0.00150 |
| Noisy parity / potential Hessian RMSE | 0.0111 / 0.0124 |
| Potential parity and curl | Zero by construction |
| Outlier potential / robust potential flux RMSE | 0.00739 / 0.00150 |
| Ordinary outlier minimum sampled Hessian eigenvalue | -0.0764 |
| Robust outlier minimum sampled eigenvalue | Approximately 0.401 |
| Stronger-saturation true minimum eigenvalue | 0.02 |
| Exact two-path disagreement | At most 2.22e-16 |
| Parity-only counterexample path difference at (0.6,0.7) | -0.294 |

The potential improves noisy flux prediction here but has slightly worse
derivatives than the parity fit. Constraints do not prove truth or convexity:
the outlier fit remains conservative and symmetric yet develops negative
sampled differential inductance. The robust case does not establish global
positivity or a universal ranking. RBFs are not numerically benchmarked.
Sparse sampling and stronger saturation are separate cases in the generated
table, rather than reused diagnostic injections.

## Paper 2

**Symmetry-Based Identification and Correction of Stator-Resistance and
Rotor-Angle Errors from dq Flux-Linkage Maps** lives in
`papers/flux_map_error_diagnostics/`.

Its eleven sections are introduction; reconstruction; admissible structure;
input sensitivities; exact angle transformation; residuals; identification;
synthetic examples; engineering/correction; limitations; conclusion. Six figures
show frames, parity decomposition, resistance fingerprint, the two angle
operations, speed separation, and injected-error maps.

Resistance error means used minus true; angle error means estimated minus
true electrical angle. Positive angle advances estimated axes counterclockwise,
while fixed-vector coordinates rotate oppositely. Exact rotation changes both
current argument and flux projection. Its Hessian is an orthogonal congruence
of the original Hessian: a coherent constant angle offset preserves reciprocity
while rotating the reflection axis. This prevents a false angle diagnosis by
curl alone and is preserved explicitly.

Resistance mismatch adds epsilon_R J i / omega_e at fixed observed current.
A voltage error proportional to -i produces exactly the same field; speed
diversity cannot distinguish these causes by itself. An estimate can identify
an effective drop mismatch without uniquely identifying DC winding resistance.
Temperature, frequency, pairing/interpolation, current labels, and delay
remain explicit nuisance assumptions.

The normalized polynomial includes reciprocal cross-saturation. On the stated
[-1.1,1.1]^2 domain positive diagonal dominance proves positive differential
gains. Errors are injected into generated voltages and maps reconstructed,
independently of the map derivation. The script differentiates the potential
symbolically and checks six measurement sensitivities, exact rotation, limiting
cases, speed scaling, confounding, rank, estimation signs, and correction.

Results in `numerics/validation.json`:

| Check/illustration | Result |
|---|---|
| Reference parity | Maximum 0 |
| Sampled minimum reference Hessian eigenvalue | 0.34 |
| Independent central-difference angle sensitivity | Maximum discrepancy 2.68e-10 |
| Resistance/voltage-error confounding | Maximum difference 1.11e-16 |
| Three-speed design | 90 pairs, rank 2, scaled condition number 1.248 |
| Injected joint resistance/angle | 0.025 ohm / 0.02 rad |
| First-order joint estimates | 0.02500021 ohm / 0.01999830 rad |
| Angle 0.02 full-map linearization discrepancy | 3.59e-4 times flux base |
| Angle 0.02 forbidden-residual discrepancy | 3.13e-6 times flux base |
| Correction maximum residual before/after | 0.07023 / 2.154e-6 times flux base |
| Proposed resistance from a used 0.105 ohm | 0.07999979 ohm |

The full-map remainder is quadratic locally. The forbidden residual remainder
is cubic in this smooth, exactly paired symmetric example because these
channels are odd in angle. This does not transfer automatically to arbitrary
noisy/interpolated pairs. Saturation can increase or reduce angle sensitivity;
no universal monotonic claim is made.

## Reuse, evidence, and remaining work

The small `magnetic_model.py` content helper is identical in both experiment
folders. Each script imports its own copy and runs independently. Tests compare
the baseline implementation with an independent symbolic expression. Experiments,
tables and plots belong to their respective papers; neither loads the other's
sections or numerical output. This content reuse is separate from the canonical
shared notation and presentation infrastructure.

Sources include Jebai et al.'s energy-based modeling and saturation papers in
Paper 1, Liu et al.'s resistance/inverter and position-offset work in Paper 2,
standard machine/matrix texts where cited, and official B-spline/RBF documentation.
Companion references are explicitly unpublished working drafts. The didactic
structure connects algebra, geometry, physics, engineering assumptions and
counterfactual cases.

Both are closed, buildable learning drafts. Measured-machine validation,
Monte Carlo uncertainty studies, an RBF benchmark, broader sampling/boundary
tests, explicit convexity-constrained fitting, and an implemented MeasEval
integration remain future work. These are limitations, not completed evidence.
Final build/layout checks are in [the architecture audit](architecture_migration.md).
