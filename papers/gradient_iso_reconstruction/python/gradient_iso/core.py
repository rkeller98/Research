"""N-D MATLAB migration with explicit numerical and interpretation contracts.

Derivatives are with respect to the supplied coordinates. Normalize physical
coordinates explicitly before calling, and apply the chain rule afterwards.
Iso coverage is a geometric descriptor, not calibrated confidence.
"""
from dataclasses import dataclass, field
from itertools import combinations, product
import warnings

import numpy as np
from scipy.spatial import Delaunay, QhullError, cKDTree
from scipy.spatial.distance import cdist

from .backend import PointSet, SampledField, EdgeIntersector


@dataclass(frozen=True)
class Options:
    order: int = 1
    levels: int = 25
    validity_range: float = 3.0
    representative: str = "centroid"
    bandwidth: float | None = None
    sigma_factor: float = 1.0
    max_condition: float = 1e8
    max_simplices: int = 100_000
    max_intersections: int = 2_000_000
    level_mode: str = "uniform"
    query_chunk: int = 128
    intersection_chunk: int = 4096
    constant_tolerance: float = 1e-10

    def __post_init__(self):
        for name, lower in (("order", 1), ("levels", 2), ("max_simplices", 1),
                            ("max_intersections", 1), ("query_chunk", 1),
                            ("intersection_chunk", 1)):
            value = getattr(self, name)
            if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)) or value < lower:
                raise ValueError(f"{name} must be an integer >= {lower}")
        for name in ("validity_range", "max_condition", "constant_tolerance"):
            if not np.isfinite(getattr(self, name)) or getattr(self, name) <= 0:
                raise ValueError(f"{name} must be finite and positive")
        if self.bandwidth is not None and (not np.isfinite(self.bandwidth) or self.bandwidth <= 0):
            raise ValueError("bandwidth must be finite and positive")
        if not np.isfinite(self.sigma_factor):
            raise ValueError("sigma_factor must be finite")
        if self.representative not in ("centroid", "circumcenter"):
            raise ValueError("representative must be centroid or circumcenter")
        if self.level_mode not in ("uniform", "quantile"):
            raise ValueError("level_mode must be uniform or quantile")


@dataclass
class DerivativeCloud:
    order: int
    points: np.ndarray
    values: np.ndarray
    source_simplices: np.ndarray
    condition: np.ndarray
    inverse_edge_norm: np.ndarray
    rejected_simplices: int
    omitted_vertices: np.ndarray
    component_axes: tuple
    iso: list = field(default_factory=list)
    iso_status: list = field(default_factory=list)
    rms_edge_length: float = np.nan
    coverage: np.ndarray | None = None
    component_coverage: np.ndarray | None = None
    threshold: float = np.nan

    @property
    def raw_hessian(self):
        if self.order != 2:
            raise ValueError("A Hessian requires derivative order 2")
        d = self.points.shape[1]
        return self.values.reshape(-1, d, d)

    @property
    def symmetric_hessian(self):
        raw = self.raw_hessian
        return (raw + raw.transpose(0, 2, 1)) / 2

    @property
    def laplacian(self):
        return np.trace(self.raw_hessian, axis1=1, axis2=2)

    @property
    def symmetry_defect(self):
        raw = self.raw_hessian
        return np.linalg.norm(raw - raw.transpose(0, 2, 1), axis=(1, 2))


def triangulate(points):
    """Canonical input ordering; return indices in the caller's row basis."""
    basis = PointSet(points)
    x = basis.coordinates
    if x.shape[1] < 2 or len(x) < x.shape[1] + 1:
        raise ValueError("Need d >= 2 and at least d+1 unique support points")
    order = np.lexsort(tuple(x[:, j] for j in range(x.shape[1] - 1, -1, -1)))
    try:
        tri = Delaunay(x[order])
    except QhullError as exc:
        raise ValueError("Support is rank deficient or cannot be Delaunay triangulated") from exc
    simplices = order[tri.simplices]
    omitted = np.setdiff1d(np.arange(len(x)), simplices.ravel())
    return simplices, omitted


