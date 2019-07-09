# -*- coding: utf-8 -*-


import os

model_path="./"
#Project directory structure
execfile("project_directories.py")

from postprocess import limit_state_data as lsd
from postprocess import RC_material_distribution
from materials.aci import ACI_limit_state_checking

lsd.LimitStateData.internal_forces_results_directory= model_path+internal_forces_results_directory
lsd.LimitStateData.check_results_directory= model_path+check_results_directory

#Reinforced concrete sections on each element.
reinfConcreteSections= RC_material_distribution.loadRCMaterialDistribution()

limitStateLabel= lsd.normalStressesResistance.label
lsd.normalStressesResistance.controller= ACI_limit_state_checking.BiaxialBendingNormalStressController(limitStateLabel)
lsd.normalStressesResistance.check(reinfConcreteSections)



