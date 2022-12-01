# `lsys`

Create and visualize lindenmayer systems.


## Getting Started

`lsys` is a library for creating Lindenmayer systems inspired by Flake's **The Computational Beauty of Nature**.
The graphics in that book are extraordinary, and this little tool helps make similar graphics with matplotlib.

From the text, an L-system consists of a special seed, an axiom, from which the fractal growth follows according to certain production rules.
For example, if 'F' is move foward and "+-" are left and right, we can make the well-known Dragon curve using the following axiom and production rules:



```python
import matplotlib.pyplot as plt

import lsys
from lsys import Lsys, Fractal


axiom = "FX"
rule = {"X": "X+YF+", "Y": "-FX-Y"}

dragon = Lsys(axiom=axiom, rule=rule, ignore="XY")

for depth in range(4):
    dragon.depth = depth
    print(depth, dragon.string)

```

    0 FX
    1 FX+YF+
    2 FX+YF++-FX-YF+
    3 FX+YF++-FX-YF++-FX+YF+--FX-YF+
    

Note how the production rules expand on the axiom, expanding it at each depth according to the characters in the string.
If we interpret the string as a turtle graphics instruction set and move forward each time we see 'F' and left or right each time we see '-' or '+' we can visualize the curve.



```python
dragon.depth = 3
_ = dragon.plot(lw=5)
```


    
![png](readme_files/readme_4_0.png)
    



```python
dragon.depth = 12
_ = dragon.plot(lw=1)
```


    
![png](readme_files/readme_5_0.png)
    


The `Lsys` object exposes multiple options for interacting with the results of the L-system expansion, including the xy coordinates, depths of each segment, and even functions for forming bezier curves to transition between vertices of the fractal.
This allows for easier visulaization of the path that the fractal takes when the vertices of the expansion start to overlap.
For the Dragon curve, this can lead to some satisfying results.



```python
dragon.depth = 4

fig, axes = plt.subplots(1, 2, figsize=(6, 3))

_ = dragon.plot(ax=axes[0], lw=5, c="k", square=True)
_ = dragon.plot(ax=axes[1], lw=5, square=True, as_bezier=True)

```


    
![png](readme_files/readme_7_0.png)
    



```python
dragon.depth = 12
_ = dragon.plot(lw=1, as_bezier=True)
```


    
![png](readme_files/readme_8_0.png)
    


It's also possible to use a colormap to show the path.
The most efficient way to do this in `matplotlib` uses the `PathCollection` with each segment as a cubic bezier curve.
By default, the curves are approximately circular, but the weight of the control points can be adjusted.



```python
dragon.depth = 4
fig, axes = plt.subplots(1, 4, figsize=(12, 5))

for ax, weight in zip(axes, [0.3, None, 0.8, 1.5]):
    _ = dragon.plot_bezier(ax=ax, bezier_weight=weight, lw=3, square=True)
```


    
![png](readme_files/readme_10_0.png)
    


The bezier functionality also allows for applying a color map, which is useful for uncovering how the path unfolds, especially for large depths of the fractal



```python
fig, axes = plt.subplots(1, 2, figsize=(6, 3))

for ax, depth in zip(axes, [4, 13]):
    dragon.depth = depth
    _ = dragon.plot_bezier(ax=ax, lw=1.5, square=True, cmap="viridis")
```


    
![png](readme_files/readme_12_0.png)
    



```python
hilbert = Lsys(**Fractal["Hilbert"])
fig, axes = plt.subplots(1, 2, figsize=(6, 3))

for ax, depth in zip(axes, [2, 7]):
    hilbert.depth = depth
    _ = hilbert.plot_bezier(ax=ax, lw=1, square=True, cmap="viridis")
```


    
![png](readme_files/readme_13_0.png)
    


The plotting features allow for a fast and deep rendering, as well as a slower rendering algorithm that allows the user to choose the number of bezier segments per segment in the line collection.
This feature allows for either high fidelity (many segments) color rendering of the smooth bezier path, or low fidelity



