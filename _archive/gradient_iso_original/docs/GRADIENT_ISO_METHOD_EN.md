# Gradient-Iso Method (N-D): Complete Engineering Documentation

## 1. Purpose and Scope

The **Gradient-Iso method** reconstructs local differential structure from an unstructured point cloud of scalar measurements.

Given samples
- input points: `X in R^(Nxd)`
- scalar field values: `f in R^N`

it builds, in a fully geometric and model-agnostic way:
- first-order derivative field (gradient)
- second-order derivative field (Hessian, if requested)
- Laplacian (trace of Hessian, if requested)
- confidence estimates for local reliability
- search guidance (directions and candidate next points)

This is not tied to a specific domain (e.g., electrical machines). It is an **N-dimensional general method**.

---

## 2. High-Level Idea

Instead of fitting one global surrogate model, the method uses **local simplex geometry**:

1. Build Delaunay simplices in the current domain.
2. Fit local affine maps inside each simplex.
3. Extract local derivatives from affine coefficients.
4. Recursively repeat on derivative clouds to obtain higher-order derivatives.
5. Build iso-derivative structures and derive a confidence score from their local density/consistency.
6. Use derivative direction + confidence for search guidance.

Why this is useful:
- preserves local structure
- avoids global model bias
- naturally supports irregular sampling
- scales conceptually to arbitrary dimension `d`

---

## 3. Inputs and Main Outputs

## 3.1 Primary Inputs

- `X [N x d]`: domain points
- `f [N x 1]`: scalar values at points in `X`
- `approx_order (K >= 1)`: derivative order depth
- options (`opts`):
  - `M`: number of iso levels per derivative component
  - `validity_range`: Delaunay edge-length based filtering factor
  - `point_mode`: simplex representative (`centroid` or `circumcenter`)
  - `sigma_factor`: confidence threshold factor
  - `bandwidth`: Gaussian kernel bandwidth for confidence scoring

## 3.2 Main Outputs

- `result.orders{k+1}`: reconstructed field at order `k` (`k=0..K`)
- `result.confidence`: score, mean/std, threshold, mask
- `result.derivatives`:
  - `gradient` (if `K>=1`)
  - `hessian` and `laplacian` (if `K>=2`)
- `result.search_guidance`:
  - maximize/minimize directions
  - confidence-scaled step sizes
  - candidate next points

---

## 4. Step-by-Step Method Breakdown

## Step 0: Validate Inputs

### Input
`X`, `f`, `approx_order`, `opts`

### Thought
Before geometric operations, we must guarantee shape, finiteness, and consistency.

### What is done
- check numeric, finite, real arrays
- ensure `size(X,1) == size(f,1)`
- ensure enough points for triangulation: `N >= d+1`

### Why
Most downstream failures in geometric methods are caused by invalid/degenerate input.

### Output
Validated and safe working set.

### What matters
If your data are sparse or degenerate, all later derivative estimates degrade.

---

## Step 1: Build Order-0 Representation

### Input
Validated `X`, `f`

### Thought
We keep the raw scalar field as order 0 baseline.

### What is done
- store original points/values as level 0
- compute Delaunay triangulation on `X`

### Why
This level is the reference domain for all recursive derivative levels.

### Output
`orders{1}` containing raw field information.

### What matters
Delaunay quality strongly affects local neighborhoods and conditioning.

---

## Step 2: Local Affine Fit per Simplex (Core Derivative Primitive)

### Input
Current cloud `(current_X, current_V)` at recursion level `ord-1`

### Thought
Inside one simplex, a local affine approximation is the smallest stable differential model.

### What is done
For each simplex:
1. select simplex vertices
2. choose representative point (`centroid`/`circumcenter`)
3. solve linear system for affine coefficients
4. derivative = linear coefficient part

If previous level has multiple components, do this for each component.

### Why
For affine `a^T x + b`, derivative is directly available and local.

### Output
- `reps`: representative points for this order
- `grads`: derivative components at representatives

### What matters
- rank-deficient local systems are skipped
- local geometry quality determines derivative quality

---

## Step 3: Build Derivative Cloud for Current Order

### Input
`reps`, `grads`

### Thought
The derivative itself becomes a new sampled field.

### What is done
- remove invalid rows
- triangulate on representative points
- keep edge-validity information (`valid_vectors`)

### Why
Recursion requires a clean cloud at each derivative order.

### Output
`orders{ord+1}` with points, derivative values, triangulation.

### What matters
If too many simplices are invalid, recursion can stop due to too few support points.

---

## Step 4: Build Iso-Derivative Bundle

### Input
Packed cloud `[reps, grads]`, triangulation, number of levels `M`

### Thought
Derivative consistency can be inspected through iso-structures per component.

### What is done
For each derivative component:
- sample `M` iso levels from min to max
- run simplex-based iso search (`delaunay_search_N`) per level
- store iso points/levels

### Why
Iso geometry provides robust structural information beyond pointwise derivative noise.

### Output
`iso.levels`, `iso.points`, `iso.labels`

### What matters
`M` too low misses structure; `M` too high increases cost and sensitivity.

---

