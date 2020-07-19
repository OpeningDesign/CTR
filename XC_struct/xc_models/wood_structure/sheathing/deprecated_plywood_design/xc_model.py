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
# http://www.pfsteco.com/techtips/pdf/tt_plywooddesigncapacities
structuralPanelGeom=  structural_panels.PlywoodPanelSections['19/32']
plywood= typical_materials.MaterialData(name='Douglas-Fri Plywood',E=4.2e9,nu=0.2,rho=500)
section= structuralPanelGeom.defElasticShearSection2d(preprocessor,plywood)

thickness= structuralPanelGeom.h

spanBendingStiffness= (32-1.5+0.25)*0.0254
spanInternalForces= 32*0.0254
#span= spanBendingStiffness
span= spanInternalForces
pointHandler= preprocessor.getMultiBlockTopology.getPoints
pt1= pointHandler.newPntFromPos3d(geom.Pos3d(0.0,0.0,0.0))
pt2= pointHandler.newPntFromPos3d(geom.Pos3d(span,0.0,0.0))
pt3= pointHandler.newPntFromPos3d(geom.Pos3d(2.0*span,0.0,0.0))
pt4= pointHandler.newPntFromPos3d(geom.Pos3d(3.0*span,0.0,0.0))
pt11= pointHandler.newPntFromPos3d(geom.Pos3d(0.0,thickness,0.0))
pt12= pointHandler.newPntFromPos3d(geom.Pos3d(span,thickness,0.0))
pt13= pointHandler.newPntFromPos3d(geom.Pos3d(2.0*span,thickness,0.0))
pt14= pointHandler.newPntFromPos3d(geom.Pos3d(3.0*span,thickness,0.0))
pt21= pointHandler.newPntFromPos3d(geom.Pos3d(0.0,2*thickness,0.0))
pt22= pointHandler.newPntFromPos3d(geom.Pos3d(span,2*thickness,0.0))
pt23= pointHandler.newPntFromPos3d(geom.Pos3d(2.0*span,2*thickness,0.0))
pt24= pointHandler.newPntFromPos3d(geom.Pos3d(3.0*span,2*thickness,0.0))

lines= preprocessor.getMultiBlockTopology.getLines
l1= lines.newLine(pt1.tag,pt2.tag)
l2= lines.newLine(pt2.tag,pt3.tag)
l3= lines.newLine(pt3.tag,pt4.tag)
l11= lines.newLine(pt11.tag,pt12.tag)
l12= lines.newLine(pt12.tag,pt13.tag)
l13= lines.newLine(pt13.tag,pt14.tag)
l21= lines.newLine(pt21.tag,pt22.tag)
l22= lines.newLine(pt22.tag,pt23.tag)
l23= lines.newLine(pt23.tag,pt24.tag)

infSet= preprocessor.getSets.defSet("inf")
infSet.getLines.append(l1)
infSet.getLines.append(l2)
infSet.getLines.append(l3)

midSet= preprocessor.getSets.defSet("mid")
midSet.getLines.append(l11)
midSet.getLines.append(l12)
midSet.getLines.append(l13)

supSet= preprocessor.getSets.defSet("sup")
supSet.getLines.append(l21)
supSet.getLines.append(l22)
supSet.getLines.append(l23)


# Mesh
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)

trfs= preprocessor.getTransfCooHandler
lin= trfs.newLinearCrdTransf2d("lin")
seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultMaterial= section.name
seedElemHandler.defaultTransformation= "lin"
elem= seedElemHandler.newElement("ElasticBeam2d",xc.ID([0,0]))

xcTotalSet= preprocessor.getSets.getSet("total")
mesh= infSet.genMesh(xc.meshDir.I)
infSet.fillDownwards()
mesh= midSet.genMesh(xc.meshDir.I)
midSet.fillDownwards()
mesh= supSet.genMesh(xc.meshDir.I)
supSet.fillDownwards()

# Constraints
for p in [pt1,pt2,pt3,pt4]:
    n= p.getNode()
    modelSpace.fixNode00F(n.tag)

for n in midSet.nodes:
    pos= n.getInitialPos3d
    nInf= infSet.getNearestNode(pos)
    modelSpace.constraints.newEqualDOF(nInf.tag,n.tag,xc.ID([1]))

for n in supSet.nodes:
    pos= n.getInitialPos3d
    nMid= midSet.getNearestNode(pos)
    modelSpace.constraints.newEqualDOF(nMid.tag,n.tag,xc.ID([1]))

for p in [pt12,pt13]:
    n= p.getNode()
    pos= n.getInitialPos3d
    nInf= infSet.getNearestNode(pos)
    modelSpace.constraints.newEqualDOF(nInf.tag,n.tag,xc.ID([0]))

for p in [pt22,pt23]:
    n= p.getNode()
    pos= n.getInitialPos3d
    nMid= midSet.getNearestNode(pos)
    modelSpace.constraints.newEqualDOF(nMid.tag,n.tag,xc.ID([0]))


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

uYMax= -1e6
for n in infSet.nodes:
    uY= -n.getDisp[1]
    uYMax= max(uY,uYMax)

r= spanInternalForces/uYMax
print('thickness= ', thickness*1e3, ' mm')
print('uYMax= ', uYMax*1e3, ' mm (L/'+str(r)+')')

DeltaLL= 12*L*span**4/1743.0/section.sectionProperties.EI()/3.0 #Three layers
r= span/DeltaLL
print('DeltaLL= ', DeltaLL*1e3, ' mm (L/'+str(r)+')')

# Bending and shear strength (5-ply)
CD= AWCNDS_materials.getLoadDurationFactor(0.5/365.25/24)
print("Cd= ",CD)
Ft= 3640*4.44822/0.3048/section.sectionProperties.A
Fb= CD*444.0/structuralPanelGeom.Wzel()*4.44822*0.0254/0.3048
Fv= CD*215*4.44822/0.3048/structuralPanelGeom.h

sgMax= -1e6
tauMax= -1e6
for e in supSet.elements:
    e.getResistingForce()
    m1= e.getM1
    sg1= abs(m1/section.sectionProperties.I*structuralPanelGeom.h/2)
    tau1= abs(e.getV1/section.sectionProperties.A)
    sgMax= max(sgMax,sg1)
    tauMax= max(tauMax,tau1)
    m2= e.getM2
    sg2= abs(m2/section.sectionProperties.I*structuralPanelGeom.h/2)
    tau2= abs(e.getV2/section.sectionProperties.A)
    sgMax= max(sgMax,sg2)
    tauMax= max(tauMax,tau2)

print('sgMax= ', sgMax/1e6,' MPa')
print('Fb= ', Fb/1e6,' MPa')
if(Fb>sgMax):
    print('OK')
else:
    print('KO')
#print('Ft= ', Ft/1e6,' MPa')
print('Fv= ', Fv/1e6,' MPa')
print('tauMax= ', tauMax/1e6,' MPa')
if(Fv>tauMax):
    print('OK')
else:
    print('KO')