```python
dragon.depth = 4

fig, axes = plt.subplots(1, 5, figsize=(15, 3))

# Default renderer for bezier, peak bezier rendering performance for colormapped renderings, noticably
# low color fidelity per curve at low fractal depths
_ = dragon.plot_bezier(ax=axes[0], lw=10, square=True, cmap="magma")

# line collection with custom n-segments, slower rendering due to many lines, customizably
# high or low color fidelity per curve
_ = dragon.plot_bezier(ax=axes[1], lw=10, square=True, cmap="magma", segs=10, as_lc=True)
_ = dragon.plot_bezier(ax=axes[2], lw=10, square=True, cmap="magma", segs=1, as_lc=True)

# High rendering performance, but rendered as single path with a single color.
# This is the default render if `segs` is not None and `as_lc` is not set True (default is False)
_ = dragon.plot_bezier(ax=axes[3], lw=10, square=True, segs=10, c="C2")
_ = dragon.plot_bezier(ax=axes[4], lw=10, square=True, segs=1, c="C0")
```


    
![png](readme_files/readme_15_0.png)
    


## Exploring Other Fractals



```python
Serpinski_Maze = {
    "name": "Serpinski Maze",
    "axiom": "F",
    "rule": "F=[-G+++F][-G+F][GG--F],G=GG",
    "da": 60,
    "a0": 0,
    "ds": 0.5,
    "depth": 4,
}

_ = Lsys(**Serpinski_Maze).plot()

```


    
![png](readme_files/readme_17_0.png)
    



```python
def build_computational_beauty_of_nature_plot(lsystem: Lsys, depths=None, **fig_kwargs):

    if depths is None:
        depths = [0, 1, 4]

    assert len(depths) == 3, "`depths` must be length 3"

    fig_kwargs_default = dict(
        figsize=(9, 3.5),
        gridspec_kw={"wspace": 0, "hspace": 0.01, "height_ratios": [1, 10]},
    )

    fig_kwargs_default.update(fig_kwargs)

    lsystem.depth = depths[-1]
    xlim, ylim = lsys.viz.get_coord_lims(lsystem.coords, pad=5, square=True)

    fig, axes = plt.subplot_mosaic([[1, 1, 1], [2, 3, 4]], **fig_kwargs_default)

    for i, (l, ax) in enumerate(axes.items()):
        ax.set_xticks([])
        ax.set_yticks([])

    plot_text = (
        f"{lsystem.name}  "
        r"$\bf{Angle:}$ "
        f"{lsystem.da}   "
        r"$\bf{Axiom:}$ "
        r"$\it{" + lsystem.axiom + "}$   "
        r"$\bf{Rule(s):}$ "
        r"$\it{" + lsystem.rule + "}$   "
    )

    axes[1].text(
        0.01,
        0.5,
        plot_text,
        math_fontfamily="dejavuserif",
        fontfamily="serif",
        va="center",
        size=8,
    )

    plot_axes = [axes[i] for i in [2, 3, 4]]

    for ax, depth in zip(plot_axes, depths):
        lsystem.depth = depth
        lsystem.plot(ax=ax, lw=0.5, c="k")

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        _ = ax.set_aspect("equal")

    return fig, axes
```


```python
_ = build_computational_beauty_of_nature_plot(
    lsystem=Lsys(**Serpinski_Maze),
    depths=[0, 1, 7],
)
```


    
![png](readme_files/readme_19_0.png)
    


## Additional Rendering Options


The `lsys` library has a few rendering helpers, like one to build up custom color maps.
Here is one of my favorites:



```python
dragon.depth = 6
cmap = lsys.viz.make_colormap(
    [
        "midnightblue",
        "blue",
        "cyan",
        "lawngreen",
        "yellow",
        "orange",
        "red",
        "firebrick",
    ]
)
_ = dragon.plot(lw=5, square=True, as_lc=True, cmap=cmap)
```


    
![png](readme_files/readme_22_0.png)
    


This colormap helper can also assist with non-hideous abuses of colormaps, like when rendering a tree-like fractal.


```python
Fractal["Tree2"]
```




    {'depth': 4,
     'axiom': 'F',
     'rule': 'F = |[5+F][7-F]-|[4+F][6-F]-|[3+F][5-F]-|F',
     'da': 8,
     'a0': 82,
     'ds': 0.65}




```python
tree = Lsys(**Fractal["Tree2"])
tree.depth = 5
_ = tree.plot(c="k", lw=0.3)
```


    
![png](readme_files/readme_25_0.png)
    


We can add some color by creating a colormap that transitions from browns to greens.


```python
cmap = lsys.viz.make_colormap(
    ["saddlebrown", "saddlebrown", "sienna", "darkgreen", "yellowgreen"]
)
_ = tree.plot(as_lc=True, cmap=cmap)
```


    
![png](readme_files/readme_27_0.png)
    


