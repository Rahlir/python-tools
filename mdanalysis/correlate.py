"""Utilities for calculation of relatively fast direct correlations"""
import numpy as np
from numba import jit, vectorize, float32, float64


__all__ = ["prepare_numba_correlation", "prepare_legendre"]


def prepare_numba_correlation(vectorized_function):
    @jit(nopython=True)
    def correlate(data, dt, normalize=False, upper_acf_time=None):
        N = data.shape[0]

        if upper_acf_time is None:
            upper_index = N
        else:
            upper_index = int(upper_acf_time/dt+1)

        corr = np.zeros(upper_index)

        for k in range(N):
            upper = min(k+upper_index, N)
            populate_up_to = min(upper_index, N-k)
            corr[:populate_up_to] += vectorized_function(np.dot(data[k, :], data[k:upper, :].T))

        corr /= np.arange(1, data.shape[0]+1)[::-1][:upper_index]
        if normalize:
            corr /= corr[0]
        return corr

    return correlate


def prepare_legendre(order, numba=True):
    if order == 1:
        def P(x):
            return x
    elif order == 2:
        def P(x):
            return 0.5 * (3.0*x**2 - 1.0)
    else:
        raise NotImplementedError("Order {:d} of Legendre polynomial has not been implemented".format(order))

    if numba:
        vectorizing_factory = vectorize([float32(float32), float64(float64)], nopython=True)
        return vectorizing_factory(P)
    else:
        return P
