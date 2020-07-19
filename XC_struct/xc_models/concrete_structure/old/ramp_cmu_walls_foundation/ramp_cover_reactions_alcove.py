# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

import math
import vtk
import xc_base
import geom
import xc
from solution import predefined_solutions
from model import predefined_spaces
from materials import typical_materials
from materials.aci import ACI_materials

from materials.sections import section_properties
from actions import load_cases as lcm
from actions import combinations as combs

# Problem type
precastPlanks= xc.FEProblem()
precastPlanks.title= 'Precast planks on ramp cover with alcove'
preprocessor= precastPlanks.getPreprocessor   
nodes= preprocessor.getNodeHandler

#Materials
## Concrete material
concrete= ACI_materials.c4000

## Rectangular cross-section definition
plankSectionGeometry= section_properties.RectangularSection(name="plankSection",b=1.0,h=.30) # Section geometry.
plankSectionMaterial= concrete.getElasticMaterialData() # Section material.
plankSection= plankSectionGeometry.defElasticShearSection2d(preprocessor,plankSectionMaterial)

# Model geometry
#Units
foot2m= 0.3048
inch2m= 0.0254

## Points.
d1= 9*foot2m+2*inch2m
d2= 15*foot2m+3*inch2m-d1
span1= 6.20683636363636
span1= 6.20683636363636
span2= 5*0.3048

print('d1= ', d1, ' m')
print('d2= ', d2, ' m')
print('span1= ', span1, ' m')
print('span2= ', span2, ' m')

pointHandler= preprocessor.getMultiBlockTopology.getPoints
p0= pointHandler.newPntFromPos3d(geom.Pos3d(0.0,0.0,0.0))
p1= pointHandler.newPntFromPos3d(geom.Pos3d(d1,0.0,0.0))
p2= pointHandler.newPntFromPos3d(geom.Pos3d(d1+d2,0.0,0.0))
p3a= pointHandler.newPntFromPos3d(geom.Pos3d(span1,0.0,0.0))
p3b= pointHandler.newPntFromPos3d(geom.Pos3d(span1,0.0,0.0))
p4= pointHandler.newPntFromPos3d(geom.Pos3d(span1+span2,0.0,0.0))

## Lines
lineHandler= preprocessor.getMultiBlockTopology.getLines
l1= lineHandler.newLine(p0.tag,p1.tag)
l2= lineHandler.newLine(p1.tag,p2.tag)
l3= lineHandler.newLine(p2.tag,p3a.tag)
l4= lineHandler.newLine(p3b.tag,p4.tag)

# Mesh
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)

trfs= preprocessor.getTransfCooHandler
lin= trfs.newLinearCrdTransf2d("lin")
seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultMaterial= plankSection.name
seedElemHandler.defaultTransformation= "lin"
elem= seedElemHandler.newElement("ElasticBeam2d",xc.ID([0,0]))

xcTotalSet= preprocessor.getSets.getSet('total')
mesh= xcTotalSet.genMesh(xc.meshDir.I)

# Constraints
modelSpace.fixNode00F(p0.getNode().tag)
modelSpace.fixNode00F(p3a.getNode().tag)
modelSpace.fixNode00F(p3b.getNode().tag)
modelSpace.fixNode00F(p4.getNode().tag)

# Loads
loadManager= preprocessor.getLoadHandler
loadCases= loadManager.getLoadPatterns
## Load modulation.
ts= loadCases.newTimeSeries("constant_ts","ts")
loadCases.currentTimeSeries= "ts"

## Load case definition
loadCaseManager= lcm.LoadCaseManager(preprocessor)
loadCaseNames= ['deadLoad','liveLoad','snowLoad','windLoad']
loadCaseManager.defineSimpleLoadCases(loadCaseNames)

