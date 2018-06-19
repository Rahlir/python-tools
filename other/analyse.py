"""Tools for analysing diffusion of a simulation"""

import re
import itertools
import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler

def extract_d(path, temps):
    """Extract diffusion coefficient per temperature"""
    print(temps)
    y = np.array([])
    x = np.array([])
    for temp in temps:
        file_name = '{}/arkr-simulation-{:d}/analysis/msd.log'.format(path, temp)
        print(temp, file_name)
        #temp = int(re.findall('\d+', file_name))
        x = np.append(x, temp)
        with open(file_name) as f:
            msd = float(re.findall('\d+\.\d+|\d+', f.readlines()[11])[0])
            y = np.append(y, msd)

    return x, y

def d_plot(x_vals, lines):
    """Plot diffusion coefficient vs temperature"""
    plt.figure()
    plt.rc('lines', linewidth=1.5)
    def_cycler = cycler('color', ['k', 'r', '0.2', 'b', '0.3', 'g']) \
                + cycler('marker', ['', 'o', '', 'o', '', 'o']) \
                + cycler('linestyle', ['-', '', '-', '', '-', ''])
    plt.rc('axes', prop_cycle=def_cycler)
    for ind, (desc, func) in enumerate(lines.items()):
        plt.plot(x_vals[ind], func, label=desc)
        plt.plot(x_vals[ind], func)
    plt.xlabel('Temperature (K)')
    plt.ylabel('Diffusion Coefficient 1e-5 cm^2/s')
    plt.title('Diffusion Coef vs Temperature')
    plt.grid()
    plt.legend()

def extract_msd(path, temp):
    """Extract msd per time for a given temperature"""
    y = np.array([])
    x = np.array([])
    file_name = '{}/arkr-simulation-{:d}/analysis/msd.xvg'.format(path, temp)
    with open(file_name) as f:
        for line in itertools.islice(f, 21, None):
            time = float(re.findall('\d+\.\d+|\d+', line)[0])
            msd = float(re.findall('\d+\.\d+|\d+', line)[1])
            x = np.append(x, time)
            y = np.append(y, msd)
    return x, y

def msd_plot(x, lines):
    """Plot msd vs time for a given temperature"""
    plt.figure()
    plt.rc('lines', linewidth=1.5)
    plt.plot(x, lines, 'k')
    plt.xlabel('Time (ps)')
    plt.ylabel(r'Mean Square Displacement $nm^2$')
    plt.title('MSD vs Time')
    plt.grid()
