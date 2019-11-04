# -*- coding: utf-8 -*-
from postprocess.control_vars import *
from postprocess import limit_state_data as lsd
from postprocess import output_handler


execfile("../model_gen.py") #FE model generation

#Load properties to display:
execfile(cfg.verifFatigueFile)



limitStateLabel= lsd.fatigueResistance.label

#Possible arguments: 'getAbsSteelStressIncrement',  'concreteBendingCF',  'concreteLimitStress',  'shearLimit' , 'concreteShearCF', 'Mu',  'Vu'

argument='getAbsSteelStressIncrement'

setDisp= allShells
oh= output_handler.OutputHandler(modelSpace)
oh.outputStyle.cameraParameters= cameraParameters
oh.displayFieldDirs1and2(limitStateLabel,argument,setToDisplay=setDisp,component=None, fileName= None,defFScale=0.0)



