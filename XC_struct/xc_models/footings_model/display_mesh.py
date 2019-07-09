# -*- coding: utf-8 -*-

execfile('./footings_xc_model.py')
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.FE_model import vtk_FE_graphic


defDisplay= vtk_FE_graphic.RecordDefDisplayEF()
setToDisplay= xcTotalSet #totalSet

defDisplay.FEmeshGraphic(xcSet= setToDisplay,caption='mesh')

