"""Common degree-four symmetric potential fit and exact derivatives.
Migrated unchanged from the audited composite solver.
"""

import numpy as np
from magnetic_model import flux, hessian

DEGREE = 4
KNOTS = np.r_[np.full(5, -1.0), [-0.5, 0.0, 0.5], np.full(5, 1.0)]
N = len(KNOTS) - DEGREE - 1


def bsplines(z, degree=DEGREE, derivative=0):
    """Cox-de Boor basis and exact derivative recurrence on the knot domain."""
    z = np.clip(np.atleast_1d(z).astype(float), -1 + 1e-12, 1 - 1e-12)
    if derivative > degree:
        return np.zeros((len(z), len(KNOTS) - degree - 1))
    if degree == 0:
        return ((z[:, None] >= KNOTS[:-1]) & (z[:, None] < KNOTS[1:])).astype(float)
    lower = bsplines(z, degree - 1, max(0, derivative - 1))
    count = len(KNOTS) - degree - 1
    ans = np.zeros((len(z), count))
    for j in range(count):
        left = KNOTS[j + degree] - KNOTS[j]
        right = KNOTS[j + degree + 1] - KNOTS[j + 1]
        if derivative:
            if left:
                ans[:, j] += degree * lower[:, j] / left
            if right:
                ans[:, j] -= degree * lower[:, j + 1] / right
        else:
            if left:
                ans[:, j] += (z - KNOTS[j]) * lower[:, j] / left
            if right:
                ans[:, j] += (KNOTS[j + degree + 1] - z) * lower[:, j + 1] / right
    return ans


def design(points, dx=0, dy=0, parity=None):
    bx = bsplines(points[:, 0], derivative=dx)
    by = bsplines(points[:, 1], derivative=dy)
    if parity is not None:
        reflect = bsplines(-points[:, 1], derivative=dy) * (-1) ** dy
        by = 0.5 * (by + parity * reflect)
        by = by[:, : N // 2]
    return np.einsum("km,kn->kmn", bx, by).reshape(len(points), -1)


def grid(size, limit=0.95):
    return np.array(
        [
            (x, y)
            for x in np.linspace(-limit, limit, size)
            for y in np.linspace(-limit, limit, size)
        ]
    )


REGGRID = grid(11, 0.99)
# Uniform quadrature including cell area; half weights at outer edges.
QW = np.ones(11)
QW[[0, -1]] = 0.5
QW = np.sqrt(np.outer(QW, QW).reshape(-1)) * (1.98 / 10)


def roughness(parity, order):
    parts = []
    for dx in range(order + 1):
        dy = order - dx
        factor = np.sqrt((1, 2, 1)[dx] if order == 2 else (1, 3, 3, 1)[dx])
        parts.append(factor * QW[:, None] * design(REGGRID, dx, dy, parity))
    return np.vstack(parts)


def null_gauge():
    g = design(np.zeros((1, 2)), parity=1)
    return np.linalg.svd(g, full_matrices=True)[2][1:].T


Z = null_gauge()


def solve(points, values, mode, lam, robust=False):
    if mode == "Potential":
        G = np.vstack([design(points, 1, 0, 1), design(points, 0, 1, 1)]) @ Z
        target = np.r_[values[:, 0], values[:, 1]]
        penalty = roughness(1, 3) @ Z
        weights = np.ones(len(target))
        for _ in range(8 if robust else 1):
            c = np.linalg.lstsq(
                np.vstack([G * weights[:, None], np.sqrt(lam) * penalty]),
                np.r_[target * weights, np.zeros(len(penalty))],
                rcond=None,
            )[0]
            if robust:
                e = abs(G @ c - target)
                weights = np.sqrt(np.minimum(1.0, 0.01 / np.maximum(e, 1e-15)))
        return (mode, Z @ c)
    coefficients = []
    for component in range(2):
        parity = None if mode == "Independent" else (1 if component == 0 else -1)
        G = design(points, parity=parity)
        P = roughness(parity, 2)
        c = np.linalg.lstsq(
            np.vstack([G, np.sqrt(lam) * P]),
            np.r_[values[:, component], np.zeros(len(P))],
            rcond=None,
        )[0]
        coefficients.append(c)
    return (mode, coefficients)


def predict(fit, points):
    mode, c = fit
    if mode == "Potential":
        f = np.column_stack([design(points, 1, 0, 1) @ c, design(points, 0, 1, 1) @ c])
        dd, dq, qq = [design(points, *der, 1) @ c for der in ((2, 0), (1, 1), (0, 2))]
        H = np.stack([np.column_stack([dd, dq]), np.column_stack([dq, qq])], axis=1)
        return f, H
    f, derivatives = [], []
    for component in range(2):
        parity = None if mode == "Independent" else (1 if component == 0 else -1)
        f.append(design(points, parity=parity) @ c[component])
        derivatives.append(
            np.column_stack(
                [
                    design(points, 1, 0, parity) @ c[component],
                    design(points, 0, 1, parity) @ c[component],
                ]
            )
        )
    return np.column_stack(f), np.stack(derivatives, axis=1)


def metrics(fit, points, saturation):
    f, H = predict(fit, points)
    fm, _ = predict(fit, points * np.array([1.0, -1.0]))
    parity = np.column_stack([0.5 * (f[:, 0] - fm[:, 0]), 0.5 * (f[:, 1] + fm[:, 1])])
    return dict(
        flux_rmse=float(np.sqrt(np.mean((f - flux(points, saturation)) ** 2))),
        hessian_rmse=float(np.sqrt(np.mean((H - hessian(points, saturation)) ** 2))),
        parity_rmse=float(np.sqrt(np.mean(parity**2))),
        curl_rmse=float(np.sqrt(np.mean((H[:, 1, 0] - H[:, 0, 1]) ** 2))),
        min_symmetric_hessian_eigenvalue=float(
            np.linalg.eigvalsh(0.5 * (H + H.swapaxes(1, 2))).min()
        ),
    )
