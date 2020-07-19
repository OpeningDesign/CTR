# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division

import os
from postprocess import limit_state_data as lsd
from model.sets import sets_mng as sUtils

model_path="./"
#Project directory structure
execfile(model_path+'env_config.py')
lsd.LimitStateData.envConfig= cfg

modelDataInputFile=model_path+"footings_xc_model.py" #data for FE model generation
execfile(modelDataInputFile)

#RC sections definition.
execfile(model_path+'sectionsDef.py')

#Define section for each element (spatial distribution of RC sections).
for fs in footingSetList:
    key= fs.name[0:2]
    fs.fillDownwards()
    reinfConcreteSectionDistribution.assign(elemSet= fs.elements, setRCSects= rcSects[key])


reinfConcreteSectionDistribution.dump()

#Elements with an assigned section.
elementsWithSection= reinfConcreteSectionDistribution.getElementSet(prep)

loadCombinations= prep.getLoadHandler.getLoadCombinations

#Limit states to calculate internal forces for.
limitStates= [lsd.normalStressesResistance, # Normal stresses resistance.
lsd.shearResistance, # Shear stresses resistance (IS THE SAME AS NORMAL STRESSES, THIS IS WHY IT'S COMMENTED OUT).
lsd.freqLoadsCrackControl, # RC crack control under frequent loads
lsd.quasiPermanentLoadsCrackControl, # RC crack control under quasi-permanent loads
lsd.fatigueResistance # Fatigue resistance.
] 

for ls in limitStates:
  ls.saveAll(combContainer=combContainer,setCalc= elementsWithSection,fConvIntForc= 1.0)
  print('combinations for ', ls.label, ': ', loadCombinations.getKeys())