## Step 5: Compute Confidence Score

### Input
Top-order domain points + iso bundles

### Thought
A point should be trusted if nearby derivative iso-structure is dense and coherent.

### What is done
- collect iso points per component
- compute Gaussian distance-based local score per point/component
- aggregate component scores by geometric mean
- compute threshold `mu + sigma_factor * std`

### Why
Confidence separates reliable from uncertain local differential statements.

### Output
`result.confidence`:
- `score`
- `mean`, `std`
- `threshold`
- `mask`

### What matters
Confidence is not only for anomaly flags; it is crucial for search risk control.

---

## Step 6: Explicit Derivative Outputs (Engineering Layer)

### Input
`orders`, `approx_order`

### Thought
Users need direct access to physical/mathematical objects, not only raw component vectors.

### What is done
- always expose gradient (`K>=1`)
- if `K>=2`, reshape second-order components into Hessian matrices
- compute Laplacian = `trace(Hessian)`

### Why
This enables optimization and curvature-based reasoning directly.

### Output
`result.derivatives.gradient`, `result.derivatives.hessian`, `result.derivatives.laplacian`

### What matters
Second-order information needs adequate sampling density; otherwise curvature can be noisy.

---

## Step 7: Search Guidance Construction (N-D, Domain-Agnostic)

### Input
Gradient cloud + confidence scores

### Thought
A practical method must propose **where to go next** and **how much to trust the proposal**.

### What is done
At each guidance point:
- compute gradient norm
- build normalized maximize/minimize directions
- map confidence onto adaptive step size
- generate candidate next points:
  - `next_point_maximize`
  - `next_point_minimize`
- compute an improvement proxy

### Why
Direction without confidence is risky; confidence without direction is not actionable.

### Output
`result.search_guidance` with vectors, step sizes, proposals, and confidence.

### What matters
This layer is intentionally generic; domain constraints can be added on top.

---

## 5. Interpretation Guide

## 5.1 Gradient
- Points toward local increase of the scalar field.
- Larger norm means stronger local change.

## 5.2 Hessian
- Encodes local curvature and coupling between dimensions.
- Useful for detecting ridges, valleys, and saddle behavior.

## 5.3 Laplacian
- Summarizes net local curvature.
- Positive/negative trends can indicate bowl-like vs ridge-like local behavior (context-dependent).

## 5.4 Confidence
- High confidence: local derivative structure is geometrically coherent.
- Low confidence: consider more sampling before trusting optimization steps.

---

## 6. Complexity and Practical Limits

- Delaunay triangulation can become expensive in high dimensions.
- Memory and simplex count can grow quickly with `d` and `N`.
- Recursive orders reduce effective sample robustness.

Practical guidance:
- start with `K=1`
- use `K=2` only when sampling density is sufficient
- tune `M`, `validity_range`, and confidence settings before increasing complexity

---

## 7. Parameter Tuning Recommendations

- `M` (iso levels):
  - low: faster, less detail
  - high: richer structure, more noise/cost sensitivity

- `validity_range`:
  - lower: stricter geometric filtering
  - higher: more coverage, possible instability

- `sigma_factor`:
  - lower: more points considered uncertain
  - higher: stricter uncertainty flagging

- `point_mode`:
  - `centroid`: generally robust default
  - `circumcenter`: can be useful but may be less stable in some geometries

---

## 8. Failure Modes and Safeguards

Potential failure modes:
- degenerate simplices / rank deficiency
- sparse local coverage
- noisy second-order reconstructions
- confidence mismatch across recursion levels

Safeguards already in code:
- rank checks
- invalid simplex skipping
- minimum-support checks (`>= d+1`)
- confidence projection back to guidance level

Recommended additional safeguards (future work):
- Hessian symmetrization and conditioning checks
- bounded/constraint-aware step proposals
- adaptive bandwidth selection
- local re-sampling policy when confidence is low

---

## 9. Minimal Usage Pattern (MATLAB)

```matlab
opts = struct();
opts.M = 28;
opts.validity_range = 3;
opts.point_mode = 'centroid';
opts.sigma_factor = 1.0;

res = gradient_iso_pipeline_nd(X, f, 2, opts);

G = res.derivatives.gradient;      % gradient field
H = res.derivatives.hessian;       % Hessian field (if K>=2)
L = res.derivatives.laplacian;     % Laplacian (if K>=2)
S = res.search_guidance;           % direction + next-point proposals
C = res.confidence;                % confidence score and threshold
```

---

## 10. What This Method Is and Is Not

It is:
- a geometric differential reconstruction method for unstructured N-D scalar data
- a confidence-aware search guidance method
- domain-agnostic and recursive

It is not:
- a global regression model
- guaranteed globally optimal search
- a replacement for domain constraints/safety logic

---

## 11. Summary

The Gradient-Iso method transforms sparse scalar samples into actionable local differential intelligence:
- **what the local trend is** (gradient)
- **how the local landscape bends** (Hessian/Laplacian)
- **how much to trust this information** (confidence)
- **where to evaluate next** (search guidance)

This makes it suitable as a core module for general N-dimensional measurement-driven optimization workflows.
