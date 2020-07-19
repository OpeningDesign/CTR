# -*- coding: utf-8 -*-
from postprocess.control_vars import *
from postprocess import limit_state_data as lsd
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.FE_model import quick_graphics as qg


execfile("../model_gen.py") #FE model generation

#Load properties to display:
execfile(cfg.projectDirTree.getVerifShearFile())

#  Config
argument= 'CF'      #Available arguments:
                    # RC elements:'CF', 'N', 'My', 'Mz', 'Mu',
                    #             'Vy', 'Vz', 'theta', 'Vcu', 'Vsu', 'CF'
                    # steel elements: 'CF', 'Vy'
setDispRes=beam   #set of linear elements to display results
setDisp=beam   #set of elements (any type) to be displayed
scaleFactor=1      #scale factor to apply to the auto-scales diagram (can be negative)
fUnitConv=1          #unit conversion factor (i.e N->kN => fUnitConv= 1e-3)
#  End config 

caption= cfg.capTexts[lsd.shearResistance.label] + ', ' + cfg.capTexts[argument] + '. '#+ setsDispRes[0].description.capitalize() + ', ' 

lcs= qg.LoadCaseResults(FEcase)
lcs.displayBeamResult(attributeName=lsd.shearResistance.label,itemToDisp=argument,beamSetDispRes=setDispRes,setToDisplay=setDisp,caption=caption,fileName=None,defFScale=0.0)