def simplex_derivatives(points, values, *, order=1, options=None):
    """Solve E G = delta V, with edge vectors as rows of E.

    All value components share one solve. G.T is flattened component-major:
    at order two: [f_11, f_12, ..., f_21, f_22, ...]. No least-squares
    fallback silently accepts rank-deficient cells. Condition refers to the
    anchored edge matrix in the supplied coordinate metric.
    """
    opts = options or Options()
    x = PointSet(points).coordinates
    v = np.asarray(values, dtype=float)
    if v.ndim == 1:
        v = v[:, None]
    if v.ndim != 2 or len(v) != len(x) or v.shape[1] < 1 or not np.isfinite(v).all():
        raise ValueError("values must be finite with shape (N,) or (N,C)")
    simplices, omitted = triangulate(x)
    if len(simplices) > opts.max_simplices:
        raise ValueError(f"{len(simplices)} simplices exceed max_simplices; reduce N, d or order")
    reps, gradients, kept, conds, inverse_norms = [], [], [], [], []
    for ids in simplices:
        pts = x[ids]
        e = pts[1:] - pts[0]
        singular = np.linalg.svd(e, compute_uv=False)
        cond = np.inf if singular[-1] == 0 else singular[0] / singular[-1]
        if not np.isfinite(cond) or cond > opts.max_condition:
            continue
        try:
            g = np.linalg.solve(e, v[ids[1:]] - v[ids[0]])
            rep = pts.mean(axis=0)
            if opts.representative == "circumcenter":
                rep = pts[0] + np.linalg.solve(2 * e, np.sum(e * e, axis=1))
        except np.linalg.LinAlgError:
            continue
        if not np.isfinite(g).all() or not np.isfinite(rep).all():
            continue
        reps.append(rep)
        gradients.append(g.T.ravel())
        kept.append(ids)
        conds.append(cond)
        inverse_norms.append(1 / singular[-1])
    if not reps:
        raise ValueError("No well-conditioned simplices remain")
    reps = np.asarray(reps)
    if len(np.unique(reps, axis=0)) != len(reps):
        raise ValueError("Duplicate representatives: use centroids or resolve geometry explicitly")
    d = x.shape[1]
    axes = tuple(product(range(d), repeat=order))
    return DerivativeCloud(order, reps, np.asarray(gradients), np.asarray(kept),
                           np.asarray(conds), np.asarray(inverse_norms),
                           len(simplices) - len(kept), omitted, axes)


def gaussian_coverage(queries, intersections, bandwidth, *, query_chunk=128, intersection_chunk=4096):
    """Exact all-intersection mean with bounded temporary memory.

    Preserve per-edge vertex multiplicity from EdgeIntersector. This is an
    empirical counting measure, not contour arc-length or surface measure.
    """
    if len(intersections) == 0:
        return np.full(len(queries), np.nan)
    result = np.zeros(len(queries))
    for start in range(0, len(queries), query_chunk):
        q = queries[start:start + query_chunk]
        total = np.zeros(len(q))
        for pstart in range(0, len(intersections), intersection_chunk):
            p = intersections[pstart:pstart + intersection_chunk]
            distances = cdist(q, p, metric="sqeuclidean")
            total += np.exp(-distances / (2 * bandwidth**2)).sum(axis=1)
        result[start:start + len(q)] = total / len(intersections)
    return result


