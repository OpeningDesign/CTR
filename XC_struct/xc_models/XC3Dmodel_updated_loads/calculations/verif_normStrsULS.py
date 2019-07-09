# -*- coding: utf-8 -*-
from postprocess.config import output_config as oc
from postprocess import limit_state_data as lsd
from postprocess import RC_material_distribution
from materials.sia262 import SIA262_limit_state_checking as lscheck

#Results directories
execfile("../model_gen.py") #FE model generation

#Reinforced concrete sections on each element.
#reinfConcreteSections=RC_material_distribution.RCMaterialDistribution()
#reinfConcreteSections.mapSectionsFileName='./mapSectionsReinforcement.pkl'
reinfConcreteSections= RC_material_distribution.loadRCMaterialDistribution()

# variables that control the output of the checking (setCalc,
# appendToResFile .py [defaults to 'N'], listFile .tex [defaults to 'N']
outCfg=oc.verifOutVars(setCalc=overallSet,appendToResFile='N',listFile='N',calcMeanCF='Y')

limitState=lsd.normalStressesResistance
limitState.controller= lscheck.BiaxialBendingNormalStressController(limitState.label)
a=lsd.normalStressesResistance.check(reinfConcreteSections,outCfg)




