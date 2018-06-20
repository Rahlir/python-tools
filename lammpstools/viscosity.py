import time as tm
import numpy as np


def stress_acf_old(tensors, dt, n_origs, upper=None):
    if upper is None:
        upper = tensors.shape[0]*dt

    n_frames = tensors.shape[0]
    n_points = int(upper/dt)
    n_contribs = np.zeros((n_points,), dtype=np.float64)
    correlation = np.zeros((n_points,), dtype=np.float64)

    origins = np.linspace(0, n_frames, n_origs, dtype=int, endpoint=False)

    time_0 = tm.time()
    for origin in origins:
        upper_pt = origin+n_points
        time_1 = tm.time()
        dtime = 1000 * (time_1 - time_0)
        if dtime > 1.0:
            print('\rCalculating stress from origin {:.3f} ps'.format(
                origin*dt), end='', flush=True)
            time_0 = time_1
        avg = np.mean(tensors[origin:upper_pt])
        var = np.var(tensors[origin:upper_pt])

        ref = tensors[origin]
        viscosity_contr = ((tensors[origin:upper_pt]-avg)*(ref-avg))/var

        n_contribs[:viscosity_contr.shape[0]] += 1
        visc_contr_final = np.zeros((correlation.shape))
        visc_contr_final[:viscosity_contr.shape[0]] = viscosity_contr
        correlation += visc_contr_final

    result = correlation/n_contribs
    x_axis = np.linspace(0, n_points*dt-1, n_points)

    return x_axis, result


def stress_acf(tensors, dt, n_origs, upper=None, normalized=True, avg=True):
    """
    Calculate stress autocorrelation function for given 3d array of
    off-diagonal stress tensors

    :param `numpy.Array` tensors: 3d array of off-diagonal
    stress tensor entries
    :param int dt: Timestep between two data points
    :param int n_origs: Number of origins to use for the correlation function
    :param float upper: Upper window for the autocorrelation function. If
    not specified then the acf will be calculated with the delay window equal
    to the timelenght of the trajectort
    :param bool normalized: If the acf should be normalized - normalizing is
    done by dividing by variance of the data
    :param bool avg: If the autocorrelation function
    should be averaged over the three entries
    :return: x axis array and stress autocorrelation array
    :rtype: tuple -> `numpy.Array` and `numpy.Array`
    """
    if upper is None:
        upper = tensors.shape[1]*dt

    n_frames = tensors.shape[1]
    n_points = int(upper/dt)

    n_contribs = np.zeros((3, n_points), dtype=np.float64)
    correlation = np.zeros((3, n_points), dtype=np.float64)

    origins = np.linspace(0, n_frames, n_origs, dtype=int, endpoint=False)
    avg = np.mean(tensors, axis=1, keepdims=True)
    if normalized:
        var = np.var(tensors, axis=1, keepdims=True)
    else:
        var = 1.0

    time_0 = tm.time()
    for origin in origins:
        upper_pt = origin+n_points
        time_1 = tm.time()
        dtime = 1000 * (time_1 - time_0)
        if dtime > 1.0:
            print('\rCalculating stress from origin {:.3f} ps'.format(
                origin*dt), flush=True, end='')
            time_0 = time_1

        ref = tensors[:, origin, np.newaxis]
        viscosity_contr = ((tensors[:, origin:upper_pt]-avg)*(ref-avg))/var

        n_contribs[:, :viscosity_contr.shape[1]] += 1
        correlation[:viscosity_contr.shape[0],
                    :viscosity_contr.shape[1]] += viscosity_contr

    result = correlation/n_contribs
    x_axis = np.linspace(0, n_points*dt-1, n_points)

    if avg:
        return x_axis, np.mean(result, axis=0)

    return x_axis, result
