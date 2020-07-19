# -*- coding: utf-8 -*-
''' Verification test based on example 1 of section 6-8
    of TM 5-809-3 manual.
'''
    
from __future__ import division
from __future__ import print_function

import math
from materials.aci import ACI_materials
from materials.tm5_809_3 import tm5_809_3_materials

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2019, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

inch2Meter= .0254
foot2Meter= .3048
pound2Newton= 4.4482216282509
lbSqft2Pascal= 47.880258888889


S_iu= 48.0 # Cell spacing (inches).
S= S_iu*inch2Meter # Cell spacing (meters).
cellReinf= tm5_809_3_materials.CMUWallCellReinforcement(reinfArea= ACI_materials.num5Area)
cmuWall= tm5_809_3_materials.CMUWallFabric(thickness= 8*inch2Meter,spacing= S, cellReinf= cellReinf)
wallHeight= 4.0 # m
rho= cmuWall.getMassPerSquareMeter()

# Capacity factor
eccentricity= cmuWall.thickness/12.0

firstFloorAxialLoad= 60.28e3
firstFloorWallSelfWeight= wallHeight*rho*9.81
firstFloorMoment= firstFloorAxialLoad*eccentricity
firstFloorCapacityFactor= cmuWall.getCapacityFactor(firstFloorAxialLoad+firstFloorWallSelfWeight,firstFloorMoment,wallHeight)

Mu= cmuWall.getResistingMomentPerUnitLength()
Fu= cmuWall.getResistingAxialForcePerUnitLength(wallHeight)
basementWallSelfWeight= 2.0*wallHeight*rho*9.81
basementAxialLoad= 60.28e3
basementMoment= firstFloorMoment # N m/m Design moment

basementCapacityFactor= cmuWall.getCapacityFactor(basementAxialLoad+basementWallSelfWeight,basementMoment,wallHeight)

print('rho= ', rho, 'kg/m2')
print('Fu= ', Fu/1e3, 'kN/m')
print('Mu= ', Mu/1e3, 'kN.m/m')
print('wallHeight= ', wallHeight, 'm')
print('eccentricity= ', eccentricity*1e2, 'cm')
print('firstFloorAxialLoad= ', firstFloorAxialLoad/1e3, 'kN/m')
print('firstFloorMoment= ', firstFloorMoment/1e3, 'kN.m/m')
print('firstFloorCapacityFactor= ', firstFloorCapacityFactor)
print('basementAxialLoad= ', basementAxialLoad/1e3, 'kN/m')
print('basementMoment= ', basementMoment/1e3, 'kN.m/m')
print('basementCapacityFactor= ', basementCapacityFactor)
