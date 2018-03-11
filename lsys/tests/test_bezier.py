import pytest

import numpy

import lsys
from lsys import bezier


@pytest.mark.parametrize(('n', 'k', 'expected'),
                         [
    (0, 0, 1),
    (2, 1, 2),
    (6, 2, 15),
    (9, 4, 126),
])
def test_binomial(n, k, expected):
    result = bezier.binomial(n, k)

    assert result == expected


@pytest.mark.parametrize(('p0', 'p1', 'w', 'expected'),
                         [
    ([0, 0], [.5, .5], .5,   [.25,  .25]),
    ([0, 0], [1,   1], .5,   [.5,   .5]),
    ([0, 0], [1,   1], .333, [.333, .333]),
])
def test_ctrl_pts(p0, p1, w, expected):
    p0 = numpy.array(p0, dtype=numpy.float)
    p1 = numpy.array(p1, dtype=numpy.float)
    expected = numpy.array(expected, dtype=numpy.float)
    result = bezier.ctrl_pts(p0, p1, w)

    numpy.testing.assert_equal(result, expected)


@pytest.mark.parametrize(('n', 'k', 'expected'),
                         [
    (0, 0, [1.000000, 1.000000, 1.000000, 1.000000, 1.000000, ]),
    (1, 0, [1.000000, 0.750000, 0.500000, 0.250000, 0.000000, ]),
    (1, 1, [0.000000, 0.250000, 0.500000, 0.750000, 1.000000, ]),
    (2, 0, [1.000000, 0.562500, 0.250000, 0.062500, 0.000000, ]),
    (2, 1, [0.000000, 0.375000, 0.500000, 0.375000, 0.000000, ]),
    (2, 2, [0.000000, 0.062500, 0.250000, 0.562500, 1.000000, ]),
    (3, 0, [1.000000, 0.421875, 0.125000, 0.015625, 0.000000, ]),
    (3, 1, [0.000000, 0.421875, 0.375000, 0.140625, 0.000000, ]),
    (3, 2, [0.000000, 0.140625, 0.375000, 0.421875, 0.000000, ]),
    (3, 3, [0.000000, 0.015625, 0.125000, 0.421875, 1.000000, ]),
])
def test_lsys_bezier_poly(n, k, expected):
    t = numpy.array([0, .25, .5, .75, 1])
    expected = numpy.array(expected, dtype=numpy.float)
    result = bezier.poly(n, k)(t)

    numpy.testing.assert_equal(result, expected)


@pytest.mark.parametrize(('pts', 'segs', 'expected'), [
    (numpy.array([
        [0, 0],
        [1, 1],
        [2, 0]
    ]),
        5,
        numpy.array([
            [0.,  0.],
            [0.4,  0.32],
            [0.8,  0.48],
            [1.2,  0.48],
            [1.6,  0.32],
            [2.,  0.]
        ])
    ),
    (numpy.array([
        [0, 0],
        [1, 1],
        [1, 1],
        [2, 0],
    ]),
        5,
        numpy.array([
            [0.,  0.],
            [0.496,  0.48],
            [0.848,  0.72],
            [1.152,  0.72],
            [1.504,  0.48],
            [2.,  0.]
        ])
    ),
    (numpy.array([
        [0, 0, 0],
        [.5, 1, 2],
        [2, 0, 0],
    ]),
        5,
        numpy.array([
            [0.,  0.,  0.],
            [0.24,  0.32,  0.64],
            [0.56,  0.48,  0.96],
            [0.96,  0.48,  0.96],
            [1.44,  0.32,  0.64],
            [2.,  0.,  0.]
        ])
    )
])
def test_bezier(pts, segs, expected):
    res = bezier.bezier(pts, segs)
    numpy.testing.assert_allclose(res, expected)


@pytest.mark.parametrize(('keep', 'weight', 'expected'), [
    (True, None, (
        numpy.array([
            0.,
            0.5,  0.68347576,
            0.89173788,
            1.10826212,
            1.31652424,
            1.5,
            2.]),
        numpy.array([
            0.,
            0.5,
            0.63245961,
            0.69868941,
            0.69868941,
            0.63245961,
            0.5,
            0.]))),
    (False, None, (
        numpy.array([
            0.5,
            0.68347576,
            0.89173788,
            1.10826212,
            1.31652424,
            1.5
        ]),
        numpy.array([
            0.5,
            0.63245961,
            0.69868941,
            0.69868941,
            0.63245961,
            0.5]))
     ),
    (True, 0.5, (
        numpy.array([0.,  0.5,  0.676,  0.888,  1.112,  1.324,  1.5,  2.]),
        numpy.array([0.,  0.5,  0.62,  0.68,  0.68,  0.62,  0.5,  0.]))),
    (False, 0.5, (
        numpy.array([0.5,  0.676,  0.888,  1.112,  1.324,  1.5]),
        numpy.array([0.5,  0.62,  0.68,  0.68,  0.62,  0.5]))
     ),

])
def test_bezier_xy(keep, weight, expected):
    pts = numpy.array([
        [0, 0],
        [1, 1],
        [1, 1],
        [2, 0],
    ])
    res = bezier.bezier_xy(pts[:, 0], pts[:, 1],
                           weight=weight, segs=5, keep_ends=keep)
    numpy.testing.assert_allclose(res, expected)


def test_bezier_xy_curve():
    d = lsys.Lsys(**lsys.Fractal['Dragon'])
    d.depth = 2
    res = bezier.bezier_xy(d.x, d.y, segs=4)
    exp = (numpy.array([0.,  0.,  0.03931847,  0.14651593,  0.30545542,
                        0.5,  0.5,  0.69454458,  0.85348407,  0.96068153,
                        1.,  1.,  1.03931847,  1.14651593,  1.30545542,
                        1.5,  2.]),
           numpy.array([0.,  0.5,  0.69454458,  0.85348407,  0.96068153,
                        1.,  1.,  0.96068153,  0.85348407,  0.69454458,
                        0.5,  0.5,  0.30545542,  0.14651593,  0.03931847,
                        0.,  0.]))

    numpy.testing.assert_allclose(res, exp, rtol=1e-03)


def test_circular_weight_ref():
    """ensure that circular weight returns value similar to
    ref:
        http://spencermortensen.com/articles/bezier-circle/
        0.551915024494
    """
    tol = 1e8
    rem = bezier.circular_weight(90) - 0.55191502  # 4494

    assert numpy.abs(rem) < tol


@pytest.mark.parametrize('angle', numpy.arange(20, 180, 5))
def test_circular_weight_equals_find_weight(angle):
    tol = 1e8
    cw = bezier.circular_weight(angle)
    fcw = bezier.find_circular_weight(angle)[0]
    rem = cw - fcw

    assert numpy.abs(rem) < tol


@pytest.mark.parametrize(
    ('angle', 'guess'),
    zip(
        [0, 180, 90, 90],
        [.5, .5, 0, 1],
    )
)
def test_find_circular_weight_raises(angle, guess):
    with pytest.raises(ValueError):
        bezier.find_circular_weight(angle, guess)


@pytest.mark.parametrize(('angle', 'guess', 'max_iters'), [
    (90, .5, 1),
    (90, .99, 1),
    (45, .1, 1)
])
def test_find_circular_weight_one_iter(angle, guess, max_iters):
    res = bezier.find_circular_weight(
        angle, guess=guess, max_iters=max_iters)[0]
    assert res == guess
