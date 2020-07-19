from postprocess.xcVtk import vtk_graphic_base
from postprocess.reports import graphical_reports
D=graphical_reports.RecordLoadCaseDisp(loadCaseName='D',loadCaseDescr='ULS1: 1.2*D+1.6*L+0.5*S',loadCaseExpr='1.0*D',setsToDispLoads=[overallSet],setsToDispDspRot=[overallSet],setsToDispIntForc=[])
D.cameraParameters= vtk_graphic_base.CameraParameters('XYZPos')

ULS1=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS1',loadCaseDescr='ULS1: 1.2*D+1.6*L+0.5*S',loadCaseExpr='1.2*D+1.6*L+0.5*S',setsToDispLoads=[overallSet],setsToDispDspRot=[overallSet],setsToDispIntForc=[])
ULS1.unitsScaleLoads=1e-3
ULS1.unitsScaleDispl=1e3
ULS1.unitsDispl='[mm]'
ULS1.unitsScaleMom=1e-3
ULS1.unitsMom='[m.kN]'
ULS1.unitsScaleForc=1e-3
ULS1.unitsForc='[kN]'
ULS1.setsToDispBeamIntForc=[ties]
ULS1.listBeamIntForc=['N']
ULS1.cameraParameters= vtk_graphic_base.CameraParameters('XYZPos')
'''
ULS1.setsToDispBeamLoads=[beamY]
ULS1.vectorScalePointLoads=0.005
ULS1.compElLoad='transComponent'
'''
