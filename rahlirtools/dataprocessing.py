"""Useful tools"""

import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler

def extract_numbers(text_file, identifier, columns=None):
    """Extract numbers from a text file"""

    with open(text_file) as fnm:
        for line in fnm:
            if identifier in line:
                labels = line.split()
                print(labels)
                break
        else:
            raise ValueError("{} not found in the file {}".format(identifier, text_file))
        data = np.genfromtxt(fnm, usecols=columns, invalid_raise=False)

    # ~ is a shorthand for numpy.logical_not
    data = data[~np.isnan(data).any(axis=1)]
    return labels, data.T

# def pretty_plot(x, y, title):
#     plt.figure()
#     plt.rc('lines', linewidth=1.5)
#     plt.rc('axes', prop_cycler=cycler('color', ['k', 'b', 'r', 'g', 'm', 'c', 'y']))
# 
#     if isinstance(y, dict) and len(y) > 1:
#         if len(x.shape) == 1:
#             x = np.tile(x, (len(y), 1))
#         __plot_2d(x, y, labels=True)
#     elif len(y.shape) > 1:
#         if x.shape 
# 
# def __plot_2d(x, y, labels=False):
#     if labels:
#         for x_axis, (desc, func) in zip(x, y.items()):
#             plt.plot(x_axes, func, label=desc)
#     else:
#         for x_axis, func in zip(x, y):
#             plt.plot(x_axes, func)
