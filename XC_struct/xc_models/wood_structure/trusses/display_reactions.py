# -*- coding: utf-8 -*-
import sys
from postprocess import output_handler
from postprocess.xcVtk import vtk_graphic_base

arg1= str(sys.argv[1])
execfile(arg1)

## Graphic stuff.
oh= output_handler.OutputHandler(modelSpace)

oh.outputStyle.cameraParameters= vtk_graphic_base.CameraParameters('Custom')
oh.outputStyle.cameraParameters.viewUpVc= [0,0,1]
oh.outputStyle.cameraParameters.posCVc= [0,-100,0]
oh.displayFEMesh()#setToDisplay= chordSet)
oh.displayReactions()
