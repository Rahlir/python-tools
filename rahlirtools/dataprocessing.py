"""Useful tools for data processing"""

import warnings
import numpy as np


def extract_numbers(text_file, identifier, columns=None):
    """
    Extract numbers from a text file containing ordered columns of numbers
    """
    with open(text_file) as fnm:
        for line in fnm:
            if identifier in line:
                labels = line.split()
                break
        else:
            raise ValueError("{} not found \
                    in the file {}".format(identifier, text_file))

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            data = np.genfromtxt(fnm, usecols=columns, invalid_raise=False)

    # ~ is a shorthand for numpy.logical_not
    data = data[~np.isnan(data).any(axis=1)].T

    result = {label: data[i].copy() for i, label in enumerate(labels)}
    return result
