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

# Problem type
sheathingBeam= xc.FEProblem()
sheathingBeam.title= 'Sheating design'
preprocessor= sheathingBeam.getPreprocessor   
nodes= preprocessor.getNodeHandler
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)

# Materials
# Mechanical properties taken from:
structuralPanel= structural_panels.OSBPanelSections['19/32']
section= structuralPanel.defElasticShearSection2d(preprocessor, angle= 0.0)
thickness= structuralPanel.h

spanBendingStiffness= (32-1.5+0.25)*0.0254
spanInternalForces= 32*0.0254
span= spanInternalForces
pointHandler= preprocessor.getMultiBlockTopology.getPoints
pt1= pointHandler.newPntFromPos3d(geom.Pos3d(0.0,0.0,0.0))
pt2= pointHandler.newPntFromPos3d(geom.Pos3d(span,0.0,0.0))
pt3= pointHandler.newPntFromPos3d(geom.Pos3d(2.0*span,0.0,0.0))
pt4= pointHandler.newPntFromPos3d(geom.Pos3d(3.0*span,0.0,0.0))

lines= preprocessor.getMultiBlockTopology.getLines
l1= lines.newLine(pt1.tag,pt2.tag)
l2= lines.newLine(pt2.tag,pt3.tag)
l3= lines.newLine(pt3.tag,pt4.tag)

supSet= preprocessor.getSets.defSet("sup")
supSet.getLines.append(l1)
supSet.getLines.append(l2)
supSet.getLines.append(l3)

# Mesh
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)

trfs= preprocessor.getTransfCooHandler
lin= trfs.newLinearCrdTransf2d("lin")
seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultMaterial= section.name
seedElemHandler.defaultTransformation= "lin"
elem= seedElemHandler.newElement("ElasticBeam2d",xc.ID([0,0]))

xcTotalSet= preprocessor.getSets.getSet("total")
mesh= supSet.genMesh(xc.meshDir.I)
supSet.fillDownwards()

# Constraints
for p in [pt1,pt2,pt3,pt4]:
    n= p.getNode()
    modelSpace.fixNode00F(n.tag)


# Actions
L= 40*47.88026 # Live load N/m2
D= 15*47.88026 # Dead load N/m2
W= D+L
loadCaseManager= lcm.LoadCaseManager(preprocessor)
loadCaseNames= ['deadLoad','liveLoad','totalLoad']
loadCaseManager.defineSimpleLoadCases(loadCaseNames)

# Dead load.
cLC= loadCaseManager.setCurrentLoadCase('deadLoad')
for e in supSet.elements:
    e.vector2dUniformLoadGlobal(xc.Vector([0.0,-D]))

# Live load.
cLC= loadCaseManager.setCurrentLoadCase('liveLoad')
for e in supSet.elements:
    e.vector2dUniformLoadGlobal(xc.Vector([0.0,-L]))

# Total load.
cLC= loadCaseManager.setCurrentLoadCase('totalLoad')
for e in supSet.elements:
    e.vector2dUniformLoadGlobal(xc.Vector([0.0,-W]))

#We add the load case to domain.
preprocessor.getLoadHandler.addToDomain("totalLoad")

# Solution
# Linear static analysis.
analysis= predefined_solutions.simple_static_linear(sheathingBeam)
result= analysis.analyze(1)

# Bending and shear strength
CD= AWCNDS_materials.getLoadDurationFactor(0.5/365.25/24)
print("Cd= ",CD)
Fb= CD*structuralPanel.getFb(angle= 0.0)
Fv= CD*structuralPanel.getFv()
FbS= Fb/CD*structuralPanel.Wzel()/(4.44822*0.0254/0.3048)

sgMax= -1e6
tauMax= -1e6
for e in supSet.elements:
    e.getResistingForce()
    m1= e.getM1
    sg1= abs(m1/section.sectionProperties.I*structuralPanel.h/2)
    tau1= abs(e.getV1/section.sectionProperties.A)
    sgMax= max(sgMax,sg1)
    tauMax= max(tauMax,tau1)
    m2= e.getM2
    sg2= abs(m2/section.sectionProperties.I*structuralPanel.h/2)
    tau2= abs(e.getV2/section.sectionProperties.A)
    sgMax= max(sgMax,sg2)
    tauMax= max(tauMax,tau2)

print('span= ', span, ' m (', span/0.0254, 'in)')
print('thickness= ', thickness*1e3, ' mm')
print('sgMax= ', sgMax/1e6,' MPa')
print('Fb= ', Fb/1e6,' MPa')
print('FbS= ', FbS,' (lb-in/ft of width)')
if(Fb>sgMax):
    print('OK')
else:
    print('KO')
print('Fv= ', Fv/1e6,' MPa')
print('tauMax= ', tauMax/1e6,' MPa')
if(Fv>tauMax):
    print('OK')
else:
    print('KO')

