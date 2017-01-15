# import standard moduls
import numpy as np
import random
from random import randint, choice
import jinja2
import json
from lxml import etree
from math import *
import os

from datetime import datetime
import gzip
from itertools import product
from math import sin, cos

##########################################################
#-------------------------- CONSTANTS -------------------#
##########################################################
# supported figures
FIGURES = ('rect', 'circle', 'polygon', 'line')

#  attributes about the picture
#!!! PICTURE_ATTRIBS = ('nr_of_figures', 'pic_struct', 'figure')
#!!! KEINE GRID RANDOM CIRCLE UND SPIRAL STRUKTUREN IMPLEMNTIERT

# special attributes for different figures which position the SVG elements 
LINE_ATTRIBS =  ('x1', 'x2', 'y1', 'y2')
FIGURE_ATTRIBS = ('x', 'y', 'height', 'width')

# supported SVG 'style' attributes for figures
SVG_ATTRIBS = ('fill', 'opacity', 'stroke',
               'stroke-opacity', 'stroke-width', 'stroke-linecap')

# define the SVG pictures size, background the basic SVG jinja2 template   
PIC_ATTRIBS = {'svg_width':'21in', 'svg_height':'21in',
        'w_points':'100', 'h_points':'100',
        'fill':'white', 'opacity':'1.',
        'stroke':'goldenrod',
        'stroke_opacity':'.7', 'stroke_width':'.5'}

# The basic jinja2 template to generate the SVG picture
jinja2_template ="""<?xml version="1.0" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink/" 
    width="{{svg_width}}" height="{{svg_height}}"
viewBox="0 0 {{w_points}} {{h_points}}" version="1.2">

  <desc>Picture by J. Wendt</desc>
  <!-- START Generator PARAMETERS in Json -->
  <desc>{{gen_params}}</desc>
  <!-- END Generator PARAMETERS in Json -->

  <!-- Show outline of canvas using 'rect' element -->
  <rect id="bg-00" x="0" y="0" width="{{w_points}}" height="{{h_points}}" fill="{{fill}}"
    opacity="{{opacity}}"
  stroke="{{stroke}}" stroke-opacity="{{stroke_opacity}}" stroke-width="{{stroke_width}}"/>

</svg>
"""

#--------------------------file function------------------------------#
def timestamp():
    """Return a timestamp  of the form YYYYMMDD-HHMM-SSSSSS"""
    return datetime.now().strftime('%Y%m%d-%H%M-%S%f')

def create_output_directory(root = '', form = 'triangle'):
    directory_name = root + form + '-' + timestamp()
    os.mkdir(directory_name)
    return directory_name


def tofile(fname, content):
    """write string based content to file fname """
    with open(fname, 'wt') as f:
     f.write(content)


def fromfile(fname):
    file = open (fname,'rt')
    content = file.read()
    file.close()
    return content

#---------------------------json functions----------------------------#
def save_json(fname, params):
    f = open(fname, 'w')
    json.dump(params, f, sort_keys=True, indent=2)
    f.close()


def load_json(fname):
    f = open(fname, 'r')
    result = json.load(f)
    f.close()
    return result

#---------------------------gzip functions----------------------------#
def gzip_file(fname):
    #gzip eine datei und hänge ein z an das ende
    with open(fname , 'rb') as f_in:
        with gzip.open(fname + 'z', 'wb') as f_out:
            f_out.writelines(f_in)


def unzip_file(fname):
    with open(fname , 'rb') as f:
        content = f.read()
    return gzip.decompress(content)


def gzip_content2file(fname, content):
    with gzip.open(fname, 'wb') as f:
        f.write(content)


def zip_data(string):
    return gzip.compress(bytes(string, 'utf-8'))


def unzip(data):
    return  gzip.decompress(data).decode("utf-8")

#---------------------------Geometric functions---------------------------#
def create_triangle(x1,y1, l):
    """Create an isosceles triangle"""
    x2 = x1 + l
    y2 = y1
    x3 = x1 + l/2.
    y3 = y1 + l * sin(pi/3)
    sx = x1 + l/2.
    sy = y1 + l * sin(pi/3) / 2.
    return (x1, y1, x2, y2, x3, y3, sx, sy)

#-----------------------coordinate functions------------------------------#
def new_0_coord(pos, new_0 =(40., 55.)):
    """Transform a pos to a cartesian coordinate system with new_0 as zero point"""
    return [new_0[i] + pos[i] for i in [0, 1]]


def polar2cartesian(r, theta):
    """ Transform a polar position r, theta to a cartesian point (x, y)"""
    x = r * cos(theta)
    y = r * sin(theta)
    return (x, y)


def round_coord_2(p):
    """round a 2-dim point p to 2 digits"""
    return ( round(p[0], 2), round(p[1], 2) )

