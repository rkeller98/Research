"""Exact P1 path and Green tests, migrated from the audited composite.
No quadrature error implies nothing about interpolation or measurement error.
"""
import numpy as np
from scipy.spatial import Delaunay
from scipy.interpolate import LinearNDInterpolator

class AffineMesh:
    """Independent triangle gradients and exact integrals of a P1 vector field.

    A path is split at ALL mesh-edge crossings. The midpoint rule is exact
    on each affine segment. This removes quadrature error, not interpolation
    error. Curl is piecewise constant and undefined classically on edges.
    """

    def __init__(self, coordinates, flux):
        self.coordinates = np.asarray(coordinates)
        self.flux = np.asarray(flux)
        self.tri = Delaunay(self.coordinates)
        self.interp = LinearNDInterpolator(self.tri, self.flux)
        vertices = self.coordinates[self.tri.simplices]
        delta = (
            self.flux[self.tri.simplices[:, :2]]
            - self.flux[self.tri.simplices[:, 2]][:, None, :]
        )
        self.gradient = np.einsum("nvc,nvk->nck", delta, self.tri.transform[:, :2, :])
        self.curl = self.gradient[:, 1, 0] - self.gradient[:, 0, 1]
        side1, side2 = vertices[:, 1] - vertices[:, 0], vertices[:, 2] - vertices[:, 0]
        self.area = abs(side1[:, 0] * side2[:, 1] - side1[:, 1] * side2[:, 0]) / 2
        self.vertices = vertices
        edges = np.concatenate(
            [
                self.tri.simplices[:, [0, 1]],
                self.tri.simplices[:, [1, 2]],
                self.tri.simplices[:, [2, 0]],
            ]
        )
        edges = np.unique(np.sort(edges, axis=1), axis=0)
        self.edge_a, self.edge_b = (
            self.coordinates[edges[:, 0]],
            self.coordinates[edges[:, 1]],
        )

    def segment(self, start, end):
        start, end = np.asarray(start, dtype=float), np.asarray(end, dtype=float)
        if (self.tri.find_simplex(np.array([start, end]), tol=1e-10) < 0).any():
            raise ValueError("Segment outside convex hull")
        r, s = end - start, self.edge_b - self.edge_a
        a = self.edge_a - start
        denom = r[0] * s[:, 1] - r[1] * s[:, 0]
        good = abs(denom) > 1e-14
        t = np.full(len(s), np.nan)
        u = t.copy()
        t[good] = (a[good, 0] * s[good, 1] - a[good, 1] * s[good, 0]) / denom[good]
        u[good] = (a[good, 0] * r[1] - a[good, 1] * r[0]) / denom[good]
        valid = good & (t > 0) & (t < 1) & (u >= -1e-12) & (u <= 1 + 1e-12)
        breaks = np.unique(np.r_[0.0, t[valid], 1.0])
        middle = start + ((breaks[:-1] + breaks[1:]) / 2)[:, None] * r
        values = self.interp(middle)
        if not np.isfinite(values).all():
            raise ValueError("Nonfinite interpolated segment")
        return float(np.sum((values @ r) * np.diff(breaks)))

    def paths(self, x, y):
        wa = self.segment((0, 0), (x, 0)) + self.segment((x, 0), (x, y))
        wb = self.segment((0, 0), (0, y)) + self.segment((0, y), (x, y))
        return wa, wb

    def rectangle_curl(self, x, y):
        """Independent Green check by clipping every intersecting triangle."""
        lo, hi = np.minimum([0, 0], [x, y]), np.maximum([0, 0], [x, y])
        candidates = (self.vertices.max(axis=1) >= lo).all(axis=1) & (
            self.vertices.min(axis=1) <= hi
        ).all(axis=1)
        total, covered = 0.0, 0.0
        for index in np.flatnonzero(candidates):
            polygon = list(self.vertices[index])
            for axis, boundary, direction in (
                (0, lo[0], 1),
                (0, hi[0], -1),
                (1, lo[1], 1),
                (1, hi[1], -1),
            ):
                if not polygon:
                    break
                clipped = []
                previous = polygon[-1]
                was_inside = direction * (previous[axis] - boundary) >= 0
                for point in polygon:
                    inside = direction * (point[axis] - boundary) >= 0
                    if inside != was_inside:
                        fraction = (boundary - previous[axis]) / (
                            point[axis] - previous[axis]
                        )
                        clipped.append(previous + fraction * (point - previous))
                    if inside:
                        clipped.append(point)
                    previous, was_inside = point, inside
                polygon = clipped
            if len(polygon) >= 3:
                v = np.asarray(polygon)
                # Shift before the shoelace sum to avoid cancellation.
                v = v - v[0]
                area = (
                    abs(
                        np.sum(
                            v[:, 0] * np.roll(v[:, 1], -1)
                            - v[:, 1] * np.roll(v[:, 0], -1)
                        )
                    )
                    / 2
                )
                total += self.curl[index] * area
                covered += area
        assert np.isclose(covered, abs(x * y), rtol=2e-10, atol=1e-8)
        return np.sign(x * y) * total

    def table(self, omega):
        # Keep the exact mesh/integration checks usable in lightweight NumPy/
        # SciPy research environments; tabular export alone needs pandas.
        import pandas as pd
        center = self.vertices.mean(axis=1)
        lengths = np.stack(
            [
                np.linalg.norm(self.vertices[:, a] - self.vertices[:, b], axis=1)
                for a, b in ((0, 1), (1, 2), (2, 0))
            ],
            axis=1,
        )
        circumradius = np.prod(lengths, axis=1) / (4 * self.area)
        return pd.DataFrame(
            {
                "id_center_A": center[:, 0],
                "iq_center_A": center[:, 1],
                "area_A2": self.area,
                "curl_Wb_per_A": self.curl,
                "delta_R_eq_curl_ohm": omega * self.curl / 2,
                "circumradius_A": circumradius,
                "edge_condition": np.linalg.cond(
                    self.vertices[:, :2] - self.vertices[:, 2, None]
                ),
                "L_dq_H": self.gradient[:, 0, 1],
                "L_qd_H": self.gradient[:, 1, 0],
            }
        )
