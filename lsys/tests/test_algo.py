import pytest

import numpy

from lsys import algo


COORDS = numpy.array(
    [
        [[0.0, 0.0], [0.0, 1.0]],
        [[0.0, 1.0], [1.0, 1.0]],
        [[1.0, 1.0], [1.0, 0.0]],
        [[1.0, 0.0], [2.0, 0.0]],
        [[2.0, 0.0], [2.0, -1.0]],
        [[2.0, -1.0], [1.0, -1.0]],
        [[1.0, -1.0], [1.0, -2.0]],
        [[1.0, -2.0], [2.0, -2.0]],
    ]
)

X = numpy.array(
    [0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0]
)

Y = numpy.array(
    [
        0.0,
        1.0,
        1.0,
        1.0,
        1.0,
        0.0,
        0.0,
        0.0,
        0.0,
        -1.0,
        -1.0,
        -1.0,
        -1.0,
        -2.0,
        -2.0,
        -2.0,
    ]
)


@pytest.mark.parametrize(
    ("num", "expected"),
    [
        (5, 1.2417853825280818),
        (0, 0),
    ],
)
def test_add_noise(num, expected):
    numpy.random.seed(42)
    assert algo.add_noise(num) == expected


@pytest.mark.parametrize(
    ("array_like", "expected"),
    [
        (
            numpy.array([0, 1, 2, 3, 4, 5], dtype=float),
            numpy.array([0.5, 1.5, 2.5, 3.5, 4.5], dtype=float),
        ),
        (
            [0, 1, None, 2, 3, numpy.nan, 4, 5, numpy.nan],
            numpy.array([0.5, 1.5, 2.5, 3.5, 4.5], dtype=float),
        ),
        (
            numpy.array([0, 1, None, 2, 3, numpy.nan, 4, 5, numpy.nan]),
            numpy.array([0.5, 1.5, 2.5, 3.5, 4.5], dtype=float),
        ),
        (
            -1 * numpy.array([0, 1, 2, 3, 4, 5], dtype=float),
            -1 * numpy.array([0.5, 1.5, 2.5, 3.5, 4.5], dtype=float),
        ),
    ],
)
def test_midpoints(array_like, expected):
    result = algo.midpoints(array_like)
    numpy.testing.assert_allclose(result, expected)


def test_xy_to_coords():
    coords = algo.xy_to_coords(X, Y, stride=2)
    numpy.testing.assert_equal(coords, COORDS)


def test_coords_to_xy():
    x, y = algo.coords_to_xy(COORDS)
    numpy.testing.assert_equal(x, X)
    numpy.testing.assert_equal(y, Y)