#-----------------------structurial functions------------------------------#
def spiral_points(rotations, length, nr_of_points):
    def spiral_radius_list(length,steps):
        """return al list of the radius for a spiral"""
        dr = float(length) / steps
        return [dr * i for i in range(steps)]

    def spiral_angle_list(rotations, steps):
        """return al list of the  angles for a spiral"""
        return [((rotations*2*pi)/steps) * i for i in range(steps)]

    return list(map(polar2cartesian, spiral_radius_list(length, nr_of_points),
            spiral_angle_list(rotations, nr_of_points)))


def circles(nr_of_cir, min_r, max_r, nr_of_points):
    def circle_points(r, nr_of_points):
        return  list(map(polar2cartesian, nr_of_points * [r],
            [((2* pi) / nr_of_points) * i for i in range(nr_of_points)]))

    dr = (max_r - min_r) / float(nr_of_cir)
    points =[]
    for s in range(nr_of_cir):
        points += circle_points( min_r + s * dr, nr_of_points)
    return points

#---------------------------------------------------------------------------#
def create_grid(y_steps, x_steps, y_start=0.0, y_end=100.0, x_start=0.0, x_end=100.0):
    """Create a grid to tile a picture with rectangles
    Input:
    x_steps: Number of tiles in the row
    y_steps: Number of tiles in the columns
    ?_start, ?_end: Optinal start and end points for tiling
    Output:
    l: the tiling grid wit upper left tiling start points
    width, height: the width and height of one tile """

    x = np.linspace(x_start, x_end, x_steps +1)
    y = np.linspace(y_start, y_end, y_steps + 1)
    l = [(round(e[0], 3), round(e[1], 3)) for e in  product(x[:-1], y[:-1])]
    width = (x_end - x_start) / x_steps
    height = (y_end - y_start) / y_steps
    return l, width, height


def get_random_border_point(start_x=0, end_x=100, start_y=0, end_y=100):
    """return a Point which lays on the border of the picture
    Used to create parallel lines"""
    fixed_side = choice(('x', 'y'))
    if fixed_side == 'x':
        fixed_num = choice((start_x, end_x))
        var = randint(start_y, end_y)
        return(fixed_num, var)
    elif fixed_side == 'y':
        fixed_num = choice((start_y, end_y))
        var = randint(start_x, end_x)
        return(var, fixed_num)


#-------------------------- FUNCTIONS -------------------#
# functions to create attributte values are callable by dict keys 
def fifo_func(values):
    return values.pop(0)


def svg_rotate(x, y, w, h,  values=('rc', ((0,90), ))):
        r = RM_FUNCTION[values[0]](*values[1])
        xc = x + 0.5 * w
        yc = y + 0.5 * h
        return 'rotate(' + ', '.join((str(r), str(xc), str(yc))) + ')'


# functions are callable by dict keys
RM_FUNCTION = {'ri': random.randint,
               'rr': random.randrange,
               'rc': random.choice,
#              'ro': svg_rotate,
               'ar': fifo_func}


def get_palette(palette_id):
    palettes =  load_json('color-palettes.data',)
    return palettes[str(palette_id)]



class Figure(object):
    """ Figure creates SVG elements for the picture like rectangle, circle, triangle or lines """

    def __init__(self, figure, params):
        self.figure = figure
        if self.figure == 'line':
            self.mandatory_attribs = LINE_ATTRIBS
        else:
            self.mandatory_attribs = FIGURE_ATTRIBS
        self.params = params
        self.attribs = {}
        self.checked = self.set_and_check_mandatory_attributes()
        self.set_attributes()

    def set_and_check_mandatory_attributes(self):
        if not self.figure in FIGURES:
            return False
        ok = True
        for attr in self.mandatory_attribs:
            if not attr in self.params:
                ok = False
                print (self.figure, attr, ':\tnot defined.')
                break
        return ok

    def set_attributes(self):
        """The random/algorithm based SVG attributes creation is done here"""
        for attr in self.params:
            if (attr in self.mandatory_attribs) or (attr in SVG_ATTRIBS):
                v = self.params[attr]
                self.attribs[attr] = RM_FUNCTION[v[0]](*v[1])
        if 'transform' in self.params and not self.figure == 'line':
            self.attribs['transform'] = svg_rotate(\
                *[self.attribs[k] for k in ('x','y','width','height')],
                values = self.params['transform'])

    def attribs_to_string(self):
        return {k: str(v) for k, v in self.attribs.items()}


