# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
import csv
from dxfwrite import DXFEngine as dxf
import xc_base
import geom

csvFile= open('footings_geometry.csv')
reader= csv.reader(csvFile)
drawing = dxf.drawing('footings.dxf')
drawing.add_layer('footings')
drawing.add_layer('columns')
drawing.add_layer('footings_text')

b= 16*2.54/100.0 #column dimensions.
c= 16*2.54/100.0

offset= 0.25

for row in reader:
    id= row[0]
    center= geom.Pos2d(float(row[2]),float(row[3]))
    thickness= float(row[5])
    drawing.add(dxf.text(id,(center.x+offset,center.y+offset), height= 0.2, color=5, layer='footings_text'))
    B= float(row[6])
    BxL_text_metric= 'BxL(m)= '+ "{0:.2f}".format(B) + 'x' + "{0:.2f}".format(B)
    text_metric=  BxL_text_metric + ' x T(m)= ' + str(thickness)
    drawing.add(dxf.text(text_metric,(center.x+offset,center.y-0.25), height= 0.1, color=5, layer='footings_text'))
    BxL_text_us= 'BxL(feet)= '+ "{0:.1f}".format(B*3.28084) + 'x' + "{0:.1f}".format(B*3.28084)
    text_us=  BxL_text_us + ' x T(inches)= ' + str(thickness*100.0/2.54)
    drawing.add(dxf.text(text_us,(center.x+offset,center.y-0.5), height= 0.1, color=5, layer='footings_text'))
    drawing.add(dxf.point((center.x, center.y), color=7, layer='footings'))
    pointA= center+geom.Vector2d(-B/2.0,-B/2.0)
    pointB= center+geom.Vector2d(B/2.0,-B/2.0)
    pointC= center+geom.Vector2d(B/2.0,B/2.0)
    pointD= center+geom.Vector2d(-B/2.0,B/2.0)
    face3d= [(pointA.x,pointA.y),(pointB.x,pointB.y),(pointC.x,pointC.y),(pointD.x,pointD.y)]
    drawing.add(dxf.face3d(face3d, color=7, layer='footings'))
    pointA= center+geom.Vector2d(-b/2.0,-c/2.0)
    pointB= center+geom.Vector2d(b/2.0,-c/2.0)
    pointC= center+geom.Vector2d(b/2.0,c/2.0)
    pointD= center+geom.Vector2d(-b/2.0,c/2.0)
    face3d= [(pointA.x,pointA.y),(pointB.x,pointB.y),(pointC.x,pointC.y),(pointD.x,pointD.y)]
    drawing.add(dxf.face3d(face3d, color=1, layer='columns'))
   
drawing.save()
