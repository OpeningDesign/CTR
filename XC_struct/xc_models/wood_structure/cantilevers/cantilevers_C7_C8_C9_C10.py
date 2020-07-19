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
from materials.awc_nds import AWCNDS_materials

# Loads
from actions import load_cases as lcm

# Units
inchToMeter= 2.54/100.0
footToMeter= 0.3048
poundToN= 4.44822
psiToPa= 6894.76
psfToNm2= 47.88026

# Problem type
cantilever= xc.FEProblem()
cantilever.title= 'Cantilevers C7, C8, C9 and C10'
preprocessor= cantilever.getPreprocessor   
nodes= preprocessor.getNodeHandler
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)

# Materials LSL 1.55E (page 10 of the PDF document from "SolidStart")
header= AWCNDS_materials.LSL155HeaderSections['3.5x14']
section= header.defElasticShearSection2d(preprocessor)

# Cantilever geometry
cantileverLength= 0.95
centerSpacing= 12.0*inchToMeter # Distance between trusses
## Key points
pointHandler= preprocessor.getMultiBlockTopology.getPoints
p0= pointHandler.newPntFromPos3d(geom.Pos3d(0.0,0.0,0.0))
p1= pointHandler.newPntFromPos3d(geom.Pos3d(cantileverLength,0.0,0.0))

## Lines
lines= list()
lineHandler= preprocessor.getMultiBlockTopology.getLines
l= lineHandler.newLine(p0.tag,p1.tag) 

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
n0= p0.getNode()
modelSpace.fixNode000(n0.tag)

# Actions
loadCaseManager= lcm.LoadCaseManager(preprocessor)
loadCaseNames= ['load']
loadCaseManager.defineSimpleLoadCases(loadCaseNames)

## Loads on nodes.
cLC= loadCaseManager.setCurrentLoadCase('load')
floorLoad= (0.9*16*footToMeter*(15+40)*psfToNm2)/2.0 # N
facadeLoad= 0.73e3*16*footToMeter*(3.3528+3.302+0.6096)/2.0 #N
totalLoad= xc.Vector([0.0,-floorLoad-facadeLoad,0.0])
p1.getNode().newLoad(totalLoad)

#We add the load case to domain.
preprocessor.getLoadHandler.getLoadPatterns.addToDomain('load')

# Solution
# Linear static analysis.
analysis= predefined_solutions.simple_static_linear(cantilever)
result= analysis.analyze(1)

# Checking
nodes.calculateNodalReactions(True,1e-7)
Vmax= n0.getReaction[1]
Mmax= n0.getReaction[2]
print('*****',cantilever.title,'******')
print('Floor load: ', floorLoad/1e3, ' kN')
print('Facade load: ', facadeLoad/1e3, ' kN')
print('Total load: ', totalLoad[1]/1e3, ' kN')
print('Header: ', header.sectionName)

## Shear
Vu= header.Vs
print('Vmax= ', Vmax/1e3, ' kN Vu= ', Vu/1e3, ' kN; F= ',Vmax/Vu)

## Bending
Mu= header.Ms
print('Mmax= ', Mmax/1e3, ' kN.m Mu= ', Mu/1e3, ' kN.m; F= ',Mmax/Mu)

## Deflection
dY= p1.getNode().getDisp[1]
ratio1= abs(dY)/cantileverLength
print('dY= ',dY*1e3,' mm; ratio= L/', 1.0/ratio1)
