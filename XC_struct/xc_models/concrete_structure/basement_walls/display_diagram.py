
execfile('./basement_wall.py')

#Graphic output
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.FE_model import vtk_FE_graphic
from postprocess.xcVtk import vtk_internal_force_diagram as gde
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.FE_model import quick_graphics as qg
from postprocess.reports import graphical_reports as gr

lcs= qg.QuickGraphics(wallFEModel)
cp= vtk_graphic_base.CameraParameters('ZPos')

loadCasesToDisplay= getLoadCasesForDisplaying()
internalForceToDisplay= 'Mz'

for lc in loadCasesToDisplay:
    lcs.solve(loadCaseName=lc.loadCaseName,loadCaseExpr=lc.loadCaseExpr)
    lcs.displayIntForcDiag(internalForceToDisplay,wall.wallSet,1e-3,-1.0,'(kN m)',cp)


#Define the diagram to display:
# scaleFactor, unitConversionFactor, element sets and magnitude to display.
#lcs.displayNodeValueDiagram('uY',setToDisplay= bridgeSectionSet,fConvUnits=1e3,scaleFactor=-0.05,viewDef= vtk_graphic_base.CameraParameters('ZPos'))
