# -*- coding: utf-8 -*-
from postprocess.control_vars import *
from postprocess import limit_state_data as lsd
from postprocess.xcVtk.FE_model import vtk_display_limit_state as dls


execfile("../model_gen.py") #FE model generation

#Load properties to display:
execfile(cfg.verifFatigueFile)



limitStateLabel= lsd.fatigueResistance.label

#Possible arguments: 'getAbsSteelStressIncrement',  'concreteBendingCF',  'concreteLimitStress',  'shearLimit' , 'concreteShearCF', 'Mu',  'Vu'

argument='getAbsSteelStressIncrement'

setDisp= allShells
dls.displayFieldDirs1and2(limitStateLabel,argument,setDisp,None,1.0,None,cfg.capTexts,defFScale=0.0)



