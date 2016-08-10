######################################
### will be an own module: gp_algorithms

import random

#algorithms to generate attributes
def random_choice(values):
    return random.choice(values)

def random_randint(values):
    return random.randint(*values)

def random_randrange(values):
    return random.randrange(*values)

def random_sample(values):
    return random.sample(*values)

def fifo_loop(seq):
        result = seq.pop(0)
        seq.append(result)
        return result

#algorithms to mutate and combine pictures

def pic_merger(list_of_pics_figurelists):
    """Add and sort figures of  different pictures"""
    pass

def pic_shuffle(list_of_pics_figurelists):
    pass
######################################
### will be an own module: gp_elements
from math import sin, pi


def generate_figure(controls, xmlplus = ''):
    figure = {}
    for k, algorithm in controls.items():
        figure[k] = getattr(attr_funcs, algorithm['func'])(*algorithm['params'])
    if k == 'transform':
        if figure['figures'] == 'circle' or figure['transform'] == 0:
            del figure['transform']
        else:
            figure['transform'] = attr_funcs.transform_rotate(*[figure[k] 
                                  for k in ('x','y','width','height')], angle = figure['transform'])
            
    attr_funcs.streamline_attribs(figure)   

    s = '{}="{}"'
    attrs =[]
    for k, v in figure.items():
        if not k == 'figures': 
            attrs.append(s.format(k, v))
    attrs.sort()
    return '<{} '.format(figure['figures']) + ' '.join(attrs) + ' ' + xmlplus + '/>'

def streamline_attribs(element):
    """Delete all attributes that are not requiered"""
    def create_triangle(x1,y1, l):
        """Create an isosceles triangle"""
        x2 = x1 + l
        y2 = y1
        x3 = x1 + l/2.
        y3 = y1 + l * sin(pi/3)
        return (x1, y1, x2, y2, x3, y3)

    def fit_circle(elem):
        elem['r'] =  (elem['height'])
        elem['cx'] = "{:0.2f}".format(elem['x'] + elem['r'])
        elem['cy'] =  "{:0.2f}".format(elem['y'] + elem['r'])

    def fit_polygon(elem):
        t = create_triangle(elem['x'], elem['y'], elem['height'])
        elem['points'] = "{:0.2f},{:0.2f} {:0.2f},{:0.2f} {:0.2f},{:0.2f}".\
        format(*t)

    #allowed svg attributes
    BASE_ATTRIBUTES    = ('figures', 'id', 'stroke', 'stroke-opacity', 'stroke-width',)
    LINE_ATTRIBUTES    = ('x1', 'x2', 'y1', 'y2',  'stroke-linecap')
    FILL_ATTRIBUTES    = ('fill', 'opacity')
    RECT_ATTRIBUTES    = ('x', 'y', 'height', 'width',  'transform')
    POLY_ATTRIBUTES    = ('points',  'transform')
    CIRC_ATTRIBUTES    = ('cx',  'cy', 'r')

    if element['figures'] == 'line':
        allowed = BASE_ATTRIBUTES + LINE_ATTRIBUTES
    elif element['figures'] == 'rect':
        allowed = BASE_ATTRIBUTES + FILL_ATTRIBUTES + RECT_ATTRIBUTES
    elif element['figures'] == 'circle':
        allowed = BASE_ATTRIBUTES + FILL_ATTRIBUTES + CIRC_ATTRIBUTES
        fit_circle(element)
    elif element['figures'] == 'polygon':
        allowed = BASE_ATTRIBUTES + FILL_ATTRIBUTES + POLY_ATTRIBUTES
        fit_polygon(element)

    element_keys = list(element.keys())
    for k in element_keys:
        if k not in allowed: del element[k]


def transform_rotate(x, y, w, h, angle= 0):
    xc = x + 0.5 * w
    yc = y + 0.5 * h
    return 'rotate(' + ', '.join((str(angle), str(xc), str(yc))) + ')'