## Dead load.
cLC= loadCaseManager.setCurrentLoadCase('deadLoad')
pfsToN_m2= 0.04788026e3
deadLoad= 4914+20.0*pfsToN_m2
for e in xcTotalSet.elements:
    e.vector2dUniformLoadGlobal(xc.Vector([0.0,-deadLoad]))
p1.getNode().newLoad(xc.Vector([0.0,-13.02e3,0.0])) # WL16
p2.getNode().newLoad(xc.Vector([0.0,-21.49e3,0.0])) # WL3

## Live load.
cLC= loadCaseManager.setCurrentLoadCase('liveLoad')
liveLoad= 40.0*pfsToN_m2
for e in xcTotalSet.elements:
    e.vector2dUniformLoadGlobal(xc.Vector([0.0,-liveLoad]))
p1.getNode().newLoad(xc.Vector([0.0,-18.12e3,0.0])) # WL16
p2.getNode().newLoad(xc.Vector([0.0,-31.36e3,0.0])) # WL3

## Snow load.
cLC= loadCaseManager.setCurrentLoadCase('snowLoad')
p1.getNode().newLoad(xc.Vector([0.0,-12.92e3,0.0])) # WL16
p2.getNode().newLoad(xc.Vector([0.0,-12.92e3,0.0])) # WL3

## Wind load.
cLC= loadCaseManager.setCurrentLoadCase('windLoad')
p1.getNode().newLoad(xc.Vector([0.0,8.17e3,0.0])) # WL16
p2.getNode().newLoad(xc.Vector([0.0,8.17e3,0.0])) # WL3

#Load combinations
combContainer= combs.CombContainer()

#Quasi-permanent situations.
combContainer.SLS.qp.add('ELS00', '1.0*selfWeight+1.0*deadLoad+0.5*liveLoad')

# Service limit states.
# 'selfWeight','deadLoad','liveLoad','snowLoad','windLoad','quakeLoad']
#Equation 16-8
combContainer.ULS.perm.add('EQ1608', '1.0*deadLoad')
#Equation 16-9
combContainer.ULS.perm.add('EQ1609', '1.0*deadLoad+1.0*liveLoad')
#Equation 16-10
combContainer.ULS.perm.add('EQ1610', '1.0*deadLoad+1.0*snowLoad')
#Equation 16-11
combContainer.ULS.perm.add('EQ1611', '1.0*deadLoad+0.75*liveLoad+0.75*snowLoad')
#Equation 16-12
combContainer.ULS.perm.add('EQ1612', '1.0*deadLoad+0.6*windLoad')
#Equation 16-13
combContainer.ULS.perm.add('EQ1613', '1.0*deadLoad+0.45*windLoad+0.75*liveLoad+0.75*snowLoad')
#Equation 16-14-> doesn' apply
#Equation 16-15
combContainer.ULS.perm.add('EQ1615', '0.6*deadLoad+0.6*windLoad')
#Equation 16-16 -> doesn't apply


#Strength ultimate states. (type 2).
# 'selfWeight','deadLoad','liveLoad','snowLoad','windLoad','quakeLoad']
#Equation 16-1
combContainer.ULS.perm.add('EQ1601', '1.4*deadLoad')
#Equation 16-2
combContainer.ULS.perm.add('EQ1602', '1.2*deadLoad+1.6*liveLoad+0.5*snowLoad')
#Equation 16-3
combContainer.ULS.perm.add('EQ1603A', '1.2*deadLoad+1.6*snowLoad+0.5*liveLoad')
combContainer.ULS.perm.add('EQ1603B', '1.2*deadLoad+1.6*snowLoad+0.5*windLoad')
#Equation 16-4
combContainer.ULS.perm.add('EQ1604', '1.2*deadLoad+1.0*windLoad+0.5*liveLoad+0.5*snowLoad')
#Equation 16-5
combContainer.ULS.perm.add('EQ1605', '1.2*deadLoad+0.5*liveLoad+0.7*snowLoad')
#Equation 16-6 -> doesn't apply
#Equation 16-7 -> doesn't apply


