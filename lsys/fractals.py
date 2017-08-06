# -*- coding: utf-8 -*-

"""
These are pre-built fractal definitions as dictionaries, **kwargs
"""
Fractal = dict(
    Weed3={
        "depth": 4,
        "axiom": 'F',
        "rule": 'F = |[-F]|[+F][-F]F',
        "da": 20,
        "a0": 90,
        "ds": 1. / 3,
    },

    Tree1={
        "depth": 5,
        "axiom": 'F',
        "rule": 'F = ||[3-F][3+F]|[--F][++F]|F',
        "da": 20,
        "a0": 90,
        "ds": .5,
    },

    Tree2={
        "depth": 4,
        "axiom": 'F',
        "rule": 'F = |[5+F][7-F]-|[4+F][6-F]-|[3+F][5-F]-|F',
        "da": 8,
        "a0": 90 - 8,
        "ds": .65,
    },

    Dragon={
        "axiom": 'FX',
        "rule": 'X = X+YF+, Y = -FX-Y',
        "depth": 12,
        "a0": 90,
        "da": 90,
        "ignore": "XY"
    },

    Dragon45={
        "axiom": 'L',
        "rule": 'L = L+F+R+F+L-F-R, R = L+F+R-F-L-F-R',
        "depth": 5,
        "a0": 0,
        "da": 45,
        "ds": 1,
        "forward": 'LRF'
    },

    Terdragon={
        'axiom': 'F',
        'rule': 'F = F-F+F',
        'da': 120,
    },

    Hilbert={
        "axiom": '+RF-LFL-FR+',
        "rule": 'L = +RF-LFL-FR+, R = -LF+RFR+FL-',
        "depth": 5,
        "a0": 90,
        "da": 90,
        "ds": 1,
        "ignore": 'LR'
    },


    QuadKochIsland={
        "depth": 3,
        "axiom": 'F-F-F-F',
        "rule": 'F = F-F+F+FF-F-F+F',
        "da": 90,
        "ds": .22
    },


    SquareSpikes={
        "depth": 4,
        "axiom": 'F18-F18-F18-F',
        "rule": 'F = F17-F34+F17-F',
        "da": 5,
        "ds": .45
    },

    Gosper={
        'forward': 'ab',
        'da': 60,
        'depth': 2,
        'rule': 'a=a-b--b+a++aa+b-,b=+a-bb--b-a++a+b',
        'axiom': 'a'},

    Hexdragon={
        "depth": 6,
        "a0": 180,
        "da": 60,
        "axiom": 'F',
        "rule": 'F = F+L+F-L-F, L = L',
        "forward": 'FL'
    },

    Plant_a={
        "depth": 4,
        "a0": 90,
        "da": 25.7,
        "axiom": 'F',
        "rule": 'F = F[+F]F[-F]F',
        "unoise": 0.3
    },


    Plant_b={
        "depth": 4,
        "da": 20,
        "axiom": 'F',
        "rule": 'F = F[+F]F[-F][F]',
        "unoise": 0.4
    },


    Plant_c={
        "depth": 4,
        "da": 22.5,
        "axiom": 'F',
        "rule": 'F = FF-[-F+F+F]+[+F-F-F]',
        "unoise": 0.2
    },


    Plant_d={
        "depth": 7,
        "da": 20,
        "axiom": 'F[+X]F[-X]+X',
        "rule": 'X = F[+X]F[-X]+X,F = FF',
        "unoise": 0.3,
        "ignore": 'X'
    },


    Plant_e={
        "depth": 8,
        "a0": 90,
        "da": 30,
        "axiom": 'F[+X][-X]FX',
        "rule": 'X = F[+X][-X]FX,F = FF',
        "unoise": 0,
        "ignore": 'X',
    },

    Plant_f={
        "depth": 6,
        "a0": 70,
        "da": 25,
        "axiom": 'F-[[X]+X]+F[+FX]-X',
        "rule": 'X = F-[[X]+X]+F[+FX]-X, F = FF',
        "ds": .95,
        "unoise": 0.4,
        "ignore": 'X',
    },

    Serpinski_Gasket={
        "axiom": 'F--F--F',
        "rule": 'F=F--F--F--GG,G=GG',
        "a0": 0,
        "da": 60,
        "depth": 3,
    },

    Two_Ys={
        "axiom": '[F]4-F',
        "rule": 'F=|[+F][-F]',
        "a0": 90,
        "da": 45,
        "ds": .65,
        "depth": 5,
    },
    Big_H={
        "axiom": '[F]--F',
        "rule": 'F=|[+F][-F]',
        "a0": 90,
        "da": 90,
        "ds": .65,
        "depth": 5,
    },

    Twig={
        "axiom": 'F',
        "rule": 'F=|[-F][+F]',
        "a0": 90,
        "da": 20,
        "ds": .5,
        "depth": 7
    },

    Weed1={
        "axiom": 'F',
        "rule": 'F=F[-F]F[+F]F',
        "a0": 90,
        "da": 25,
        "ds": .333333333,
        "depth": 4
    },

    Weed2={
        "axiom": 'F',
        "rule": 'F=|[-F]|[+F]F',
        "a0": 90,
        "da": 25,
        "ds": 0.4,
        "depth": 4
    },

    Bush1={
        "axiom": 'F',
        "rule": 'F=FF+[+F-F-F]-[-F+F+F]',
        "a0": 90,
        "da": 25,
        "ds": 0.5,
        "depth": 3
    },

    Bush2={
        "axiom": 'F',
        "rule": 'F=|[+F]|[-F]+F',
        "a0": 90,
        "da": 20,
        "ds": 0.5,
        "depth": 5
    },

    Tree3={
        "axiom": 'F',
        "rule": 'F=|[--F][+F]-F',
        "a0": 90,
        "da": 20,
        "ds": 0.7,
        "depth": 7
    },

    Putmans_Tattoo={
        "axiom": '-FXF--FXF--FXF',
        "rule": 'X=[-F+FXF+F]+F-FXF-F+,F=FF',
        "a0": 0,
        "da": 60,
        "ds": 0.5,
        "depth": 4,
        "ignore": 'X'
    },

    Serpinski_Curve={
        "axiom": 'XF',
        "rule": 'X=YF+XF+Y,Y=XF-YF-X',
        "ignore": 'XY',
        "a0": 0,
        "da": 60,
        "ds": 0.5,
        "depth": 6
    },

    Crosses={
        "axiom": 'FX',
        "rule": 'X=FX+FX+FXFY-FY-,Y=+FX+FXFY-FY-FY,F=V',
        "ignore": 'XYV',
        "a0": 0,
        "da": 90,
        "ds": 0.5,
        "depth": 5
    },

    Penrose_Snowflake={
        "axiom": 'F4-F4-F4-F4-F',
        "rule": 'F=F4-F4-F10-F++F4-F',
        "a0": 0,
        "da": 18,
        "ds": 0.5,
        "depth": 3
    },
)

#    Sacred_Geometry = {
#        "axiom" : '-AAAAAA',
#        "rule" : 'A=F--F--F--F--F--F--F--F--F--F--[+++++++++++++++++++AAAAAA]',
#        "ignore" : 'A',
#        "step" : 50,
#        "a0" : 0,
#        "da" : 3,
#        "ds" : 0.5,
#        "depth" : 3
#        }

# f.draw(start = (-100,-200))

# fractals = [weed3,Tree1,Tree2,dragon,Hilbert,QuadKochIsland,SquareSpikes,
#     hexdragon,Plant_a,Plant_b,Plant_c,Plant_d,Plant_e,Plant_f]
