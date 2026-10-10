"""Vendored dimensionless magnetic model; also copied into the companion paper."""

import numpy as np


def coenergy(i, saturation=1.0):
    x, y = np.asarray(i).T
    return (
        x
        + 0.3 * x * x
        + 0.5 * y * y
        - saturation * (0.01 * x**4 + 0.02 * y**4)
        - 0.03 * x * x * y * y
        + 0.02 * x * y * y
    )


def flux(i, saturation=1.0):
    x, y = np.asarray(i).T
    return np.stack(
        [
            1 + 0.6 * x - 0.04 * saturation * x**3 - 0.06 * x * y * y + 0.02 * y * y,
            y - 0.08 * saturation * y**3 - 0.06 * x * x * y + 0.04 * x * y,
        ],
        axis=-1,
    )


def hessian(i, saturation=1.0):
    x, y = np.asarray(i).T
    dd = 0.6 - 0.12 * saturation * x * x - 0.06 * y * y
    qq = 1 - 0.24 * saturation * y * y - 0.06 * x * x + 0.04 * x
    dq = -0.12 * x * y + 0.04 * y
    return np.stack([np.stack([dd, dq], axis=-1), np.stack([dq, qq], axis=-1)], axis=-2)
