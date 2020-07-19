# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division
import xc_base
import geom
import xc
from model import predefined_spaces
from model.geometry import truss_generators
from materials import typical_materials
from materials.sections import section_properties
from solution import predefined_solutions
from actions import load_cases
from actions import combinations as combs
from postprocess import output_handler
from postprocess.xcVtk import vtk_graphic_base

inchToMeter= 2.54/100.0
feetToMeter= 0.3048
psfTokNm2= 0.04788026
psfToNm2= 1e3*psfTokNm2
centerSpacing= 12.0*inchToMeter
depth= (22-2)*inchToMeter
poundToN= 4.44822

# Load data.
upperChordDeadLoad= 10*centerSpacing*psfToNm2
upperChordLiveLoad= 40*centerSpacing*psfToNm2
lowerChordDeadLoad= 5*centerSpacing*psfToNm2

#########################################################
# Problem definition.
feProblem= xc.FEProblem()
preprocessor= feProblem.getPreprocessor
modelSpace= predefined_spaces.StructuralMechanics3D(preprocessor.getNodeHandler)

#########################################################
# Material definition.
## Material itself.
wood= typical_materials.MaterialData(name= 'wood',E=12.4e9,nu=0.33,rho=500)
## Geometry of the bars.
### Geometry of the upper chord section.
upperChordPlg= geom.Polygon2d()
upperChordPlg.appendVertex(geom.Pos2d(2*inchToMeter,0.0))
upperChordPlg.appendVertex(geom.Pos2d(2*inchToMeter,2.0*inchToMeter))
upperChordPlg.appendVertex(geom.Pos2d(centerSpacing/2.0,2.0*inchToMeter))
upperChordPlg.appendVertex(geom.Pos2d(centerSpacing/2.0,(2.0+3/4.0)*inchToMeter))
upperChordPlg.appendVertex(geom.Pos2d(-centerSpacing/2.0,(2.0+3/4.0)*inchToMeter))
upperChordPlg.appendVertex(geom.Pos2d(-centerSpacing/2.0,2.0*inchToMeter))
upperChordPlg.appendVertex(geom.Pos2d(-2*inchToMeter,2.0*inchToMeter))
upperChordPlg.appendVertex(geom.Pos2d(-2*inchToMeter,0.0))
centroidOffset= upperChordPlg.getCenterOfMass().y-inchToMeter
#print(centroidOffset)
upperChordSectionGeometry= section_properties.PolygonalSection("upperChordGeom",upperChordPlg)

lumber4x2Geom= section_properties.RectangularSection("lumber4x2Geom",b=3.5*inchToMeter,h=1.5*inchToMeter)
lowerChordSectionGeometry= lumber4x2Geom
diagonalSectionsGeometry= lumber4x2Geom
## XC materials definition
### Material for beam-column elements
upperChordSection= upperChordSectionGeometry.defElasticShearSection3d(preprocessor,wood)
lowerChordSection= lowerChordSectionGeometry.defElasticShearSection3d(preprocessor,wood)
postsSection= lowerChordSection
### Material for truss elements
diagonalsMaterial= typical_materials.defElasticMaterial(preprocessor,"diagonalsMaterial",wood.E, rho= wood.rho)

depth= 24*inchToMeter-lowerChordSectionGeometry.h+centroidOffset
panelSize= 60*inchToMeter


#########################################################
# Mesh generation.

cantileverSpan= 2.0*feetToMeter+2.0*inchToMeter+1.5*inchToMeter

## Truss A
pA= geom.Pos3d(cantileverSpan,0.0,0.0)
pB= geom.Pos3d(11.223-0.8,0.0,0.0)
pC= geom.Pos3d(cantileverSpan,0.0,depth)
pD= geom.Pos3d(11.223-0.8,0.0,depth)
lowerChordAxisA= geom.Segment3d(pA,pB)
upperChordAxisA= geom.Segment3d(pC,pD)
trussA= truss_generators.FanTruss(lowerChordAxisA, upperChordAxisA, trussModule= panelSize)
trussA.name= '2A'
trussA.lowerChordMaterial= lowerChordSection
trussA.upperChordMaterial= upperChordSection
trussA.diagonalMaterial= diagonalsMaterial
trussA.diagonalArea= diagonalSectionsGeometry.A()
trussA.postsMaterial= postsSection

trussA.genMesh(feProblem)

