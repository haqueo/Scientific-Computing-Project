import pytest
import solution as s
import numpy as np

def test_weight_matrix():
    data = s.generate_connectivity('./data/jobslist')

    weight = s.generate_weight_matrix(data)
    # long ones
    assert np.array_equal(weight[:,26],[-1]*28)
    assert np.array_equal(weight[0:13,27],[-1]*13)
    assert np.array_equal(weight[13:26,27],[0]*13)
    assert np.array_equal(weight[27,:],[-1]*28)
    assert weight[0,13] == 41
    assert weight[1,14] == 51
    assert weight[13,0] == -1

def test_matrixgeneration(): # test passed
    data = s.generate_connectivity('./data/jobslist')

    assert data[0][1] == 41
    assert data[4][2] == []
    assert data[9][1] == 49
    assert data[10][2] == [12]
    assert data[0][2] == [1,7,10]

def test_longest_path():
    data = s.generate_connectivity('./data/jobslist')
    weights = s.generate_weight_matrix(data)
    adjusted_weights = -1*weights

    assert s.updated_bellman_ford(26,27,adjusted_weights) == [26, 0, 13, 1, 14, 4, 17, 27]