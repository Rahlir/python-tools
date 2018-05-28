import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import mdtraj as md


def msd(trajectory, top, chunks=100, atoms='all'):
    """
    Returns histogram in time of positions in z-coordinate from given trajectory
    TODO: Is there need for centers?
    """
    traj_top = md.load(top)
    topology = traj_top.topology
    traj = md.iterload(trajectory, top=topology, chunk=chunks)

    if atoms != 'all':
        atoms = 'name ' + atoms

    indicies = topology.select(atoms)

    if indicies.size == 0:
        raise ValueError('No atoms with {:s}'.format(atoms))

    init = False

    fmt_progress = '\rframe = {:d} | {:.3f} ms / frame'
    i_frame = 0
    time_0 = time.time()
    msds = []
    for chunk in traj:
        if not init:
            ref = chunk.xyz[0, :, :]

        msd_ind = (chunk.xyz - ref)**2
        msd = np.mean(msd_ind, axis=1).sum(axis=1)
        msds.append(msd)


        time_1 = time.time()
        print(fmt_progress.format(i_frame, 1000 * (time_1 - time_0) / len(chunk)),
              flush=True, end='')
        time_0 = time_1
        i_frame += chunks

    print()

    result = np.array(msds)

    return result
