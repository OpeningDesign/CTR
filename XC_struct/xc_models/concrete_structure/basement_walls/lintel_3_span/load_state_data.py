from postprocess.xcVtk import vtk_graphic_base
from postprocess.reports import graphical_reports
D=graphical_reports.RecordLoadCaseDisp(loadCaseName='DeadL',loadCaseDescr='D: dead load',loadCaseExpr='1.0*DeadL',setsToDispLoads=[beam],setsToDispDspRot=[overallSet],setsToDispIntForc=[])
L=graphical_reports.RecordLoadCaseDisp(loadCaseName='LiveL',loadCaseDescr='L: live load (uniform)',loadCaseExpr='1.0*LiveL_ru+1.0*LiveL_pu',setsToDispLoads=[overallSet],setsToDispDspRot=[overallSet],setsToDispIntForc=[])
S=graphical_reports.RecordLoadCaseDisp(loadCaseName='SnowL',loadCaseDescr='S: snow load',loadCaseExpr='1.0*SnowL',setsToDispLoads=[overallSet],setsToDispDspRot=[overallSet],setsToDispIntForc=[])

#Ultimate limit states
ULS01=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS01',loadCaseDescr='ULS01: 1.4*D',loadCaseExpr='1.4*DeadL',setsToDispLoads=[overallSet],setsToDispDspRot=[overallSet],setsToDispIntForc=[])

ULS02=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS02',loadCaseDescr='ULS02: 1.2*D + 1.6*L + 0.5*S',loadCaseExpr='1.2*DeadL+1.6*LiveL+0.5*SnowL',setsToDispLoads=[overallSet],setsToDispDspRot=[overallSet],setsToDispIntForc=[])

ULS03=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS03',loadCaseDescr='ULS03: 1.2*D + 1.6*S + 1.0*L',loadCaseExpr='1.2*DeadL+1.0*LiveL+1.6*SnowL',setsToDispLoads=[overallSet],setsToDispDspRot=[overallSet],setsToDispIntForc=[])

LS=[D,L,S]
ULS=[ULS01,ULS02,ULS03]
for lc in LS+ULS:
    lc.setsToDispDspRot=[overallSet]
    lc.setsToDispIntForc=[]
    lc.unitsScaleLoads=1e-3
    lc.unitsScaleDispl=1e3
    lc.unitsDispl='[mm]'
    lc.unitsScaleMom=1e-3
    lc.unitsMom='[m.kN]'
    lc.unitsScaleForc=1e-3
    lc.unitsForc='[kN]'
    lc.setsToDispBeamLoads=[overallSet]
    lc.setsToDispBeamIntForc=[beam,column]
    lc.listBeamIntForc=['N','Mz','Qy']
    lc.cameraParameters= vtk_graphic_base.CameraParameters('XYZPos')
    lc.setsToDispBeamLoads=[overallSet]
    
