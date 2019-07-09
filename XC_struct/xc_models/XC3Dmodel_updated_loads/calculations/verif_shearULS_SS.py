# -*- coding: utf-8 -*-
from postprocess import limit_state_data as lsd
from materials.ec3 import EC3_limit_state_checking as EC3lscheck
from postprocess.config import output_config as oc

execfile("../model_gen.py") #FE model generation

#Steel beams definition
execfile("../steel_beams_def.py")

setCalc=beamXsteel+columnZsteel
# variables that control the output of the checking (setCalc,
# appendToResFile .py [defaults to 'N'], listFile .tex [defaults to 'N']
outCfg=oc.verifOutVars(setCalc=setCalc,appendToResFile='N',listFile='N',calcMeanCF='Y')

limitState=lsd.shearResistance
limitState.controller= EC3lscheck.ShearController(limitState.label)
a=limitState.runChecking(outCfg)


