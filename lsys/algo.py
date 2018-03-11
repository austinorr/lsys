
import numpy

from . import validate


def add_noise(num, scale=.5):
    """produces a random value distributed normally between +- num
    """
    if num:
        return num * numpy.random.normal(0.0, scale)
    return 0


def midpoints(np_array):
    """
    Converts np array to an array of midpoints ignoring

    Parameters
    ----------
    np_array : array-like
        1-dimensional data

    Returns
    -------
    1-D numpy.array
        The length of the output is one less than
        the length of the input array.

    """
    i = 1

    np_array = validate.is_np(np_array)

    result = (np_array[~numpy.isnan(np_array)][i:] +
              np_array[~numpy.isnan(np_array)][:-i]) / 2

    return result


def coords_to_xy(coords):
    """
    Parameters
    ---------
    coords : numpy.array
        a 2D array

    Returns
    -------
    x : numpy.array
        a 1D array
    y :
    """
    x = coords[:, :, 0].flatten()
    y = coords[:, :, 1].flatten()

    return x, y

def split_array_on_nan(array):
    mask = numpy.ma.masked_invalid(array)
    clump_ix = numpy.ma.clump_unmasked(mask)
    return [array[s] for s in clump_ix]


def xy_to_coords(x, y):
    _x = validate.is_np(x)
    _y = validate.is_np(y)

    points = numpy.array([x, y]).T.reshape(-1, 1, 2)
    segments = numpy.concatenate([points[:-1], points[1:]], axis=1)

    return segments[[~numpy.any(numpy.isnan(segments[:, :, 0]), axis=1)]]
