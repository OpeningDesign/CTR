from postprocess.xcVtk import vtk_graphic_base
from postprocess.reports import graphical_reports

ULS01=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS01',loadCaseDescr='ULS01',loadCaseExpr='1.4*Dead_LC',setsToDispLoads=[],setsToDispDspRot=beamSets,setsToDispIntForc=[])

ULS02=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS02',loadCaseDescr='ULS02',loadCaseExpr='1.2*Dead_LC+1.6*Live_LC+0.5*Snow_LC',setsToDispLoads=[],setsToDispDspRot=[walls],setsToDispIntForc=[])

ULS03=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS03',loadCaseDescr='ULS03',loadCaseExpr='1.2*Dead_LC+1.6*Snow_LC+0.5*Wind_LC',setsToDispLoads=[],setsToDispDspRot=beamSets,setsToDispIntForc=[])

ULS04=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS04',loadCaseDescr='ULS04',loadCaseExpr='1.2*Dead_LC+1.0*Live_LC+1.0*Wind_LC',setsToDispLoads=[],setsToDispDspRot=beamSets,setsToDispIntForc=[])

ULS05=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS05',loadCaseDescr='ULS05',loadCaseExpr='0.9*Dead_LC+1.0*Wind_LC',setsToDispLoads=[],setsToDispDspRot=beamSets,setsToDispIntForc=[])

ULSs=[ULS01,ULS02,ULS03,ULS04,ULS05]

for us in ULSs:
    us.listDspRot=['uZ']
#    us.setsToDispBeamIntForc=[beamXsteel,WbeamYsteel,CbeamYsteel,EbeamYsteel]
#    us.listBeamIntForc=['Mz', 'Qy']
    us.setsToDispBeamIntForc=[columnZsteel]
    us.listBeamIntForc=['My','Mz', 'Qy','Qz']
