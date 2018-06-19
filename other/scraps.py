import matplotlib.pyplot as plt
import numpy as np


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
