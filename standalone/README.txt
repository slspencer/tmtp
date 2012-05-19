tmtp

This is the standalone application for generating a sewing pattern from a design specified in a file.

There is not yet any good documentation for this (This is it).

Output format is SVG. 

Client data (measurements) are imported from a json
data file specified on the command line. 
Client data is stored in the customer directory.

Support modules for this application are in the tmtpl directory. 
Line styles are defined in a json file specified on the command line.
A set of styles is in the file tmtp_styles.json

It is a known bug in this code that prevents Nautilus from rendering a thumbnail of the file.

The output (at this time) contains both reference and pattern objects. Command line options
will be added to control this, but for now you have to edit the sample design file.


In order to generate a pattern, use the following 2 steps in command line format:

1. create the pattern
./mkpattern --tooltips --client=./customer/<client's measurements JSON file> --pattern=./patterns/<collection>/<pattern design file>  --styles=tmtp_styles.json <output file name>

Example: ./mkpattern --tooltips --client=./customer/Susancm.json --pattern=./patterns/Misc/my_jeans.py --styles=tmtp_styles.json foo.svg

2. two options, a or b. 

a. keep reference layer & outset the cutting lines:
inkscape --file=foo.svg --verb=ZoomPage --select=A.cuttingline --select=B.cuttingline --select=C.cuttingline --verb=SelectionOffset --verb=EditDeselect --verb=FileSave

b. remove reference layer & outset the cutting lines
inkscape --file=foo.svg --verb=ZoomPage --select=reference --select=tooltip --verb=EditDelete --select=A.cuttingline --select=B.cuttingline --select=C.cuttingline --verb=SelectionOffset --verb=EditDeselect --verb=FileSave

The output file (foo.svg in above examples) can be viewed with most browsers, or Inkscape with the following command line:
  With browser:  google-chrome <output file name>
  With Inkscape:  inkscape --file=<output file name>

If option 2a is used above, open the output file in an SVG-animation compatible browser to view names of the pattern points by passing the mouse pointer over the points. 



