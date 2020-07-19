# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

__author__= "Luis C. Pérez Tato (LCPT) , Ana Ortega (AO_O) "
__copyright__= "Copyright 2016, LCPT, AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es, ana.ortega@ciccp.es "

import math
import xc_base
import geom
import xc
from model import predefined_spaces
from materials.awc_nds import AWCNDS_materials as mat
from materials.awc_nds import dimensional_lumber
import plates_model
import check

footToMeter= 0.3048
inchToMeter= 2.54/100.0

# Geometry
wallHeight= 11*footToMeter-22*inchToMeter
studSpacing= 16.0*inchToMeter
# Materials
# Spruce-pine-fir No. 2 
wood= dimensional_lumber.SprucePineFirWood(grade= 'stud')
studSection= mat.DimensionLumberSection(name= '2x6', woodMaterial= wood)

#Loads
## Wind loads
windWallPressure= 0.0 # Pa
windStudPressure= windWallPressure*studSpacing # N/m

print('wind load:', windStudPressure/1e3, ' kN/m')

title= '3rd floor AB interior stud.'
# Actions
## Reduction in uniform live loads.
# AT= 1*10.0*10.0 # Tributary area
# KLL= 2 # Live load element factor (ASCE-7 Table 4-2)
# liveLoadReductionFactor= (0.25+4.57/math.sqrt(KLL*AT)) # ASCE-7 Eq. 4.7-1 (SI)
# liveLoadReductionFactor= max(0.4,liveLoadReductionFactor) # Two or more floors
liveLoadReductionFactor= 1.0
print('Live load reduction factor: ', liveLoadReductionFactor)

## Load definition (values from truss_AB_reactions.ods)
deadLoad= xc.Vector([0.0,7.02e3]) # kN/m
liveLoad= liveLoadReductionFactor*xc.Vector([0.0,10.55e3]) # kN/m
snowLoad= xc.Vector([0.0,22.10e3]) # kN/m
windLoad= xc.Vector([windStudPressure,-13.96]) # kN/m

studObj= plates_model.Stud(title, studSection, studSpacing, wallHeight);
studObj.printHeader()
studObj.check(deadLoad, liveLoad, snowLoad, windLoad)
