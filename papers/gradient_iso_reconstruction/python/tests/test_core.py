import numpy as np
import pytest
from numpy.testing import assert_allclose

from gradient_iso import Options, reconstruct, simplex_derivatives, search_guidance
from gradient_iso.core import gaussian_coverage
from gradient_iso.backend import PointSet, SampledField, EdgeIntersector


@pytest.mark.parametrize("d", [2, 3, 4])
def test_affine_reproduction_and_constant_iso(d):
    x = np.random.default_rng(17).uniform(-1, 1, (50, d))
    g = np.arange(1., d + 1)
    cloud = reconstruct(x, x @ g + 3)[0]
    assert_allclose(cloud.values, np.broadcast_to(g, cloud.values.shape), atol=3e-12)
    assert set(cloud.iso_status) == {"constant_component"}
    assert np.isnan(cloud.coverage).all()
    guidance = search_guidance([cloud], x)
    assert_allclose(guidance["direction"], np.broadcast_to(g / np.linalg.norm(g), cloud.values.shape))
    assert (guidance["linear_gain"] > 0).all()


def test_translation_component_order_and_chain_rule():
    rng = np.random.default_rng(3)
    x = rng.uniform(-1, 1, (70, 2))
    h = np.array([[2., 3.], [3., 5.]])
    # Differentiate the exact vector gradient; isolates tensor packing from
    # the separate approximation error of recursive reconstruction.
    c = simplex_derivatives(x, x @ h, order=2)
    assert_allclose(c.raw_hessian, np.broadcast_to(h, c.raw_hessian.shape), atol=1e-11)
    assert_allclose(c.symmetry_defect, 0, atol=1e-11)
    assert_allclose(c.laplacian, 7)
    moved = simplex_derivatives(x + [1000, -2000], x @ h, order=2)
    assert_allclose(moved.raw_hessian, np.broadcast_to(h, moved.raw_hessian.shape), atol=1e-8)
    scales = np.array([10., .2])
    physical = x * scales
    g = np.array([2., -5.])
    c = simplex_derivatives(x, physical @ g)
    assert_allclose(c.values / scales, np.broadcast_to(g, c.values.shape), atol=1e-11)


def test_recursive_affine_zero_hessian_and_laplacian():
    x = np.random.default_rng(13).normal(size=(60, 2))
    first, second = reconstruct(x, x @ [2., -1.] + 7, Options(order=2))
    assert_allclose(second.raw_hessian, 0, atol=3e-10)
    assert_allclose(second.laplacian, 0, atol=3e-10)
    assert first.order == 1 and second.order == 2


def test_row_permutation_invariance():
    x = np.random.default_rng(19).normal(size=(60, 2))
    y = np.sum(x**2, axis=1)
    p = np.random.default_rng(9).permutation(len(x))
    a, b = reconstruct(x, y)[0], reconstruct(x[p], y[p])[0]
    ia = np.lexsort((a.points[:, 1], a.points[:, 0]))
    ib = np.lexsort((b.points[:, 1], b.points[:, 0]))
    assert_allclose(a.points[ia], b.points[ib])
    assert_allclose(a.values[ia], b.values[ib])
    assert_allclose(a.coverage[ia], b.coverage[ib], atol=1e-14)


def test_circumcenter_has_exact_isotropic_quadratic_gradient():
    x = np.array([[0., 0.], [2., 0.], [.4, .3]])
    values = .5*np.sum(x*x, axis=1)
    c = simplex_derivatives(x, values, options=Options(representative="circumcenter"))
    assert_allclose(c.points, [[1, -11/12]])
    assert_allclose(c.values, c.points)
    centroid = simplex_derivatives(x, values)
    assert not np.allclose(centroid.values, centroid.points)


def test_chunked_kernel_is_exact():
    rng = np.random.default_rng(2)
    q, p = rng.normal(size=(21, 3)), rng.normal(size=(35, 3))
    expected = np.exp(-np.sum((q[:, None] - p[None])**2, axis=2) / (2 * .7**2)).mean(axis=1)
    assert_allclose(gaussian_coverage(q, p, .7, query_chunk=4, intersection_chunk=5), expected)
    assert np.isnan(gaussian_coverage(q, p[:0], .7)).all()


def test_shared_intersector_invariant_and_plateau_contract():
    points = PointSet([[0, 0], [1, 0], [0, 1], [1.1, 1]])
    field = SampledField(points, np.column_stack((points.coordinates @ [2., 1.], np.ones(4))))
    intersector = EdgeIntersector(points)
    cuts = intersector.intersect(field, 0, [.5, 1.5])
    assert_allclose(cuts.values[:, 0], cuts.levels)
    assert_allclose(cuts.coordinates @ [2., 1.], cuts.levels)
    assert len(intersector.intersect(field, 1, [1]).coordinates) == 0


def test_noise_covariance_matches_edge_geometry():
    x = np.array([[0., 0.], [1., 0.], [.2, .4]])
    cloud = simplex_derivatives(x, np.zeros(3))
    ids = cloud.source_simplices[0]
    e = x[ids[1:]] - x[ids[0]]
    inv = np.linalg.inv(e)
    covariance = inv @ (np.eye(2) + np.ones((2, 2))) @ inv.T
    eta = np.random.default_rng(71).normal(size=(150_000, 3))
    estimates = np.linalg.solve(e, (eta[:, ids[1:]] - eta[:, ids[0], None]).T).T
    assert_allclose(np.cov(estimates, rowvar=False), covariance, rtol=.02, atol=.02)


def test_support_and_guard_failures():
    with pytest.raises(ValueError, match="unique"):
        reconstruct([[0, 0], [0, 0], [1, 1]], [0, 1, 2])
    with pytest.raises(ValueError, match="rank deficient"):
        reconstruct([[0, 0], [1, 1], [2, 2]], [0, 1, 2])
    with pytest.raises(ValueError, match="finite"):
        reconstruct([[0, 0], [1, 0], [0, 1]], [0, np.nan, 1])
    x = np.random.default_rng(1).normal(size=(30, 2))
    with pytest.raises(ValueError, match="max_simplices"):
        reconstruct(x, np.sum(x**2, axis=1), Options(max_simplices=1))
    with pytest.raises(ValueError, match="max_intersections"):
        reconstruct(x, np.sum(x**2, axis=1), Options(max_intersections=1))
    c = reconstruct([[0, 0], [1, 0], [0, 1]], [0, 1, 2])[0]
    assert_allclose(c.values, [[1, 2]])
    assert c.iso_status == ["insufficient_support"] * 2
    with pytest.raises(ValueError, match="at least d"):
        reconstruct([[0, 0], [1, 0], [0, 1]], [0, 1, 2], Options(order=2))


@pytest.mark.parametrize("kw", [{"order": True}, {"levels": 1}, {"bandwidth": 0},
                                   {"sigma_factor": np.nan}, {"representative": "wrong"}])
def test_option_validation(kw):
    with pytest.raises(ValueError):
        Options(**kw)


def test_threshold_monotonicity_and_hull_flags():
    x = np.random.default_rng(11).normal(size=(40, 2))
    y = np.sum(x**2, axis=1)
    a, b = reconstruct(x, y, Options(sigma_factor=0))[0], reconstruct(x, y, Options(sigma_factor=2))[0]
    assert b.threshold > a.threshold
    assert np.sum(b.coverage < b.threshold) >= np.sum(a.coverage < a.threshold)
    proposal = search_guidance([a], x, step_fraction=100)
    assert not proposal["inside_hull"].all()
