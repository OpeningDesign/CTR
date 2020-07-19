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

span= 19.2/3*inchToMeter

# Materials
# Mechanical properties taken from:
# http://www.pfsteco.com/techtips/pdf/tt_plywooddesigncapacities
lumber2x6Geom= section_properties.RectangularSection("lumber2x6Geom",b=5.5*inchToMeter,h=1.5*inchToMeter)
plate= AWCNDS_materials.ColumnMember(span,span, lumber2x6Geom)
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
section= lumber2x6Geom.defElasticShearSection2d(preprocessor,hem_fir)

thickness= lumber2x6Geom.h

pointHandler= preprocessor.getMultiBlockTopology.getPoints
pt1= pointHandler.newPntFromPos3d(geom.Pos3d(0.0,0.0,0.0))
pt2= pointHandler.newPntFromPos3d(geom.Pos3d(span,0.0,0.0))
pt3= pointHandler.newPntFromPos3d(geom.Pos3d(2.0*span,0.0,0.0))
pt4= pointHandler.newPntFromPos3d(geom.Pos3d(3.0*span,0.0,0.0))
pt5= pointHandler.newPntFromPos3d(geom.Pos3d(4.0*span,0.0,0.0))
pt11= pointHandler.newPntFromPos3d(geom.Pos3d(0.0,thickness,0.0))
pt12= pointHandler.newPntFromPos3d(geom.Pos3d(span,thickness,0.0))
pt13= pointHandler.newPntFromPos3d(geom.Pos3d(2.0*span,thickness,0.0))
pt14= pointHandler.newPntFromPos3d(geom.Pos3d(3.0*span,thickness,0.0))
pt15= pointHandler.newPntFromPos3d(geom.Pos3d(4.0*span,thickness,0.0))

lines= preprocessor.getMultiBlockTopology.getLines
l1= lines.newLine(pt1.tag,pt2.tag)
l2= lines.newLine(pt2.tag,pt3.tag)
l3= lines.newLine(pt3.tag,pt4.tag)
l4= lines.newLine(pt4.tag,pt5.tag)
l11= lines.newLine(pt11.tag,pt12.tag)
l12= lines.newLine(pt12.tag,pt13.tag)
l13= lines.newLine(pt13.tag,pt14.tag)
l14= lines.newLine(pt14.tag,pt15.tag)

infSet= preprocessor.getSets.defSet("inf")
infSet.getLines.append(l1)
infSet.getLines.append(l2)
infSet.getLines.append(l3)
infSet.getLines.append(l4)

supSet= preprocessor.getSets.defSet("sup")
supSet.getLines.append(l11)
supSet.getLines.append(l12)
supSet.getLines.append(l13)
supSet.getLines.append(l14)


# Mesh
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)
# nodes.newSeedNode() DEPRECATED
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

## Mid-span nodes.
midSpanNodes= list()
for l in supSet.getLines:
    midSpanNodes.append(supSet.getNearestNode(l.getCentroid()))

# Constraints
supportedNodes= list()
for p in [pt1,pt2,pt3,pt4,pt5]:
    n= p.getNode()
    modelSpace.fixNode00F(n.tag)
    supportedNodes.append(n)

for n in supSet.nodes:
    pos= n.getInitialPos3d
    nInf= infSet.getNearestNode(pos)
    modelSpace.constraints.newEqualDOF(nInf.tag,n.tag,xc.ID([1]))

for p in [pt12,pt13,pt14]:
    n= p.getNode()
    pos= n.getInitialPos3d
    nInf= infSet.getNearestNode(pos)
    modelSpace.constraints.newEqualDOF(nInf.tag,n.tag,xc.ID([0]))


# Actions
trussLoad= 10.27e3 # N/truss (two trusses here)
loadCaseManager= lcm.LoadCaseManager(preprocessor)
loadCaseNames= ['totalLoad']
loadCaseManager.defineSimpleLoadCases(loadCaseNames)

# Total load.
cLC= loadCaseManager.setCurrentLoadCase('totalLoad')
for n in midSpanNodes:
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
    sg1= abs(m1/section.sectionProperties.I*lumber2x6Geom.h/2)
    sgMax= max(sgMax,sg1)
    m2= e.getM2
    sg2= abs(m2/section.sectionProperties.I*lumber2x6Geom.h/2)
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
sgMax= RMax/lumber2x6Geom.A()
print('RMax= ', RMax/1e3, ' kN')
print('sgMax= ', sgMax/1e6, ' MPa')
print('Fc_perp= ', Fc_perp/1e6, ' MPa')
if(Fc_perp>sgMax):
    print('OK')
else:
    print('KO')
