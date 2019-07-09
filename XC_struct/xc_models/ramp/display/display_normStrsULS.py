# -*- coding: utf-8 -*-
from postprocess.control_vars import *
from postprocess import limit_state_data as lsd
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.FE_model import vtk_display_limit_state as dls


#FE model generation
execfile("../model_gen.py")

#Load properties to display:
execfile(cfg.verifNormStrFile)


#  Config
argument= 'CF' #Possible arguments: 'CF', 'N', 'My','Mz'
fUnitConv=1.0  #unit conversion factor (i.e N->kN => fUnitConv= 1e-3)
setDisp= foot  #Set of shell elements to be displayed
cameraParameters= vtk_graphic_base.CameraParameters('XYZPos')
rgMinMax=(0,1.0)     #truncate values to be included in the range
                     #(if None -> don't truncate)
#  End config 


dls.displayFieldDirs1and2(limitStateLabel=lsd.normalStressesResistance.label,argument=argument,elementSet=setDisp,component=None,fUnitConv=fUnitConv,fileName=None,captionTexts=cfg.capTexts,defFScale=0.0,viewDef= cameraParameters,rgMinMax=rgMinMax)




