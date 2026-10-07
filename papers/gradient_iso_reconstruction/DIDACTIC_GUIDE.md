# Didactic contract for Gradient-Iso

Read `../../WRITING_GUIDE.md` and `../../docs/didactic_contract.md` first.
The paper uses the shared notation, glossary, styles and publication structure.

The reader should discover a simplex gradient as directional finite differences,
not memorize an augmented matrix inversion. Coordinate scaling must precede
triangulation: it selects a metric and changes locality. Show the chain rule
before interpreting derivatives in physical units.

Distinguish curvature bias from noise amplification. Explain determinant as
volume and singular values as directional observability. An exact value fit
through d+1 samples has no redundancy with which to diagnose its gradient.

Recursive lifting creates a new support and a new interpolant at every order.
Keep mixed partials raw; symmetrization removes antisymmetry without proving
accuracy. The Laplacian cannot distinguish every saddle from a flat field.

Iso cuts are per-edge geometric observations. Explain their interpolation
invariant, plateau omissions, vertex multiplicity, level-range sensitivity and
bandwidth limits. Derive the score as a kernel integral of a counting measure.
Use the affine counterexample before proposing any confidence interpretation.

Synthetic labels must follow the source vertices. Cells share measurements;
use independent dataset seeds rather than treating all cells as independent.
Show measured trial improvement alongside linear predictions and report
negative evidence without recasting it as successful anomaly detection.