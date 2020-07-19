from postprocess.xcVtk import vtk_graphic_base
from postprocess.reports import graphical_reports


lULS01=graphical_reports.RecordLoadCaseDisp(loadCaseName='lULS01',loadCaseDescr='ULS01',loadCaseExpr='1.4*Dead_LC',setsToDispLoads=[],setsToDispDspRot=[overallSet],setsToDispIntForc=[walls])

lULS02=graphical_reports.RecordLoadCaseDisp(loadCaseName='lULS02',loadCaseDescr='ULS02',loadCaseExpr='1.2*Dead_LC+1.6*Live_LC+0.5*Snow_LC',setsToDispLoads=[],setsToDispDspRot=[overallSet],setsToDispIntForc=[walls])

lULS03=graphical_reports.RecordLoadCaseDisp(loadCaseName='lULS03',loadCaseDescr='ULS03',loadCaseExpr='1.2*Dead_LC+1.6*Snow_LC+0.5*Wind_LC',setsToDispLoads=[],setsToDispDspRot=[overallSet],setsToDispIntForc=[walls])

lULS04=graphical_reports.RecordLoadCaseDisp(loadCaseName='lULS04',loadCaseDescr='ULS04',loadCaseExpr='1.2*Dead_LC+1.0*Live_LC+1.0*Wind_LC',setsToDispLoads=[],setsToDispDspRot=[overallSet],setsToDispIntForc=[walls])

lULS05=graphical_reports.RecordLoadCaseDisp(loadCaseName='lULS05',loadCaseDescr='ULS05',loadCaseExpr='0.9*Dead_LC+1.0*Wind_LC',setsToDispLoads=[],setsToDispDspRot=[overallSet],setsToDispIntForc=[walls])

ULSs=[lULS01,lULS02,lULS03,lULS04,lULS05]

for us in ULSs:
    us.listDspRot=['uX','uZ']
#    us.setsToDispBeamIntForc=[beamXsteel,WbeamYsteel,CbeamYsteel,EbeamYsteel]
#    us.listBeamIntForc=['Mz', 'Qy']
    us.setsToDispBeamIntForc=[steelMembers]
    us.listBeamIntForc=['N','My','Mz', 'Qy','Qz']
