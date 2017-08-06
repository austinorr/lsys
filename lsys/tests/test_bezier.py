import pytest

import numpy

from .. import bezier


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
        [ 0.  ,  0.  ],
        [ 0.4 ,  0.32],
        [ 0.8 ,  0.48],
        [ 1.2 ,  0.48],
        [ 1.6 ,  0.32],
        [ 2.  ,  0.  ]
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
        [ 0.   ,  0.   ],
        [ 0.496,  0.48 ],
        [ 0.848,  0.72 ],
        [ 1.152,  0.72 ],
        [ 1.504,  0.48 ],
        [ 2.   ,  0.   ]
        ])
    ),
    (numpy.array([
        [0, 0, 0], 
        [.5, 1, 2],
        [2, 0, 0],
        ]),
    5,
    numpy.array([
        [ 0.  ,  0.  ,  0.  ],
        [ 0.24,  0.32,  0.64],
        [ 0.56,  0.48,  0.96],
        [ 0.96,  0.48,  0.96],
        [ 1.44,  0.32,  0.64],
        [ 2.  ,  0.  ,  0.  ]
        ])
    )
])
def test_bezier(pts, segs, expected):
    res = bezier.bezier(pts, segs)
    numpy.testing.assert_allclose(res, expected)


def test_circular_weight_ref():
    """ensure that circular weight returns value similar to
    ref:
        http://spencermortensen.com/articles/bezier-circle/
        0.551915024494
    """
    tol = 1e8
    rem = bezier.circular_weight(90) - 0.55191502#4494

    assert numpy.abs(rem) < tol



@pytest.mark.parametrize('angle', numpy.arange(20, 180, 5))
def test_circular_weight_equals_find_weight(angle):
    tol = 1e8
    cw = bezier.circular_weight(angle)
    fcw = bezier.find_circular_weight(angle)[0]
    rem = cw - fcw

    assert numpy.abs(rem) < tol
