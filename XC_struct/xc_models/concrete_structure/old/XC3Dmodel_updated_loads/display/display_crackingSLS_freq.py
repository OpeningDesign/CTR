# -*- coding: utf-8 -*-
from postprocess.control_vars import *
from postprocess import limit_state_data as lsd
from postprocess.xcVtk import vtk_graphic_base
from postprocess import output_handler

#FE model generation
execfile("../model_gen.py")

#Load properties to display:
execfile(cfg.projectDirTree.getVerifCrackFreqFile())


#  Config
argument= 'wk'    #Possible arguments: 'N', 'My','Mz','s_rmax','eps_sm','wk'

setDisp= wall     #Set of shell elements to be displayed
cameraParameters= vtk_graphic_base.CameraParameters('XYZPos')
rgMinMax=(0,0.3)  #truncate values to be included in the range
                  #(if None -> don't truncate)
#  End config 

oh= output_handler.OutputHandler(modelSpace)
oh.outputStyle.cameraParameters= cameraParameters
oh.displayFieldDirs1and2(limitStateLabel=lsd.freqLoadsCrackControl.label,argument=argument,setToDisplay=setDisp,component=None,fileName=None,defFScale=0.0,rgMinMax=rgMinMax) 




