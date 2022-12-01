import numpy
import matplotlib
from matplotlib.collections import LineCollection, PathCollection
from matplotlib.path import Path

from . import algo
from . import bezier
from . import validate


def plot(x, y, ax=None, **kwargs):
    """Plots 'x' vs 'y' using matplotlib. This is a convenience wrapper that
    creates the axes if it doesn't exist, and sets some nice rendering defaults
    for plotting l-systems.

    Parameters
    ----------
    x : numpy.array
        1D numpy array of points
    y : numpy.array
        1D numpy array of points
    ax : matplotlib.axes.Axes, optional (default = None)
        the axes artist for plotting. If `None` is given, a new figure
        will be created.
    kwargs : dict, optional
        all remaining keyword arguments are passed into the `plot()` command

    Returns
    -------
    ax : matplotlib.axes.Axes

    """
    if "solid_capstyle" not in kwargs:  # pragma: no cover
        kwargs["solid_capstyle"] = "round"

    _, axes = validate.axes_object(ax)
    _ = axes.plot(x, y, **kwargs)
    return axes


def plot_collection(collection, ax=None):
    _, axes = validate.axes_object(ax)
    axes.add_collection(collection)
    return axes


def construct_line_collection(coords, **kwargs):
    if "cmap" in kwargs and "array" not in kwargs:  # pragma: no cover
        kwargs["array"] = numpy.linspace(0.0, 1.0, len(coords))

    if "capstyle" not in kwargs:  # pragma: no cover
        kwargs["capstyle"] = "round"

    lines = LineCollection(coords, **kwargs)

    return lines


def bezier_segment_mpl(x, y, angle=None, weight=None, keep_ends=None):

    if angle is not None and weight is None:  # pragma: no cover
        weight = bezier.circular_weight(angle)
    if weight is None:  # pragma: no cover
        raise ValueError("one of angle or weight are required.")
    xmid, ymid = algo.midpoints(x), algo.midpoints(y)
    temp = numpy.vstack((xmid, ymid)).T
    rng = numpy.arange(0, len(temp) - 1, 2)
    paths = []
    for i in rng:
        pt = temp[i : i + 3]
        a = pt[0]
        b = bezier.ctrl_pts(pt[0], pt[1], weight)
        c = bezier.ctrl_pts(pt[2], pt[1], weight)
        d = pt[2]
        verts = [a, b, c, d]
        codes = [1, 4, 4, 4]  # {1: Path.MOVETO, 4: Path.CURVE4}
        paths.append(Path(verts, codes))
    if keep_ends:
        pi = [Path([[x[0], y[0]], [xmid[0], ymid[0]]])]
        pe = [Path([[xmid[-1], ymid[-1]], [x[-1], y[-1]]])]
        return pi + paths + pe
    return paths


def bezier_paths_mpl(x, y, weight=None, angle=None, keep_ends=None):

    if angle is not None and weight is None:  # pragma: no cover
        weight = bezier.circular_weight(angle)
    if weight is None:  # pragma: no cover
        raise ValueError("one of angle or weight are required.")

    _x = [x[s] for s in numpy.ma.clump_unmasked(numpy.ma.masked_invalid(x))]
    _y = [y[s] for s in numpy.ma.clump_unmasked(numpy.ma.masked_invalid(y))]

    paths = []
    for segx, segy in zip(_x, _y):
        _paths = bezier_segment_mpl(segx, segy, weight=weight, keep_ends=keep_ends)
        paths.extend(_paths)
    return paths


def construct_bezier_path_collection(coords, **kwargs):

    angle = kwargs.pop("angle", None)
    weight = kwargs.pop("weight", None)
    keep_ends = kwargs.pop("keep_ends", None)

    if angle is not None and weight is None:  # pragma: no cover
        weight = bezier.circular_weight(angle)
    if weight is None:  # pragma: no cover
        raise ValueError("one of angle or weight are required.")

    x, y = algo.coords_to_xy(coords)

    paths = bezier_paths_mpl(x, y, weight=weight, angle=angle, keep_ends=keep_ends)

    if "cmap" in kwargs and "array" not in kwargs:  # pragma: no cover
        kwargs["array"] = numpy.linspace(0.0, 1.0, len(paths))
    if "capstyle" not in kwargs:  # pragma: no cover
        kwargs["capstyle"] = "round"
    if "facecolor" not in kwargs:  # pragma: no cover
        kwargs["facecolor"] = "none"

    pc = PathCollection(paths, **kwargs)

    return pc


