# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division
import xc_base
import geom
import xc
from model import predefined_spaces
from solution import predefined_solutions
from materials.sections import section_properties
from materials import typical_materials
from materials.awc_nds import structural_panels

# Loads
from actions import load_cases as lcm

# Units
inchToMeter= 2.54/100.0
footToMeter= 0.3048
poundToN= 4.44822
psiToPa= 6894.76
psfToNm2= 0.047880258888889e3

# Problem type
lvlBeam= xc.FEProblem()
lvlBeam.title= 'Third floor facade beam'
preprocessor= lvlBeam.getPreprocessor
nodes= preprocessor.getNodeHandler
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)

# Materials LVL 1.55E (page 10 of the PDF document from "SolidStart")
beam= structural_panels.LVLHeaderSections['3.5x18']
section= beam.defElasticShearSection2d(preprocessor)

# Beam geometry
beamSpan= 10.0*footToMeter

## Key points
pointHandler= preprocessor.getMultiBlockTopology.getPoints
p0= pointHandler.newPntFromPos3d(geom.Pos3d(0.0,0.0,0.0))
p1= pointHandler.newPntFromPos3d(geom.Pos3d(beamSpan,0.0,0.0))

## Lines
lineHandler= preprocessor.getMultiBlockTopology.getLines
l1= lineHandler.newLine(p0.tag,p1.tag)

# Mesh
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)
trfs= preprocessor.getTransfCooHandler
lin= trfs.newLinearCrdTransf2d("lin")
seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultMaterial= section.name
seedElemHandler.defaultTransformation= "lin"
elem= seedElemHandler.newElement("ElasticBeam2d",xc.ID([0,0]))

xcTotalSet= preprocessor.getSets.getSet('total')

mesh= xcTotalSet.genMesh(xc.meshDir.I)

# Constraints
modelSpace.fixNode00F(p0.getNode().tag)
modelSpace.fixNode00F(p1.getNode().tag)

# Actions
loadCaseManager= lcm.LoadCaseManager(preprocessor)
loadCaseNames= ['load']
loadCaseManager.defineSimpleLoadCases(loadCaseNames)

## Loads on elements.
cLC= loadCaseManager.setCurrentLoadCase('load')
selfWeight= beam.getLinearDensity()*9.81
wallHeight= 13*footToMeter+7.125*inchToMeter+2*(1*footToMeter+6*inchToMeter)
wallWeight= 12*psfToNm2
tributaryRoofWidth= 1*footToMeter
D= 15*47.88026+wallWeight*wallHeight+selfWeight # Dead load N/m
S= 42*47.88026 # Snow load N/m
tributaryLoad= D+S*tributaryRoofWidth #N/m
uniformLoad= xc.Vector([0.0,-tributaryLoad,0.0]) 
for e in xcTotalSet.elements:
  e.vector2dUniformLoadGlobal(uniformLoad)


#We add the load case to domain.
preprocessor.getLoadHandler.getLoadPatterns.addToDomain('load')

# Solution
# Linear static analysis.
analysis= predefined_solutions.simple_static_linear(lvlBeam)
result= analysis.analyze(1)

# Checking
print('*****',lvlBeam.title,'******')
print('Wall height: ', wallHeight, ' m')
print('Wall weight: ', wallWeight/1e3, ' kN/m2')
print('Wall length: ', beamSpan, ' m')
print('Uniform load: ', uniformLoad[1]/1e3, ' kN/m')
#print('Beam: ', beam.sectionName)

nodes.calculateNodalReactions(True,1e-7)
Vmax= max(p0.getNode().getReaction[1],p1.getNode().getReaction[1])
eMidSpan= xcTotalSet.getNearestElement(geom.Pos3d(beamSpan/2.0,0.0,0.0))
Mmax= max(abs(eMidSpan.getM1),abs(eMidSpan.getM2))

## Shear
Vu= beam.Vs
print('Vmax= ', Vmax/1e3, ' kN Vu= ', Vu/1e3, ' kN; F= ',Vmax/Vu)

## Bending
Mu= beam.Ms
print('Mmax= ', Mmax/1e3, ' kN Mu= ', Mu/1e3, ' kN; F= ',Mmax/Mu)

## Deflection
ratioI= beam.Iz()/(2252*(0.0254)**4)
nMidSpan= l1.getNearestNode(geom.Pos3d(beamSpan/2.0,0.0,0.0))
dMidSpan= ratioI*nMidSpan.getDisp[1]
ratio1= abs(dMidSpan)/beamSpan
print('dY= ',dMidSpan*1e3,' mm; ratio= L/', 1.0/ratio1, 'L= ', beamSpan, ' m')

print('**** Reaction ****')
RD= p0.getNode().getReaction[1]
RL= p1.getNode().getReaction[1]
print('R_D=', RD/1e3, ' kN (', RD/poundToN, 'lbs)')
print('R_L=', RL/1e3, ' kN (', RL/poundToN, 'lbs)')
