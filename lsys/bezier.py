"""
This module has functions helpful in the construction of general
bezier curves, as well as fitting cubic bezier curves between
vertices calculated by the :class:``lsys.Lsys``

In addition, this module contains the code used to determine the
symetric weight factor needed to determine the position of control
points that form near-circular curves between three points with
an arbitrary interior angle, buiding on the work documented
`here <http://spencermortensen.com/articles/bezier-circle/>`_.
"""

from __future__ import division
import numpy

from . import validate
from . import algo


def ctrl_pts(p0, p1, w):
    """
    Calculate the position of a new point along vector
    `p0` to `p1` with magnitude `w`.

    Parameters
    ----------
    p0 : 1D array
        the starting point
    p1 : 1D array
        the end point
    w : float
        the weight factor

    Returns
    -------
    point : 1D array
        a point along vector `p0` to `p1` with magnitude `w`
    """
    p0 = validate.is_np(p0)
    p1 = validate.is_np(p1)
    vec = p1 - p0
    return p0 + vec * w


def binomial(n, k):
    """
    Parameters
    ----------
    n : integer
        the order of the binomial to expand
    k : integer
        the zero indexed position of the binomial expansion
        coefficient to return

    Returns
    -------
    coefficient : integer
        coefficient for the nth order binomial expansion, kth term

    reference: http://pomax.github.io/bezierinfo/
    """

    tri = [[1],              # n=0
           [1, 1],            # n=1
           [1, 2, 1],          # n=2
           [1, 3, 3, 1],        # n=3
           [1, 4, 6, 4, 1],      # n=4
           [1, 5, 10, 10, 5, 1],    # n=5
           [1, 6, 15, 20, 15, 6, 1],  # n=6
           ]

    while n >= len(tri):
        s = len(tri)
        nextrow = [0 for i in range(s + 1)]
        nextrow[0] = 1
        prev = s - 1
        for i in range(1, s):
            nextrow[i] = tri[prev][i - 1] + tri[prev][i]
        nextrow[s] = 1
        tri.append(nextrow)
    return tri[n][k]


def poly(n, k):
    """
    Expands binomial and computes value at `t`

    Parameters
    ----------
    n : integer
        nth order of polynomial
    k : integer
        positional term for binomial expansion coefficient

    Returns
    -------
    value : float or list of floats


    Reference
    ---------
    https://gist.github.com/Juanlu001/7284462
    """
    coeff = binomial(n, k)

    def _poly(t):
        """Calculates value at t between bezier points"""
        return coeff * (1 - t)**(n - k) * t**(k)

    return _poly


def bezier(points, segs=100):
    """
    Computes nth order bezier curves through the `points` provided
    and returns the curve as a list of points to produce line segments.

    The order of the bezier curve is determined by the length of
    the list of points. The length of the output curve numpy.array is
    equal to `segs` + 1, such that `segs` is equal to the number of
    line segments between the points of the array.

    Parameters
    ----------
    points : list-like
        2D array
    segs : integer, optional (default = 100)
        The number of line segments to approximate bezier curve

    Returns
    -------
    curve : numpy.array
        2D array of points along the curve.

    Reference
    ---------
    https://gist.github.com/Juanlu001/7284462
    """

    points = validate.is_np(points)
    dims = points.shape[1]

    # increment num such that final line segments will be equal to `segs`
    num = segs + 1

    n = len(points)
    t = numpy.linspace(0, 1, num=num)
    curve = numpy.zeros((num, dims), dtype=float)
    for i, pt in enumerate(points):
        curve += numpy.outer(poly(n - 1, i)(t), pt)

    return curve


def circular_weight(angle):
    """This function utilizes the precomputed circular bezier function
    with a fit to a 10th order curve created by the following code block:

    .. code-block:: python

        x = numpy.arange(.5, 180, 0.5)
        y = []
        for i in x:
            y.append(bezier.find_circular_weight(i, tol=1e-12, max_iters=500))
        y = numpy.array(y)
        z = numpy.polyfit(x, y, 10)


    Parameters
    ----------
    angle : float
        enter the angle to be traversed in degrees

    Returns
    -------
    weight : float
        Weight value for calculating bezier control points that
        approximate a circular curve.

    """
    z = numpy.array([
        -2.45143082907626980583458614241573e-24,
        1.58856196152315352138612607918623e-21,
        -5.03264989277462933391916020538014e-19,
        8.57954915199159887348249578203777e-17,
        -1.09982713519619074150585319501519e-14,
        6.42175701661701683377126465867012e-13,
        -1.95012445981222027957307425487916e-10,
        6.98338125134285339870680633234242e-10,
        -1.27018636324842636571531492850617e-05,
        5.58069196465371404519196542326487e-08,
        6.66666581437823202449521886592265e-01
    ])

    p = numpy.poly1d(z)

    return p(angle)


