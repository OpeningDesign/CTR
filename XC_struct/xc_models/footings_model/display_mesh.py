# -*- coding: utf-8 -*-

execfile('./footings_xc_model.py')
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.FE_model import vtk_FE_graphic


displaySettings= vtk_FE_graphic.DisplaySettingsFE()
setToDisplay= xcTotalSet #totalSet

displaySettings.FEmeshGraphic(xcSet= setToDisplay,caption='mesh')