This has rendered each of our line segments in the order that the string expansion of the axiom and rules defined.
It's interesting to see when each part of the tree appears in the linear order of the string expansion, but it's not really tree-like and it's not yet 'non-hideous'.
We can do better.

The `Lsys` objects store an array of the depth of each line segment.
This depth changes when the string expansion algorithm encounters a push character ("[") or a pop character ("]"). 
Not every fractal has push and pop characters, but for those that do, the depth array can be useful for rendering.


```python
cmap = lsys.viz.make_colormap(
    ["saddlebrown", "saddlebrown", "sienna", "darkgreen", "yellowgreen"]
)
_ = tree.plot(as_lc=True, array=tree.depths, cmap=cmap)
```


    
![png](readme_files/readme_29_0.png)
    


This is somewhat closer to the intention.
Now the colors are mapped correctly to each segments fractal depth and trunk/stem segments are brown while branch and leaf segments are green.
Even still, we can do better.

If we render each depth in separate line collections and in order of depth rather than in order of the string expansion, we can improve our tree-like rendering.


```python
import numpy
from matplotlib.collections import LineCollection
```


```python
tree = Lsys(**Fractal["Tree2"])

for d in range(5):
    tree.depth=d
    print(set(tree.depths))
```

    {0}
    {1}
    {1, 2}
    {1, 2, 3}
    {1, 2, 3, 4}
    

_*Sidenote:*_ The string expansion rules for this fractal nuke the first depth (0th) on the first expansion with the "|[" character combo. 
We'll account for this when we render things.


```python
tree = Lsys(**Fractal["Tree2"])
tree.depth = 5

fig, ax = plt.subplots(figsize=(7, 7))
cmap = lsys.viz.make_colormap(
    ["saddlebrown", "saddlebrown", "sienna", "darkgreen", "yellowgreen"]
)
_ = lsys.viz.pretty_format_ax(ax=ax, coords=tree.coords)

for depth in range(tree.depth):
    # each depth will have a single value for color, lineweight, and alpha.
    color = cmap((depth + 1) / tree.depth)
    lw = 10 / (depth + 2)
    alpha = 0.5 if depth + 2 >= tree.depth else 1

    lc = LineCollection(
        tree.coords[tree.depths == (depth + 1)],
        color=color,
        lw=lw,
        alpha=alpha,
        capstyle="round",
    )

    ax.add_collection(lc)
```


    
![png](readme_files/readme_34_0.png)
    


## Rendering Sequences

It can be fun to see how each of these fractals evolve, so here are a few examples of watching how the dragon fractal 'winds' itself up.


```python
d = Lsys(**Fractal["Dragon"])
d.a0 = 0
depths = range(12)
rows = int(numpy.ceil(len(depths) / 4))
fig_width = 12
fig_height = int(fig_width / 4 * rows)
fig, axes = plt.subplots(rows, 4, figsize=(fig_width, fig_height))

for ax, depth in zip(axes.flatten(), depths):
    d.depth = depth
    ax = d.plot_bezier(ax=ax, lw=3, square=True, cmap='viridis', segs=10)
```


    
![png](readme_files/readme_36_0.png)
    


Sequences like this lend themselves nicely to creating animations.
Here's one showing another way this fractal 'winds' in on itself.
For this one to work, we've got to do some math to scale each plot and change the start angle for each depth.


```python
from matplotlib import animation
from matplotlib import rc
rc("animation", html="html5")
```


```python
d = Lsys(**Fractal["Dragon"])
# The difference between depth 0 and depth 1 shows where the sqrt(2) comes from 
# as the line shifts into a right triangle. 
d.ds = 1 / numpy.sqrt(2)  

# start with bearing to the right and find all bearings for our depths
# by adding 45 deg to the start bearing for each depth
d.a0 = 0
depths = list(range(12))
a0s = [d.a0 + 45 * i for i in depths]

fig, ax = plt.subplots(figsize=(6, 6))

# set axes lims to enclose the final wound up dragon using a helper function
# that takes the coordinates of the fractal.
d.depth = depths[-1]
d.a0 = a0s[-1]
ax = lsys.viz.pretty_format_ax(ax, coords=d.coords, pad=10, square=True)

frames = []
for i in depths:
    d.depth = i
    d.a0 = a0s[i]

    # helper function makes the bezier paths for us given the fractal 
    # coordinates and the interior angle to span with the bezier curve.
    paths = lsys.viz.construct_bezier_path_collection(
        d.coords, angle=d.da, keep_ends=True
    )

    pc = ax.add_collection(paths)

    frames.append([pc])

anim = animation.ArtistAnimation(fig, frames, blit=True, interval=500)
plt.close()
anim
```




