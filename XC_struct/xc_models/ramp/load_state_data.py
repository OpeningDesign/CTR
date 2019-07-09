# -*- coding: utf-8 -*-

'''In this script we define default data of load cases to be used (or changed)
while displaying loads or results associated to single load cases 
'''
from postprocess.xcVtk import vtk_graphic_base
from postprocess.reports import graphical_reports
from postprocess.xcVtk import vtk_graphic_base
'''
Definition of record objects with these attributes:
  loadCaseName:  name of the load case to be depicted
  loadCaseDescr: description text of the load case
  loadCaseExpr:  mathematical expression to define the load case (ex:
                 '1.0*GselfWeight+1.0*DeadLoad')
  setsToDispLoads: ordered list of sets of elements to display loads
  setsToDispBeamLoads: ordered list of sets of beam elements to display loads
                 (defaults to [])
  compElLoad: component of load on beam elements to be represented
              available components: 'axialComponent', 'transComponent',
              'transYComponent','transZComponent'
  unitsScaleLoads: factor to apply to loads if we want to change
                 the units (defaults to 1).
  unitsLoads: text to especify the units in which loads are 
                 represented (defaults to 'units:[m,kN]')
  vectorScaleLoads: factor to apply to the vectors length in the 
                 representation of loads (defaults to 1 -> auto-scale).
  vectorScalePointLoads: factor to apply to the vectors length in the 
                 representation of nodal loads (defaults to 1).
  multByElemAreaLoads: boolean value that must be True if we want to 
                 represent the total load on each element 
                 (=load multiplied by element area) and False if we 
                 are going to depict the value of the uniform load 
                 per unit area (defaults to False)
  listDspRot: ordered list of displacement or rotations to be displayed
                 available components: 'uX', 'uY', 'uZ', 'rotX', rotY', 'rotZ'
                 (defaults to ['uX', 'uY', 'uZ'])
  setsToDispDspRot: ordered list of sets of elements to display displacements 
                 or rotations
  unitsScaleDispl: factor to apply to displacements if we want to change
                 the units (defaults to 1).
  unitsDispl: text to especify the units in which displacements are 
                 represented (defaults to '[m]'
  listIntForc:   ordered list of internal forces to be displayed as scalar field 
                 over «shell» elements
                 available components: 'N1', 'N2', 'M1', 'M2', 'Q1', 'Q2'
                 (defaults to ['N1', 'N2', 'M1', 'M2', 'Q1', 'Q2'])
  setsToDispIntForc: ordered list of sets of elements (of type «shell»)to 
                    display internal forces
  listBeamIntForc: ordered list of internal forces to be displayed 
                 as diagrams on lines for «beam» elements
                 available components: 'N', 'My', 'Mz', 'Qy', 'Qz','T'
                 (defaults to ['N', 'My', 'Mz', 'Qy', 'Qz','T'])
  setsToDispBeamIntForc: ordered list of sets of elements (of type «beam»)to 
                    display internal forces (defaults to [])
  scaleDispBeamIntForc: tuple (escN,escQ,escM) correponding to the scales to 
                  apply to displays of, respectively, N Q and M beam internal 
                  forces (defaults to (1.0,1.0,1.0) -> auto-scale)
  unitsScaleForc: factor to apply to internal forces if we want to change
                 the units (defaults to 1).
  unitsForc: text to especify the units in which forces are 
                 represented (defaults to '[kN/m]')
  unitsScaleMom: factor to apply to internal moments if we want to change
                 the units (defaults to 1).
  unitsMom:  text to especify the units in which bending moments are 
                 represented (defaults to '[kN.m/m]')
  cameraParameters: parameters that define the position and orientation of the
                 camera (defaults to "XYZPos")
  
  cameraParametersBeams: parameters that define the position and orientation of the
                 camera for beam elements displays (defaults to "XYZPos")
  
'''






D=graphical_reports.RecordLoadCaseDisp(loadCaseName='DeadL',loadCaseDescr='D: dead load',loadCaseExpr='1.0*DeadL',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])


