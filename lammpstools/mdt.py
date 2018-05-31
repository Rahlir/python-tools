import numpy as np
import mdtraj as md


def load_traj(trajectory, top):
    """
    Calculate MSD for given trajectory
    """
    print("Loading trajectories from {:s}".format(trajectory), flush=True)
    traj = md.load(trajectory, top=top)
    print("Trajectory loaded")
    return traj


def msd(traj, atoms='all', average=False):
    """
    Calculate MSD for given trajectory object (mdtraj.Trajectory)
    """
    assert isinstance(traj, md.Trajectory)
    if atoms != 'all':
        atoms = 'name ' + atoms

    indicies = traj.topology.select(atoms)

    dt = traj.timestep

    if indicies.size == 0:
        raise ValueError('No atoms with {:s}'.format(atoms))

    n_contribs = np.zeros((traj.n_frames-1,), dtype=np.float64)
    correlation = np.zeros((traj.n_frames-1, traj.n_atoms), dtype=np.float64)
    origins = np.linspace(0, traj.n_frames-1, 51, dtype=int, endpoint=True)

    for origin in origins:
        ref = traj.xyz[origin, indicies, :]
        msd_contr = ((traj.xyz[origin+1:, indicies, :] - ref)**2).sum(axis=2)

        n_contribs[:msd_contr.shape[0]] += 1
        msd_contr_final = np.zeros((correlation.shape))
        msd_contr_final[:msd_contr.shape[0], :msd_contr.shape[1]] = msd_contr
        correlation += msd_contr_final

    n_contribs_new = np.tile(n_contribs, (correlation.shape[1], 1)).T
    result = correlation/n_contribs_new

    x_axis = np.linspace(dt, traj.n_frames-1, result.shape[0])

    if average:
        return x_axis, np.mean(result, axis=1)

    return x_axis, result
