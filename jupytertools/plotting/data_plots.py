"""Useful functions for generic plots of data"""

import matplotlib.pyplot as plt
from .styling import save_to_disk


__all__ = ['plot_all']


def plot_all(dictionary, keys_sorted=True, keys=None, xlim=None, ylim=None, x_label='', y_label='',
             title='', filename=None, save=False, **kwargs):
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

    for name in sorted_name_list:
        x, y = dictionary[name]
        plt.plot(x, y, label=name)

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
