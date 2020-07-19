# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2019, LCPT, AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

footToMeter= 0.3048
inchToMeter= 2.54/100.0
psiToPa= 6894.76
kNToPound= 224.809
kNmTokipsft= 0.737562121169657
kNmToPoundft= kNmTokipsft*1000.0

# Geometry
wallHeight= 11*footToMeter-22*inchToMeter
studHeight= wallHeight-3*2*inchToMeter
trussSpacing= 1.0*footToMeter
studSpacing= 19.2*inchToMeter


#Loads
## Wind loads
windWallPressure= 852.0 # Pa
windStudPressure= windWallPressure*studSpacing # N/m
windHForce= windStudPressure*studHeight/2.0
windVForce= (3.35e3-4.65e3)/0.6/trussSpacing*studSpacing

## Gravity loads
wallGLoad= 4.65e3/trussSpacing # dead load N/m facade Zone AB at first floor
studGLoad= wallGLoad*studSpacing

frictionCoefficient= 0.62

verticalNetLoad= (studGLoad+windVForce)
frictionForce= verticalNetLoad*frictionCoefficient

print('stud dead load Wstud=',studGLoad/1e3,'kN/stud')
print('wind horizontal force FHw=',windHForce/1e3,'kN/stud')
print('wind vertical force FVw=',windVForce/1e3,'kN/stud')
print('net vertical load Wnet=',verticalNetLoad/1e3,'kN/stud')
print('friction force: Ff=',frictionForce/1e3,'kN/stud')
print('F= ',frictionForce/windHForce)

