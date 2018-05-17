"""
Module to draw histogram for a given trajectory
"""

import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import mdtraj as md


def density_hist(trajectory, top, chunks=100, atoms='all', cut_first=True):
    """
    Returns histogram in time of positions in z-coordinate from given trajectory
    TODO: Is there need for centers?
    """
    traj_top = md.load(top)
    topology = traj_top.topology
    traj = md.iterload(trajectory, top=topology, chunk=chunks)

    # Automate edges. Do I need centers?
    edges = np.array([i*0.1 for i in range(0, 150)])
    centers = 0.5 * (edges[1:] + edges[:-1])

    result = np.empty((1, len(edges)-1))

    if atoms != 'all':
        atoms = 'name ' + atoms

    indicies = topology.select(atoms)

    if indicies.size == 0:
        raise ValueError('No atoms with {:s}'.format(atoms))

    fmt_progress = '\rframe = {:d} | {:.3f} ms / frame'
    i_frame = 0
    time_0 = time.time()
    for chunk in traj:
        new_z = chunk.xyz[:, indicies, 2]
        hists = np.array([np.histogram(new_z[i], bins=edges)[0] for i in range(0, new_z.shape[0])])
        ave_hist = np.average(hists, axis=0)
        result = np.vstack((result, ave_hist))

        time_1 = time.time()
        print(fmt_progress.format(i_frame, 1000 * (time_1 - time_0) / len(chunk)),
              flush=True, end='')
        time_0 = time_1
        i_frame += chunks

    print()

    if cut_first:
        result = result[1:]

    return centers, result


def plot_density(histogram, time_u='Picoseconds', dist_u='Angstrom', d_time=10, d_dist=0.1):
    """
    Plots density histogram for given 2d array. Array should be of form 'histogram[frame, z_pos]'
    """
    colors = cm.magma_r
    colors.set_under('white')

    plt.figure()
    plt.imshow(histogram, extent=[0, histogram.shape[1]*d_dist, 0, histogram.shape[0]*d_time],
               cmap=colors, aspect='auto', origin='lower', vmin=1)
    plt.colorbar()
    plt.xlabel('Z-position ({:s})'.format(dist_u))
    plt.ylabel('Time ({:s})'.format(time_u))
