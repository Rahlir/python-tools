"""Useful tools"""

import re
import itertools
import numpy as np

def extract_numbers(text_file, start=0, end=None, pattern=r'\b\d+\.?\d*\b'):
    """Extract numbers from a text file"""

    with open(text_file) as f:
        for line in itertools.islice(f, start, end):
            numbers = [float(n) for n in re.findall(pattern, line)]

    return 0
