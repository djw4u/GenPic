# GenPic - under heavy construction
## actually documentation and coding not synched.
## Be patient or contect the project owner


GenPic is a collection of IPython notebooks to generate SVG images and manage them.

You can create impressive digital art pictures using only:

   + SVG
   + Python >3.4 and IPython - easy to install with
     [Anaconda](https://www.continuum.io/downloads).

Choose how to store the generated pictures and data

   + In local files 
   + Or for more sophisticated use in a database
      (SQLite is used as an example via SQLAlchemy wrapper).


## A short overview of the files of the project

### The IPytohn notebooks (ipynb)

1. *GPGH01-Show-Palettes* visualizes the color palettes of the file *color-palettes.data*.

2. *GPGH02-Picture-Generator*  generates SVG pictures using parameters to control:
   
   * The picture style and structure.
   * The form ,color, position and size of the picture elements.

2. *GPGH03-Images-to-HTML* generates HTML based cataloges to navigate through
   picture galeries by a webbrowser. 

2. *GPGH04-Manipulate-Images* manipulates existing pictures to create new ones.

### The Data and SVG files

1.  *color-palettes.data* provides nice color palettes in an Json format.
2.  

Visit the website of [GenPic](http://djw4u.github.io/GenPic/)
