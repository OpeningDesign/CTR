# -*- coding: utf-8 -*-

execfile('./basement_wall.py')
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.FE_model import vtk_FE_graphic


defDisplay= vtk_FE_graphic.RecordDefDisplayEF()
defDisplay.cameraParameters= vtk_graphic_base.CameraParameters('ZPos') 
setToDisplay= totalSet
defDisplay.FEmeshGraphic(xcSet= setToDisplay,caption='mesh')

