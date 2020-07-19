# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import xc_base
import geom
import xc
from model import predefined_spaces
from solution import predefined_solutions
from materials.awc_nds import AWCNDS_materials
from materials.awc_nds import structural_panels
from materials import typical_materials

# Loads
from actions import load_cases as lcm
from actions import combinations as combs

inch2meter= 0.0254
foot2meter= .3048

# Problem type
sheathingCantilever= xc.FEProblem()
sheathingCantilever.title= 'Check sheating stiffness'
preprocessor= sheathingCantilever.getPreprocessor   
nodes= preprocessor.getNodeHandler
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)

# Materials
structuralPanel= structural_panels.OSBPanelSections['3/4']
section= structuralPanel.defElasticShearSection2d(preprocessor, angle= 0.0)
thickness= structuralPanel.h

# Model
spanA= 1*foot2meter
spanB= 4*foot2meter
pointHandler= preprocessor.getMultiBlockTopology.getPoints
pt1= pointHandler.newPntFromPos3d(geom.Pos3d(0.0,0.0,0.0))
pt2= pointHandler.newPntFromPos3d(geom.Pos3d(spanA,0.0,0.0))
pt3= pointHandler.newPntFromPos3d(geom.Pos3d(0.0,1.0,0.0))
pt4= pointHandler.newPntFromPos3d(geom.Pos3d(spanB,1.0,0.0))

lines= preprocessor.getMultiBlockTopology.getLines
l1= lines.newLine(pt1.tag,pt2.tag)
l2= lines.newLine(pt3.tag,pt4.tag)

setA= preprocessor.getSets.defSet("setA")
setA.getLines.append(l1)
setB= preprocessor.getSets.defSet("setB")
setB.getLines.append(l2)

# Mesh
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)

trfs= preprocessor.getTransfCooHandler
lin= trfs.newLinearCrdTransf2d("lin")
seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultMaterial= section.name
seedElemHandler.defaultTransformation= "lin"
elem= seedElemHandler.newElement("ElasticBeam2d",xc.ID([0,0]))

xcTotalSet= preprocessor.getSets.getSet("total")
mesh= setA.genMesh(xc.meshDir.I)
setA.fillDownwards()
mesh= setB.genMesh(xc.meshDir.I)
setB.fillDownwards()

# Modify stiffness
ratioA= 3550/2550.0
ratioI= 300000/80500.0/1.6
for e in setB.elements:
    secProp= e.sectionProperties
    secProp.A*= ratioA
    secProp.I*= ratioI
    e.sectionProperties= secProp
  
# Constraints
for p in [pt1,pt3]:
    n= p.getNode()
    modelSpace.fixNode000(n.tag)

# Actions
L= 1e3 # Live load N
loadCaseManager= lcm.LoadCaseManager(preprocessor)
loadCaseNames= ['liveLoad']
loadCaseManager.defineSimpleLoadCases(loadCaseNames)

# Live load.
cLC= loadCaseManager.setCurrentLoadCase('liveLoad')
pt2.getNode().newLoad(xc.Vector([L,-L,0.0]))
pt4.getNode().newLoad(xc.Vector([L,-L,0.0]))

#We add the load case to domain.
preprocessor.getLoadHandler.addToDomain("liveLoad")

# Solution
# Linear static analysis.
analysis= predefined_solutions.simple_static_linear(sheathingCantilever)
result= analysis.analyze(1)


# Checking

## Bending stiffness.
uA= pt2.getNode().getDisp[0]
uB= pt4.getNode().getDisp[0]
vA= pt2.getNode().getDisp[1]
vB= pt4.getNode().getDisp[1]

print('uA= ',uA*1e3, ' mm')
print('uB= ',uB*1e3, ' mm')
print('vA= ',vA*1e3, ' mm')
print('vB= ',vB*1e3, ' mm')

