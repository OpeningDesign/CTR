# -*- coding: utf-8 -*-
''' wood bearing wall along ramp walls #146'''
from __future__ import division
from __future__ import print_function

__author__= "Luis C. Pérez Tato (LCPT) , Ana Ortega (AO_O) "
__copyright__= "Copyright 2020, LCPT, AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es, ana.ortega@ciccp.es "

from materials.sections import section_properties
from materials.awc_nds import AWCNDS_materials

footToMeter= 0.3048
inchToMeter= 2.54/100.0
psiToPa= 6894.76
kNToPound= 224.809
kNmTokipsft= 0.737562121169657
kNmToPoundft= kNmTokipsft*1000.0

# Geometry
wallHeight= 11*footToMeter-24*inchToMeter
studHeight= wallHeight-2*2*inchToMeter
studSpacing= 12.0*inchToMeter
lumber2x4Geom= section_properties.RectangularSection("lumber2x4Geom",b=1.5*inchToMeter,h=3.5*inchToMeter)

# Spruce-pine-fir stud NDS table 4A page 35.
stud= AWCNDS_materials.ColumnMember(0.3,studHeight, lumber2x4Geom)
E_adj= 440000*psiToPa
Fb= 675*psiToPa
Fv= 135*psiToPa
Fc= 725*psiToPa
Cr= 1.15
CF= 1.3
Fc_adj= Fc*CF
Fb_adj= Fb*Cr*CF

#Loads
## Wind loads
windWallPressure= 0.0 # Pa
windStudPressure= windWallPressure*studSpacing # N/m
Mwind= windStudPressure*studHeight**2/8.0

## Gravity loads
wallGLoad= 21.72e3 # N/m only 2nd floor trusses (CD_reactions.ods)
studGLoad= wallGLoad*studSpacing
Mtotal= Mwind#+studGLoad*0.02 # Kurt dixit

## stresses
fc= studGLoad/stud.section.A()
fb1= Mtotal/stud.section.getElasticSectionModulusZ()
fb2= 0.0


#Checking
Cp= stud.getColumnStabilityFactor(c= 0.8, E_adj= E_adj,Fc_adj= Fc_adj)
Fc_adj*= Cp
capacity= stud.section.A()*Fc_adj
FcE1= stud.getFcE1(E_adj= E_adj)
print('FcE1= ',FcE1)
FcE2= stud.getFcE2(E_adj= E_adj)
RB= stud.getBendingSlendernessRatioB()
FbE= stud.getFbE(E_adj= E_adj)
CF= stud.getCapacityFactor(E_adj, Fc_adj, Fb_adj, Fb_adj, fc,fb1, fb2)

print('wall height= ',wallHeight, ' m')
print('stud height= ',studHeight, ' m')
print('stud spacing= ',studSpacing, ' m')
print('sections dimensions: ', str(stud.section.b*1e3)+'x'+str(stud.section.h*1e3), ' mm')
print('wind load:', windStudPressure/1e3, ' kN/m')
print('bending moment due to wind:', Mwind/1e3, ' kN m', Mwind/1e3*kNmToPoundft, ' lb ft')
print('total bending moment:', Mtotal/1e3, ' kN m', Mtotal/1e3*kNmToPoundft, ' lb ft')
print('gravity wall load:', wallGLoad/1e3, ' kN/m')
print('gravity stud load:', studGLoad/1e3, ' kN', studGLoad/1e3*kNToPound, ' lb')
print ('compression stress: ', fc/1e6, ' MPa', fc/psiToPa, ' psi')
print('unbraced length x:', stud.getUnbracedLengthB(), ' m')
print('unbraced length y:', stud.unbracedLengthH, ' m')
print('Fc\'= ', Fc_adj/1e6,' MPa')
print('Fb\'= ', Fb_adj/1e6,' MPa')
print('E\'= ', E_adj/1e9,' GPa')
print('stud stability factor Cp= ', Cp)
print('stud capacity = ', capacity/1e3, ' kN')
print('FcE1= ', FcE1/1e6,' MPa')
print('FcE2= ', FcE2/1e6,' MPa')
print('RB= ', RB,' m')
print('FbE= ', FbE/1e6,' MPa')
print('capacity factor CF= ', CF)
