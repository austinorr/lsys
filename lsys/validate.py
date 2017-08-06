from matplotlib import pyplot

import numpy as np


def axes_object(ax):
    """ Checks if a value if an Axes. If None, a new one is created.
    Both the figure and axes are returned (in that order).

    """

    if ax is None:
        fig, ax = pyplot.subplots()
    
    elif isinstance(ax, pyplot.Axes):
        fig = ax.figure
    else:
        msg = "`ax` must be a matplotlib Axes instance or None"
        raise ValueError(msg)

    return fig, ax


def is_np(listlike):
    if not isinstance(listlike, np.ndarray) or listlike.dtype != np.float:
        listlike = np.array(listlike, dtype=np.float)

    return listlike
