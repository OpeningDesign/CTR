# -*- coding: utf-8 -*-
from __future__ import division

import math

ft2m=0.3048
in2m=0.0254
pound2N=4.45

#Geometry
floorWidth=round(22*in2m,2)
rimSpan=round(24*in2m,2)
rimHeigth=round(22*in2m,2)
floorTh=3/4.*in2m #floor thickness
rimTh=1.5*in2m #rim board thickness
botPlTh=2*in2m  #bottom plate thickness
studXdim=round(2*in2m+2*math.tan(botPlTh),2) 
#studYdim=round(6*in2m,2)
studYdim=round(3*in2m,2)

#Materials
Ewood=9.308e9  #Pa
nuWood=0.2
rhoWood=2700  #kg/m3

#Loads
pointLoad=39.2e3*rimSpan  #point load at center span (39.2 N/m * span)


xList=[0,rimSpan/2.-studXdim/2.,rimSpan/2.+studXdim/2.,rimSpan]
yList=[0,floorWidth/2.-studYdim/2.,floorWidth/2.+studYdim/2.,floorWidth]
zList=[0,rimHeigth]

eSize=0.075