Lunif=graphical_reports.RecordLoadCaseDisp(loadCaseName='LiveLunif',loadCaseDescr='Lunif: live load (uniform)',loadCaseExpr='1.0*LiveLunif',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

LconcSpan1=graphical_reports.RecordLoadCaseDisp(loadCaseName='LiveLconcSpan1',loadCaseDescr='LconcSpan1: live load (concentrated on mid-span 1)',loadCaseExpr='1.0*LiveLconcSpan1',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

LconcSpan2=graphical_reports.RecordLoadCaseDisp(loadCaseName='LiveLconcSpan2',loadCaseDescr='LconcSpan2: live load (concentrated on mid-span 2)',loadCaseExpr='1.0*LiveLconcSpan2',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

LconcSpan3=graphical_reports.RecordLoadCaseDisp(loadCaseName='LiveLconcSpan3',loadCaseDescr='LconcSpan3: live load (concentrated on mid-span 3)',loadCaseExpr='1.0*LiveLconcSpan3',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

LC=[D,Lunif,LconcSpan1,LconcSpan2,LconcSpan3]
for lc in LC:
    lc.unitsScaleLoads=1e-3
    lc.unitsScaleDispl=1e3
    lc.unitsDispl='[mm]'
    lc.unitsScaleMom=1e-3
    lc.unitsMom='[m.kN]'
    lc.unitsScaleForc=1e-3
    lc.unitsForc='[kN]'
    lc.cameraParameters= vtk_graphic_base.CameraParameters('XYZPos')
    lc.vectorScalePointLoads=0.005
    lc.compElLoad='transComponent'

'''
Lpu=graphical_reports.RecordLoadCaseDisp(loadCaseName='LiveL_pu',loadCaseDescr='L_pu: live load (uniform on terraces)',loadCaseExpr='1.0*LiveL_pu',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

Lps=graphical_reports.RecordLoadCaseDisp(loadCaseName='LiveL_ps',loadCaseDescr='L_ps: live load (staggered pattern on terraces)',loadCaseExpr='1.0*LiveL_ps',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

L=graphical_reports.RecordLoadCaseDisp(loadCaseName='LiveL',loadCaseDescr='L: live load (uniform)',loadCaseExpr='1.0*LiveL_ru+1.0*Lpu',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

S=graphical_reports.RecordLoadCaseDisp(loadCaseName='SnowL',loadCaseDescr='S: snow load',loadCaseExpr='1.0*SnowL',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])


W_WE=graphical_reports.RecordLoadCaseDisp(loadCaseName='Wind_WE',loadCaseDescr='W_WE: Wind West-East',loadCaseExpr='1.0*Wind_WE',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

W_NS=graphical_reports.RecordLoadCaseDisp(loadCaseName='Wind_NS',loadCaseDescr='W_NS: Wind North-South',loadCaseExpr='1.0*Wind_NS',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])


#Ultimate limit states
ULS01=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS01',loadCaseDescr='ULS01: 1.4*D',loadCaseExpr='1.4*DeadL',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

ULS02_a=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS02_a',loadCaseDescr='ULS02_a: 1.2*D + 1.6*Lru + Lpu + 0.5*S',loadCaseExpr='1.2*DeadL+1.6*LiveL_ru+1.0*LiveL_pu+0.5*SnowL',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

ULS02_b=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS02_b',loadCaseDescr='ULS02_b: 1.2*D + 1.6*Lrs + Lps + 0.5*S',loadCaseExpr='1.2*DeadL+1.6*LiveL_rs+1.0*LiveL_ps+0.5*SnowL',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

ULS03_a=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS03_a',loadCaseDescr='ULS03_a: 1.2*D + 1.6*S + 0.5*Lru + Lpu',loadCaseExpr='1.2*DeadL+0.5*LiveL_ru+1.0*LiveL_pu+1.6*SnowL',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

ULS03_b=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS03_b',loadCaseDescr='ULS03_b: 1.2*D + 1.6*S + 0.5*Lrs + Lps',loadCaseExpr='1.2*DeadL+0.5*LiveL_rs+1.0*LiveL_ps+1.6*SnowL',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

ULS04_a=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS04_a',loadCaseDescr='ULS04_a: 1.2*D + 1.6*S + 0.5*W_WE',loadCaseExpr='1.2*DeadL+1.6*SnowL+0.5*Wind_WE',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

ULS04_b=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS04_b',loadCaseDescr='ULS04_b: 1.2*D + 1.6*S + 0.5*W_NS',loadCaseExpr='1.2*DeadL+1.6*SnowL+0.5*Wind_NS',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

ULS05_a=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS05_a',loadCaseDescr='ULS05_a: 1.2*D + W_WE + 0.5*Lru + Lpu',loadCaseExpr='1.2*DeadL+1.0*Wind_WE+0.5*LiveL_ru+1*LiveL_pu',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

ULS05_b=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS05_b',loadCaseDescr='ULS05_b: 1.2*D + W_NS + 0.5*Lru + Lpu',loadCaseExpr='1.2*DeadL+1.0*Wind_NS+0.5*LiveL_ru+1*LiveL_pu',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

ULS05_c=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS05_c',loadCaseDescr='ULS05_c: 1.2*D + W_WE + 0.5*Lrs + Lps',loadCaseExpr='1.2*DeadL+1.0*Wind_WE+0.5*LiveL_rs+1*LiveL_ps',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

ULS05_d=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS05_d',loadCaseDescr='ULS05_d: 1.2*D + W_NS + 0.5*Lrs + Lps',loadCaseExpr='1.2*DeadL+1.0*Wind_NS+0.5*LiveL_rs+1*LiveL_ps',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

ULS06_a=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS06_a',loadCaseDescr='ULS06_a: 1.2*D + 0.5*Lru + Lpu + 0.2*S',loadCaseExpr='1.2*DeadL+0.5*LiveL_ru+1*LiveL_pu+0.2*SnowL',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

ULS06_b=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS06_b',loadCaseDescr='ULS06_b: 1.2*D + 0.5*Lrs + Lps + 0.2*S',loadCaseExpr='1.2*DeadL+0.5*LiveL_rs+1*LiveL_ps+0.2*SnowL',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

ULS07_a=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS07_a',loadCaseDescr='ULS07_a: 0.9*D + W_WE',loadCaseExpr='0.9*DeadL+1.0*Wind_WE',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

ULS07_b=graphical_reports.RecordLoadCaseDisp(loadCaseName='ULS07_b',loadCaseDescr='ULS07_b: 0.9*D + W_NS',loadCaseExpr='0.9*DeadL+1.0*Wind_NS',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

# Serviceability limit states (design of footings)
SLS01=graphical_reports.RecordLoadCaseDisp(loadCaseName='SLS01',loadCaseDescr='SLS01: 1.0*D',loadCaseExpr='1.0*DeadL',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

SLS02_a=graphical_reports.RecordLoadCaseDisp(loadCaseName='SLS02_a',loadCaseDescr='SLS02_a: 1.0*D + 1.0*Lru + Lpu + 0.3*S',loadCaseExpr='1.0*DeadL+1.0*LiveL_ru+1.0*LiveL_pu+0.3*SnowL',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

SLS02_b=graphical_reports.RecordLoadCaseDisp(loadCaseName='SLS02_b',loadCaseDescr='SLS02_b: 1.0*D + 1.0*Lrs + Lps + 0.3*S',loadCaseExpr='1.0*DeadL+1.0*LiveL_rs+1.0*LiveL_ps+0.3*SnowL',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

SLS03_a=graphical_reports.RecordLoadCaseDisp(loadCaseName='SLS03_a',loadCaseDescr='SLS03_a: 1.0*D + 1.0*S + 0.3*Lru + 0.3*Lpu',loadCaseExpr='1.0*DeadL+0.3*LiveL_ru+0.3*LiveL_pu+1.0*SnowL',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

SLS03_b=graphical_reports.RecordLoadCaseDisp(loadCaseName='SLS03_b',loadCaseDescr='SLS03_b: 1.0*D + 1.0*S + 0.3*Lrs + 0.3*Lps',loadCaseExpr='1.0*DeadL+0.3*LiveL_rs+0.3*LiveL_ps+1.0*SnowL',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

SLS04_a=graphical_reports.RecordLoadCaseDisp(loadCaseName='SLS04_a',loadCaseDescr='SLS04_a: 1.0*D + W_WE + 1.0*Lru + Lpu',loadCaseExpr='1.0*DeadL+1.0*Wind_WE+1.0*LiveL_ru+1*LiveL_pu',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

SLS04_b=graphical_reports.RecordLoadCaseDisp(loadCaseName='SLS04_b',loadCaseDescr='SLS04_b: 1.0*D + W_NS + 1.0*Lru + Lpu',loadCaseExpr='1.0*DeadL+1.0*Wind_NS+1.0*LiveL_ru+1*LiveL_pu',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

SLS04_c=graphical_reports.RecordLoadCaseDisp(loadCaseName='SLS04_c',loadCaseDescr='SLS04_c: 1.0*D + W_WE + 1.0*Lrs + Lps',loadCaseExpr='1.0*DeadL+1.0*Wind_WE+1.0*LiveL_rs+1*LiveL_ps',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

SLS04_d=graphical_reports.RecordLoadCaseDisp(loadCaseName='SLS04_d',loadCaseDescr='SLS04_d: 1.0*D + W_NS + 1.0*Lrs + Lps',loadCaseExpr='1.0*DeadL+1.0*Wind_NS+1.0*LiveL_rs+1.0*LiveL_ps',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

SLS05_a=graphical_reports.RecordLoadCaseDisp(loadCaseName='SLS05_a',loadCaseDescr='SLS05_a: 1.0*D + W_WE',loadCaseExpr='1.0*DeadL+1.0*Wind_WE',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])

SLS05_b=graphical_reports.RecordLoadCaseDisp(loadCaseName='SLS05_b',loadCaseDescr='SLS05_b: 1.0*D + W_NS',loadCaseExpr='1.0*DeadL+1.0*Wind_NS',setsToDispLoads=[ramp],setsToDispDspRot=[ramp],setsToDispIntForc=[ramp])


LC=[D,Lru,Lrs,Lpu,Lps,S,W_WE,W_NS]
for lc in LC:
    lc.unitsScaleLoads=1e-3
    lc.unitsScaleDispl=1e3
    lc.unitsDispl='[mm]'
    lc.unitsScaleMom=1e-3
    lc.unitsMom='[m.kN]'
    lc.unitsScaleForc=1e-3
    lc.unitsForc='[kN]'
    lc.setsToDispBeamIntForc=[beams,columns]
    lc.listBeamIntForc=['My','Mz','Qy','Qz','N']
    lc.cameraParameters= vtk_graphic_base.CameraParameters('XYZPos')
    lc.setsToDispBeamLoads=[]
    lc.vectorScalePointLoads=0.005
    lc.compElLoad='transComponent'

#D.vectorScalePointLoads=1
    
ULS=[ULS01,ULS02_a,ULS02_b,ULS03_a,ULS03_b,ULS04_a,ULS04_b,ULS05_a,ULS05_b,ULS05_c,ULS05_d,ULS06_a,ULS06_b,ULS07_a,ULS07_b]
for lc in ULS:
    lc.setsToDispDspRot=[]#[ramp]
    lc.setsToDispIntForc=[]
    lc.unitsScaleLoads=1e-3
    lc.unitsScaleDispl=1e3
    lc.unitsDispl='[mm]'
    lc.unitsScaleMom=1e-3
    lc.unitsMom='[m.kN]'
    lc.unitsScaleForc=1e-3
    lc.unitsForc='[kN]'
#    lc.setsToDispBeamIntForc=[beams]
#    lc.listBeamIntForc=['My','Qz']
    lc.setsToDispBeamIntForc=[columns]
    lc.listBeamIntForc=['N','My','Mz','Qy','Qz']
    lc.cameraParameters= vtk_graphic_base.CameraParameters('XYZPos')
    lc.setsToDispBeamLoads=[]
    lc.vectorScalePointLoads=0.005
    lc.compElLoad='transYComponent'
    lc.compElLoad='axialComponent'

SLS=[SLS01,SLS02_a,SLS02_b,SLS03_a,SLS03_b,SLS04_a,SLS04_b,SLS05_a,SLS05_b]
for lc in SLS:
    lc.setsToDispDspRot=[]#[ramp]
    lc.setsToDispIntForc=[]
    lc.unitsScaleLoads=1e-3
    lc.unitsScaleDispl=1e3
    lc.unitsDispl='[mm]'
    lc.unitsScaleMom=1e-3
    lc.unitsMom='[m.kN]'
    lc.unitsScaleForc=1e-3
    lc.unitsForc='[kN]'

    # lc.setsToDispBeamIntForc=[beams]
    # lc.listBeamIntForc=['My','Qz']
    lc.setsToDispBeamIntForc=[columns]
    lc.listBeamIntForc=['N','My','Mz','Qy','Qz']
    lc.setsToDispBeamIntForc=[beams]
    lc.listBeamIntForc=['My','Qz']
#    lc.setsToDispBeamIntForc=[columns]
#    lc.listBeamIntForc=['N','My','Mz','Qy','Qz']
    lc.listBeamIntForc=['My']#,'Qz']
    lc.cameraParameters= vtk_graphic_base.CameraParameters('XYZPos')
    lc.setsToDispBeamLoads=[]
    lc.vectorScalePointLoads=0.005
    lc.compElLoad='transYComponent'
    lc.compElLoad='axialComponent'
'''