def pretty_format_ax(ax, x=None, y=None, coords=None, pad=5, square=None):
    """
    Parameters
    ----------
    ax : matplotlib.axes.Axes
        the axes artist for plotting.
    x : numpy.array, optional
        1D numpy array of points
    y : numpy.array, optional
        1D numpy array of points
    coords : numpy.array, optional
        2D numpy array of points
    pad : float or int, optional (default = 5)
        the percent spacing between plot data and axes lines. This can be used
        to zoom the plot.
    square : bool, optional (default = False)
        whether to make the output plot a square with equal aspect
        ratios for the axes.

    Returns
    -------
    ax : matplotlib.axes.Axes

    """

    if square is None:
        square = True

    if coords is not None:
        xlim, ylim = get_coord_lims(coords, pad=pad, square=square)
    else:
        xlim, ylim = get_xy_lims(x, y, pad=pad, square=square)

    _ = ax.set_xlim(xlim)
    _ = ax.set_ylim(ylim)
    _ = ax.set_xticks([])
    _ = ax.set_yticks([])

    if square:
        _ = ax.set_aspect("equal")
    ax.get_figure().subplots_adjust(
        left=0.05, right=1 - 0.05, bottom=0.05, top=1 - 0.05
    )
    return ax


def square_aspect(xlim, ylim):
    """Calculates the limits to produce a square plot if all axes are
    equal scale.

    """
    x0, x1 = xlim
    y0, y1 = ylim

    x_range = numpy.abs(x1 - x0)
    y_range = numpy.abs(y1 - y0)

    if x_range > y_range:
        fac = (x_range - y_range) / 2

        return xlim, [y0 - fac, y1 + fac]

    else:
        fac = (y_range - x_range) / 2

        return [x0 - fac, x1 + fac], ylim


def pad_lim(lim, pad=None):
    if pad is None:
        pad = 0
    _min, _max = lim
    pad = (_max - _min) * pad / 100
    lim = [_min - pad, _max + pad]

    return lim


def get_coord_lims(coords, pad=None, square=None):

    x, y = algo.coords_to_xy(coords)

    return get_xy_lims(x, y, pad=pad, square=square)


def get_xy_lims(x, y, pad=None, square=None):

    x0, x1 = numpy.nanmin(x), numpy.nanmax(x)
    y0, y1 = numpy.nanmin(y), numpy.nanmax(y)
    xlim, ylim = pad_lim([x0, x1], pad=pad), pad_lim([y0, y1], pad=pad)

    if square:
        return square_aspect(xlim, ylim)

    return xlim, ylim


def make_colormap(seq):
    """Return a LinearSegmentedColormap with colors defined as the sequence.

    The sequence red to blue can be defined as:
    `make_colormap(['red', 'blue'])`
    or equivalently
    `make_colormap([(1,0,0), 'blue'])`

    For more control over color transitions, floats can be included after pairs
    of colors to indicate the percentage of the color map that the transition
    should take place.

    `make_colormap(['red', 'green', .25, 'green', 'blue'])`




    Parameters
    ----------
    seq : list
        a sequence of floats, strings, or RGB-tuples.
        The floats should be in increasing order
        and in the interval (0, 1).

    Returns
    -------
    cmap : matplotlib.colors.LinearSegmentedColormap

    Examples
    --------

    References
    ----------
    http://stackoverflow.com/questions/16834861/create-own-colormap-using-matplotlib-and-plot-color-scale
    """
    CC = matplotlib.colors.ColorConverter()
    LSC = matplotlib.colors.LinearSegmentedColormap

    temp1 = seq
    if all(isinstance(x, str) for x in seq):
        if len(seq) > 2:
            temp1 = []
            f = 1.0 / (len(seq) - 1)
            for i in range(len(seq) - 1):
                temp1.append(seq[i])
                temp1.append(seq[i + 1])
                if i < len(seq) - 2:
                    temp1.append(f * (i + 1))

    temp2 = []
    for color in temp1:
        if isinstance(color, str):
            color = CC.to_rgb(color)
        temp2.append(color)
    seq = [(None,) * 3, 0.0] + temp2 + [1.0, (None,) * 3]
    cdict = {"red": [], "green": [], "blue": []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict["red"].append([item, r1, r2])
            cdict["green"].append([item, g1, g2])
            cdict["blue"].append([item, b1, b2])
    return LSC("CustomMap", cdict)
