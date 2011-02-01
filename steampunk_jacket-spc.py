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

           """
           effect() is main module called in body of short program at end of this file
           this module calls modules listed above to get the work done
           """


           # reference & pattern layers
           reference_layer = self.NewLayer( 'Reference', self.document.getroot(), 'layer' )        # reference_layer = reference information
           pattern_layer    = self.NewLayer( 'Pattern',   self.document.getroot(), 'layer')        # pattern_layer = pattern lines & marks

           # document signature
           font_size    =  60
           text_space =  ( font_size * 1.1 )
           x, y = border, border
           self.WriteText( pattern_layer, x,   y,  font_size, 'company',  company_name,   no_transform )
           y = y + text_space
           self.WriteText( pattern_layer, x, y, font_size, 'pattern_number', pattern_number,  no_transform )
           y = y + text_space
           self.WriteText( pattern_layer, x, y, font_size, 'pattern_name',  pattern_name,    no_transform )
           y = y + text_space
           self.WriteText( pattern_layer, x, y, font_size, 'client',  client_name,   no_transform )
           y = y + text_space

          # pattern start, count & placement
           begin = Point( 'begin',  x,   (y + pattern_offset), 'corner',  reference_layer,  no_transform)
           #begin.DrawPoint()
           layout = Layout( 'layout',  begin.x,  begin.y,  reference_layer)
           pattern_start = Point('pattern_start', begin.x, begin.y,  'corner', reference_layer,  no_transform)

           # Jacket Back
           jacket = Pattern('jacket',  self.NewLayer('Jacket',  pattern_layer,  'layer') )
           jacket.back = PatternPiece('jacket.back', self.NewLayer('Jacket_Back',  jacket.layer,  'layer') )
           jb = jacket.back
           jb.id  = 'jacket.back'
           jb.letter = 'A'
           jb.fabric  = 2
           jb.interfacing = 0
           jb.lining = 0
           jb.start = pattern_start
           jb.width = max(back_shoulder_width, back_chest_width, back_waist_width, back_hip_width) + (2*seam_allowance) + (3*cm_to_pt)  # 3cm ease assumed
           jb.height = back_neck_length + back_jacket_length + hem_allowance + (2*seam_allowance) + (3*cm_to_pt) #3cm ease assumed
           jb.transform  = 'translate(' + str(pattern_start.x) +', '+ str(pattern_start.y) + ' )'
           jb.seam.center = Generic()
           jb.seam.side = Generic()
           jb.seam.shoulder = Generic()
           jb.seam.neck = Generic()
           jb.seam.armhole = Generic()
           jb.seam.hem = Generic()

           # reference back center seam points for nape, shoulder, chest, waist, hip, hem
           jb.nape = Point('jacket.back.nape',   0,   0, 'corner',   reference_layer,  no_transform)   # start calculations from nape at 0,0
           jb.seam.center.shoulder = Point('jacket.back.seam.center.shoulder',  jb.nape.x,    jb.nape.y + back_shoulder_length, 'smooth', reference_layer,  no_transform)
           jb.seam.center.chest = Point( 'jacket.back.seam.center.chest',  jb.nape.x + (1*cm_to_pt),  jb.nape.y + back_chest_length,  'smooth', reference_layer, jb.transform  )
           jb.seam.center.waist = Point( 'jacket.back.seam.center.waist', jb.nape.x + (2.5*cm_to_pt),  jb.nape.y + back_waist_length,    'symmetric', reference_layer, jb.transform)
           jb.seam.center.hip =  Point( 'jacket.back.seam.center.hip', jb.nape.x + (2*cm_to_pt),    jb.seam.center.waist.y + back_hip_length, 'smooth', reference_layer,  jb.transform )
           jb.seam.center.hem = Point( 'jacket.back.seam.center.hem', jb.nape.x + (1.5*cm_to_pt),  back_jacket_length,   'smooth', reference_layer, jb.transform )
           jb.seam.center.hem_allowance = Point( 'jacket.back.seam.center.hem_allowance', jb.seam.center.hem.x +0, jb.seam.center.hem.y + hem_allowance, 'corner', reference_layer ,  jb.transform)

           # reference back side seam points for chest, waist, hip, hem
           jb.seam.side.chest = Point( 'jacket.back.seam.side.chest', jb.nape.x + back_shoulder_width - (1*cm_to_pt),  jb.nape.y + back_chest_length, 'smooth', reference_layer, jb.transform )
           jb.seam.side.waist = Point( 'jacket.back.seam.side.waist', jb.nape.x + back_shoulder_width - (3*cm_to_pt),  jb.nape.y + back_waist_length, 'symmetric',  reference_layer, jb.transform )
           jb.seam.side.hip = Point( 'jacket.back.seam.side.hip', jb.nape.x + back_shoulder_width - (2*cm_to_pt),  jb.seam.side.waist.y + back_hip_length, 'smooth', reference_layer, jb.transform )
           jb.seam.side.hem = Point( 'jacket.back.seam.side.hem', jb.nape.x + back_shoulder_width - (1.5*cm_to_pt),   back_jacket_length, 'smooth', reference_layer, jb.transform )
           jb.seam.side.hem_allowance = Point( 'jacket.back.seam.side.hem_allowance', jb.seam.side.hem.x, jb.seam.side.hem.y + hem_allowance, 'corner',  reference_layer, jb.transform )

           # armscye points
           jb.balance = Point( 'jacket.back.balance', jb.nape.x + back_shoulder_width,  jb.nape.y + back_balance_length, 'smooth', reference_layer,  jb.transform )
           jb.underarm = Point( 'jacket.back.underarm', jb.nape.x + back_shoulder_width, jb.nape.y + back_balance_length + abs(back_balance_length - back_chest_length)*(.48), 'smooth', reference_layer,  jb.transform )

           # diagonal shoulder line
           jb.seam.shoulder.high = Point( 'jacket.back.seam.shoulder.high', jb.nape.x + back_neck_width, jb.nape.y - back_neck_length, 'corner', reference_layer,  jb.transform )
           jb.seam.shoulder.low   = Point( 'jacket.back.seam.shoulder.low', jb.seam.center.shoulder.x + back_shoulder_width + (1*cm_to_pt), jb.seam.center.shoulder.y, 'corner', reference_layer,  jb.transform )

           # Back Vertical Reference Grid
           d = 'M '+ jb.nape.coords   + ' v ' + str( jb.height )
           self.DrawPath( reference_layer, d , 'reference' , 'Jacket Back - Center', jb.transform )
           d = 'M '+ str(jb.nape.x + back_shoulder_width) + ', ' + str(jb.nape.y) + ' v ' + str( jb.height)
           self.DrawPath( reference_layer, d , 'reference' , 'Jacket Back - Shoulder Width',   jb.transform )
           d = 'M '+ str(jb.nape.x + jb.width) + ', ' + str(jb.nape.y)       + ' v ' + str( jb.height )
           self.DrawPath( reference_layer, d , 'reference' , 'Jacket Back - Side',   jb.transform )
           d = 'M '+ jb.seam.shoulder.high.coords  +' v '+ str(back_neck_length)
           self.DrawPath( reference_layer, d, 'reference', 'Jacket Back - Neck',     jb.transform )

           # Back Horizontal Reference Grid
           d = 'M '+ jb.nape.coords  + ' h ' + str( jb.width )   # top grid line
           self.DrawPath( reference_layer, d, 'reference', 'Jacket Back - Top',  jb.transform )
           d = 'M ' + str(jb.nape.x) + ', ' + str( jb.seam.center.shoulder.y)   + ' h ' + str( jb.width ) # shoulder grid line
           self.DrawPath( reference_layer, d, 'reference', 'Jacket Back - Shoulder', jb.transform )
           d = 'M ' + str(jb.nape.x) + ', ' + str( jb.seam.center.chest.y)        + ' h ' + str( jb.width ) # chest grid line
           self.DrawPath( reference_layer, d, 'reference', 'Jacket Back - Chest',    jb.transform )
           d = 'M ' + str(jb.nape.x) + ', ' + str( jb.seam.center.waist.y)         + ' h ' + str( jb.width) # waist
           self.DrawPath( reference_layer, d, 'reference', 'Jacket Back - Waist',    jb.transform )
           d = 'M ' + str(jb.nape.x) + ', ' + str( jb.seam.center.hip.y )           + ' h ' + str( jb.width ) #hip
           self.DrawPath( reference_layer, d, 'reference', 'Jacket Back - Hip',      jb.transform )
           d = 'M ' + str(jb.nape.x) + ', ' + str( jb.seam.center.hem.y )         + ' h ' + str( jb.width ) # hem
           self.DrawPath( reference_layer, d, 'reference', 'Jacket Back - Hem',      jb.transform )
           d = 'M ' + str(jb.nape.x) + ', ' + str( jb.seam.center.hem_allowance.y )  + ' h ' + str( jb.width )# hem allowance
           self.DrawPath( reference_layer, d, 'reference', 'Jacket Back - Hem',      jb.transform )
           d = 'M ' + str(jb.nape.x) + ', ' + str(jb.nape.y + jb.height)                + ' h ' + str( jb.width )
           self.DrawPath( reference_layer, d, 'reference', 'Jacket Back - End',      jb.transform )

           # Back Center Seam line clockwise from bottom left:
           x1, y1 = self.PointwithSlope( jb.seam.center.hip.x, jb.seam.center.hip.y, jb.seam.center.hem.x, jb.seam.center.hem.y, abs( jb.seam.center.hip.y - jb.seam.center.waist.y )*(.3), 'normal' )
           c1 = Point( 'c1', x1, y1, 'control', reference_layer, jb.transform)
           c2 = Point( 'c2', jb.seam.center.waist.x,  jb.seam.center.waist.y + abs( jb.seam.center.waist.y -  jb.seam.center.hip.y   ) * (.3), 'control', reference_layer, jb.transform )
           c3 = Point( 'c3', jb.seam.center.waist.x,  jb.seam.center.waist.y - abs( jb.seam.center.waist.y - jb.seam.center.chest.y ) * (.3), 'control', reference_layer,  jb.transform )

           x1, y1 = self.PointwithSlope( jb.seam.center.chest.x, jb.seam.center.chest.y, jb.seam.center.shoulder.x, jb.seam.center.shoulder.y, abs( jb.seam.center.chest.y - jb.seam.center.waist.y )*(.3), 'normal' )
           c4 = Point( 'c4', x1, y1, 'control', reference_layer,  jb.transform )
           c5 = Point( 'c5', jb.seam.center.chest.x - abs(jb.seam.center.chest.x - jb.seam.center.shoulder.x)*(.3), jb.seam.center.chest.y - abs( jb.seam.center.chest.y - jb.seam.center.shoulder.y )*(.3), 'control', reference_layer,  jb.transform )
           c6 = Point( 'c6', jb.seam.center.shoulder.x, jb.seam.center.shoulder.y + abs( jb.seam.center.shoulder.y - jb.seam.center.chest.y )*(.3), 'control', reference_layer,  jb.transform )

           # Back Center Seam path
           jb.seam.center.path  = 'L '+ jb.seam.center.hem_allowance.coords +' L '+  jb.seam.center.hem.coords + ' L ' +  jb.seam.center.hip.coords +' C '+ c1.coords +' '+ c2.coords +' '+ jb.seam.center.waist.coords +' C '+ c3.coords +' '+ c4.coords +' '+ jb.seam.center.chest.coords +' C '+ c5.coords +' '+ c6.coords + ' '+ jb.seam.center.shoulder.coords +' L '+ jb.nape.coords

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
