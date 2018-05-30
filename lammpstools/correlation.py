import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import mdtraj as md


def msd(trajectory, top, chunks=100, atoms='all'):
    """
    Calculate MSD for given trajectory
    """
    print("Loading trajectories from {:s}".format(trajectory))
    traj = md.load(trajectory, top=top)
    assert isinstance(traj, md.Trajectory)
    print("Trajectory loaded")

    if atoms != 'all':
        atoms = 'name ' + atoms

    indicies = traj.topology.select(atoms)

    if indicies.size == 0:
        raise ValueError('No atoms with {:s}'.format(atoms))

    n_contribs = np.zeros((traj.n_frames,), dtype=np.float64)
    correlation = np.zeros((traj.n_frames,), dtype=np.float64)
    origins = np.arange(0, traj.n_frames, 100)

    for origin in origins:
        ref = traj.xyz[origin, indicies, :]
        msd_contr = (traj.xyz[origin:, indicies, :] - ref)**2
        msd_contr_tot = np.mean(msd_contr, axis=1).sum(axis=1)
        n_contribs[:msd_contr_tot.shape[0]] += 1
        msd_contr_tot.resize((correlation.shape))
        correlation += msd_contr_tot

    result = correlation/n_contribs

    return result