class SVGPicture(object):
    """SVGPicture creates the SVG Picture. Iz is the hull for the figures created
by the class Figure"""

    def __init__(self, params, pic_attribs=PIC_ATTRIBS):
        self.pic_attribs = pic_attribs
        self.params = params
        self.create_picture()


    def set_svg_root(self, template_id=4):
        #load the SVG-template to jinja2
        template = jinja2.Template(jinja2_template)
        self.pic_attribs['gen_params'] = self.params_to_json()
        svg_base = template.render(self.pic_attribs)
        # Create a basic SVG/XML root
        self.root = etree.fromstring(svg_base)


    def create_picture(self):
        self.set_svg_root()
        #for fig in self.params["figures"]:
        for i in range(self.params["nr_of_figures"]):
            f = self.params['figures']
            figure = RM_FUNCTION[f[0]](*f[1])
            self.root.append(etree.Element(figure,
                    attrib= Figure(figure, self.params).attribs_to_string()))
        self.fit_svg_circles()
        self.fit_svg_polygons()


    def set_svg_root(self, template_id=4):
        #load the SVG-template to jinja2
        template = jinja2.Template(jinja2_template)
        self.pic_attribs['gen_params'] = self.params_to_json()
        svg_base = template.render(self.pic_attribs)
        # Create a basic SVG/XML root
        self.root = etree.fromstring(svg_base)


    def add_figures(self, figures):
        for fig in figures:
            self.root.append(etree.Element(fig,
                    attrib= Figure(fig, self.params).attributes_to_str()))
        self.fit_svg_circles()
        self.fit_svg_polygons()
        self.new_image = True


    def fit_svg_circles(self):
        elem_circles = self.root.findall('circle')
        for e in elem_circles:
            e.attrib['r'] = "{:0.2f}".format(max(float(e.attrib['height']),
                                                 float(e.attrib['width'])) / 2)
            e.attrib['cx'] = "{:0.2f}".format(float(e.attrib['x']) + float(e.attrib['r']))
            e.attrib['cy'] = "{:0.2f}".format(float(e.attrib['y']) + float(e.attrib['r']))
            etree.strip_attributes(e, 'x', 'y', 'width', 'height', 'transform')


    def fit_svg_polygons(self):
        elem_polygons = self.root.findall('polygon')
        for e in elem_polygons:
            e.attrib['width'] = e.attrib['height']
            t = create_triangle(float(e.attrib['x']), float(e.attrib['y']) ,
                                max(float(e.attrib['height']), float(e.attrib['width'])))
            e.attrib['points'] = "{:0.2f},{:0.2f} {:0.2f},{:0.2f} {:0.2f},{:0.2f}".\
            format(*t[:-2])
            etree.strip_attributes(e, 'x', 'y', 'width', 'height')


    def add_id_to_svg_elems(self):
        def idplus1_func(a):
            return a + 1
        tags = ('rect', 'cirlce', 'polygon', 'line')
        c = [e for e in self.root.getchildren() if e.tag in tags]
        self.add_tag_to_elements('id', id1_func, c)


    def add_figures(self, figures):
        for fig in figures:
            self.root.append(etree.Element(fig,
                    attrib= Figure(fig, self.params).attributes_to_str()))
        self.fit_svg_circles()
        self.fit_svg_polygons()


    def add_tag_to_svg_elems(self, tag, valfunc, elements):
        for i, e in enumerate(elements):
            e.attrib[tag] = str(valfunc(i))


    def copyright_to_xml(self):
        # append a copyriht information to the SVG output. Set x,y position etc.. 
        copyright = etree.SubElement(self.root, "text")
        copyright.text = "© d-j-w, Hamburg 2016 - " + timestamp()
        copyright.attrib['x'] = "1"
        copyright.attrib['y'] = "99"
        copyright.attrib['fill'] = "silver"
        copyright.attrib['style'] = "font-size:0.5mm"


    def xml_to_string(self):
        # convert the SVG/XML root to a string  
        return '<?xml version="1.0" standalone="no"?>\n' + \
            etree.tostring(self.root).decode('utf-8').replace('><', '>\n<')


    def params_to_json(self):
        # This has to be done  if the params changed BEFORE THE IMAGE IS STORED
        const_attrs = {}
        const_attrs['params'] = {k:v for k,v in self.params.items() if
                               (not type(v) == tuple) or not v[0] == 'ar' }
        return json.dumps(const_attrs, separators=(',', ':'))


    def to_file(self, directory='svg', zip=True):
        #store image into a file
        root = os.path.join(os.getcwd(), directory)
        if zip:
            f = open(os.path.join(root,'pic-' + timestamp() + '.svgz'), 'wb')
            f.write(zip_data(self.xml_to_string()))
        else:
            f = open(os.path.join(root,'pic-' + timestamp() + '.svg'), 'wt')
            f.write(self.xml_to_string())
        f.close()
        print(timestamp())