def iso_diagnostics(cloud, opts):
    x, v = cloud.points, cloud.values
    cloud.iso, cloud.iso_status = [], []
    cloud.component_coverage = np.full_like(v, np.nan)
    cloud.coverage = np.full(len(x), np.nan)
    if len(x) < x.shape[1] + 1:
        cloud.iso = [None] * v.shape[1]
        cloud.iso_status = ["insufficient_support"] * v.shape[1]
        return
    simplices, _ = triangulate(x)
    if len(simplices) > opts.max_simplices:
        raise ValueError("Derivative basis exceeds max_simplices")
    pairs = np.asarray(list(combinations(range(x.shape[1] + 1), 2)))
    edges = np.unique(np.sort(simplices[:, pairs].reshape(-1, 2), axis=1), axis=0)
    edge_lengths = np.linalg.norm(x[edges[:, 1]] - x[edges[:, 0]], axis=1)
    cloud.rms_edge_length = np.sqrt(np.mean(np.sort(edge_lengths**2)))
    bandwidth = opts.bandwidth or cloud.rms_edge_length
    basis = PointSet(x)
    sampled = SampledField(basis, v)
    intersector = EdgeIntersector(basis, validity_range=opts.validity_range)
    # Guard the upstream (E,L) allocation, before invoking it. A conservative
    # bound uses all unique edges before the upstream length filter.
    if len(edges) * opts.levels > opts.max_intersections:
        raise ValueError("Edge-level product exceeds max_intersections; reduce levels or support")
    for component in range(v.shape[1]):
        vc = v[:, component]
        tolerance = opts.constant_tolerance * max(1., np.max(np.abs(vc)))
        if np.ptp(vc) <= tolerance:
            cloud.iso.append(None)
            cloud.iso_status.append("constant_component")
            continue
        levels = (np.linspace(vc.min(), vc.max(), opts.levels)
                  if opts.level_mode == "uniform" else
                  np.unique(np.quantile(vc, np.linspace(0, 1, opts.levels))))
        intersections = intersector.intersect(sampled, component, levels)
        cloud.iso.append(intersections)
        cloud.iso_status.append("ok" if len(intersections.coordinates) else "empty")
        cloud.component_coverage[:, component] = gaussian_coverage(
            x, intersections.coordinates, bandwidth, query_chunk=opts.query_chunk,
            intersection_chunk=opts.intersection_chunk)
    # All components must be defined. Constant components are not evidence of
    # low reliability, and must not become an artificial epsilon penalty.
    defined = np.isfinite(cloud.component_coverage).all(axis=1)
    scores = cloud.component_coverage[defined]
    with np.errstate(divide="ignore"):
        cloud.coverage[defined] = np.exp(np.mean(np.log(scores), axis=1))
    if defined.any():
        s = cloud.coverage[defined]
        cloud.threshold = float(s.mean() + opts.sigma_factor * (s.std(ddof=1) if len(s) > 1 else 0))


def reconstruct(points, values, options=None):
    """Return derivative clouds for orders 1..K; iso diagnostics per order.

    Recursion differentiates reinterpolated derivative samples on new meshes.
    It does not compute the classical Hessian of the original P1 interpolant.
    """
    opts = options or Options()
    v = np.asarray(values, dtype=float)
    if v.ndim == 2 and v.shape[1] == 1:
        v = v[:, 0]
    if v.ndim != 1:
        raise ValueError("reconstruct requires a scalar field with shape (N,) or (N,1)")
    clouds = []
    x = PointSet(points).coordinates
    for order in range(1, opts.order + 1):
        if v.size * x.shape[1] > opts.max_simplices * 100:
            raise ValueError("Derivative component growth exceeds the research memory guard")
        cloud = simplex_derivatives(x, v, order=order, options=opts)
        if len(cloud.omitted_vertices):
            warnings.warn(f"Order {order}: Qhull omitted {len(cloud.omitted_vertices)} support points", RuntimeWarning)
        iso_diagnostics(cloud, opts)
        clouds.append(cloud)
        x, v = cloud.points, cloud.values
    return clouds


def search_guidance(clouds, input_points, *, step_fraction=.25, minimize=False):
    """Conservative heuristic proposals in the supplied coordinate metric.

    Step uses a fraction of the nearest input-point spacing at each centroid.
    Undefined iso coverage does not suppress an exact constant gradient.
    Proposals outside the input convex hull are flagged. Caller must check
    domain constraints and accept/reject using new objective evaluations.
    """
    if not np.isfinite(step_fraction) or step_fraction <= 0:
        raise ValueError("step_fraction must be finite and positive")
    first = clouds[0]
    x = PointSet(input_points).coordinates
    d = x.shape[1]
    if first.points.shape[1] != d or first.values.shape[1] != d:
        raise ValueError("First cloud must be a scalar gradient in the input dimension")
    norm = np.linalg.norm(first.values, axis=1)
    direction = np.divide(first.values, norm[:, None], out=np.zeros_like(first.values), where=norm[:, None] > 0)
    if minimize:
        direction = -direction
    top = clouds[-1]
    index = cKDTree(top.points).query(first.points)[1]
    coverage = top.coverage[index]
    spacing = cKDTree(x).query(first.points, k=2)[0][:, 1]
    step = step_fraction * spacing
    step[norm == 0] = 0
    proposed = first.points + step[:, None] * direction
    order = np.lexsort(tuple(x[:, j] for j in range(d - 1, -1, -1)))
    inside = Delaunay(x[order]).find_simplex(proposed) >= 0
    return {"points": first.points, "direction": direction, "step": step,
            "proposed": proposed, "inside_hull": inside, "coverage": coverage,
            "coverage_transfer_distance": np.linalg.norm(top.points[index] - first.points, axis=1),
            "linear_gain": norm * step}
