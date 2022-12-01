import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

import pytest

from lsys import validate


def _pyplot():

    from matplotlib import pyplot

    return pyplot


def test_axes_object_invalid():
    with pytest.raises(ValueError):
        validate.axes_object("junk")


def test_axes_object_with_ax():
    fig, ax = _pyplot().subplots()
    fig1, ax1 = validate.axes_object(ax)
    assert isinstance(ax1, Axes)
    assert isinstance(fig1, Figure)
    assert ax1 is ax
    assert fig1 is fig


def test_axes_object_with_None():
    fig1, ax1 = validate.axes_object(None)
    assert isinstance(ax1, Axes)
    assert isinstance(fig1, Figure)


@pytest.mark.parametrize(
    ("listlike", "expected"),
    [
        ([0.5, 0.5], np.array([0.5, 0.5], dtype=float)),
        (np.array([0.5, 0.5], dtype=float), np.array([0.5, 0.5], dtype=float)),
    ],
)
def test_is_np(listlike, expected):
    result = validate.is_np(listlike)
    np.array_equal(result, expected)
