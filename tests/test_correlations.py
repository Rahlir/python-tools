import pytest

import numpy as np
import mdanalysis as md


def init_correlationfunctions():
    cfs = md.CorrelationFunctions()

    cf1 = np.random.random((100, 1000))
    cf1_obj = md.CorrelationFunction(cf1, "cf1")

    cf2 = np.random.random((100, 1000))
    cf2_obj = md.CorrelationFunction(cf2, "cf2")

    cfs.add(cf1_obj)
    cfs.add(cf2_obj)

    return cfs


def test_cfs_muliplication():
    cfs = init_correlationfunctions()

    scale = np.random.random()

    cfs_new = cfs * scale

    for cf_key in cfs:
        orig = cfs[cf_key]
        new = cfs_new[cf_key]
        correct_result = orig.cf_var * scale
        assert (correct_result == new.cf_var).all()

        # Check that orig != new
        assert not (orig.cf_var == new.cf_var).any()


def test_cfs_division():
    cfs = init_correlationfunctions()

    scale = np.random.random()

    cfs_new = cfs / scale

    for cf_key in cfs:
        orig = cfs[cf_key]
        new = cfs_new[cf_key]
        correct_result = orig.cf_var / scale
        assert (correct_result == new.cf_var).all()

        # Check that orig != new
        assert not (orig.cf_var == new.cf_var).any()


def test_cf_multiplication():
    cf_var = np.random.random((100, 1000))
    cf = md.CorrelationFunction(cf_var, "cf")

    scale = np.random.random()

    cf_new = cf * scale

    correct_result = cf.cf_var * scale

    assert (correct_result == cf_new.cf_var).all()


def test_cf_division():
    cf_var = np.random.random((100, 1000))
    cf = md.CorrelationFunction(cf_var, "cf")

    scale = np.random.random()

    cf_new = cf / scale

    correct_result = cf.cf_var / scale

    assert (correct_result == cf_new.cf_var).all()


def test_cf_multiplication_average():
    cf_var = np.random.random((100, 1000))
    cf = md.CorrelationFunction(cf_var, "cf")

    original_avg = cf.average_cf

    scale = np.random.random()

    cf_new = cf * scale

    new_avg = cf_new.average_cf

    correct_32f = np.array(original_avg*scale, dtype=np.float32)
    tested_32f = np.array(new_avg, dtype=np.float32)

    assert (correct_32f == tested_32f).all()
