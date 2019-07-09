# -*- coding: utf-8 -*-

execfile('./basement_wall.py')
from postprocess.reports import graphical_reports as gr
from postprocess.xcVtk import vtk_graphic_base


#available components: 'axialComponent', 'transComponent', 'transYComponent',
#                      'transZComponent'

cp= vtk_graphic_base.CameraParameters('ZPos')

loadCasesToDisplay= getLoadCasesForDisplaying()

for lc in loadCasesToDisplay:
    lc.displayLoadOnSets()
