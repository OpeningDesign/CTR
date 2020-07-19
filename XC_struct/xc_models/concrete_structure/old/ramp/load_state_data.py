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

