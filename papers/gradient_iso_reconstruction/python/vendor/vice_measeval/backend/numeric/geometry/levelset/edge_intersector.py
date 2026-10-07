"""Delaunay-edge level-set intersection for sampled numeric fields.

The module provides a reusable ``EdgeIntersector`` for fields sampled on a
fixed ``PointSet``. The point basis is triangulated once and its unique,
geometrically valid edges are prepared once. Arbitrary ``SampledField``
instances defined on the same ordered basis can then be intersected with one
or more scalar levels without rebuilding the triangulation.

The implementation is independent of motor-specific MeasEval semantics.
"""

from dataclasses import dataclass
from itertools import combinations

import numpy as np
import scipy as sp
from numpy.typing import ArrayLike, NDArray

from vice_measeval.backend.numeric.model.point_set import PointSet
from vice_measeval.backend.numeric.model.sampled_field import SampledField

FloatArray = NDArray[np.float64]
IntArray = NDArray[np.int64]


@dataclass(frozen=True)
class EdgeIntersections:
    """Immutable results of edge-level intersections.

    Each row represents one intersection between one prepared triangulation
    edge and one requested scalar level.

    Parameters
    ----------
    coordinates : FloatArray
        Interpolated coordinates with shape ``(M, D)``, where ``M`` is the
        number of detected intersections and ``D`` is the dimension of the
        underlying ``PointSet``.
    values : FloatArray
        Interpolated field values with shape ``(M, K)``, where ``K`` is the
        number of components in the intersected ``SampledField``.
    levels : FloatArray
        Requested level associated with each intersection, shape ``(M,)``.
    edges : IntArray
        Point indices of the intersected prepared edges, shape ``(M, 2)``.
    lambdas : FloatArray
        Linear interpolation factors along the intersected edges, shape
        ``(M,)``. Values lie in the closed interval ``[0, 1]``.

    Notes
    -----
    The result preserves edge-level intersections rather than unique geometric
    points. Consequently, if a requested level passes exactly through a vertex
    shared by multiple edges, the same geometric coordinate may appear more
    than once with different edge provenance.

    All result arrays are copied and exposed as read-only views after construction.
    Mutating constructor inputs cannot change an existing result.
    """

    coordinates: FloatArray
    values: FloatArray
    levels: FloatArray
    edges: IntArray
    lambdas: FloatArray

    def __post_init__(self) -> None:
        """Own read-only copies of all result arrays."""
        for name in ("coordinates", "values", "levels", "edges", "lambdas"):
            dtype = np.int64 if name == "edges" else np.float64
            owned = np.array(getattr(self, name), dtype=dtype, copy=True)
            owned.flags.writeable = False
            view = owned.view()
            view.flags.writeable = False
            object.__setattr__(self, name, view)


