# -*- coding: utf-8 -*-

from postprocess.reports import graphical_reports as gr
from postprocess.xcVtk import vtk_graphic_base

execfile('./footings_xc_model.py')

#available components: 'axialComponent', 'transComponent', 'transYComponent',
#                      'transZComponent'

loadCasesToDisplay=[]
for lcName in loadCaseNames:
    lc= loadPatterns[lcName]
    rlcd= gr.getRecordLoadCaseDispFromLoadPattern(lc)
    rlcd.setsToDispLoads=[xcTotalSet]
    loadCasesToDisplay.append(rlcd)

for lc in loadCasesToDisplay:
    lc.displayLoadOnSets()
