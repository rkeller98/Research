"""Vendored dimensionless magnetic model; also copied into the companion paper."""
import numpy as np


def coenergy(i, saturation=1.):
    x, y = np.asarray(i).T
    return x+.3*x*x+.5*y*y-saturation*(.01*x**4+.02*y**4)-.03*x*x*y*y+.02*x*y*y


def flux(i, saturation=1.):
    x, y = np.asarray(i).T
    return np.stack([1+.6*x-.04*saturation*x**3-.06*x*y*y+.02*y*y,
                     y-.08*saturation*y**3-.06*x*x*y+.04*x*y], axis=-1)


def hessian(i, saturation=1.):
    x, y = np.asarray(i).T
    dd = .6-.12*saturation*x*x-.06*y*y
    qq = 1-.24*saturation*y*y-.06*x*x+.04*x
    dq = -.12*x*y+.04*y
    return np.stack([np.stack([dd, dq], axis=-1), np.stack([dq, qq], axis=-1)], axis=-2)
