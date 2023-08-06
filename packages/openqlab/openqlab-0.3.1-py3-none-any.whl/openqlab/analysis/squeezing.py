"""Simple squeezing calculations."""

from typing import Union

import numpy as np

from openqlab.conversion import db

_DATA_TYPES = Union[float, list, np.array]


def losses(sqz: _DATA_TYPES, anti_sqz: _DATA_TYPES):
    """Calculate losses from known squeezing and anti-squeezing levels.

    Parameters
    ----------
    sqz : float, :obj:`numpy.array`
        The squeezing level (negative value, because it is below vacuum).
    anti_sqz : float, :obj:`numpy.array`
        The anti-squeezing level (positive value, because it is above vacuum).
    """
    sqz = _ensure_np_array(sqz)
    anti_sqz = _ensure_np_array(anti_sqz)

    L = (1 - db.to_lin(sqz) * db.to_lin(anti_sqz)) / (
        2 - db.to_lin(sqz) - db.to_lin(anti_sqz)
    )
    return L


def initial(sqz: _DATA_TYPES, anti_sqz: _DATA_TYPES):
    """Calculate the initial squeezing level from known squeezing and anti-squeezing levels.

    Parameters
    ----------
    sqz : float, :obj:`numpy.array`
        The squeezing level (negative value, because it is below vacuum).
    anti_sqz : float, :obj:`numpy.array`
        The anti-squeezing level (positive value, because it is above vacuum).
    """
    sqz = _ensure_np_array(sqz)
    anti_sqz = _ensure_np_array(anti_sqz)

    L = losses(sqz, anti_sqz)
    initial_sqz = 10 * np.log10((db.to_lin(anti_sqz) - L) / (1 - L))
    return initial_sqz


def max(loss: _DATA_TYPES):
    """Calculate the maximum possible squeezing level with given loss.

    Parameters
    ----------
    loss : float, :obj:`numpy.array`
        Level of losses (number, relative to 1).
    """
    loss = _ensure_np_array(loss)

    return db.from_lin(db.to_lin(-100) * (1 - loss) + loss)


def _ensure_np_array(value):
    if isinstance(value, list):
        return np.asarray(value)
    return value
