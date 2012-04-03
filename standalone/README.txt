This is the standalone application for generating a sewing pattern from a design specified in a file.

There is not yet any good documentation for this (This is it).

Output format is SVG. Client data (measurements) are imported from a json
data file specified on the command line.

Line styles are defined in a json file specified on the command line.

There is a sample design file in this directory named SamplePattern.

Sample client data is in the file pdata.json

A set of styles is in the file tmtp_styles.json

In order to generate a pattern from the sample, use the following command line format:

./mkpattern --tooltips --client=<client's measurements JSON file> --pattern=<pattern design file>  --styles=tmtp_styles.json <output file name>

Example: ./mkpattern --tooltips --client=Susancm.json --pattern=New_Jeans2.py --styles=tmtp_styles.json foo.svg

The output can then be viewed with most browsers, or Inkscape with the following command line:
  With browser:  google-chrome <output file name>
  With Inkscape:  inkscape --file=<output file name>

It is a known bug in this code that prevents Nautilus from rendering a thumbnail of the file.

The output (at this time) contains both reference and pattern objects. Command line options
will be added to control this, but for now you have to edit the sample design file.

Support modules for this application are in the tmtpl directory.

