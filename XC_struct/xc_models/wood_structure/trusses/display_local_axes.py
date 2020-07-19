# -*- coding: utf-8 -*-

#execfile('./xc_model.py')
execfile('./trusses_11_56.py')
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.FE_model import vtk_FE_graphic

displaySettings= vtk_FE_graphic.DisplaySettingsFE()
displaySettings.cameraParameters= vtk_graphic_base.CameraParameters('Custom')
displaySettings.cameraParameters.viewUpVc= [0,0,1]
displaySettings.cameraParameters.posCVc= [0,-100,0]
setToDisplay= xcTotalSet #impactOnBody #totalSet

displaySettings.displayLocalAxes(xcSet= xcTotalSet, caption= 'local axes',vectorScale=0.3)


