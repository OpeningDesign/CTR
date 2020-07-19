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
from materials.sections import section_properties as sp
from solution import predefined_solutions
from actions import load_cases
from actions import combinations as combs

inchToMeter= 2.54/100.0
feetToMeter= 0.3048
psfTokNm2= 0.04788026
psfToNm2= 1e3*psfTokNm2
centerSpacingTrusses= 24.0*inchToMeter
centerSpacingJoists= 32.0*inchToMeter
joistLoadFactor= centerSpacingJoists/centerSpacingTrusses

# Load data.
upperChordDeadLoad= 10*centerSpacingTrusses*psfToNm2
upperChordLiveLoad= 40*centerSpacingTrusses*psfToNm2
lowerChordDeadLoad= 5*centerSpacingTrusses*psfToNm2

#########################################################
# Problem definition.
feProblem= xc.FEProblem()
preprocessor= feProblem.getPreprocessor
modelSpace= predefined_spaces.StructuralMechanics3D(preprocessor.getNodeHandler)

#########################################################
# Material definition.
## Material itself.
wood= typical_materials.MaterialData(name= 'wood',E=13.1e9,nu=0.33,rho=500)
## Geometry of the bars.
### Geometry of the upper chord section.
upperChordPlg= geom.Polygon2d()
upperChordPlg.appendVertex(geom.Pos2d(2*inchToMeter,0.0))
upperChordPlg.appendVertex(geom.Pos2d(2*inchToMeter,2.0*inchToMeter))
upperChordPlg.appendVertex(geom.Pos2d(centerSpacingTrusses/2.0,2.0*inchToMeter))
upperChordPlg.appendVertex(geom.Pos2d(centerSpacingTrusses/2.0,(2.0+3/4.0)*inchToMeter))
upperChordPlg.appendVertex(geom.Pos2d(-centerSpacingTrusses/2.0,(2.0+3/4.0)*inchToMeter))
upperChordPlg.appendVertex(geom.Pos2d(-centerSpacingTrusses/2.0,2.0*inchToMeter))
upperChordPlg.appendVertex(geom.Pos2d(-2*inchToMeter,2.0*inchToMeter))
upperChordPlg.appendVertex(geom.Pos2d(-2*inchToMeter,0.0))
centroidOffset= upperChordPlg.getCenterOfMass().y-inchToMeter
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

depthC= 22*inchToMeter-lowerChordSectionGeometry.h+centroidOffset
depthD= 22*inchToMeter-lowerChordSectionGeometry.h+centroidOffset
panelSize= 60*inchToMeter


#########################################################
# Mesh generation.

## Truss C
lowerChordAxisC= geom.Segment3d(geom.Pos3d(0.0,0.0,0.0),geom.Pos3d(9.82345-0.8,0.0,0.0))
upperChordAxisC= geom.Segment3d(geom.Pos3d(0.0,0.0,depthC),geom.Pos3d(9.82345-0.8,0.0,depthC))
trussC= truss_generators.FanTruss(lowerChordAxisC, upperChordAxisC, trussModule= panelSize)
trussC.name= '2C'
trussC.lowerChordMaterial= lowerChordSection
trussC.upperChordMaterial= upperChordSection
trussC.diagonalMaterial= diagonalsMaterial
trussC.diagonalArea= diagonalSectionsGeometry.A()
trussC.postsMaterial= postsSection

trussC.genMesh(feProblem)

## Truss D
trussDGap= depthC-depthD
lowerChordAxisD= geom.Segment3d(geom.Pos3d(12.4422-0.8,0.0,trussDGap),geom.Pos3d(21.80845-1.6,0.0,trussDGap))
upperChordAxisD= geom.Segment3d(geom.Pos3d(12.4422-0.8,0.0,depthD+trussDGap),geom.Pos3d(21.80845-1.6,0.0,depthD+trussDGap))
trussD= truss_generators.FanTruss(lowerChordAxisD, upperChordAxisD, trussModule= panelSize)
trussD.name= '2D'
trussD.lowerChordMaterial= lowerChordSection
trussD.upperChordMaterial= upperChordSection
trussD.diagonalMaterial= diagonalsMaterial
trussD.diagonalArea= diagonalSectionsGeometry.A()
trussD.postsMaterial= postsSection

trussD.genMesh(feProblem)

## Sheathing (in tension between trusses)
points= preprocessor.getMultiBlockTopology.getPoints
sheathing_A= trussC.getUpperChordFrontEndPoint()
sheathing_B= trussD.getUpperChordBackEndPoint()
sheathing_l= preprocessor.getMultiBlockTopology.getLines.newLine(sheathing_A.tag,sheathing_B.tag)
sheathingTrf= trussD.crdTransf
E= 2e6*6894.76 # Modulus of elasticity (Pa)
sheathingMat= typical_materials.MaterialData(name='sheathing',E=E,nu=0.2,rho=500)
sheathingSectionGeometry= sp.RectangularSection('sheathingSection',0.75*inchToMeter,centerSpacingTrusses)
sheathingSection=  sheathingSectionGeometry.defElasticShearSection3d(preprocessor,sheathingMat)
seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultMaterial= sheathingSection.name
seedElemHandler.defaultTransformation= sheathingTrf.name
elem= seedElemHandler.newElement("ElasticBeam3d",xc.ID([0,0]))
sheathing_l.genMesh(xc.meshDir.I)