def find_circular_weight(angle,  guess=0.5, tol=1e-9, max_iters=50, r=10, segs=100):
    """
    Finds weight factor for bezier control points such that the `angle`
    QRS will be filled with cubic bezier curve approximating a circle
    that is tangent at the points Q and S.

    Parameters
    ----------
    angle : float
        the turn angle in degrees. e.g., if turn angle is 30 degrees, then the angle
        that needs to be spanned by the curve is 150 degrees.
    guess : float, optional (default=0.5)
        the initial value for the bisection search
    tol : float, optional (default=1e-9)
        the tolerance for ceasing bisection search
    max_iters : int, optional (default=50)
        the maximum iterations for bisection search
    r : float, optional (default=10)
        the radius for the circle. the larger this value, the more precise the
        weight will be since tolerance is absolute.
    segs : int, optional (defualt=100)
        number of points to consider on the circle, and bezier points to compute.

    Returns
    -------
    weight : float
        the magnitude for scaling control points relative to start and end points.
    error_np : 1D numpy.array
        an array of float error values from the curve to circular radius
    error : float
        the max error minus min error
    iterations : integer
        the count of bisection search iterations

    References
    ----------
    http://spencermortensen.com/articles/bezier-circle/


               ^
               | /
               |/   \
    h -- -- -- R    angle
              / \   /
             / | \
            /  |  \
           /  o o  \
          /o   |   o\
         /o    |    o\
    0 - Q o----+----o S -- >
               0

    """

    if not 0 < angle < 180:
        raise ValueError('`angle` must be between 0 and 180, exclusive')

    if not 0 < guess < 1:
        raise ValueError('`guess` must be between 0 and 1, exclusive')

    deg = (180 - angle) / 2
    theta = numpy.deg2rad(deg)  # half of the interior angle formed by QRS

    r = r
    # y location of acute angle QRS apex
    h = r * numpy.cos(theta) / numpy.tan(theta)
    x = 0  # x location of acute angle QRS apex
    kc = -h * numpy.tan(theta) * numpy.tan(theta)  # y value of circle center
    xc = h * numpy.tan(theta)  # x value of circle and line RS tangent point

    pt0 = numpy.array([-xc, 0])  # position of point Q
    pt2 = numpy.array([xc, 0])  # position of point S
    ptm = numpy.array([x, h])  # position of apex point R

    a = 1  # upper bound for bisection search
    b = 0  # lower bound for bisection search

    guess_gen = gen_new_guess(guess, pt0, pt2, ptm, kc, r, a, b, segs)
    for i in range(max_iters):

        guess, error_np, error, a, b = next(guess_gen)
        if -tol < error < tol:
            return guess, error_np, error, i

    return guess, error_np, error, i


def gen_new_guess(guess, pt0, pt2, ptm, kc, r, a, b, segs):
    """Generator to produce the next guess in the bisection search sequence"""
    while True:
        pc1 = ctrl_pts(pt0, ptm, guess)  # first bezier control point along QR
        pc2 = ctrl_pts(pt2, ptm, guess)  # second bezier control point along RS
        # build cubic bezier curve with `segs` segments
        t = bezier([pt0, pc1, pc2, pt2], segs)
        # determine radial distance from each bezier point to the circle center
        radial_dist = numpy.sqrt(numpy.sum((t - [0, kc])**2, axis=1))
        # radial distance from circle to bezier curve
        error_np = radial_dist - r
        tmax = numpy.abs(error_np.max())
        tmin = numpy.abs(error_np.min())
        error = (tmax - tmin)  # minimize the range with bisection search

        yield guess, error_np, error, a, b

        if error > 0:
            a = guess
        else:
            b = guess
        guess = (a + b) / 2


def bezier_xy(x, y, weight=None, angle=90, segs=100, keep_ends=True):
    """
    Compute cubic bezier curves between each set of three points
    using symetric control points offset by the `weight`.

    Parameters
    ----------
    x : list-like
        a 1D array of x values
    y : list-like
        a 1D array of y values
    weight : float, optional (default = None)
        Weight given to intermediate bezier control points. If
        `None` then the weight will be determined by the `angle`
    angle : float, optional (default = 90)
        the interior angle for the bezier sections to traverse
    segs : integer, optional (default = 100)
        the number of segments for bezier curve approzimation between
        each set of three points
    keep_ends : bool, optional (default = True)
        include start and end coordinates in output

    Returns
    -------
    tx : numpy.array
        an array of x values
    ty : numpy.array
        an array of y values

    """

    if weight is None:
        weight = circular_weight(angle)

    xmid, ymid = algo.midpoints(x), algo.midpoints(y)

    temp = numpy.vstack(([xmid], [ymid])).T

    rng = numpy.arange(0, len(temp) - 1, 2)
    tx = []
    ty = []
    last_pt = None
    for i in rng:
        pt = temp[i:i + 3]
        if i > 0 and not numpy.array_equal(pt[0], last_pt):
            continue
        c1 = ctrl_pts(pt[0], pt[1], weight)
        c2 = ctrl_pts(pt[2], pt[1], weight)
        t = bezier([pt[0], c1, c2, pt[2]], segs)
        tx.append(t[:, 0])
        ty.append(t[:, 1])
        last_pt = pt[2]

    tx = numpy.array(tx).flatten()
    ty = numpy.array(ty).flatten()

    if keep_ends:

        tx = numpy.concatenate((x[:1], tx, x[-1:]))
        ty = numpy.concatenate((y[:1], ty, y[-1:]))

    return tx, ty
