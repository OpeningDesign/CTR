# -*- coding: utf-8 -*-
from postprocess.config import output_config as oc
from postprocess import limit_state_data as lsd
from postprocess import RC_material_distribution
from materials.ehe import EHE_limit_state_checking as lschck  #Checking material for shear limit state according to EHE08
#from materials.sia262 import SIA262_limit_state_checking as lschck  #Checking material for shear limit state according to SIA262

execfile('../model_gen.py')

#Reinforced concrete sections on each element.
reinfConcreteSections= RC_material_distribution.loadRCMaterialDistribution()

# variables that control the output of the checking (setCalc,
# appendToResFile .py [defaults to 'N'], listFile .tex [defaults to 'N']
outCfg=oc.verifOutVars(setCalc=beamY,appendToResFile='N',listFile='N')

limitStateLabel= lsd.shearResistance.label
lsd.shearResistance.controller= lschck.ShearController(limitStateLabel)
lsd.shearResistance.check(reinfConcreteSections,outCfg)