class EdgeIntersector:
    """Intersect sampled field levels with edges of a fixed Delaunay basis.

    An ``EdgeIntersector`` owns the prepared geometric state required for
    repeated level-set intersections on one immutable ``PointSet`` basis.

    Construction performs three steps:

    1. Canonically order the basis for deterministic triangulation.
    2. Build a Delaunay triangulation.
    3. Extract unique undirected edges and remove excessively long edges.

    Once constructed, the prepared edges can be reused for arbitrary
    ``SampledField`` instances defined on the same ordered point basis.

    Parameters
    ----------
    basis : PointSet
        Immutable point coordinates defining the triangulation basis.
    validity_range : float, default=3.0
        Maximum accepted edge length relative to the RMS edge length of the
        triangulation. The comparison is performed using squared lengths, so
        no square root is required.

    Raises
    ------
    TypeError
        If ``basis`` is not a ``PointSet`` or ``validity_range`` is not a real
        numeric value.
    ValueError
        If ``validity_range`` is not finite and strictly positive, the point
        basis cannot be Delaunay triangulated, or the validity filter removes
        all triangulation edges.

    Notes
    -----
    The basis is immutable through ``PointSet``. Therefore triangulation and
    edge preparation are performed only once per ``EdgeIntersector`` instance.

    Triangulation is performed after canonical lexicographic ordering of the
    coordinates. The resulting simplex indices are mapped back to the original
    ``PointSet`` row indices so that prepared edges remain aligned with
    ``SampledField`` rows.
    """

    def __init__(self, basis: PointSet, validity_range: float = 3.0):
        if not isinstance(basis, PointSet):
            raise TypeError(f"basis must be a PointSet; got {type(basis).__name__}.")

        if isinstance(validity_range, (bool, np.bool_)) or not isinstance(
            validity_range, (int, float, np.integer, np.floating)
        ):
            raise TypeError(
                f"validity_range must be a real number; "
                f"got {type(validity_range).__name__}."
            )

        if not np.isfinite(validity_range) or validity_range <= 0:
            raise ValueError(
                f"validity_range must be finite and greater than zero; "
                f"got {validity_range}."
            )

        self._basis = basis
        self._validity_range = float(validity_range)

        self._simplices = self._triangulate()
        self._edges = self._prepare_edges()

    def _triangulate(self) -> IntArray:
        """Triangulate the fixed point basis into deterministic simplices."""
        coordinates = self._basis.coordinates

        sort_keys = tuple(
            coordinates[:, dimension]
            for dimension in range(coordinates.shape[1] - 1, -1, -1)
        )
        order = np.lexsort(sort_keys)

        try:
            triangulation = sp.spatial.Delaunay(coordinates[order])
        except sp.spatial.QhullError as exc:
            raise ValueError(
                "EdgeIntersector requires a non-degenerate point basis that can be "
                "Delaunay triangulated."
            ) from exc

        except ValueError as exc:
            raise ValueError(
                "EdgeIntersector requires a non-degenerate point basis that can be "
                "Delaunay triangulated (at least two spatial dimensions)."
            ) from exc

        return np.asarray(order[triangulation.simplices], dtype=np.int64)

    def _prepare_edges(self) -> IntArray:
        """Extract unique edges and remove edges exceeding the validity range."""
        vertex_pairs = np.array(
            list(combinations(range(self._simplices.shape[1]), 2)),
            dtype=np.int64,
        )

        # Extract every edge from every simplex.
        edges = self._simplices[:, vertex_pairs].reshape(-1, 2)

        # Treat edges as undirected and remove duplicates shared by simplices.
        edges = np.sort(edges, axis=1)
        edges = np.unique(edges, axis=0)

        # Compute squared edge lengths in the PointSet coordinate space.
        edge_vectors = (
            self._basis.coordinates[edges[:, 0]] - self._basis.coordinates[edges[:, 1]]
        )
        # A common scale cancels from the RMS comparison and keeps squares
        # representable for very small or large edge lengths.
        length_scale = np.max(np.abs(edge_vectors))
        edge_lengths_squared = np.sum((edge_vectors / length_scale) ** 2, axis=1)

        # Compare squared lengths directly:
        #
        #     l_e^2 < validity_range^2 * mean(l^2)
        #
        # which is equivalent to limiting the edge length relative to the
        # RMS edge length without evaluating square roots.
        with np.errstate(over="ignore", under="ignore"):
            # Original point indices change edge order under permutations.
            # Sort lengths before reduction to keep a threshold tie deterministic.
            mean_length_squared = np.mean(np.sort(edge_lengths_squared))
            threshold = (
                np.square(np.float64(self._validity_range)) * mean_length_squared
            )
        valid_mask = edge_lengths_squared < threshold
        edges = edges[valid_mask, :]

        if edges.shape[0] == 0:
            raise ValueError(
                "EdgeIntersector preparation removed all triangulation edges; "
                f"validity_range={self._validity_range} is too restrictive for this basis."
            )

        return edges

    def intersect(
        self,
        field: SampledField,
        search_component: int,
        levels: ArrayLike,
    ) -> EdgeIntersections:
        """Intersect scalar field levels with the prepared triangulation edges.

        The selected field component is linearly interpolated along every
        prepared edge. For each requested level, an intersection is returned
        whenever the corresponding interpolation factor lies in ``[0, 1]``.

        The same interpolation factor is then applied to the basis coordinates
        and to all components of the ``SampledField``.

        Parameters
        ----------
        field : SampledField
            Field sampled on the same ordered ``PointSet`` basis used to
            construct this ``EdgeIntersector``.
        search_component : int
            Zero-based index of the scalar field component whose levels are
            intersected.
        levels : ArrayLike
            One scalar level or a one-dimensional collection of levels.

        Returns
        -------
        EdgeIntersections
            Coordinates, interpolated field values, requested levels, source
            edges, and interpolation factors for every valid edge-level
            intersection.

        Raises
        ------
        TypeError
            If ``field`` is not a ``SampledField`` or ``search_component`` is
            not an integer.
        ValueError
            If ``field`` is sampled on a different ordered point basis,
            ``levels`` is not scalar or one-dimensional, contains no entries,
            or contains non-finite values.
        IndexError
            If ``search_component`` is outside the available field-component
            range.

        Notes
        -----
        Field values and prepared edges are aligned by their common ordered
        ``PointSet`` basis. Equality of the basis is currently verified by its
        stable fingerprint.

        Edges whose search-component endpoints contain ``NaN`` are ignored.

        Edges with equal search-component values are also ignored because they
        do not define a unique linear intersection factor. If such an edge lies
        exactly on a requested level, its intersection is the complete edge
        rather than one unique point and is therefore intentionally not
        represented by this result type.

        Intersections at shared vertices are preserved per edge. No geometric
        deduplication is performed.

        The interpolated search-component value is not overwritten with the
        requested level. This intentionally preserves the numerical result so
        that tests can verify the interpolation invariant instead of masking
        possible implementation errors.
        """
        if not isinstance(field, SampledField):
            raise TypeError(
                f"field must be a SampledField; got {type(field).__name__}."
            )

        if field.points.fingerprint != self._basis.fingerprint:
            raise ValueError(
                "Field rows must be defined on the same ordered support points "
                "referenced by the prepared EdgeIntersector edges; "
                f"field basis fingerprint={field.points.fingerprint}, "
                f"basis fingerprint={self._basis.fingerprint}."
            )

        if isinstance(search_component, (bool, np.bool_)) or not isinstance(
            search_component, (int, np.integer)
        ):
            raise TypeError(
                f"search_component must be an integer; "
                f"got {type(search_component).__name__}."
            )

        if not (0 <= search_component < field.n_components):
            raise IndexError(
                f"search_component {search_component} is out of range; "
                f"expected 0 <= search_component < {field.n_components}."
            )

        levels = np.asarray(levels, dtype=np.float64)

        if levels.ndim > 1:
            raise ValueError(
                f"levels must be a scalar or one-dimensional array; "
                f"got shape={levels.shape}."
            )

        levels = np.atleast_1d(levels)

        if levels.size == 0:
            raise ValueError("levels must contain at least one level.")

        if not np.isfinite(levels).all():
            raise ValueError("levels must contain only finite values.")

        search_values = field.values[:, search_component]

        # Evaluate the selected field component at both vertices of every edge.
        start_values = search_values[self._edges[:, 0]]
        end_values = search_values[self._edges[:, 1]]

        with np.errstate(over="ignore", invalid="ignore"):
            denominator = end_values - start_values

        # A unique point intersection requires finite endpoint values and a
        # non-constant search component along the edge.
        finite_edges = np.isfinite(start_values) & np.isfinite(end_values)
        non_constant_edges = denominator != 0.0
        usable_edges = finite_edges & non_constant_edges

        # One interpolation factor is calculated for every edge-level pair:
        #
        #     lambda = (level - f_start) / (f_end - f_start)
        #
        # Shape: (E, L), with E prepared edges and L requested levels.
        lambdas = np.full(
            (self._edges.shape[0], levels.size),
            np.nan,
            dtype=np.float64,
        )

        with np.errstate(over="ignore", invalid="ignore"):
            np.divide(
                levels[None, :] - start_values[:, None],
                denominator[:, None],
                out=lambdas,
                where=usable_edges[:, None],
            )

        # Finite endpoints of opposite sign can have an overflowing difference.
        # Rescale only these rows; the interpolation factor is scale invariant.
        overflow_edges = finite_edges & ~np.isfinite(denominator)
        if np.any(overflow_edges):
            scale = np.maximum(
                np.abs(start_values[overflow_edges]), np.abs(end_values[overflow_edges])
            )
            start_scaled = start_values[overflow_edges] / scale
            end_scaled = end_values[overflow_edges] / scale
            lambdas[overflow_edges] = (
                levels[None, :] / scale[:, None] - start_scaled[:, None]
            ) / (end_scaled - start_scaled)[:, None]

        # A level intersects the finite line segment exactly when lambda lies
        # within the closed interval [0, 1].
        valid_mask = (lambdas >= 0.0) & (lambdas <= 1.0)

        edge_indices, level_indices = np.nonzero(valid_mask)

        intersection_lambdas = lambdas[edge_indices, level_indices]
        intersection_edges = self._edges[edge_indices]
        intersection_levels = levels[level_indices]

        # Interpolate the geometric coordinates.
        start_coordinates = self._basis.coordinates[intersection_edges[:, 0]]
        end_coordinates = self._basis.coordinates[intersection_edges[:, 1]]

        weights = intersection_lambdas[:, None]
        coordinates = (1.0 - weights) * start_coordinates + weights * end_coordinates

        # Interpolate every field component using the same geometric factor.
        start_field_values = field.values[intersection_edges[:, 0], :]
        end_field_values = field.values[intersection_edges[:, 1], :]

        values = (1.0 - weights) * start_field_values + weights * end_field_values

        return EdgeIntersections(
            coordinates=coordinates,
            values=values,
            levels=intersection_levels,
            edges=intersection_edges,
            lambdas=intersection_lambdas,
        )


