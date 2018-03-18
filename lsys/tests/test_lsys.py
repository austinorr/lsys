#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_lsys
----------------------------------

Tests for `lsys` module.
"""


import pytest


from contextlib import contextmanager

import lsys


result_at_depth_2 = {
    'Bush1': 'FF+[+F-F-F]-[-F+F+F]FF+[+F-F-F]-[-F+F+F]+[+FF+[+F-F-F]-[-F+F+'
    'F]-FF+[+F-F-F]-[-F+F+F]-FF+[+F-F-F]-[-F+F+F]]-[-FF+[+F-F-F]-[-F+F+'
    'F]+FF+[+F-F-F]-[-F+F+F]+FF+[+F-F-F]-[-F+F+F]]',
    'Bush2': '1.[+2.[+F]2.[-F]+F]1.[-2.[+F]2.[-F]+F]+2.[+F]2.[-F]+F',
    'Crosses': 'VVFX+FX+FXFY-FY-+VFX+FX+FXFY-FY-+VFX+FX+FXFY-FY-V+FX+FXFY-F'
    'Y-FY-V+FX+FXFY-FY-FY-',
    'Dragon': 'FX+YF++-FX-YF+',
    'Dragon45': 'L+F+R+F+L-F-R+F+L+F+R-F-L-F-R+F+L+F+R+F+L-F-R-F-L+F+R-F-L-F-R',
    'Gosper': 'A-B--B+A++AA+B--+A-BB--B-A++A+B--+A-BB--B-A++A+B+A-B--B+A++A'
    'A+B-++A-B--B+A++AA+B-A-B--B+A++AA+B-++A-BB--B-A++A+B-',
    'Hexdragon': 'F+L+F-L-F+L+F+L+F-L-F-L-F+L+F-L-F',
    'Hilbert': '+-+RF-LFL-FR+F+-LF+RFR+FL-F-LF+RFR+FL-+F+RF-LFL-FR+-F-+-LF+'
    'RFR+FL-F-+RF-LFL-FR+F+RF-LFL-FR+-F-LF+RFR+FL-+F+-LF+RFR+FL-F-+RF-L'
    'FL-FR+F+RF-LFL-FR+-F-LF+RFR+FL-+-F-+RF-LFL-FR+F+-LF+RFR+FL-F-LF+RF'
    'R+FL-+F+RF-LFL-FR+-+',
    'Penrose_Snowflake': 'F4-F4-F10-F++F4-F4-F4-F4-F10-F++F4-F4-F4-F4-F10-F'
    '++F4-F10-F4-F4-F10-F++F4-F++F4-F4-F10-F++F4-F4-F4-F4-F10-F++F4-F4-'
    'F4-F4-F10-F++F4-F4-F4-F4-F10-F++F4-F4-F4-F4-F10-F++F4-F10-F4-F4-F1'
    '0-F++F4-F++F4-F4-F10-F++F4-F4-F4-F4-F10-F++F4-F4-F4-F4-F10-F++F4-F'
    '4-F4-F4-F10-F++F4-F4-F4-F4-F10-F++F4-F10-F4-F4-F10-F++F4-F++F4-F4-'
    'F10-F++F4-F4-F4-F4-F10-F++F4-F4-F4-F4-F10-F++F4-F4-F4-F4-F10-F++F4'
    '-F4-F4-F4-F10-F++F4-F10-F4-F4-F10-F++F4-F++F4-F4-F10-F++F4-F4-F4-F'
    '4-F10-F++F4-F4-F4-F4-F10-F++F4-F4-F4-F4-F10-F++F4-F4-F4-F4-F10-F++'
    'F4-F10-F4-F4-F10-F++F4-F++F4-F4-F10-F++F4-F4-F4-F4-F10-F++F4-F',
    'Plant_a': 'F[+F]F[-F]F[+F[+F]F[-F]F]F[+F]F[-F]F[-F[+F]F[-F]F]F[+F]F[-F'
    ']F',
    'Plant_b': 'F[+F]F[-F][F][+F[+F]F[-F][F]]F[+F]F[-F][F][-F[+F]F[-F][F]]['
    'F[+F]F[-F][F]]',
    'Plant_c': 'FF-[-F+F+F]+[+F-F-F]FF-[-F+F+F]+[+F-F-F]-[-FF-[-F+F+F]+[+F-'
    'F-F]+FF-[-F+F+F]+[+F-F-F]+FF-[-F+F+F]+[+F-F-F]]+[+FF-[-F+F+F]+[+F-'
    'F-F]-FF-[-F+F+F]+[+F-F-F]-FF-[-F+F+F]+[+F-F-F]]',
    'Plant_d': 'FFFF[+FF[+F[+X]F[-X]+X]FF[-F[+X]F[-X]+X]+F[+X]F[-X]+X]FFFF['
    '-FF[+F[+X]F[-X]+X]FF[-F[+X]F[-X]+X]+F[+X]F[-X]+X]+FF[+F[+X]F[-X]+X'
    ']FF[-F[+X]F[-X]+X]+F[+X]F[-X]+X',
    'Plant_e': 'FFFF[+FF[+F[+X][-X]FX][-F[+X][-X]FX]FFF[+X][-X]FX][-FF[+F[+'
    'X][-X]FX][-F[+X][-X]FX]FFF[+X][-X]FX]FFFFFF[+F[+X][-X]FX][-F[+X][-'
    'X]FX]FFF[+X][-X]FX',
    'Plant_f': 'FFFF-[[FF-[[F-[[X]+X]+F[+FX]-X]+F-[[X]+X]+F[+FX]-X]+FF[+FFF'
    '-[[X]+X]+F[+FX]-X]-F-[[X]+X]+F[+FX]-X]+FF-[[F-[[X]+X]+F[+FX]-X]+F-'
    '[[X]+X]+F[+FX]-X]+FF[+FFF-[[X]+X]+F[+FX]-X]-F-[[X]+X]+F[+FX]-X]+FF'
    'FF[+FFFFFF-[[F-[[X]+X]+F[+FX]-X]+F-[[X]+X]+F[+FX]-X]+FF[+FFF-[[X]+'
    'X]+F[+FX]-X]-F-[[X]+X]+F[+FX]-X]-FF-[[F-[[X]+X]+F[+FX]-X]+F-[[X]+X'
    ']+F[+FX]-X]+FF[+FFF-[[X]+X]+F[+FX]-X]-F-[[X]+X]+F[+FX]-X',
    'Putmans_Tattoo': '-FFFF[-FF+FF[-F+FXF+F]+F-FXF-F+FF+FF]+FF-FF[-F+FXF+F'
    ']+F-FXF-F+FF-FF+FFFF--FFFF[-FF+FF[-F+FXF+F]+F-FXF-F+FF+FF]+FF-FF[-'
    'F+FXF+F]+F-FXF-F+FF-FF+FFFF--FFFF[-FF+FF[-F+FXF+F]+F-FXF-F+FF+FF]+'
    'FF-FF[-F+FXF+F]+F-FXF-F+FF-FF+FFFF',
    'QuadKochIsland': 'F-F+F+FF-F-F+F-F-F+F+FF-F-F+F+F-F+F+FF-F-F+F+F-F+F+F'
    'F-F-F+FF-F+F+FF-F-F+F-F-F+F+FF-F-F+F-F-F+F+FF-F-F+F+F-F+F+FF-F-F+F'
    '-F-F+F+FF-F-F+F-F-F+F+FF-F-F+F+F-F+F+FF-F-F+F+F-F+F+FF-F-F+FF-F+F+'
    'FF-F-F+F-F-F+F+FF-F-F+F-F-F+F+FF-F-F+F+F-F+F+FF-F-F+F-F-F+F+FF-F-F'
    '+F-F-F+F+FF-F-F+F+F-F+F+FF-F-F+F+F-F+F+FF-F-F+FF-F+F+FF-F-F+F-F-F+'
    'F+FF-F-F+F-F-F+F+FF-F-F+F+F-F+F+FF-F-F+F-F-F+F+FF-F-F+F-F-F+F+FF-F'
    '-F+F+F-F+F+FF-F-F+F+F-F+F+FF-F-F+FF-F+F+FF-F-F+F-F-F+F+FF-F-F+F-F-'
    'F+F+FF-F-F+F+F-F+F+FF-F-F+F',
    'Serpinski_Curve': 'XF-YF-XF+YF+XF+YF+XF-YF-XF',
    'Serpinski_Gasket': 'F--F--F--GG--F--F--F--GG--F--F--F--GG--GGGG--F--F-'
    '-F--GG--F--F--F--GG--F--F--F--GG--GGGG--F--F--F--GG--F--F--F--GG--'
    'F--F--F--GG--GGGG',
    'SquareSpikes': 'F17-F34+F17-F17-F17-F34+F17-F34+F17-F34+F17-F17-F17-F3'
    '4+F17-F18-F17-F34+F17-F17-F17-F34+F17-F34+F17-F34+F17-F17-F17-F34+'
    'F17-F18-F17-F34+F17-F17-F17-F34+F17-F34+F17-F34+F17-F17-F17-F34+F1'
    '7-F18-F17-F34+F17-F17-F17-F34+F17-F34+F17-F34+F17-F17-F17-F34+F17-'
    'F',
    'Terdragon': 'F-F+F-F-F+F+F-F+F',
    'Tree1': '1.1.[3-2.2.[3-F][3+F]2.[--F][++F]2.F][3+2.2.[3-F][3+F]2.[--F]'
    '[++F]2.F]1.[--2.2.[3-F][3+F]2.[--F][++F]2.F][++2.2.[3-F][3+F]2.[--'
    'F][++F]2.F]1.2.2.[3-F][3+F]2.[--F][++F]2.F',
    'Tree2': '1.[5+2.[5+F][7-F]-2.[4+F][6-F]-2.[3+F][5-F]-2.F][7-2.[5+F][7-'
    'F]-2.[4+F][6-F]-2.[3+F][5-F]-2.F]-1.[4+2.[5+F][7-F]-2.[4+F][6-F]-2'
    '.[3+F][5-F]-2.F][6-2.[5+F][7-F]-2.[4+F][6-F]-2.[3+F][5-F]-2.F]-1.['
    '3+2.[5+F][7-F]-2.[4+F][6-F]-2.[3+F][5-F]-2.F][5-2.[5+F][7-F]-2.[4+'
    'F][6-F]-2.[3+F][5-F]-2.F]-1.2.[5+F][7-F]-2.[4+F][6-F]-2.[3+F][5-F]'
    '-2.F',
    'Tree3': '1.[--2.[--F][+F]-F][+2.[--F][+F]-F]-2.[--F][+F]-F',
    'Twig': '1.[-2.[-F][+F]][+2.[-F][+F]]',
    'Two_Ys': '[1.[+2.[+F][-F]][-2.[+F][-F]]]4-1.[+2.[+F][-F]][-2.[+F][-F]]',
    'Weed1': 'F[-F]F[+F]F[-F[-F]F[+F]F]F[-F]F[+F]F[+F[-F]F[+F]F]F[-F]F[+F]F',
    'Weed2': '1.[-2.[-F]2.[+F]F]1.[+2.[-F]2.[+F]F]2.[-F]2.[+F]F',
    'Weed3': '1.[-2.[-F]2.[+F][-F]F]1.[+2.[-F]2.[+F][-F]F][-2.[-F]2.[+F][-F'
    ']F]2.[-F]2.[+F][-F]F'}


@pytest.mark.parametrize(('rule', 'expected'),
                         [("X = X+YF+, Y = -FX-Y", {'X': 'X+YF+',
                                                    'Y': '-FX-Y'}),
                          ("X :   X+yF+; y => -fX-y",
                           {'X': 'X+YF+', 'Y': '-FX-Y'}),
                          ('X:FX+FX+FXFY-FY-; Y->+FX+FXFY-FY-FY, F=  V',
                             {'F': 'V', 'X': 'FX+FX+FXFY-FY-',
                              'Y': '+FX+FXFY-FY-FY'}),
                          ('F=|[+F]|[-F]+F', {'F': '|[+F]|[-F]+F'}),
                          ({'X ': ' X+YF+', ' Y': '-FX-Y '},
                           {'X': 'X+YF+', 'Y': '-FX-Y'})
                          ])
def test_clean_rule(rule, expected):

    rule_result = lsys.Lsys.clean_rule(rule)

    assert(rule_result == expected)


@pytest.mark.parametrize(('axiom', 'rule', 'depth', 'expected'),
                         [
    ("FX", {'X': 'X+YF+', 'Y': '-FX-Y'}, 3, 'FX+YF++-FX-YF++-FX+YF+--FX-YF+'),
    ("0", {'0': '010', '1': '011'}, 3, '010011010010011011010011010'),
    ('a', dict(a='a-b', b='+b-a'), 2, 'a-b-+b-a'),
    ('F', {'F': '||F'}, 2, '1.1.2.2.F'),
    ('F', {'F': '||F'}, 0, 'F'),
    ('F', {'F': '||F'}, 1, '1.1.F'),
])
def test_expand(axiom, rule, depth, expected):
    result = lsys.Lsys.expand(axiom, rule, depth)
    assert(result == expected.replace(".", "|"))


def test_expand_fractal_dict():

    fractal_dict = lsys.fractals.Fractal

    for n in ['Dragon', 'Terdragon', 'Serpinski_Gasket', 'Tree1', 'SquareSpikes', 'Plant_f']:
        f = fractal_dict[n]
        axiom = f['axiom'].upper().replace(" ", "")
        depth = 2
        rule = lsys.Lsys.clean_rule(f['rule'])

        result = lsys.Lsys.expand(axiom, rule, depth)

        assert(result == result_at_depth_2[n].replace(".", "|"))


@pytest.mark.parametrize(('rule', 'expected'),
                         [("X ; X+YF+, Y ; -FX-Y", {'X': 'X+YF+',
                                                    'Y': '-FX-Y'}),
                          ("X to X+yF+; y to -fX-y",
                           {'X': 'X+YF+', 'Y': '-FX-Y'}),
                          ('X - FX+FX+FXFY-FY-; Y - +FX+FXFY-FY-FY, F=  V',
                             {'F': 'V', 'X': 'FX+FX+FXFY-FY-',
                              'Y': '+FX+FXFY-FY-FY'}),
                          ('F is |[+F]|[-F]+F', {'F': '|[+F]|[-F]+F'}),
                          (['F', '|[+F]|[-F]+F'], {'F': '|[+F]|[-F]+F'})
                          ])
def test_raise_ValueError_clean_rule(rule, expected):
    with pytest.raises(ValueError) as e:
        rule_result = lsys.Lsys.clean_rule(rule)


def test_raise_MemoryError_process():
    dragon = lsys.fractals.Fractal['Dragon']
    axiom = dragon['axiom']
    rule = lsys.Lsys.clean_rule(dragon['rule'])
    depth = 22

    with pytest.raises(MemoryError) as e:
        string = lsys.Lsys.expand(axiom, rule, depth)


def test_Lsys_setters():
    dic = {
        "axiom": 'F',
        "rule": {'F': 'F-F+F'},
        "depth": 3,
        "a0": 90,
        "da": 120,
        "step": 1,
        "ds": 1,
        "unoise": 0,
        "forward": 'F',
        "bar": "|",
        "right": "+",
        "left": "-",
        "goto": 'G',
        "ignore": 'X',
        "memory_check": False,
    }
    d = lsys.Lsys()

    for attr, val in dic.items():
        setattr(d, attr, val)
        assert hasattr(d, attr)
        assert getattr(d, attr) == val

    props = [
        "vocab",
        "commands",
        "coords",
        "depths",
        "x",
        "y",
        "_bezier_coords",
        "_bezier_x",
        "_bezier_y",
        "string",
        "_string_stale",
        "_coord_stale",
        "_bezier_stale",
    ]

    for p in props:
        getattr(d, p)
        assert hasattr(d, p)
