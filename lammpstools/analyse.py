import re
import itertools
import numpy as np


# def extract_d():
#     Ts = range(90, 171, 5)
#     print(Ts)
#     y = np.array([])
#     x = np.array([])
#     # for file_name in os.listdir():
#     for T in Ts:
#         file_name = 'arkr-simulation-{:d}/analysis/msd.log'.format(T)
#         print(T, file_name)
#         # temp = int(re.findall('\d+', file_name))
#         x = np.append(x, T)
#         with open(file_name) as f:
#             msd = float(re.findall('\d+\.\d+|\d+', f.readlines()[11])[0])
#             y = np.append(y, msd)
#
#     return x, y


def extract_msd(file_name):
    y = np.array([])
    x = np.array([])
    with open(file_name) as f:
        for line in itertools.islice(f, 21, None):
            time = float(re.findall('\d+\.\d+|\d+', line)[0])
            msd = float(re.findall('\d+\.\d+|\d+', line)[1])
            x = np.append(x, time)
            y = np.append(y, msd)
    return x, y
