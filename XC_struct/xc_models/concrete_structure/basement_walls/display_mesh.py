# -*- coding: utf-8 -*-

execfile('./basement_wall.py')
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.FE_model import vtk_FE_graphic


displaySettings= vtk_FE_graphic.DisplaySettingsFE()
displaySettings.cameraParameters= vtk_graphic_base.CameraParameters('ZPos') 
setToDisplay= totalSet
displaySettings.FEmeshGraphic(xcSet= setToDisplay,caption='mesh')

