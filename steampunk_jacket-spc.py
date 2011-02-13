#!/usr/bin/python
#
# Steampunk Pattern Inkscape extension
# steampunk_jacket.py
# Copyright:(C) Susan Spencer 2010
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation either version 2 of the License, or
# (at your option) any later version.





import sys, copy
import inkex
import simplestyle
import simplepath
import simpletransform
import math
import lxml
import xml

import tmtp

# define linux directory where this script and steampunk_jacket.inx are located
sys.path.append('/usr/share/inkscape/extensions')

# Define globals



class DrawJacket( inkex.Effect ):
    """
    Draw all Jacket Pieces
    """

    def effect(self):

# here is where I am copying from into mkpattern.py - I am deleting from this file as I build the other.


           # Jacket Back


           #Draw Jacket Back pattern piece on pattern layer
           self.DrawPath( jb.layer, jb.seam.hem.path, 'hemline',  'jacket.back.seam.hem.path',  jb.transform )
           self.DrawPath( jb.layer, jb.path, 'seamline',  'jacket.back.path_Seamline',  jb.transform )
           self.DrawPath( jb.layer, jb.path, 'cuttingline', 'jacket.back.path_Cuttingline',  jb.transform )
           self.Grainline( jb.layer, g1.x, g1.y, g2.x, g2.y, 'jacket.back.grainline.path',  jb.transform )
           #self.DrawGrainline( jb.layer, jb.grainline.path, 'jacket.back.grainline.path', jb.transform ) # use this after creating markers for Arrows at each end of grainline

           # Write description on pattern piece
           x, y = jb.nape.x + (5 * cm_to_pt) , jb.nape.y + back_shoulder_length
           font_size  = 50
           spacing = (font_size * .20)
           y = ( y+ font_size + spacing )
           self.WriteText( jb.layer,  x,  y,  font_size, 'company_name',   company_name,  jb.transform )
           y = ( y+ font_size + spacing )
           self.WriteText( jb.layer,  x,  y, font_size, 'pattern_number', pattern_number,  jb.transform )
           y = ( y+ font_size + spacing )
           self.WriteText( jb.layer, x,  y, font_size, 'jacket.back.letter', 'Pattern Piece '+ jb.letter,  jb.transform )
           if jb.fabric > 0:
             y = ( y+ font_size + spacing )
             self.WriteText( jb.layer, x, y, font_size, 'jacket.back.fabric', 'Cut '+str(jb.fabric)+ ' Fabric',  jb.transform )
           if jb.interfacing > 0:
             y = ( y+ font_size + spacing )
             self.WriteText( jb.interfacing, x,  y, font_size, 'jacket.back.interfacing', 'Cut '+str(jb.interfacing)+ ' Interfacing',     jb.transform )
           if jb.lining > 0:
             y = ( y+ font_size + spacing )
             self.WriteText( jb.lining, x, y, font_size, 'jacket.back.lining', 'Cut '+str(jb.fabric)+ ' Lining',     jb.transform )

           # document calculations
           jb.low.x,  jb.low.y,  jb.high.x,  jb.high.y = self.NewBoundingBox( jb.path, jb.start.x, jb.start.y )
           layout.document_low.x  = min( layout.document_low.x ,  jb.low.x  )
           layout.document_low.y  = min( layout.document_low.y ,  jb.low.y  )
           layout.document_high.x = max( layout.document_high.x, jb.high.x)
           layout.document_high.y = max( layout.document_high.y, jb.high.y )

           # document calculations
           layout.height = layout.document_high.y + border
           layout.width  = layout.document_high.x + border
           # reset document size
           self.svg_svg( str( layout.width ), str( layout.height ), str( border ) )

# my_effect is an instance of DrawJacket() - my_effect is an arbitrary name
# my_effect.affect() is a built-in function which causes my_effect to evaluate itself - e.g. initialize, execute and thus draw the pattern

my_effect = DrawJacket()
my_effect.affect()
