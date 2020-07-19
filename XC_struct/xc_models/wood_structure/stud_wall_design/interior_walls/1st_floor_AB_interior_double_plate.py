# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import math
import xc_base
import geom
import xc
from model import predefined_spaces
from materials.awc_nds import AWCNDS_materials as mat
from materials.awc_nds import dimensional_lumber
import plates_model

inchToMeter= 0.0254

title= '1st floor AB interior double plate.'
studSpacing= 12*inchToMeter
trussSpacing= 12*inchToMeter
# Materials
# Spruce-pine-fir No. 2 
wood= dimensional_lumber.SprucePineFirWood(grade= 'no_2')
#wood= dimensional_lumber.SprucePineFirWood(grade= 'stud')
xc_material= wood.defXCMaterial()
plateSection= mat.DimensionLumberSection(name= '2x6', woodMaterial= wood)


# Reduction in uniform live loads.
AT= 3*10.0*10.0 # Tributary area
KLL= 2 # Live load element factor (ASCE-7 Table 4-2)
liveLoadReductionFactor= (0.25+4.57/math.sqrt(KLL*AT)) # ASCE-7 Eq. 4.7-1 (SI)
liveLoadReductionFactor= max(0.4,liveLoadReductionFactor) # Two or more floors
print('Live load reduction factor: ', liveLoadReductionFactor)


# Actions
## Load definition (values from truss_AB_reactions.ods)
deadLoad= 9.14e3 # kN/truss
liveLoad= liveLoadReductionFactor*15.62e3 # kN/truss
snowLoad= 6.74e3 # kN/truss
windLoad= -4.26e3 # kN/truss

doublePlate= plates_model.DoublePlate(title, plateSection, studSpacing, trussSpacing, pointLoadFactor= 1.0/3.0);

doublePlate.check(deadLoad, liveLoad, snowLoad, windLoad)
