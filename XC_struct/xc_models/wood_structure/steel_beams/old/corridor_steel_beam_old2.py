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
steel= ASTM_materials.A572
steel.gammaM= 1.00
## Profile geometry
profile= ASTM_materials.WShape(steel,'W14X30')
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

## Loads on elements.
centerSpacing= 24.0*inch2m # Distance between trusses
uniformLoadD= 20.44e3
uniformLoadL= 29.95e3
uniformLoadS= 12.05e3
uniformLoadW= -7.61e3
uniformLoadMax= 31.66e3/centerSpacing
uniformLoad= uniformLoadMax
cLC= loadCaseManager.setCurrentLoadCase('load')
beamLoad= xc.Vector([0.0,-uniformLoad])
for e in xcTotalSet.elements:
  e.vector2dUniformLoadGlobal(beamLoad)

#Load from P3.7 and P3.1 columns
midSpan= span1+span2/2
midPos= geom.Pos3d(midSpan,0.0,0.0)
nMidSpan= xcTotalSet.getNearestNode(midPos)
nMidSpan.newLoad(xc.Vector([0.0,-60e3,0.0]))

#We add the load case to domain.
preprocessor.getLoadHandler.getLoadPatterns.addToDomain('load')

# Solution
# Linear static analysis.
analysis= predefined_solutions.simple_static_linear(halfSteelBeam)
result= analysis.analyze(1)

# Checking
n1= l1.getNearestNode(midPos)
d1= n1.getDisp[1]
nodes.calculateNodalReactions(True,1e-7)
xcTotalSet= preprocessor.getSets.getSet('total')
VMax= -1e23
VMin= -VMax
MMax= -1e23
MMin= -MMax
for e in xcTotalSet.elements:
  VMax= max(VMax,max(e.getV1, e.getV2))
  VMin= min(VMin,min(e.getV1, e.getV2))
  MMax= max(MMax,max(e.getM1, e.getM2))
  MMin= min(MMin,min(e.getM1, e.getM2))
Vmax= max(VMax,abs(VMin))
Mmax= max(MMax,abs(MMin))
eMidSpan= xcTotalSet.getNearestElement(midPos)

print('Uniform load: ', uniformLoad/1e3, ' kN/m')

## Deflection
ratio1= abs(d1)/span2
print('dY= ',d1*1e3,' mm; ratio= L/', 1/ratio1, 'L= ', span2, ' m')

## Shear
Vu= profile.steelType.fy/math.sqrt(3.0)*profile.get('Avy')/1.67
print('Vmax= ', Vmax/1e3, ' kN Vu= ', Vu/1e3, ' kN; F= ',Vmax/Vu)

## Bending
Mu= profile.getWz()*profile.steelType.fy/1.67#250e6
print('Mmax= ', Mmax/1e3, ' kN m Mu= ', Mu/1e3, ' kN m; F= ',Mmax/Mu)

## Reactions.
R1= p1.getNode().getReaction[1]
R2= p2.getNode().getReaction[1]

print('R1= ', R1/1e3,' kN')
print('R2= ', R2/1e3,' kN')
