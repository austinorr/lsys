import pytest

import numpy

import lsys
from lsys import algo


COORDS = numpy.array([[[0.,  0.],
                       [0.,  1.]],

                      [[0.,  1.],
                       [1.,  1.]],

                      [[1.,  1.],
                       [1.,  0.]],

                      [[1.,  0.],
                       [2.,  0.]],

                      [[2.,  0.],
                       [2., -1.]],

                      [[2., -1.],
                       [1., -1.]],

                      [[1., -1.],
                       [1., -2.]],

                      [[1., -2.],
                       [2., -2.]]]
                     )

X = numpy.array([0.,  0.,  0.,  1.,  1.,  1.,  1.,  2.,  2.,  2.,  2.,  1.,  1.,
                 1.,  1.,  2.])

Y = numpy.array([0.,  1.,  1.,  1.,  1.,  0.,  0.,  0.,  0., -1., -1., -1., -1.,
                 -2., -2., -2.])


@pytest.mark.parametrize(('num', 'expected'),
                         [
    (5, 1.2417853825280818),
    (0, 0),
])
def test_add_noise(num, expected):
    numpy.random.seed(42)
    assert algo.add_noise(num) == expected


@pytest.mark.parametrize(('array_like', 'expected'),
                         [
    (numpy.array([0, 1, 2, 3, 4, 5], dtype=numpy.float),
        numpy.array([0.5,  1.5,  2.5,  3.5,  4.5], dtype=numpy.float)),
    ([0, 1, None, 2, 3, numpy.nan, 4, 5, numpy.nan],
        numpy.array([0.5,  1.5,  2.5,  3.5,  4.5], dtype=numpy.float)),
    (numpy.array([0, 1, None, 2, 3, numpy.nan, 4, 5, numpy.nan]),
        numpy.array([0.5,  1.5,  2.5,  3.5,  4.5], dtype=numpy.float)),

    (-1 * numpy.array([0, 1, 2, 3, 4, 5], dtype=numpy.float),
        -1 * numpy.array([0.5,  1.5,  2.5,  3.5,  4.5], dtype=numpy.float)),

])
def test_midpoints(array_like, expected):
    result = algo.midpoints(array_like)
    numpy.testing.assert_allclose(result, expected)


def test_xy_to_coords():
    coords = algo.xy_to_coords(X, Y)
    numpy.testing.assert_equal(coords, COORDS)


def test_xy_to_coords_raises_shape():
    with pytest.raises(ValueError):

        algo.xy_to_coords(X, Y[:-1])


def test_coords_to_xy():
    x, y = algo.coords_to_xy(COORDS)
    numpy.testing.assert_equal(x, X)
    numpy.testing.assert_equal(y, Y)
