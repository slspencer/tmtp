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



           # Back Neck seam line clockwise from jb.nape to high point of shoulder:
           x1, y1       = self.PointwithSlope( jb.seam.shoulder.high.x, jb.seam.shoulder.high.y, jb.seam.shoulder.low.x, jb.seam.shoulder.low.y, (abs( jb.seam.shoulder.high.y - jb.nape.y )*(.75)), 'perpendicular')
           c1 = Point( 'c1_!', x1, y1, 'control', reference_layer,  jb.transform) #c1 is perpendicular to shoulder line at jb.seam.shoulder.high.

           x1, y1       = self.PointwithSlope( jb.nape.x, jb.nape.y, jb.seam.shoulder.high.x, jb.nape.y, ( -(abs( jb.seam.shoulder.high.x - jb.nape.x ) ) * (.50) ), 'normal')
           c2 = Point( 'c2_!', x1, y1, 'control', reference_layer, jb.transform)

           # Back Neck Seam path - starts with 'jacket.back.nape' from Back_Center_Seam
           jb.seam.neck.path = 'M ' + jb.nape.coords + ' C '+ c2.coords +' '+ c1.coords +' '+ jb.seam.shoulder.high.coords

           # Back Shoulder & Armhole seam lines clockwise from high point to low point of shoulder to top of side seam
           c1   = Point( 'c1_@', jb.seam.shoulder.high.x + (abs( jb.seam.shoulder.low.x - jb.seam.shoulder.high.x )*(.33)), jb.seam.shoulder.high.y + (abs( jb.seam.shoulder.low.y - jb.seam.shoulder.high.y )*(.4)),  'control', reference_layer,  jb.transform )
           c2   = Point( 'c2_@', jb.seam.shoulder.high.x + (abs( jb.seam.shoulder.low.x - jb.seam.shoulder.high.x )*(.6) ), jb.seam.shoulder.high.y + (abs( jb.seam.shoulder.low.y - jb.seam.shoulder.high.y )*(.66)), 'control', reference_layer,   jb.transform )

           # Back Shoulder Seam path - starts with 'jacket.back.seam.shoulder.high.coords' from Back_Neck_Seam
           jb.seam.shoulder.path = ' C '+ c1.coords +' '+ c2.coords +' '+ jb.seam.shoulder.low.coords
           jb.seam.armhole.path  = ' Q ' + jb.balance.coords + ' ' + jb.underarm.coords

           # Back Side seam line clockwise from jb.underarm. to hem
           x1, y1 = self.PointwithSlope( jb.seam.side.chest.x, jb.seam.side.chest.y, jb.underarm.x, jb.underarm.y, abs(jb.seam.center.chest.y - jb.seam.side.waist.y) * (.3) , 'normal')
           c1 = Point( 'c1_*' , x1, y1, 'control' , reference_layer,  jb.transform)

           c2 = Point( 'c2_*', jb.seam.side.waist.x, jb.seam.side.waist.y - (abs( jb.seam.side.waist.y - jb.seam.side.chest.y )*(.3)), 'control', reference_layer,  jb.transform )
           c3 = Point( 'c3_*', jb.seam.side.waist.x, jb.seam.side.waist.y + (abs( jb.seam.side.waist.y - jb.seam.side.hip.y )*(.3)),   'control', reference_layer,  jb.transform )

           x1, y1  = self.PointwithSlope( jb.seam.side.hip.x, jb.seam.side.hip.y, jb.seam.side.hem.x, jb.seam.side.hem.y, (abs(jb.seam.side.waist.y - jb.seam.side.hip.y)*(.3)), 'normal')
           c4 = Point( 'c4_*', x1, y1, 'control', reference_layer,  jb.transform )

           # Back Side Seam path -- starts with 'jacket.back.underarm.' from Back_Shoulder_Armhole_Seam
           jb.seam.side.path  = ' L '+ jb.seam.side.chest.coords +' C '+ c1.coords + ' '+ c2.coords +' '+ jb.seam.side.waist.coords +' C '+ c3.coords +' '+ c4.coords +' '+ jb.seam.side.hip.coords +' L '+ jb.seam.side.hem.coords + ' ' + jb.seam.side.hem_allowance.coords

           # Back Hemline path
           jb.seam.hem.path = 'M ' +  jb.seam.center.hem.coords + ' L ' + jb.seam.side.hem.coords

           # Grainline
           g1 = Point( 'g1', (jb.seam.shoulder.low.x)/2, jb.underarm.y, 'grainline', reference_layer,  jb.transform )
           g2 = Point( 'g2', g1.x, g1.y + (60*cm_to_pt), 'grainline', reference_layer,  jb.transform )
           jb.grainline = Generic()   #not in use at this time
           jb.grainline.path = 'M '+ g1.coords + ' L ' + g2.coords # not in use at this time

           # Jacket Back Pattern path
           jb.path = jb.seam.neck.path +' '+ jb.seam.shoulder.path + ' '+ jb.seam.armhole.path +' '+ jb.seam.side.path + ' ' + jb.seam.center.path +' z'

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
