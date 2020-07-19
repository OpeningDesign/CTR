from postprocess.xcVtk import vtk_graphic_base
from postprocess.reports import graphical_reports

ULS01=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS01',loadCaseDescr='ULS01: 1.0*ULS1',loadCaseExpr='1.0*ULS1',setsToDispLoads=[overallSet],setsToDispDspRot=[overallSet],setsToDispIntForc=[rim])
ULS01.cameraParameters= vtk_graphic_base.CameraParameters('XYZPos')
ULS01.unitsScaleLoads=1e-3
ULS01.unitsScaleDispl=1e3
ULS01.unitsDispl='[mm]'
ULS01.unitsScaleMom=1e-3
ULS01.unitsMom='[m.kN]'
ULS01.unitsScaleForc=1e-3
ULS01.unitsForc='[kN]'
ULS01.setsToDispBeamIntForc=[]
ULS01.listBeamIntForc=[]
ULS01.cameraParameters= vtk_graphic_base.CameraParameters('XYZPos')
ULS01.setsToDispBeamLoads=[]








ULS1=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS1',loadCaseDescr='ULS1: 1.0*ULS1',loadCaseExpr='1.0*ULS1',setsToDispLoads=[overallSet],setsToDispDspRot=[overallSet],setsToDispIntForc=[overallSet])
ULS1.cameraParameters= vtk_graphic_base.CameraParameters('XYZPos')
