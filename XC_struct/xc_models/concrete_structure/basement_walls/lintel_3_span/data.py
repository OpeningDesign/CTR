# -*- coding: utf-8 -*-
from __future__ import division

import math

ft2m=0.3048
in2m=0.0254

pound2N=4.45
#Hollowcore 8"
hSlab=8*in2m
Rhollow=(2+25/32.)*in2m
distHollows=(7+3/8.)*in2m
sectAreaSlab=(distHollows*hSlab-math.pi*Rhollow**2)*1/distHollows  #section area 1m slab

spanSlab=23*ft2m+2*in2m

#Geometry
lBeam=round(3*ft2m,2)
wallTh=round(10*in2m,2)
wBeam=wallTh
hBeam=10*in2m
lBearing=0.3
wColumn=wallTh
dimYColumn=lBearing
wallHeight=3*ft2m

yBeamEnd=round(0.5*lBeam+lBearing/2.,2)
yBeamCent=0.6*yBeamEnd
zBeam=3*ft2m+hBeam/2.
zColumn=zBeam-0.01
#Loads
deadL=110*pound2N/(ft2m)**2   #dead load (
liveL=100*pound2N/(ft2m)**2    # live load (40 psf)
snowL=42*pound2N/(ft2m)**2    # snow load (42 psf)

xList=[0]
yList=[0,yBeamCent,yBeamEnd]
zList=[0,zColumn,zBeam]

eSize=0.25
