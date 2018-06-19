"""
Module to draw histogram for a given trajectory
"""

import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import mdtraj as md


def density_hist(trajectory, top, chunks=100, atoms='all'):
    """
    Returns histogram in time of positions in z-coordinate from given
    trajectory TODO: Is there need for centers?
    """
    traj_top = md.load(top)
    topology = traj_top.topology
    traj = md.iterload(trajectory, top=topology, chunk=chunks)

    # Automate edges. Do I need centers?
    edges = np.array([i*0.1 for i in range(0, 150)])
    centers = 0.5 * (edges[1:] + edges[:-1])

    if atoms != 'all':
        atoms = 'name ' + atoms

    indicies = topology.select(atoms)

    if indicies.size == 0:
        raise ValueError('No atoms with {:s}'.format(atoms))

    fmt_progress = '\rframe = {:d} | {:.3f} ms / frame'
    i_frame = 0
    time_0 = time.time()
    hists = []
    for chunk in traj:
        hist, edges = np.histogram(chunk.xyz[:, indicies, 2], bins=edges)
        hists.append(hist.astype(float) / len(chunk))

        time_1 = time.time()
        print(fmt_progress.format(i_frame, 1000 * (time_1 - time_0) / len(chunk)),
              flush=True, end='')
        time_0 = time_1
        i_frame += chunks

    print()

    result = np.array(hists)

    return centers, result


def plot_density(histogram, time_u='Picoseconds', dist_u='Angstrom',
                 d_time=10, d_dist=0.1):
    """
    Plots density histogram for given 2d array. Array should be of form
    'histogram[frame, z_pos]'
    """
    colors = cm.magma_r
    colors.set_under('white')

    plt.figure()
    plt.imshow(histogram, extent=[0, histogram.shape[1]*d_dist, 0,
               histogram.shape[0]*d_time], cmap=colors, aspect='auto',
               origin='lower', vmin=1)
    plt.colorbar()
    plt.xlabel('Z-position ({:s})'.format(dist_u))
    plt.ylabel('Time ({:s})'.format(time_u))


def plot_densities(histograms, titles=[], time_u='Picoseconds',
                   dist_u='Angstrom', d_time=10, d_dist=0.1):
    """
    Plots multiple density histograms for given list of 2d arrays
    """
    fig, axes = plt.subplots(len(histograms), 1, figsize=(8, 6))
    colors = cm.magma_r
    colors.set_under('white')
    max_v = max([histogram.max() for histogram in histograms])
    max_plt = len(histograms)

    for i, ax in enumerate(axes.flat):
        histogram = histograms[i]
        image = ax.imshow(histogram.T,
                          extent=[0, histogram.shape[0]*d_time, 0, histogram.shape[1]*d_dist],
                          cmap=colors, aspect='auto', origin='lower', vmin=1e-15, vmax=max_v)

        if len(titles) > i:
            ax.set_title(titles[i])

        if i+1 != max_plt:
            ax.set_xticklabels([])
        else:
            ax.set_xlabel('Time ({:s})'.format(time_u))

        ax.set_ylabel('Z-position ({:s})'.format(dist_u))

    plt.tight_layout()

    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    fig.colorbar(image, cax=cbar_ax)
