######################################
### will be an own module: gp_algorithms

from datetime import datetime
import random


# basic help functions
def timestamp():
    """Return a timestamp  of the form YYYYMMDD-HHMM-SSSSSS"""
    return datetime.now().strftime('%Y%m%d-%H%M-%S%f')

# manage colors
def rgb_rand(step=3):
    return random.randrange(0, 255, step)

def rgb2hex(r,g,b):
    return ('#%02x%02x%02x' % (r, g, b)).upper()

def rgb2svg(r, g, b):
    return 'rgb({}, {}, {})'.format(r, g, b)


# algorithms to generate attributes
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

# functions are callable by dict keys
RM_FUNCTION = {'random_randint': random_randint,
               'random_randrange': random_randrange,
               'random_choice': random_choice,
               'fifo_loop': fifo_loop}    

# algorithms to mutate and combine pictures

def pic_merger(list_of_pics_figurelists):
    """Add and sort figures of  different pictures"""
    pass

def pic_shuffle(list_of_pics_figurelists):
    pass
######################################
### will be an own module: gp_elements
from math import sin, pi

def get_grid(rows, cols, start_r=0, stop_r=100, start_c=0, stop_c=100):
    height = (stop_r - start_r) / rows
    width  = (stop_c - start_c) / cols
    grid = list(zip(*[[round(height * i, 2), round(width * j, 2)]
                for i in range(rows ) for j in range(cols )]))
    return (grid[0], grid[1], round(height), round(width))

def generate_figure(controls, xmlplus = ''):
    figure = {}
    for k, algorithm in controls.items():
        figure[k] = RM_FUNCTION[algorithm['func']](*algorithm['input'])
    if figure['shape'] == 'circle' or figure['transform'] == 0:
        del figure['transform']
    else:
        figure['transform'] = transform_rotate(*[figure[k] 
              for k in ('x','y','width','height')], angle = figure['transform'])
            
    streamline_attribs(figure)   

    s = '{}="{}"'
    attrs =[]
    for k, v in figure.items():
        if not k == 'shape': 
            attrs.append(s.format(k, v))
    attrs.sort()
    return '<{} '.format(figure['shape']) + ' '.join(attrs) + ' ' + xmlplus + '/>'

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
    BASE_ATTRIBUTES    = ('shape', 'id', 'stroke', 'stroke-opacity', 'stroke-width',)
    LINE_ATTRIBUTES    = ('x1', 'x2', 'y1', 'y2',  'stroke-linecap')
    FILL_ATTRIBUTES    = ('fill', 'opacity')
    RECT_ATTRIBUTES    = ('x', 'y', 'height', 'width',  'transform')
    POLY_ATTRIBUTES    = ('points',  'transform')
    CIRC_ATTRIBUTES    = ('cx',  'cy', 'r')

    if element['shape'] == 'line':
        allowed = BASE_ATTRIBUTES + LINE_ATTRIBUTES
    elif element['shape'] == 'rect':
        allowed = BASE_ATTRIBUTES + FILL_ATTRIBUTES + RECT_ATTRIBUTES
    elif element['shape'] == 'circle':
        allowed = BASE_ATTRIBUTES + FILL_ATTRIBUTES + CIRC_ATTRIBUTES
        fit_circle(element)
    elif element['shape'] == 'polygon':
        allowed = BASE_ATTRIBUTES + FILL_ATTRIBUTES + POLY_ATTRIBUTES
        fit_polygon(element)

    element_keys = list(element.keys())
    for k in element_keys:
        if k not in allowed: del element[k]


def transform_rotate(x, y, w, h, angle= 0):
    xc = x + 0.5 * w
    yc = y + 0.5 * h
    return 'rotate(' + ', '.join((str(angle), str(xc), str(yc))) + ')'
