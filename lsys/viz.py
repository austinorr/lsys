from __future__ import division

import numpy
import matplotlib
from matplotlib.collections import LineCollection

from . import validate
from . import algo


def plot(x, y, pad=5, square=False, ax=None, **kwargs):
    """Plots 'x' vs 'y' and optionally computes the limits
    of the axes based on the input data

    Parameters
    ----------
    x : numpy.array
        1D numpy array of points
    y : numpy.array
        1D numpy array of points
    pad : float or int, optional (default = 5)
        the percent spacing between plot data and axes lines. This can be used
        to zoom the plot. This is only applied if 'square' is 'True'
        #TODO: figure out how to make this also pan the plot.
    square : bool, optional (default = False)
        whether to make the output plot a square with equal aspect
        ratios for the axes.
    ax : matplotlib.axes.Axes, optional (default = None)
        the axes artist for plotting. If `None` is given, a new figure
        will be created.
    kwargs : dict, optional
        all remaining keyword arguments are passed into the `plot()` command

    Returns
    -------
    ax : matplotlib.axes.Axes

    """
    if 'solid_capstype' not in kwargs:
        kwargs['solid_capstyle']='round'

    fig, ax = validate.axes_object(ax)
    ax.plot(x, y, **kwargs)
    if square:
        xlim, ylim = get_xy_lims(x, y, pad=pad, square=square)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_aspect('equal')
    return ax


def plot_line_collection(coords, pad=5, square=False, ax=None, **kwargs):
    """Plots a 2d array of points as a `matplotlib.LineCollection` and computes
    the limits of the axes based on the input data, since this is not handled
    by matplotlib by default.

    Parameters
    ----------
    coords : numpy.array
        2D numpy array of points
    pad : float or int, optional (default = 5)
        the percent spacing between plot data and axes lines. This can be used
        to zoom the plot.
        #TODO: figure out how to make this also pan the plot.
    square : bool, optional (default = False)
        whether to make the output plot a square with equal aspect
        ratios for the axes.
    ax : matplotlib.axes.Axes, optional (default = None)
        the axes artist for plotting. If `None` is given, a new figure
        will be created.
    kwargs : dict, optional
        all remaining keyword arguments are passed into the :class:`LineCollection`

    Returns
    -------
    ax : matplotlib.axes.Axes

    """
    if 'cmap' in kwargs:
        if 'array' not in kwargs:
            kwargs['array'] = numpy.linspace(0.0, 1.0, len(coords))

    fig, ax = validate.axes_object(ax)
    lines = LineCollection(coords, **kwargs)
    ax.add_collection(lines)
    xlim, ylim = get_coord_lims(coords, pad, square)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    if square:
        ax.set_aspect('equal')
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

def pad_lim(lim, pad=5):
    _min, _max = lim
    pad = (_max - _min) * pad / 100
    lim = [_min - pad, _max + pad]

    return lim


def get_coord_lims(coords, pad=5, square=False):

    x, y = algo.coords_to_xy(coords)

    return get_xy_lims(x, y, pad=pad, square=square)



def get_xy_lims(x, y, pad=5, square=False):

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
            f = 1. / (len(seq) - 1)
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
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return LSC('CustomMap', cdict)
