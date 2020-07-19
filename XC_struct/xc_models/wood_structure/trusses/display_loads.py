# -*- coding: utf-8 -*-

from postprocess.reports import graphical_reports as gr
from postprocess.xcVtk import vtk_graphic_base
import sys

fileName= sys.argv[1]
#execfile('./xc_model.py')
#execfile('./trusses_11_56.py')
#execfile('./trusses_10_15.py')
#execfile('./roof_truss_AB.py')
execfile(fileName)

#available components: 'axialComponent', 'transComponent', 'transYComponent',
#                      'transZComponent'

rlcd= gr.getRecordLoadCaseDispFromLoadPattern(lp0)
rlcd.cameraParameters= vtk_graphic_base.CameraParameters('Custom')
rlcd.cameraParameters.viewUpVc= [0,0,1]
rlcd.cameraParameters.posCVc= [0,-100,0]
rlcd.setsToDispLoads=[upperChordSet]#xcTotalSet]
rlcd.setsToDispBeamLoads=[upperChordSet]#xcTotalSet]

loadCasesToDisplay=[rlcd]

#End data

for lc in loadCasesToDisplay:
    lc.displayLoadOnSets()
