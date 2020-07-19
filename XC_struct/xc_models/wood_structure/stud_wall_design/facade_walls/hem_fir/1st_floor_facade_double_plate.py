# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import xc_base
import geom
import xc
from model import predefined_spaces
from solution import predefined_solutions
from materials.awc_nds import AWCNDS_materials
from materials import typical_materials
from materials.sections import section_properties


inchToMeter= 0.0254
psiToPa= 6894.76

# Loads
from actions import load_cases as lcm
from actions import combinations as combs

# Problem type
sheathingBeam= xc.FEProblem()
sheathingBeam.title= 'Sheating design'
preprocessor= sheathingBeam.getPreprocessor   
nodes= preprocessor.getNodeHandler
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)

studSpacing= 19.2/2*inchToMeter
trussSpacing= 24*inchToMeter

# Materials
# Mechanical properties taken from:
# http://www.pfsteco.com/techtips/pdf/tt_plywooddesigncapacities
lumber2x8Geom= section_properties.RectangularSection("lumber2x8Geom",b=7.5*inchToMeter,h=1.5*inchToMeter)
plate= AWCNDS_materials.ColumnMember(studSpacing,studSpacing, lumber2x8Geom)
E= 1200000*psiToPa
E_adj= 440000*psiToPa
Fb= 675*psiToPa
Fv= 150*psiToPa # Shear parallel to grain
Fc= 800*psiToPa
Fc_perp= 405*psiToPa #Perpendicular to grain
Cr= 1.0
CF= 1.3
Cfu= 1.15 # Flat use factor NDS Supplement table 4A adjustement factors.
Fc_adj= Fc*CF
Fb_adj= Fb*Cr*CF*Cfu
# Shear perpendicular to grain is not a design factor in
# solid wood because effective control is applied through limits on design
# stresses in shear parallel to grain and compression or bearing
# perpendicular to grain.

hem_fir= typical_materials.MaterialData(name='Hem-Fir Stud',E=E,nu=0.2,rho=430)
section= lumber2x8Geom.defElasticShearSection2d(preprocessor,hem_fir)

thickness= lumber2x8Geom.h

span= studSpacing
pointHandler= preprocessor.getMultiBlockTopology.getPoints
infPoints= list()
supPoints= list()
for i in range(0,14):
    x= i*span
    infPoints.append(pointHandler.newPntFromPos3d(geom.Pos3d(x,0.0,0.0)))
    supPoints.append(pointHandler.newPntFromPos3d(geom.Pos3d(x,thickness,0.0)))

infSet= preprocessor.getSets.defSet("inf")
lines= preprocessor.getMultiBlockTopology.getLines
infLines= list()
p0= infPoints[0]
for p in infPoints[1:]:
    l= lines.newLine(p0.tag,p.tag)
    infLines.append(l)
    infSet.getLines.append(l)
    p0= p
supSet= preprocessor.getSets.defSet("sup")
supLines= list()
p0= supPoints[0]
for p in supPoints[1:]:
    l= lines.newLine(p0.tag,p.tag)
    supLines.append(l)
    supSet.getLines.append(l)
    p0= p
infSet.fillDownwards()
supSet.fillDownwards()

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
mesh= supSet.genMesh(xc.meshDir.I)
supSet.fillDownwards()

## Loaded nodes.
loadedNodes= list()
pos= supPoints[0].getPos #Position of the first loaded node
xLast= supPoints[-1].getPos.x
while pos.x<xLast:
    n= supSet.getNearestNode(pos)
    loadedNodes.append(supSet.getNearestNode(pos))
    pos+= geom.Vector3d(trussSpacing,0.0,0.0)

# Constraints
supportedNodes= list()
for p in infPoints:
    n= p.getNode()
    modelSpace.fixNode00F(n.tag)
    supportedNodes.append(n)

for n in supSet.nodes:
    pos= n.getInitialPos3d
    nInf= infSet.getNearestNode(pos)
    modelSpace.constraints.newEqualDOF(nInf.tag,n.tag,xc.ID([1]))

for p in supPoints[1:-1]:
    n= p.getNode()
    pos= n.getInitialPos3d
    nInf= infSet.getNearestNode(pos)
    modelSpace.constraints.newEqualDOF(nInf.tag,n.tag,xc.ID([0]))


# Actions
trussLoad= 9.64e3 # N/truss
loadCaseManager= lcm.LoadCaseManager(preprocessor)
loadCaseNames= ['totalLoad']
loadCaseManager.defineSimpleLoadCases(loadCaseNames)

# Total load.
cLC= loadCaseManager.setCurrentLoadCase('totalLoad')
for n in loadedNodes:
    n.newLoad(xc.Vector([0.0,-trussLoad,0.0]))

#We add the load case to domain.
preprocessor.getLoadHandler.getLoadPatterns.addToDomain("totalLoad")

# Solution
# Linear static analysis.
analysis= predefined_solutions.simple_static_linear(sheathingBeam)
result= analysis.analyze(1)

# Checking

## Bending stiffness
uYMax= -1e6
for n in infSet.nodes:
    uY= -n.getDisp[1]
    uYMax= max(uY,uYMax)

r= span/uYMax
print('thickness= ', thickness*1e3, ' mm')
print('uYMax= ', uYMax*1e3, ' mm (L/'+str(r)+')')

## Bending stiffness
sgMax= -1e6
for e in supSet.elements:
    e.getResistingForce()
    m1= e.getM1
    sg1= abs(m1/section.sectionProperties.I*lumber2x8Geom.h/2)
    sgMax= max(sgMax,sg1)
    m2= e.getM2
    sg2= abs(m2/section.sectionProperties.I*lumber2x8Geom.h/2)
    sgMax= max(sgMax,sg2)

print('sgMax= ', sgMax/1e6,' MPa')
print('Fb_adj= ', Fb_adj/1e6,' MPa')
if(Fb_adj>sgMax):
    print('OK')
else:
    print('KO')

## Compression perpendicular to grain

### Reactions
nodes.calculateNodalReactions(False,1e-7)
RMax= -1e12;
for n in supportedNodes:
    RMax= max(RMax,n.getReaction[1])
sgMax= RMax/lumber2x8Geom.A()
print('RMax= ', RMax/1e3, ' kN')
print('sgMax= ', sgMax/1e6, ' MPa')
print('Fc_perp= ', Fc_perp/1e6, ' MPa')
if(Fc_perp>sgMax):
    print('OK')
else:
    print('KO')