<video width="600" height="600" controls autoplay loop>
  <source type="video/mp4" src="data:video/mp4;base64,AAAAHGZ0eXBNNFYgAAACAGlzb21pc28yYXZjMQAAAAhmcmVlAAGrJm1kYXQAAAKgBgX//5zcRem9
5tlIt5Ys2CDZI+7veDI2NCAtIGNvcmUgMTYwIC0gSC4yNjQvTVBFRy00IEFWQyBjb2RlYyAtIENv
cHlsZWZ0IDIwMDMtMjAyMCAtIGh0dHA6Ly93d3cudmlkZW9sYW4ub3JnL3gyNjQuaHRtbCAtIG9w
dGlvbnM6IGNhYmFjPTEgcmVmPTMgZGVibG9jaz0xOjA6MCBhbmFseXNlPTB4MzoweDExMyBtZT1o
ZXggc3VibWU9NyBwc3k9MSBwc3lfcmQ9MS4wMDowLjAwIG1peGVkX3JlZj0xIG1lX3JhbmdlPTE2
IGNocm9tYV9tZT0xIHRyZWxsaXM9MSA4eDhkY3Q9MSBjcW09MCBkZWFkem9uZT0yMSwxMSBmYXN0
X3Bza2lwPTEgY2hyb21hX3FwX29mZnNldD0tMiB0aHJlYWRzPTE5IGxvb2thaGVhZF90aHJlYWRz
PTMgc2xpY2VkX3RocmVhZHM9MCBucj0wIGRlY2ltYXRlPTEgaW50ZXJsYWNlZD0wIGJsdXJheV9j
b21wYXQ9MCBjb25zdHJhaW5lZF9pbnRyYT0wIGJmcmFtZXM9MyBiX3B5cmFtaWQ9MiBiX2FkYXB0
PTEgYl9iaWFzPTAgZGlyZWN0PTEgd2VpZ2h0Yj0xIG9wZW5fZ29wPTAgd2VpZ2h0cD0yIGtleWlu
dD0yNTAga2V5aW50X21pbj0yIHNjZW5lY3V0PTQwIGludHJhX3JlZnJlc2g9MCByY19sb29rYWhl
YWQ9NDAgcmM9Y3JmIG1idHJlZT0xIGNyZj0yMy4wIHFjb21wPTAuNjAgcXBtaW49MCBxcG1heD02
OSBxcHN0ZXA9NCBpcF9yYXRpbz0xLjQwIGFxPTE6MS4wMACAAAABNmWIhAAV//73ye/AputbW7W/
k89I/Cy3PsIqP25bE7TqAAADAAADAAADAo18/4QePUAtIpKbhQs5nCKRVLor9gy4cojH1UtAuV/R
1FLGcK/olgdG43dqQzjIAAADABac8OBvFbUciuWNiEGb70v/3hvnuaNgqg5nfN9yBBG6mUjo9EAA
Bx43xx/u8eqUHuMG8gLfeAAT4DHikigCmEqG8LIZIxSEAAADAAADAAADAAAPVQrvN6SqoRKKnPdp
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
AAABAAAAAExhdmY1OC4yOS4xMDA=
">
  Your browser does not support the video tag.
</video>



## Built-in L-System Fractals

Though you may definately define your L-Systems, and are encouraged to do so, there are a number of them provided by `lsys.Fractal` for convenience.


```python
fractals = sorted(Fractal.keys())
rows = len(fractals)
fig, axes = plt.subplots(rows, 4, figsize=(12, 3*rows))
depths = [0, 1, 2, 4]

for i, fractal in enumerate(fractals):
    f = Lsys(**Fractal[fractal])
    f.unoise = 0 # This is an exciting paramter that you are encouraged to explore.
    for j, (ax, depth) in enumerate(zip(axes[i].flatten(), depths)):
        f.depth = depth
        ax = f.plot(ax=ax, as_lc=True, color="k", lw=0.5, square=True)
        name=f'{fractal} [depth={depth}]' if j==0 else f'depth={depth}'
        ax.set_title(name)
```


    
![png](readme_files/readme_41_0.png)
    



```python

```
