# -*- coding: utf-8 -*-
from postprocess.control_vars import *
from postprocess import limit_state_data as lsd
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.FE_model import quick_graphics as qg

execfile("../model_gen.py") #FE model generation

#Load properties to display:
execfile(cfg.verifNormStrFile)

#  Config
argument= 'chiLT'       #Possible arguments:
                     #RC elem: 'CF', 'N', 'My', 'Mz'
                     #steel elem: 'CF', 'N', 'My', 'Mz','Ncrd','McRdy','McRdz',
                     #            'MvRdz','MbRdz','chiLT'
setDispRes=beamXsteel+columnZsteel   #set of linear elements to display results
setDisp=overallSet   #set of elements (any type) to be displayed
scaleFactor=1        #scale factor to apply to the auto-scales diagram (can be negative)
fUnitConv=1          #unit conversion factor (i.e N->kN => fUnitConv= 1e-3)
#  End config 

caption= cfg.capTexts[lsd.normalStressesResistance.label] + ', ' + cfg.capTexts[argument] + '. '#+ setsDispRes[0].description.capitalize() + ', ' 

qg.display_beam_result(attributeName=lsd.normalStressesResistance.label,itemToDisp=argument,beamSetDispRes=setDispRes,setToDisplay=setDisp,fConvUnits=fUnitConv,scaleFactor=1.0,caption=caption,viewDef= vtk_graphic_base.CameraParameters('XYZPos'),fileName=None,defFScale=0.0)