## Cantilever
points= preprocessor.getMultiBlockTopology.getPoints  # Point container.
pt0L= points.newPntFromPos3d(geom.Pos3d(0.0,0.0,0.0)) # Low chord endpoint.
pt1L= points.getNearest(pA) # Low chord endpoint.
pt0U= points.newPntFromPos3d(geom.Pos3d(0.0,0.0,depth)) # Upper chord endpoint.
pt1U= points.getNearest(pC)

lines= preprocessor.getMultiBlockTopology.getLines  # Line container.
lC= lines.newLine(pt0L.tag,pt1L.tag) # Lower chord.
uC= lines.newLine(pt0U.tag,pt1U.tag) # Upper chord.
post= lines.newLine(pt0L.tag,pt0U.tag)
dg= lines.newLine(pt0U.tag,pt1L.tag)
dg.nDiv= 1

seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultMaterial= trussA.lowerChordMaterial.name  # Material name.
beam3d= seedElemHandler.newElement("ElasticBeam3d",xc.ID([0,0]))
lC.genMesh(xc.meshDir.I)
uC.genMesh(xc.meshDir.I)
seedElemHandler.defaultMaterial= trussA.postsMaterial.name  # Material name.
post.genMesh(xc.meshDir.I)
seedElemHandler.defaultMaterial= trussA.diagonalMaterial.name  # Material name.
seedElemHandler.dimElem= 3 #Bars defined ina a three-dimensional space.
trussElem= seedElemHandler.newElement('Truss',xc.ID([0,0]))
trussElem.sectionArea= trussA.diagonalArea
dg.genMesh(xc.meshDir.I)


#########################################################
# Boundary conditions.

## Cantilever
trussA.fixNodes(modelSpace)

# Sets

## Upper chord
upperChordSet= preprocessor.getSets.defSet("upperChordSet")
upperChordSet.getLines.append(uC)
for l in trussA.upperChordSet.getLines:
    upperChordSet.getLines.append(l)
upperChordSet.fillDownwards()

## Lower chord
lowerChordSet= preprocessor.getSets.defSet("lowerChordSet")
lowerChordSet.getLines.append(lC)
for l in trussA.lowerChordSet.getLines:
    lowerChordSet.getLines.append(l)
lowerChordSet.fillDownwards()

## Both chords
chordSet= upperChordSet+lowerChordSet
lowerChordSet.fillDownwards()

loadsOnCantilever= False
MiTekLoad= True

#########################################################
# Actions
loadCaseManager= load_cases.LoadCaseManager(preprocessor)
loadCaseNames= ['selfWeight','deadLoad','liveLoad','snowLoad','windLoad']
loadCaseManager.defineSimpleLoadCases(loadCaseNames)

## Self weight.
selfWeight= loadCaseManager.setCurrentLoadCase('selfWeight')
gravity= xc.Vector([0.0,0.0,-9.81]) #Acceleration of gravity (m/s2)
#cantilever.createSelfWeightLoads(grav= gravity)
trussA.createSelfWeightLoads(grav= gravity)

## Dead load.
secondflDeadLoad= xc.Vector([0.0,0.0,-1.34e3*centerSpacing])
cLC= loadCaseManager.setCurrentLoadCase('deadLoad')
for e in uC.elements:
  e.vector3dUniformLoadGlobal(secondflDeadLoad)
for e in trussA.upperChordSet.elements:
  e.vector3dUniformLoadGlobal(secondflDeadLoad)
n= pt0U.getNode()
if(loadsOnCantilever):
    n.newLoad(xc.Vector([0.0,0.0,-1044.55*poundToN,0.0,0.0,0.0]))
if(MiTekLoad):
    n.newLoad(xc.Vector([0.0,0.0,-2926.00*poundToN,0.0,0.0,0.0]))

## Live load.
secondflLiveLoad= xc.Vector([0.0,0.0,-1.92e3*centerSpacing])
cLC= loadCaseManager.setCurrentLoadCase('liveLoad')
for e in uC.elements:
  e.vector3dUniformLoadGlobal(secondflLiveLoad)
for e in trussA.upperChordSet.elements:
  e.vector3dUniformLoadGlobal(secondflLiveLoad)
if(loadsOnCantilever):
    n.newLoad(xc.Vector([0.0,0.0,-1107.39*poundToN,0.0,0.0,0.0]))

