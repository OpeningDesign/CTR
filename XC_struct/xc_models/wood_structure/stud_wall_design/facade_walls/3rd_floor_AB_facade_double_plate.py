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
import check

inchToMeter= 0.0254
title= '3rd floor AB facade double plate.'
studSpacing= 19.2*inchToMeter
trussSpacing= 24*inchToMeter
# Materials
# Spruce-pine-fir No. 2 
wood= dimensional_lumber.SprucePineFirWood(grade= 'no_2')
#wood= dimensional_lumber.SprucePineFirWood(grade= 'stud')
xc_material= wood.defXCMaterial()
plateSection= mat.DimensionLumberSection(name= '6x2', woodMaterial= wood)


# # Reduction in uniform live loads.
# AT= 1*10.0*5.0 # Tributary area
# KLL= 2 # Live load element factor (ASCE-7 Table 4-2)
# liveLoadReductionFactor= (0.25+4.57/math.sqrt(KLL*AT)) # ASCE-7 Eq. 4.7-1 (SI)
# liveLoadReductionFactor= max(0.4,liveLoadReductionFactor) # Two or more floors
liveLoadReductionFactor= 1.0
print('Live load reduction factor: ', liveLoadReductionFactor)


# Actions
## Load definition (values from truss_AB_reactions.ods)
deadLoad= 1.07e3 # kN/truss
liveLoad= liveLoadReductionFactor*1.64e3 # kN/truss
snowLoad= 3.44e3 # kN/truss
windLoad= -2.17e3 # kN/truss

doublePlate= plates_model.DoublePlate(title, plateSection, studSpacing, trussSpacing, pointLoadFactor= 0.95);

doublePlate.check( deadLoad, liveLoad, snowLoad, windLoad)
