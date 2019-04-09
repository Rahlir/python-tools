"""Module for thermo analysis"""

import copy

import numpy as np
import matplotlib.pyplot as plt


def plot_thermo(data_all, label_t, label_thermos, label_sims=None,
                xlim=None, units={}):
    if label_sims is None:
        label_sims = list(data_all.keys())

    label_thermos = label_thermos[::-1]  # populating rows from the bottom
    indicies = {}
    if xlim is not None:
        xmin = xlim[0]
        xmax = xlim[1]
        for label_sim in label_sims:
            time_data = data_all[label_sim][label_t]
            indicies[label_sim] = np.where((time_data >= xmin)
                                           & (time_data <= xmax))
    else:
        for label_sim in label_sims:
            time_data = data_all[label_sim][label_t]
            indicies[label_sim] = np.arange(time_data.shape[0])

    n_plt = len(label_thermos)
    rows = int(n_plt/2) + n_plt % 2

    fig_height = int(4.5*rows)
    fig, axes = plt.subplots(rows, 2, figsize=(13, fig_height),
                             sharex=True, squeeze=False)
    # If odd number of plots, first row should have only one plot
    first_empty = (n_plt % 2) > 0
    for row in range(rows):
        second_empty = (row == rows-1) and first_empty

        therm_one = label_thermos[2*row]
        if not second_empty:
            therm_two = label_thermos[2*row+1]

        row_ax = rows - row - 1

        for label_sim in label_sims:
            data_sim = data_all[label_sim]
            indicies_s = indicies[label_sim]

            if not second_empty:
                axes[row_ax, 0].plot(data_sim[label_t][indicies_s],
                                     data_sim[therm_two][indicies_s],
                                     label=label_sim)
                axes[row_ax, 1].plot(data_sim[label_t][indicies_s],
                                     data_sim[therm_one][indicies_s],
                                     label=label_sim)
            else:
                axes[row_ax, 0].plot(data_sim[label_t][indicies_s],
                                     data_sim[therm_one][indicies_s],
                                     label=label_sim + ', ' + therm_one)

        axes[row_ax, 0].legend()

        if not second_empty:
            axes[row_ax, 1].legend()
            axes[row_ax, 1].set_ylabel(
                '{:s} [{:s}]'.format(therm_one, units.get(therm_one, 'def')))
            axes[row_ax, 0].set_ylabel(
                '{:s} [{:s}]'.format(therm_two, units.get(therm_two, 'def')))
            if row_ax == rows - 1:
                axes[row_ax, 0].set_xlabel(
                    'Time [{:s}]'.format(units.get(label_t, '')))
                axes[row_ax, 1].set_xlabel(
                    'Time [{:s}]'.format(units.get(label_t, '')))
        else:
            axes[row_ax, 1].remove()
            axes[row_ax, 0].set_ylabel(
                '{:s} [{:s}]'.format(therm_one, units.get(therm_one, 'def')))

    plt.tight_layout()
    return axes, fig


def normalize(data, size, extra_kw=[]):
    """
    Normalize thermo data based which is dependent on system
    size - for instance total/potential/kinetic energies

    :param dict data: Dictionary containing `numpy.array`s of thermo data
    :param int size: Size of the system in number of atoms
    :param list extra_kw: Extra keywords that define thermo labels that
    should be normalized
    :return: Dictionary of normalized thermo data
    """
    normalized = copy.deepcopy(data)
    kws = ['Eng'] + extra_kw
    for thermo in normalized:
        if any(kw in thermo for kw in kws):
            normalized[thermo] /= size

    return normalized
