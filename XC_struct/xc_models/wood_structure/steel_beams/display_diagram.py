# -*- coding: utf-8 -*-
import sys
arg1= str(sys.argv[1])
execfile(arg1)

#Graphic output
from postprocess.xcVtk import vtk_graphic_base
from postprocess.reports import graphical_reports as gr

loadCaseToDisplay= gr.getRecordLoadCaseDispFromLoadPattern(cLC)
loadCaseToDisplay.unitsForc='[kN]'
loadCaseToDisplay.unitsMom='[kN.m]'
loadCaseToDisplay.setToDisplay= xcTotalSet
loadCaseToDisplay.cameraParameters= vtk_graphic_base.CameraParameters('Custom')
loadCaseToDisplay.cameraParameters.viewUpVc= [0,-1,0]
loadCaseToDisplay.cameraParameters.posCVc= [0,0,100]

 
#Define the diagram to display:
# scaleFactor, unitConversionFactor, element sets and magnitude to display.

#lcs.displayIntForcDiag('N',xcTotalSet,1e-3,1,'(kN)',loadCaseToDisplay.cameraParameters)
loadCaseToDisplay.displayIntForcDiag(itemToDisp='Vy')
#lcs.displayIntForcDiag('Qy',xcTotalSet,1e-3,1,'(kN)',loadCaseToDisplay.cameraParameters)
