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
from materials.astm_aisc import ASTM_materials

from materials.sections import structural_steel as steel
from materials.sections.structural_shapes import aisc_metric_shapes as shapes
from actions import load_cases as lcm
from actions import combinations as combs

#Units
foot2m= 0.3048
inch2m= 0.0254

# Problem type
halfSteelBeam= xc.FEProblem()
halfSteelBeam.title= 'Steel beams at 2dn floor'
preprocessor= halfSteelBeam.getPreprocessor   
nodes= preprocessor.getNodeHandler

#Materials
## Steel material
steel= ASTM_materials.A36
steel.gammaM= 1.00
## Profile geometry
profile= ASTM_materials.WShape(steel,'W10X26')
#profile= ASTM_materials.CShape(steel,'C10X20')
xcSection= profile.defElasticShearSection2d(preprocessor)

# Model geometry

## Points.
span1= 3*foot2m+4*inch2m+13/16*inch2m
span2= 13.0*foot2m+5.0/16.0*inch2m
print('span1= ', span1, ' m')
print('span2= ', span2, ' m')

pointHandler= preprocessor.getMultiBlockTopology.getPoints
p0= pointHandler.newPntFromPos3d(geom.Pos3d(0.0,0.0,0.0))
p1= pointHandler.newPntFromPos3d(geom.Pos3d(span1,0.0,0.0))
p2= pointHandler.newPntFromPos3d(geom.Pos3d(span1+span2,0.0,0.0))

## Lines
lineHandler= preprocessor.getMultiBlockTopology.getLines
l1= lineHandler.newLine(p0.tag,p1.tag)
l1= lineHandler.newLine(p1.tag,p2.tag)

# Mesh
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)
trfs= preprocessor.getTransfCooHandler
lin= trfs.newLinearCrdTransf2d("lin")
seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultMaterial= xcSection.name
seedElemHandler.defaultTransformation= "lin"
elem= seedElemHandler.newElement("ElasticBeam2d",xc.ID([0,0]))

xcTotalSet= preprocessor.getSets.getSet('total')
mesh= xcTotalSet.genMesh(xc.meshDir.I)

# Constraints
modelSpace.fixNode00F(p1.getNode().tag)
modelSpace.fixNode00F(p2.getNode().tag)


# Actions
loadCaseManager= lcm.LoadCaseManager(preprocessor)
loadCaseNames= ['load']
loadCaseManager.defineSimpleLoadCases(loadCaseNames)

## Loads on nodes.
centerSpacing= 24.0*inch2m # Distance between trusses
uniformLoad= 20.978e3/centerSpacing
cLC= loadCaseManager.setCurrentLoadCase('load')
beamLoad= xc.Vector([0.0,-uniformLoad])
for e in xcTotalSet.elements:
  e.vector2dUniformLoadGlobal(beamLoad)

#We add the load case to domain.
preprocessor.getLoadHandler.getLoadPatterns.addToDomain('load')

# Solution
# Linear static analysis.
analysis= predefined_solutions.simple_static_linear(halfSteelBeam)
result= analysis.analyze(1)

# Checking
midSpan= span1+span2/2
midPos= geom.Pos3d(midSpan,0.0,0.0)
n1= l1.getNearestNode(midPos)
d1= n1.getDisp[1]
nodes.calculateNodalReactions(True,1e-7)
Vmax= max(p0.getNode().getReaction[1],p1.getNode().getReaction[1])
eMidSpan= xcTotalSet.getNearestElement(midPos)
Mmax= max(abs(eMidSpan.getM1),abs(eMidSpan.getM2))

## Deflection
ratio1= abs(d1)/span2
print('dY= ',d1*1e3,' mm; ratio= L/', 1/ratio1)

## Shear
Vu= profile.steelType.fy/math.sqrt(3.0)*profile.get('Avy')
print('Vmax= ', Vmax/1e3, ' kN Vu= ', Vu/1e3, ' kN; F= ',Vmax/Vu)

## Bending
Mu= profile.getWz()*profile.steelType.fy#250e6
print('Mmax= ', Mmax/1e3, ' kN m Mu= ', Mu/1e3, ' kN m; F= ',Mmax/Mu)

from rough_calculations import ng_simple_beam

beam= ng_simple_beam.SimpleBeam()
beam.l= span2
beam.E= profile.steelType.E
beam.I= profile.Iz()
print(beam.getDeflectionUnderUniformLoad(uniformLoad,span2/2.0)*1e3)
print(beam.getBendingMomentUnderUniformLoad(uniformLoad,span2/2.0)/1e3)
