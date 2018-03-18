# -*- coding: utf-8 -*-

import warnings
import numpy

from . import viz
from . import bezier
from . import algo


class Lsys(object):
    """
    This object combines the basic language and directives
    necessary to construct a Lindenmayer system, compute
    the coordinates based on the directives, and plot the
    resulting figure.

    Attributes
    ----------
    string :
    depth
    coord
    x
    y

    References
    ----------


    """

    def __init__(
        self,
        axiom=None,
        rule=None,
        depth=0,
        a0=90,
        da=0,
        step=1,
        ds=1,
        unoise=0,
        forward='F',
        bar="|",
        right='+',
        left='-',
        goto='G',
        ignore='',
        memory_check=True,
    ):
        """
        Parameters
        ----------




        """

        if axiom is None:
            raise Exception("must enter `axiom`")

        if rule is None:
            raise Exception("must enter `rule` string or mapping")

        self._axiom = axiom.upper()
        self._rule = self.clean_rule(rule)
        self._depth = depth
        self._a0 = a0
        self._da = da
        self._step = step
        self._ds = ds
        self._unoise = unoise
        self._forward = forward.upper()
        self._bar = bar.upper()
        self._left = left.upper()
        self._right = right.upper()
        self._goto = goto.upper()
        self._ignore = ignore.upper()
        if not isinstance(memory_check, bool):
            raise ValueError('`memory_check` must be `True` or `False`.')
        self._memory_check = memory_check

        self._vocab = self._build_vocab()
        if "." in self._vocab:
            raise Exception(
                'the "." charcter is reserved and cannot be in `vocab`.')

        self._commands = self._build_commands()
        self._coords = None
        self._depths = None
        self._x = None
        self._y = None

        self._bezier_coords = None
        self._bezier_x = None
        self._bezier_y = None
        self._string = None

        self._string_stale = True
        self._coord_stale = True
        self._bezier_stale = True

    # TODO: create __repr__ method
    def __repr__(self):
        rep = "<Lsys({})>"
        args = [
            self.axiom,
            self.rule,
            self.depth,
            self.a0,
            self.da,
            self.step,
            self.ds,
            self.unoise,
            self.forward,
            self.bar,
            self.right,
            self.left,
            self.goto,
            self.ignore,
            self.memory_check,
        ]
        _repr = []
        for arg in args:
            if isinstance(arg, str):
                _repr.append("'" + arg + "'")
            else:
                _repr.append(str(arg))

        return rep.format(", ".join(_repr))

    @property
    def axiom(self):
        return self._axiom

    @axiom.setter
    def axiom(self, value):
        self._axiom = value.upper()
        self._string_stale = True
        self._coord_stale = True

    @property
    def rule(self):
        return self._rule

    @rule.setter
    def rule(self, value):
        self._rule = clean_rule(value)
        self._string_stale = True
        self._coord_stale = True

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, value):
        self._depth = value
        self._string_stale = True
        self._coord_stale = True

    @property
    def a0(self):
        return self._a0

    @a0.setter
    def a0(self, value):
        self._a0 = value
        self._coord_stale = True

    @property
    def da(self):
        return self._da

    @da.setter
    def da(self, value):
        self._da = value
        self._coord_stale = True

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, value):
        self._step = value
        self._coord_stale = True

    @property
    def ds(self):
        return self._ds

    @ds.setter
    def ds(self, value):
        self._ds = value
        self._coord_stale = True

    @property
    def unoise(self):
        return self._unoise

    @unoise.setter
    def unoise(self, value):
        self._unoise = value
        self._coord_stale = True

    @property
    def forward(self):
        return self._forward

    @forward.setter
    def forward(self, value):
        self._forward = value.upper()
        self._coord_stale = True

    @property
    def bar(self):
        return self._bar

    @bar.setter
    def bar(self, value):
        self._bar = value.upper()
        self._coord_stale = True

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        self._left = value.upper()
        self._coord_stale = True

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value):
        self._right = value.upper()
        self._coord_stale = True

    @property
    def goto(self):
        return self._goto

    @goto.setter
    def goto(self, value):
        self._goto = value.upper()
        self._coord_stale = True

    @property
    def ignore(self):
        return self._ignore

    @ignore.setter
    def ignore(self, value):
        self._ignore = value.upper()
        self._coord_stale = True

    @property
    def memory_check(self):
        return self._memory_check

    @memory_check.setter
    def memory_check(self, value):
        if not isinstance(value, bool):
            raise ValueError('Must set `memory_check` to `True` or `False`.')
        self._memory_check = value

    @property
    def string(self):
        if not self._string or self._string_stale:
            self._string = self.expand(self.axiom, self.rule,
                                       self.depth, self.bar,
                                       self.memory_check,
                                       )
            self._string_stale = False
        return self._string

    @property
    def vocab(self):
        return self._vocab

    @property
    def commands(self):
        return self._commands

    @property
    def depths(self):
        if self._coords is None or self._coord_stale:
            self._coords, self._depths = self.compute_coords()
            self._coord_stale = False
        return self._depths

    @property
    def coords(self):
        if self._coords is None or self._coord_stale:
            self._coords, self._depths = self.compute_coords()
            self._coord_stale = False
        return self._coords

    @property
    def x(self):
        if self._x is None or self._coord_stale:
            self._x, self._y = algo.coords_to_xy(self.coords)
        return self._x

    @property
    def y(self):
        if self._y is None or self._coord_stale:
            self._x, self._y = algo.coords_to_xy(self.coords)
        return self._y

    def _build_vocab(self):
        """Compile all chars used in the vocabulary of the fractal"""
        vocab = ""
        for k, v in self.rule.items():
            vocab += k
            vocab += v
        vocab += "".join([self.axiom, self.forward, self.goto,
                          self.right, self.left, self.bar, self.ignore])

        return set(vocab.replace(" ", ""))

    def _build_commands(self):
        """Compile all chars used in the vocabulary of the fractal"""
        cmd = ""
        cmd += "".join([self.forward, self.goto,
                        self.right, self.left, self.bar])

        return set(cmd.replace(" ", ""))

    @staticmethod
    def clean_rule(rule):
        """
        Clean and validate the rule mapping.

        The defaults allow syntax conventions seen in the
        "Algorithmic Botany", "Computational Beauty of Nature", and
        "Matters Computational: Ideas, Algorithms, Source Code"

        Parameters
        ----------
        rule : string or dict
            a mapping for expanding characters of the string.
            If a string is used, the format requires a valid
            separator between key and value. These include ":",
            "=", "-->", "->", "=>". If multiple rules are provided,
            they must be separated by ";" or ",".


        Returns
        -------
        rule : dict
        """
        if isinstance(rule, dict):
            clean_rule = {}
            for k, v in rule.items():
                clean_rule[k.strip().upper()] = v.strip().upper()

            return clean_rule

        elif isinstance(rule, str):
            rule = rule.upper().replace(" ", "")

            seps = [":", "=", "-->", "->", "=>"]
            divs = [";", ","]
            clean_rule = {}

            if any(s in rule for s in seps):
                for s in seps:
                    if s in rule:
                        rule = rule.replace(s, "=")
            else:
                raise ValueError('Invalid rule syntax, use {} '
                                 'to assign rules.'.format(seps))
            for d in divs:
                if d in rule:
                    rule = rule.replace(d, ",")

            rules_tmp = rule.split(",")

            for r in rules_tmp:
                k, v = r.split("=")
                clean_rule[k.strip()] = v.strip()

            return clean_rule

        else:
            raise ValueError('`rule` must be string or mapping')

    @staticmethod
    def expand(axiom, rule, depth, bar="|", memory_check=True):
        """
        String expansion implemting `rule` on `axiom` for `depth` iterations.

        Parameters
        ----------
        axiom : string
            the starting string
        rule : dict
            the rules for expanding the characters of the string
        depth : integer
            the number of times to perform the expansion
        bar : string, optional (default = "|")
            the character to indicate that a calculation should be done
            by the parser based on the present depth of the string expansion
        memory_check : bool, optional (default = True)
            stop expanding when things get too large

        Returns:
        string : str
            the string expansion for the given depth


        """
        # if depth == 0:
        #     axiom = axiom.replace(bar, str(depth) + '.')

        i = 0
        while i <= depth:
            if memory_check and len(axiom) > 5e6:
                raise MemoryError("Maximum `depth` is: {}".format(i))
            if i == 0:
                output = axiom
            else:
                output = ''
                for c in axiom:
                    if c in rule:
                        output += rule[c]
                    else:
                        output += c
            # axiom = output.replace(bar, str(i + 1) + '.')
            # this broke tests. check CBN to see if the ds values are given.
            axiom = output.replace(bar, str(i) + '.')
            i += 1
        return axiom.replace(".", bar)

    def _compute_bezier(self, bezier_weight=None, segs=100, keep_ends=True):
        """compute
        """

        self._bezier_x, self._bezier_y = bezier.bezier_xy(self.x, self.y,
                                                          angle=self.da,
                                                          weight=bezier_weight,
                                                          segs=segs,
                                                          keep_ends=keep_ends,
                                                          )
        self._bezier_coords = algo.xy_to_coords(self._bezier_x, self._bezier_y)

        return self._bezier_x, self._bezier_y

    def compute_coords(self):
        """
        Parse the string and convert to data coordinates for rendering.

        Parameters
        ----------
        self : lsys.Lsys()
            uses most of the attributes from the class constructor
            to parse the expanded string and turn it into coordinates
            for a plotter.

        Returns
        -------
        x_y : numpy.array

        depths : numpy.array

        """
        a = numpy.radians(self.a0)
        da = numpy.radians(self.da)
        depth = self.depth
        unoise = self.unoise
        step = self.step
        ds = self.ds
        string = self.string
        forward = self.forward
        bar = self.bar
        left = self.left
        right = self.right
        goto = self.goto
        ignore = self.ignore

        # a = a0

        commands_have_digits = any([c.isdigit() for c in self.commands])

        tol = 1e-9

        x = 0
        y = 0
        sx = 0
        sy = 0

        x_y = []
        stack = []
        depths = []
        num = 0
        found = False
        for c in string:
            if c.isdigit():
                num = num * 10 + int(c)

            else:
                if c in (forward + bar + goto):

                    if c == bar:
                        pres_depth = num
                    else:
                        pres_depth = depth
                    s = step * ds**pres_depth * (algo.add_noise(unoise) + 1)

                    sy = y + numpy.sin(a + algo.add_noise(unoise)) * s
                    sx = x + numpy.cos(a + algo.add_noise(unoise)) * s

                    if c == goto:
                        x_y.append(([numpy.nan, numpy.nan],
                                    [numpy.nan, numpy.nan]))
                        depths.append(pres_depth)
                        pass

                    else:
                        ax = x if numpy.abs(x) > tol else 0
                        ay = y if numpy.abs(y) > tol else 0
                        bx = sx if numpy.abs(sx) > tol else 0
                        by = sy if numpy.abs(sy) > tol else 0
                        x_y.append(([ax, ay], [bx, by]))
                        depths.append(pres_depth)

                    x = sx
                    y = sy

                    found = True

                if c in (right + left):
                    num = num or 1
                    if c == right:
                        a -= da * num * (algo.add_noise(unoise) + 1)
                    else:
                        a += da * num * (algo.add_noise(unoise) + 1)

                elif c == '[':

                    stack.append(
                        (x, y, a + (algo.add_noise(unoise) * numpy.radians(5))))

                elif c == ']':
                    x, y, a = stack.pop()

                    x_y.append(([numpy.nan, numpy.nan],
                                [numpy.nan, numpy.nan]))

                    depths.append(pres_depth)

                elif c in ignore:
                    pass

                elif not found:
                    ignore += c
                    warnings.warn("The {} character was ignored".format(c))

                num = 0
            found = False

        assert len(x_y) == len(depths)

        return numpy.array(x_y), numpy.array(depths)

    def plot_bezier(self, bezier_weight=None, segs=100, as_lc=False,
                    pad=5, square=True, keep_ends=True, ax=None, **kwargs):

        _, _ = self._compute_bezier(
            bezier_weight=bezier_weight, segs=segs, keep_ends=keep_ends)

        if as_lc:

            return viz.plot_line_collection(self._bezier_coords,
                                            pad=pad,
                                            square=square,
                                            ax=ax,
                                            **kwargs)

        return viz.plot(self._bezier_x, self._bezier_y,
                        pad=pad, square=square, ax=ax, **kwargs)

    def plot(self, as_lc=False, pad=5, square=True, ax=None, **kwargs):
        if as_lc:
            return viz.plot_line_collection(self.coords,
                                            pad=pad,
                                            square=square,
                                            ax=ax,
                                            **kwargs)

        return viz.plot(self.x, self.y, pad=pad, square=square, ax=ax, **kwargs)
