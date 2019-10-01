"""Tools for timeseries analysis"""

import numpy as np
from scipy import integrate
from copy import deepcopy
from collections.abc import MutableMapping

from jupytertools import retrieve_from_shelve


__all__ = ['get_time_axis', 'get_time_axis_like', 'integrate_series', 'load_cf',
           'CorrelationFunction', 'CorrelationFunctions']


class CorrelationFunctions(MutableMapping):
    def __init__(self, data=()):
        self.cfs = {}
        self.update(data)

    def __getitem__(self, key):
        return self.cfs[key]

    def __delitem__(self, key):
        del self.cfs[key]

    def __setitem__(self, key, cf):
        if key != cf.label:
            raise ValueError(f"Passed key {key:s} is not the same as the label of the cf object {cf.label:s}")
        self.cfs[key] = cf

    def __iter__(self):
        return iter(self.cfs)

    def __len__(self):
        return len(self.cfs)

    def __repr__(self):
        repr = f"{type(self).__name__}("
        for cf_obj in self.cfs.values():
            repr += f"\n{cf_obj.to_string_short()};"

        repr += ")"
        return repr

    def __mul__(self, other):
        if type(other) not in [int, float]:
            raise TypeError(f"unsupported operand type(s) for *: {type(self).__name__} and {type(other).__name__}")
        new_cfs = deepcopy(self)
        for label in new_cfs:
            new_cfs[label] *= other
        return new_cfs

    def __truediv__(self, other):
        if type(other) not in [int, float]:
            raise TypeError(f"unsupported operand type(s) for *: {type(self).__name__} and {type(other).__name__}")
        new_cfs = deepcopy(self)
        for label in new_cfs:
            new_cfs[label] /= other
        return new_cfs

    def add(self, cf):
        self[cf.label] = cf

    def dt(self, dt):
        for cf_obj in self.cfs.values():
            cf_obj.dt = dt


class CorrelationFunction:
    def __init__(self, cf_value, label, dt=1):
        self.label = label
        self.dt = dt

        if len(cf_value.shape) == 1:
            cf_value = cf_value[None, ...]
        self.cf_var = cf_value

    def __repr__(self):
        prefix = f"{type(self).__name__}('{self.label}': "
        suffix = f", dt={self.dt})"
        cf_repr = np.array2string(self.cf_var, edgeitems=2, prefix=prefix, suffix=suffix)
        return f"{prefix}{cf_repr}{suffix}"

    def __mul__(self, other):
        if type(other) not in [int, float]:
            raise TypeError(f"unsupported operand type(s) for *: {type(self).__name__} and {type(other).__name__}")

        new_cf = deepcopy(self)
        if hasattr(self, 'average_cf_var'):
            del new_cf.average_cf_var

        new_cf.cf_var *= other
        return new_cf

    def __truediv__(self, other):
        if type(other) not in [int, float]:
            raise TypeError(f"unsupported operand type(s) for *: {type(self).__name__} and {type(other).__name__}")

        new_cf = deepcopy(self)
        if hasattr(self, 'average_cf_var'):
            del new_cf.average_cf_var

        new_cf.cf_var /= other
        return new_cf

    def to_string_short(self):
        prefix = f"'{self.label}': "
        suffix = f", dt={self.dt}"
        cf_repr = np.array2string(self.cf_var, edgeitems=2, prefix=prefix, suffix=suffix)
        return f"{prefix}{cf_repr}{suffix}"

    @property
    def average_cf(self):
        if hasattr(self, 'average_cf_var'):
            return self.average_cf_var

        self.average_cf_var = self.cf_var.mean(axis=0)
        return self.average_cf_var


def load_cf(filename, key, foldername='shelve', label=None):
    if not label:
        label = f"{filename:s} {key:s}".replace("_", " ")

    cf_value = retrieve_from_shelve(filename, key, foldername)
    return CorrelationFunction(cf_value, label)


def get_time_axis(n_frames, dt):
    """Get time axis for a timeseries with the given number of frames

    Parameters
    ----------
    n_frames : number of frames in the timeseries
    dt : time step separating the values of the timeseries in whatever units desired

    Returns
    -------
    time_axis : numpy array representing the time axis

    """
    time_axis = np.linspace(0, n_frames*dt, n_frames, endpoint=False)
    return time_axis


def get_time_axis_like(y_axis, dt):
    """Get time axis for the given timeseries

    Parameters
    ----------
    y_axis : array-like object representing the timeseries for which the
        time axis is to be returned
    dt : time step separating the values of the timeseries in whatever units desired

    Returns
    -------
    time_axis : numpy array representing the time axis

    """
    return get_time_axis(y_axis.shape[0], dt)


def integrate_series(series, time_axis=None, const=1, dt=1, weights=None):
    """Integrate series using integrate.cumtrapz. Weights for the integral can be used

    Parameters
    ----------
    series : array-like object containing the series to be integrated
    time_axis : time axis for the series
    const : const to multiply the whole integral by
    weights : weights for the integrand, optional

    Returns
    -------
    integral : the integrated series

    """
    if weights is None:
        weights = np.full_like(series, 1)
    elif weights.shape != series.shape:
        error_msg_format = "The weights with shape {} are not compatible with the series of shape {}"
        raise ValueError(error_msg_format.format(weights.shape, series.shape))

    if time_axis is None:
        time_axis = get_time_axis_like(series, dt)

    integrand = const*series
    return integrate.cumtrapz(integrand*weights, time_axis, initial=0)
