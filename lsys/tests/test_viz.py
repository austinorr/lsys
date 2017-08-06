import numpy
from matplotlib import pyplot

import pytest

import lsys
from .. import viz
from .. import algo

BASELINE_DIR = 'baseline_images/test_viz'
TOLERANCE = 15

plotData = numpy.array([
    3.113,   3.606,   4.046,   4.046,   4.710,   6.140,   6.978,
    2.000,   4.200,   4.620,   5.570,   5.660,   5.860,   6.650,
    6.780,   6.790,   7.500,   7.500,   7.500,   8.630,   8.710,
    8.990,   9.850,   10.820,  11.250,  11.250,  12.200,  14.920,
    16.770,  17.810,  19.160,  19.190,  19.640,  20.180,  22.970,
])


@pytest.mark.parametrize(
    ('xlim', 'ylim', 'expected' ), [
    ( [6, 12], [-12, 10], ([-2, 20], [-12, 10]) ),
    ( [30, 60],[-5, 10], ([30, 60], [-12.5, 17.5]) )
    ])
def test_square_aspect(xlim, ylim, expected):
    result = viz.square_aspect(xlim, ylim)
    assert result == expected


@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR, tolerance=TOLERANCE)
def test_square_aspect2():
    numpy.random.seed(42)
    y = plotData
    x = numpy.random.uniform(-1, 1, size=len(y)) * 5

    x0, x1 = numpy.min(x), numpy.max(x)
    y0, y1 = numpy.min(y), numpy.max(y)
    xlim, ylim = viz.square_aspect([x0, x1], [y0, y1])

    fig, ax = pyplot.subplots(figsize=(4,4))
    _ = viz.plot(x, y, ax=ax, color='b', marker='o', linestyle="", square=True)

    return fig


@pytest.mark.parametrize('seq',
    [
        ['red', 'green', 'blue'],
        ['red', 'green', 'blue', 'blue'],
        ['red', 'green', 0.33, 'green',
        'blue', .66, 'blue'],
        ['r', 'g', 'b', 'b'],
    ])
@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR,
                               tolerance=TOLERANCE,
                               remove_text=True)
def test_make_colormap_plot(seq):
    numpy.random.seed(42)
    cmap = viz.make_colormap(seq)
    fig, ax = pyplot.subplots(figsize=(3, 3), dpi=300)
    N = 1000
    array_dg = numpy.random.uniform(0, 10, size=(N, 2))
    x, y = array_dg[:, 0], array_dg[:, 1]
    colors = array_dg[:, 1]
    cax = ax.scatter(x, y, c=colors, cmap=cmap, lw=0)
    cbar = fig.colorbar(cax)
    return fig


@pytest.mark.parametrize('fractal',
    [
        ('Bush1'),
        ('Bush2'),
        ('Crosses'),
        ('Dragon'),
        ('Dragon45'),
        ('Gosper'),
        ('Hexdragon'),
        ('Hilbert'),
        ('Penrose_Snowflake'),
        ('Plant_a'),
        ('Plant_b'),
        ('Plant_c'),
        ('Plant_d'),
        ('Plant_e'),
        ('Plant_f'),
        ('Putmans_Tattoo'),
        ('QuadKochIsland'),
        ('Serpinski_Curve'),
        ('Serpinski_Gasket'),
        ('SquareSpikes'),
        ('Terdragon'),
        ('Tree1'),
        ('Tree2'),
        ('Tree3'),
        ('Twig'),
        ('Two_Ys'),
        ('Weed1'),
        ('Weed2'),
        ('Weed3'),
    ]
)
@pytest.mark.mpl_image_compare(baseline_dir=BASELINE_DIR,
                               tolerance=TOLERANCE,
                               remove_text=False,
                               savefig_kwargs={'dpi':150})
def test_plot_lsys(fractal):
    kwargs = lsys.fractals.Fractal[fractal]
    f = lsys.Lsys(**kwargs)
    f.unoise = 0
    fig, axes = pyplot.subplots(1, 4, figsize=(12, 3))
    depths = [0, 1, 2, 4]
    axes = axes.flatten()
    for ax, depth in zip(axes, depths):
        f.depth = depth
        ax = f.plot(ax=ax, square=True, color='k')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(fractal)
    pyplot.close('all')
    return fig

