"""Tools for timeseries analysis"""

import numpy as np
from scipy import integrate


__all__ = ['get_time_axis', 'get_time_axis_like', 'integrate_series']


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
