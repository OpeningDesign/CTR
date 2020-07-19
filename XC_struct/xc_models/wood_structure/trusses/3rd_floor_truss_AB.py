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
centerSpacing= 12.0*inchToMeter
depth= (24-2)*inchToMeter

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

## Truss A
lowerChordAxisA= geom.Segment3d(geom.Pos3d(0.0,0.0,0.0),geom.Pos3d(11.223,0.0,0.0))
upperChordAxisA= geom.Segment3d(geom.Pos3d(0.0,0.0,depth),geom.Pos3d(11.223,0.0,depth))
trussA= truss_generators.FanTruss(lowerChordAxisA, upperChordAxisA, trussModule= panelSize)
trussA.name= '2A'
trussA.lowerChordMaterial= lowerChordSection
trussA.upperChordMaterial= upperChordSection
trussA.diagonalMaterial= diagonalsMaterial
trussA.diagonalArea= diagonalSectionsGeometry.A()
trussA.postsMaterial= postsSection

trussA.genMesh(feProblem)

## Truss B
lowerChordAxisB= geom.Segment3d(geom.Pos3d(11.223,0.0,0.0),geom.Pos3d(21.9888,0.0,0.0))
upperChordAxisB= geom.Segment3d(geom.Pos3d(11.223,0.0,depth),geom.Pos3d(21.9888,0.0,depth))
trussB= truss_generators.FanTruss(lowerChordAxisB, upperChordAxisB, trussModule= panelSize)
trussB.name= '2B'
trussB.lowerChordMaterial= lowerChordSection
trussB.upperChordMaterial= upperChordSection
trussB.diagonalMaterial= diagonalsMaterial
trussB.diagonalArea= diagonalSectionsGeometry.A()
trussB.postsMaterial= postsSection

trussB.genMesh(feProblem)

#########################################################
# Boundary conditions.

## Truss A
trussA.fixNodes(modelSpace)

## Truss B
trussB.fixNodes(modelSpace)

# Sets

## Upper chord
upperChordSet= preprocessor.getSets.defSet("upperChordSet")
for l in trussA.upperChordSet.getLines:
    upperChordSet.getLines.append(l)
for l in trussB.upperChordSet.getLines:
    upperChordSet.getLines.append(l)
upperChordSet.fillDownwards()

## Lower chord
lowerChordSet= preprocessor.getSets.defSet("lowerChordSet")
for l in trussA.lowerChordSet.getLines:
    lowerChordSet.getLines.append(l)
for l in trussB.lowerChordSet.getLines:
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
trussA.createSelfWeightLoads(grav= gravity)
trussB.createSelfWeightLoads(grav= gravity)

## Dead load.
secondflDeadLoad= xc.Vector([0.0,0.0,-1.34e3*centerSpacing])
cLC= loadCaseManager.setCurrentLoadCase('deadLoad')
for e in trussA.upperChordSet.elements:
  e.vector3dUniformLoadGlobal(secondflDeadLoad)
for e in trussB.upperChordSet.elements:
  e.vector3dUniformLoadGlobal(secondflDeadLoad)

## Live load.
secondflLiveLoad= xc.Vector([0.0,0.0,-1.92e3*centerSpacing])
cLC= loadCaseManager.setCurrentLoadCase('liveLoad')
for e in trussA.upperChordSet.elements:
  e.vector3dUniformLoadGlobal(secondflLiveLoad)
for e in trussB.upperChordSet.elements:
  e.vector3dUniformLoadGlobal(secondflLiveLoad)

## Snow load.
secondflSnowLoad= xc.Vector([0.0,0.0,0.0*centerSpacing])
cLC= loadCaseManager.setCurrentLoadCase('snowLoad')
# for e in trussA.upperChordSet.elements:
#   e.vector3dUniformLoadGlobal(secondflSnowLoad)
# for e in trussB.upperChordSet.elements:
#   e.vector3dUniformLoadGlobal(secondflSnowLoad)

## Wind load.
secondflWindLoad= xc.Vector([0.0,0.0,0.0*centerSpacing])
cLC= loadCaseManager.setCurrentLoadCase('windLoad')
# for e in trussA.upperChordSet.elements:
#   e.vector3dUniformLoadGlobal(secondflWindLoad)
# for e in trussB.upperChordSet.elements:
#   e.vector3dUniformLoadGlobal(secondflWindLoad)

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

xcTotalSet= preprocessor.getSets.getSet("total")

def reportResults(combName):
    writeResults(combName,'2nd floor',[trussA,trussB])
    
