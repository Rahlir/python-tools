"""Useful functions for generic plots of data"""

import matplotlib.pyplot as plt
from .styling import save_to_disk
from mdanalysis import get_time_axis_like


__all__ = ['plot_all', 'plot_cfs']


def plot_all(dictionary, keys_sorted=True, keys=None, xlim=None, ylim=None, x_label='', y_label='',
             title='', dt=1, style=None, filename=None, save=False, **kwargs):
    if save:
        if filename is None:
            print("To save, you must specify file name")
            save = False

    if keys is None:
        name_list = dictionary.keys()
    else:
        name_list = keys

    if keys_sorted:
        sorted_name_list = sorted(name_list)
    else:
        sorted_name_list = name_list

    if style is None:
        style = {}

    for name in sorted_name_list:
        try:
            x, y = dictionary[name]
            plt.plot(x, y, label=name, **style)
        except ValueError:
            y = dictionary[name]
            x = get_time_axis_like(y, dt)
            plt.plot(x, y, label=name, **style)

    for func_name, argument in kwargs.items():
        func = getattr(plt, func_name)
        if argument is True:
            func()
        else:
            func(argument)

    plt.legend()
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    plt.tight_layout()

    if save and filename is not None:
        save_to_disk(filename)


def plot_cfs(dictionary, keys_sorted=True, xlim=None, ylim=None, xlabel='', ylabel='', style=None,
             legend=True, title='', filename=None):
    if keys_sorted:
        name_list = sorted(dictionary.keys())
    else:
        name_list = dictionary.keys()

    if not style:
        style = {}

    for name in name_list:
        cff = dictionary[name]
        y = cff.average_cf
        x = get_time_axis_like(y, cff.dt)
        plt.plot(x, y, label=name, **style)

    if legend:
        plt.legend()

    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    plt.tight_layout()

    if filename:
        save_to_disk(filename)