## Snow load.
secondflSnowLoad= xc.Vector([0.0,0.0,0.0*centerSpacing])
cLC= loadCaseManager.setCurrentLoadCase('snowLoad')
if(loadsOnCantilever):
    n.newLoad(xc.Vector([0.0,0.0,-772.87*poundToN,0.0,0.0,0.0]))

## Wind load.
secondflWindLoad= xc.Vector([0.0,0.0,0.0*centerSpacing])
cLC= loadCaseManager.setCurrentLoadCase('windLoad')
if(loadsOnCantilever):
    n.newLoad(xc.Vector([0.0,0.0,488.33*poundToN,0.0,0.0,0.0]))

#Load combinations
combContainer= combs.CombContainer()

## Serviceability limit states.

### 'selfWeight','deadLoad','trafficLoad','liveLoad','snowLoad','windLoad','quakeLoad']
#### Equation 16-8
combContainer.SLS.qp.add('EQ1608', '1.0*selfWeight+1.0*deadLoad')
#### Equation 16-9
combContainer.SLS.qp.add('EQ1609', '1.0*selfWeight+1.0*deadLoad+1.0*liveLoad')
#### Equation 16-10
combContainer.SLS.qp.add('EQ1610', '1.0*selfWeight+1.0*deadLoad+1.0*snowLoad')
#### Equation 16-11
combContainer.SLS.qp.add('EQ1611', '1.0*selfWeight+1.0*deadLoad+0.75*liveLoad+0.75*snowLoad')
#### Equation 16-12
combContainer.SLS.qp.add('EQ1612', '1.0*selfWeight+1.0*deadLoad+0.6*windLoad')
#### Equation 16-13
combContainer.SLS.qp.add('EQ1613', '1.0*selfWeight+1.0*deadLoad+0.45*windLoad+0.75*liveLoad+0.75*snowLoad')
#### Equation 16-14-> doesn' apply
#### Equation 16-15
combContainer.SLS.qp.add('EQ1615', '0.6*selfWeight+0.6*deadLoad+0.6*windLoad')
#### Equation 16-16 -> doesn't apply
#### LIVE load only.
combContainer.SLS.qp.add('LIVE', '1.0*liveLoad')
combContainer.dumpCombinations(preprocessor)

xcTotalSet= preprocessor.getSets.getSet("total")

preprocessor.getLoadHandler.addToDomain('LIVE')#EQ1615')
# Solution
# Linear static analysis.
analysis= predefined_solutions.simple_static_linear(feProblem)
result= analysis.analyze(1)

## Graphic stuff.
oh= output_handler.OutputHandler(modelSpace)

oh.outputStyle.cameraParameters= vtk_graphic_base.CameraParameters('Custom')
oh.outputStyle.cameraParameters.viewUpVc= [0,0,1]
oh.outputStyle.cameraParameters.posCVc= [0,-100,0]

#oh.displayBlocks()
#oh.displayLocalAxes(setToDisplay= xcTotalSet)
#oh.displayLocalAxes(setToDisplay= xcTotalSet)

#oh.displayFEMesh()
#oh.displayLoads(setToDisplay= xcTotalSet)

#oh.displayDispRot(itemToDisp='uY')
oh.displayDispRot(itemToDisp='uZ')
# oh.displayIntForcDiag(itemToDisp= 'Mz', setToDisplay= xcTotalSet)
# oh.displayIntForcDiag(itemToDisp= 'Vy', setToDisplay= xcTotalSet)
# oh.displayIntForcDiag(itemToDisp= 'Mz', setToDisplay= xcTotalSet)
# oh.displayReactions(setToDisplay= xcTotalSet)
# oh.displayIntForcDiag(itemToDisp= 'Vy', setToDisplay= xcTotalSet)
# oh.displayIntForcDiag(itemToDisp= 'Vy', setToDisplay= xcTotalSet)
# oh.displayIntForcDiag(itemToDisp= 'Vy', setToDisplay= xcTotalSet)
# oh.displayIntForcDiag(itemToDisp= 'Mz', setToDisplay= xcTotalSet)
#oh.displayReactions(setToDisplay= xcTotalSet)
#oh.displayIntForcDiag(itemToDisp= 'Vy', setToDisplay= xcTotalSet)


# def reportResults(combName):
#     writeResults(combName,'2nd floor',[cantilever,trussA])
