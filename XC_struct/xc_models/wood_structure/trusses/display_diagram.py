# -*- coding: utf-8 -*-
import sys
arg1= str(sys.argv[1])
execfile(arg1)

#Graphic output
from postprocess.reports import graphical_reports as gr

loadCaseToDisplay= gr.getRecordLoadCaseDispFromLoadPattern(lp0)
loadCaseToDisplay.unitsForc='[kN]'
loadCaseToDisplay.unitsMom='[kN.m]'
loadCaseToDisplay.setToDisplay= xcTotalSet
loadCaseToDisplay.cameraParameters= modelSpace.cameraParameters

 
#Define the diagram to display:
# scaleFactor, unitConversionFactor, element sets and magnitude to display.

#lcs.displayIntForcDiag('N',xcTotalSet,1e-3,1,'(kN)',loadCaseToDisplay.cameraParameters)
loadCaseToDisplay.displayIntForcDiag(itemToDisp='N')
#lcs.displayIntForcDiag('Qy',xcTotalSet,1e-3,1,'(kN)',loadCaseToDisplay.cameraParameters)
