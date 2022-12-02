import numpy
from matplotlib.axes import Axes


def axes_object(ax):
    """Checks if a value if an Axes. If None, a new one is created.
    Both the figure and axes are returned (in that order).

    """

    if ax is None:
        from matplotlib import pyplot

        fig, ax = pyplot.subplots()

    elif isinstance(ax, Axes):
        fig = ax.figure
    else:
        msg = "`ax` must be a matplotlib Axes instance or None"
        raise ValueError(msg)

    return fig, ax


def is_np(listlike):
    if not isinstance(listlike, numpy.ndarray) or listlike.dtype != float:
        listlike = numpy.array(listlike, dtype=float)

    return listlike
