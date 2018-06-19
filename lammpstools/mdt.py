import numpy as np
import mdtraj as md


def load_traj(trajectory, top):
    """
    Load trajectory using `mdtraj.load`

    :param str trajectory: Filename of trajectory - for instance .xtc format
    :param str top: Filename of topology - for instance .gro format
    :return: Trajectory object
    :rtype: mdtraj.Trajectory
    """
    print("Loading trajectories from {:s}".format(trajectory), flush=True)
    traj = md.load(trajectory, top=top)
    print("Trajectory loaded", flush=True)
    return traj


def msd(traj, n_origs, atoms='all', average=True):
    """
    Calculate MSD for given trajectory

    :param `mdtraj.Trajectory` traj: Loaded trajectory
    :param int n_origs: Number of origins to use for the correlation function
    :param str atoms: Description of atoms using atom selection language,
    usually element name
    :param bool average: If the msd should be averaged over all atoms
    :return: x axis array and msd array
    :rtype: tuple -> `numpy.Array` and `numpy.Array`
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
    origins = np.linspace(0, traj.n_frames-1, n_origs,
                          dtype=int, endpoint=True)

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


def msd_raw_depreceated(xyz, dt, n_origs, average=True):
    """
    Depreceated. Use `msd_raw` which has parameter for upper limit to spped up
    computation
    """
    n_frames = xyz.shape[0]
    n_atoms = xyz.shape[1]
    n_contribs = np.zeros((n_frames-1,), dtype=np.float64)
    correlation = np.zeros((n_frames-1, n_atoms), dtype=np.float64)
    origins = np.linspace(0, n_frames-1, n_origs, dtype=int, endpoint=True)
    indicies = np.arange(n_atoms)  # For now, we are interested in all atoms

    for origin in origins:
        print('\rCalculating MSD from origin {:.3f} ps'.format(origin*dt),
              end='', flush=True)
        ref = xyz[origin, indicies, :]
        msd_contr = ((xyz[origin+1:, indicies, :] - ref)**2).sum(axis=2)

        n_contribs[:msd_contr.shape[0]] += 1
        msd_contr_final = np.zeros((correlation.shape))
        msd_contr_final[:msd_contr.shape[0], :msd_contr.shape[1]] = msd_contr
        correlation += msd_contr_final

    n_contribs_new = np.tile(n_contribs, (correlation.shape[1], 1)).T
    result = correlation/n_contribs_new
    x_axis = np.linspace(dt, (n_frames-1)*dt, result.shape[0])

    if average:
        return x_axis, np.mean(result, axis=1)

    return x_axis, result


def msd_raw(xyz, dt, n_origs, average=True, upper=None):
    """
    Calculate MSD for given trajectory. Unlike `msd` function,
    this function uses xyz array instead of `mdtraj.Trajectory`. Allowing
    it to be used more flexibly (for instance on center of masses trajectories)

    :param numpy.Array xyz: 3 dimensional array containing positions of objects
    for which msd is to be calculated
    :param int dt: Timestep for the given trajectory
    :param int n_origs: Number of origins to use for the correlation function
    :return: x axis array and msd array
    :rtype: tuple -> `numpy.Array` and `numpy.Array`
    """
    if upper is None:
        upper = xyz.shape[0]*dt

    n_points = int(upper/dt)
    n_frames = xyz.shape[0]
    n_atoms = xyz.shape[1]
    n_contribs = np.zeros((n_points,), dtype=np.float64)
    correlation = np.zeros((n_points, n_atoms), dtype=np.float64)
    origins = np.linspace(0, n_frames, n_origs, dtype=int, endpoint=False)
    indicies = np.arange(n_atoms)  # For now, we are interested in all atoms

    for origin in origins:
        print('\rCalculating MSD from origin {:.3f} ps'.format(origin*dt),
              end='', flush=True)

        upper_pt = origin+n_points

        ref = xyz[origin, indicies, :]
        msd_contr = ((xyz[origin:upper_pt, indicies, :] - ref)**2).sum(axis=2)

        n_contribs[:msd_contr.shape[0]] += 1
        msd_contr_final = np.zeros((correlation.shape))
        msd_contr_final[:msd_contr.shape[0], :msd_contr.shape[1]] = msd_contr
        correlation += msd_contr_final

    n_contribs_new = np.tile(n_contribs, (correlation.shape[1], 1)).T
    result = correlation/n_contribs_new
    x_axis = np.linspace(0, (n_points-1)*dt, n_points)

    if average:
        return x_axis, np.mean(result, axis=1)

    return x_axis, result


def get_coms(traj, mol_elements=['H', 'O'], mol_order=['O', 'H', 'H']):
    masses = {}
    for atom in traj.top.atoms:
        sym = atom.element.symbol
        if any(sym == mol for mol in mol_elements):
            masses[sym] = atom.element.mass
        if len(masses) == len(mol_elements):
            break

    mols = np.arange(traj.n_atoms).reshape(int(traj.n_atoms/3), 3)
    weights = [masses[element] for element in mol_order]

    return np.average(traj.xyz[:, mols], axis=2, weights=weights)
