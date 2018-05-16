"""Useful tools"""

import warnings
import numpy as np
import matplotlib.pyplot as plt
# from cycler import cycler


def extract_numbers(text_file, identifier, columns=None):
    """Extract numbers from a text file"""

    with open(text_file) as fnm:
        for line in fnm:
            if identifier in line:
                labels = line.split()
                break
        else:
            raise ValueError("{} not found \
                    in the file {}".format(identifier, text_file))

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            data = np.genfromtxt(fnm, usecols=columns, invalid_raise=False)

    # ~ is a shorthand for numpy.logical_not
    data = data[~np.isnan(data).any(axis=1)].T

    result = {label: data[i].copy() for i, label in enumerate(labels)}
    return result


def pretty_plot(x, y, title):
    labels = False
    plt.style.use('seaborn')
#     plt.style.with()
    plt.figure()
#     plt.rc('lines', linewidth=1.5)
#     plt.rc('axes', prop_cycler=cycler('color',
#           ['k', 'b', 'r', 'g', 'm', 'c', 'y']))

    if isinstance(y, dict):
        if len(y) > 1:
            if len(x.shape) == 1:
                x = np.tile(x, (len(y), 1))
        labels = True
        __plot_2d(x, y, labels)

    elif len(y.shape) > 1:
        if len(x.shape) == 1:
            x = np.tile(x, (y.shape[1], 1))
        __plot_2d(x, y)
    else:
        __plot_2d(x, y)

    plt.title(title, fontweight='bold', fontsize=14)
    if labels:
        plt.legend()


def __plot_2d(x, y, labels=False):
    if len(x.shape) == 1:
        x = np.array([x])

    if labels:
        for x_axis, (desc, func) in zip(x, y.items()):
            plt.plot(x_axis, func, label=desc)
    else:
        for x_axis, func in zip(x, y):
            plt.plot(x_axis, func)