if __name__ == "__main__":
    """Visual smoke test using Himmelblau's function."""
    import matplotlib.pyplot as plt

    from vice_measeval.backend.numeric.benchmark.test_functions import himmelblau

    x = np.linspace(-6, 6, 101)
    x_grid, y_grid = np.meshgrid(x, x)

    coordinates = np.column_stack((x_grid.ravel(), y_grid.ravel()))
    points = PointSet(coordinates)

    field_values = himmelblau(
        x_grid.ravel(),
        y_grid.ravel(),
    )
    field = SampledField(points, field_values)

    intersector = EdgeIntersector(points)

    levels = np.array([25.0, 50.0, 100.0])

    result = intersector.intersect(
        field=field,
        search_component=0,
        levels=levels,
    )

    # Compare the discrete edge intersections with Matplotlib's contour
    # extraction as a visual plausibility check.
    plt.figure()

    plt.contour(
        x_grid,
        y_grid,
        field_values.reshape(x_grid.shape),
        levels=levels,
    )

    for level in levels:
        mask = result.levels == level

        plt.scatter(
            result.coordinates[mask, 0],
            result.coordinates[mask, 1],
            s=10,
            label=f"Edge intersections: {level:g}",
        )

    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis("equal")
    plt.legend()
    plt.show()
