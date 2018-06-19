import time as tm
import numpy as np


def stress_acf(tensors, dt, n_origs, upper=None):
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
