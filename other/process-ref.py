#!/usr/bin/env python

from __future__ import print_function

import argparse
import sys
import time

import numpy as np
import mdtraj as mdt


#
# command-line arguments
#

parser = argparse.ArgumentParser()

parser.add_argument('fn_trj', type=str,
                    help='Trajectory file name.')

parser.add_argument('-t', '--top', dest='fn_top', type=str, required=True,
                    help='Topology file name.')

parser.add_argument('-A', '--A', type=str, dest='select_A', default='all',
                    help='Selection - group A.')

parser.add_argument('-B', '--B', type=str, dest='select_B', default='all',
                    help='Selection - group B.')

parser.add_argument('-c', '--cutoff', type=float, default=0.2,
                    help='Cutoff length in nm for nearest neighbor search.')

parser.add_argument('-n', '--nearest', type=int, default=4,
                    help='Number of nearest neighbors to look for.')

parser.add_argument('--chunk', type=int, default=100,
                    help='Size of trajectory chunk to load at once.')

parser.add_argument('-v', '--verbose', action='count', default=0,
                    help='Print more information. Repeat twice for per-frame details.')

# run the option parser and get results
args = parser.parse_args()
verbose = args.verbose

print(args)
print()

# load the trajectory and topology
frame_top = mdt.load(args.fn_top)
top = frame_top.topology
trj = mdt.iterload(args.fn_trj, top=top, chunk=args.chunk)

# prepare indices and pairs
idx_A = top.select(args.select_A)
n_A = len(idx_A)
idx_B = top.select(args.select_B)
n_B = len(idx_B)
pairs = []
idx_overlap = []
for iB in idx_B:
    for iA in idx_A:
        pairs.append((iB, iA))
        if iA == iB:
            idx_overlap.append(iA)
pairs = np.array(pairs, dtype=int)
idx_overlap = np.array(idx_overlap)

# print information on topology and selected groups
if verbose > 0:
    print(top)
    print('bonds: ', list(top.bonds))
    print()
    print('group A: "{:s}", {:d} atoms'.format(args.select_A, n_A))
    print(idx_A)
    print()
    print('group B: "{:s}", {:d} atoms'.format(args.select_B, n_B))
    print(idx_B)
    print()
    print('overlap: "({:s}) and ({:s})", {:d} atoms'.format(args.select_A, args.select_B, len(idx_overlap)))
    if len(idx_overlap) > 0:
        print(idx_overlap)
    print()


fmt_progress = '\rframe = {:d} | {:.3f} ms / frame'
if verbose > 1:
    end = '\n\n'
else:
    end = ''

# iterate over trajectory
t0 = time.time()
i_frame = 0
for chunk in trj:

    # set the box if we don't have one
    if chunk.unitcell_lengths is None:
        chunk.unitcell_angles = frame_top.unitcell_angles.repeat(len(chunk), axis=0)
        chunk.unitcell_lengths = frame_top.unitcell_lengths.repeat(len(chunk), axis=0)

    # calcuate distances between the two groups, shape nicely
    distances = mdt.compute_distances(chunk, pairs, opt=True).reshape((-1, n_B, n_A))
    # alternative: mdt.compute_displacements to get relative vectors
    if verbose > 1:
        print('distances.shape = {:s}'.format(distances.shape))

    # option - one nearest
    # Find the index of the nearest neighbor in group A for each atom in group B.
    idx_nearest = np.argmin(distances, axis=2)
    if verbose > 1:
        print('one nearest:')
        print('idx_nearest.shape = {:s}'.format(idx_nearest.shape))

    # option - n nearest
    # Find the indices of the n nearest neighbors in group A for each atom in group B.
    idx_nearest = np.argpartition(distances, args.nearest, axis=2)[:,:,:args.nearest]
    if verbose > 1:
        print('n nearest:')
        print('idx_nearest.shape = {:s}'.format(idx_nearest.shape))

    # option - all within cutoff
    # Find the indices of all the neighbors in group A within `cutoff` of each atom in group B.
    # This uses list comprehensions, but the equivalent explicit loops
    # commented out below do not seem to be much slower.
    # The resulting structure is: idx_nearest[i_f][iB][i_neighbor]
    # It cannot be an array, because the number of neighbors varies.
    idx_nearest = [[np.where(distances[i_f,iB,:] < args.cutoff)[0]
                    for iB in range(n_B)]
                   for i_f in range(len(chunk))]
    #idx_nearest = []
    #for i_f in range(len(chunk)):
    #    tmp = []
    #    for iB in range(n_B):
    #        tmp.append(np.where(distances[i_f,iB,:] < args.cutoff))
    #    idx_nearest.append(tmp)
    if verbose > 1:
        print('all within cutoff:')
        print('len(idx_nearest) = {:d}'.format(len(idx_nearest)))
        print(idx_nearest[0][0])
        for i in idx_nearest[0][0]:
            iA = idx_A[i]
            print(distances[0,0,iA])

    # Careful, `idx_nearest` are "local" indices of group B which need to be
    # resolved to global indices using idx_B, if needed.

    # option - find hydrogen bonds
    # This does not use the provided groups, but rather takes the whole trajectory.
    # For a subset, the trajectory itself would have to be filtered to only some atoms.
    # Needs bonds and specific hard-coded atom and residue names in the
    # topology, but the function is easy to copy and modify.
    hbonds = mdt.baker_hubbard(chunk, freq=0.0, exclude_water=False, periodic=True)
    if verbose > 1:
        print('hydrogen bonds:')
        print('hbonds.shape =', hbonds.shape)


    # TODO: do custom processing here


    # print progress and timing
    t1 = time.time()
    print(fmt_progress.format(i_frame, 1000 * (t1 - t0) / len(chunk)), end=end)
    sys.stdout.flush()
    t0 = t1
    i_frame += args.chunk

if verbose < 1:
    print()