## Joist
trussCUpperChordFrontEnd= trussC.getUpperChordFrontEndPoint()
trussDUpperChordBackEnd= trussD.getUpperChordBackEndPoint()
joist_A= points.newPntFromPos3d(trussCUpperChordFrontEnd.getPos)
joist_B= points.newPntFromPos3d(trussDUpperChordBackEnd.getPos)
joist_l= preprocessor.getMultiBlockTopology.getLines.newLine(joist_A.tag,joist_B.tag)
joistTrf= trussD.crdTransf
E= 2e6*6894.76 # Modulus of elasticity (Pa)
lvl= typical_materials.MaterialData(name='LVL',E=E,nu=0.2,rho=500)
joistSectionGeometry= sp.RectangularSection('joistSection',3.5*0.0254,6*0.0254)
joistSection=  joistSectionGeometry.defElasticShearSection3d(preprocessor,lvl)
seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultMaterial= joistSection.name
seedElemHandler.defaultTransformation= joistTrf.name
elem= seedElemHandler.newElement("ElasticBeam3d",xc.ID([0,0]))
joist_l.genMesh(xc.meshDir.I)

#########################################################
# Boundary conditions.

## Truss A
trussC.fixNodes(modelSpace)

## Truss B
trussD.fixNodes(modelSpace)

## Joist
modelSpace.constraints.newEqualDOF(trussCUpperChordFrontEnd.getNode().tag,joist_A.getNode().tag,xc.ID([0,1,2,3]))
modelSpace.constraints.newEqualDOF(trussDUpperChordBackEnd.getNode().tag,joist_B.getNode().tag,xc.ID([1,2,3]))

# Sets

## Upper chord
upperChordSet= preprocessor.getSets.defSet("upperChordSet")
for l in trussC.upperChordSet.getLines:
    upperChordSet.getLines.append(l)
for l in trussD.upperChordSet.getLines:
    upperChordSet.getLines.append(l)
upperChordSet.getLines.append(joist_l)
upperChordSet.fillDownwards()

## Lower chord
lowerChordSet= preprocessor.getSets.defSet("lowerChordSet")
for l in trussC.lowerChordSet.getLines:
    lowerChordSet.getLines.append(l)
for l in trussD.lowerChordSet.getLines:
    lowerChordSet.getLines.append(l)
lowerChordSet.fillDownwards()

## Both chords
chordSet= upperChordSet+lowerChordSet
lowerChordSet.fillDownwards()

#########################################################
# Actions
loadCaseManager= load_cases.LoadCaseManager(preprocessor)
loadCaseNames= ['selfWeight','deadLoad','liveLoad','snowLoad','windLoad']
loadCaseManager.defineSimpleLoadCases(loadCaseNames)

## Self weight.
selfWeight= loadCaseManager.setCurrentLoadCase('selfWeight')
gravity= xc.Vector([0.0,0.0,9.81]) #Acceleration of gravity (m/s2)
trussC.createSelfWeightLoads(grav= gravity)
trussD.createSelfWeightLoads(grav= gravity)
joist_l.createInertiaLoads(gravity)

## Dead load.
roofDeadLoad= xc.Vector([0.0,0.0,-1.34e3*centerSpacingTrusses])
cLC= loadCaseManager.setCurrentLoadCase('deadLoad')
for e in trussC.upperChordSet.elements:
  e.vector3dUniformLoadGlobal(roofDeadLoad)
for e in trussD.upperChordSet.elements:
  e.vector3dUniformLoadGlobal(roofDeadLoad)
for e in joist_l.elements:
  e.vector3dUniformLoadGlobal(joistLoadFactor*roofDeadLoad)

## Live load.
roofLiveLoad= xc.Vector([0.0,0.0,-1.92e3*centerSpacingTrusses])
cLC= loadCaseManager.setCurrentLoadCase('liveLoad')
for e in trussC.upperChordSet.elements:
  e.vector3dUniformLoadGlobal(roofLiveLoad)
for e in trussD.upperChordSet.elements:
  e.vector3dUniformLoadGlobal(roofLiveLoad)
for e in joist_l.elements:
  e.vector3dUniformLoadGlobal(joistLoadFactor*roofLiveLoad)

## Snow load.
roofSnowLoad= xc.Vector([0.0,0.0,0.0*centerSpacingTrusses])
cLC= loadCaseManager.setCurrentLoadCase('snowLoad')
# for e in trussC.upperChordSet.elements:
#   e.vector3dUniformLoadGlobal(roofSnowLoad)
# for e in trussD.upperChordSet.elements:
#   e.vector3dUniformLoadGlobal(roofSnowLoad)
# for e in joist_l.elements:
#   e.vector3dUniformLoadGlobal(joistLoadFactor*roofSnowLoad)

## Wind load.
roofWindLoad= xc.Vector([0.0,0.0,0.0*centerSpacingTrusses])
cLC= loadCaseManager.setCurrentLoadCase('windLoad')
# for e in trussC.upperChordSet.elements:
#   e.vector3dUniformLoadGlobal(roofWindLoad)
# for e in trussD.upperChordSet.elements:
#   e.vector3dUniformLoadGlobal(roofWindLoad)
# for e in joist_l.elements:
#   e.vector3dUniformLoadGlobal(joistLoadFactor*roofWindLoad)

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
#### Equation 16-14-> doesn't apply
#### Equation 16-15
combContainer.SLS.qp.add('EQ1615', '0.6*selfWeight+0.6*deadLoad+0.6*windLoad')
#### Equation 16-16 -> doesn't apply
#### LIVE load only.
combContainer.SLS.qp.add('LIVE', '1.0*liveLoad')

xcTotalSet= preprocessor.getSets.getSet("total")

def reportResults(combName):
    writeResults(combName,'2nd floor',[trussC,trussD])

    

