import numpy as np


def cum_avg(arr):
    """Returns cummulative average of a given `numpy.array`"""
    cum_arr = np.cumsum(arr)
    num_entries = np.arange(1, cum_arr.shape[0]+1)
    return cum_arr / num_entries
