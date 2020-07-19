# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

import xc_base
import geom
import xc
import math
import os
import sys
from model import predefined_spaces
from materials import typical_materials
from materials import steel_base
from materials.sections import section_properties
from postprocess import output_handler
from solution import predefined_solutions
from model.sets import sets_mng

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2014, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

inch2meter= 0.0254
psi2Pa= 6894.76
pci2Nm3= 271447.14116097
pound2N= 4.4482216
kip2N= pound2N*1000

B= 24*inch2meter
plank_thickness= 12*inch2meter
elem_size= 1.0*inch2meter

# Problem type
feProblem= xc.FEProblem()
preprocessor= feProblem.getPreprocessor
nodes= preprocessor.getNodeHandler

modelSpace= predefined_spaces.SolidMechanics3D(nodes)

unifGrids= preprocessor.getMultiBlockTopology.getUniformGrids
uGrid= unifGrids.newUniformGrid()

uGrid.Lx= B
uGrid.Ly= B
uGrid.Lz= plank_thickness
uGrid.nDivX= int(uGrid.Lx/elem_size)
if(uGrid.nDivX%2!=0):
    uGrid.nDivX+=1
uGrid.nDivY= int(uGrid.Ly/elem_size)
if(uGrid.nDivY%2!=0):
    uGrid.nDivY+=1
uGrid.nDivZ= int(uGrid.Lz/elem_size)

#########################################################
# Graphic stuff.
oh= output_handler.OutputHandler(modelSpace)

#oh.displayBlocks()


# Materials definition

## Reinforced concrete
Ec= 3.6e6*psi2Pa
concrete= typical_materials.defElasticIsotropic3d(preprocessor, "concrete",Ec,0.2,2500)

## Anchor bolt
### Anchor bolt steel
anchorBoltSteel= steel_base.BasicSteel(E= 210e9,nu= 0.3, fy= 250e6, fu= 300e6, gammaM= 1.0)

### Cross section properties
diam= 0.25*inch2meter
boltSectionGeom= section_properties.CircularSection(name= 'boltSectionGeom', Rext= diam/2.0)
boltSection= boltSectionGeom.defElasticShearSection3d(preprocessor, anchorBoltSteel)


# Mesh generation

## Concrete block
seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultMaterial= concrete.name
brick= seedElemHandler.newElement("Brick",xc.ID([0,0,0,0,0,0,0,0]))

numElem= uGrid.nDivX*uGrid.nDivY*uGrid.nDivZ
uGrid.genMesh(xc.meshDir.I)

setBricks= preprocessor.getSets.defSet('bricks')
for e in uGrid.getElements:
    center= e.getPosCentroid(False)
    if((center.x<B/2.0) and (center.y<B/2.0)): 
        setBricks.elements.append(e)

setBricks.fillDownwards()

## Anchor bolt
bottomCenter= geom.Pos3d(B/2.0,B/2.0,plank_thickness)
topCenter= geom.Pos3d(B/2.0,B/2.0,0.0)
xcTotalSet= modelSpace.getTotalSet()

anchorConcreteNodes= sets_mng.get_nodes_wire(xcTotalSet,[bottomCenter,topCenter])
assert(len(anchorConcreteNodes)==(uGrid.nDivZ+1))
anchorBoltNodes= list()
coupledNodes= list()

nodes.newSeedNode(3,6);
for n in anchorConcreteNodes:
    pos= n.getInitialPos3d
    newNode= nodes.newNodeXYZ(pos.x,pos.y,pos.z)
    anchorBoltNodes.append((newNode,pos.z))
    coupledNodes.append((n,newNode)) # Nodes to link together

## Anchor bolt top node
boltTopZ= plank_thickness+1.0*inch2meter 
boltTopNode= nodes.newNodeXYZ(B/2.0,B/2.0,boltTopZ)
anchorBoltNodes.append((boltTopNode,boltTopZ))


anchorBoltNodes= sorted(anchorBoltNodes, key=lambda nod: nod[1]) # sort by z

## Anchor bolt elements definition
lin= preprocessor.getTransfCooHandler.newLinearCrdTransf3d('lin')
lin.xzVector= xc.Vector([1.0,0,0])
elements= preprocessor.getElementHandler
elements.defaultTransformation= "lin"
elements.defaultMaterial= boltSection.name
anchorElements= list()
n0= anchorBoltNodes[0][0]
for i in range(1,len(anchorBoltNodes)):
    n1= anchorBoltNodes[i][0]
    print(n0.tag, n1.tag)
    beam3d= elements.newElement("ElasticBeam3d",xc.ID([n0.tag,n1.tag]))
    anchorElements.append(beam3d)
    n0= n1

setBolt= preprocessor.getSets.defSet('bolt')
for e in anchorElements:
    setBolt.elements.append(e)
setBolt.fillDownwards()

# Constraints

## Classify nodes
contour_nodes= list()
plate_nodes= list()
anchorPlateSide= 4*inch2meter # Side of the anchor plate
effectiveAnchorPlateSide= 0.2*anchorPlateSide # Effective dimension


for n in uGrid.getNodes:
    pos= n.getInitialPos3d
    if((pos.x<1e-3) or (pos.y<1e-3) or (abs(pos.x-B)<1e-3) or (abs(pos.y-B)<1e-3)):
        contour_nodes.append(n)
        
## Fix contour nodes
for n in contour_nodes:
    modelSpace.fixNode("000",n.tag)

## Link anchor to concrete
for t in coupledNodes:
    eqDof= modelSpace.newEqualDOF(t[0].tag,t[1].tag,xc.ID([0,1,2]))

## Fix torsional DOF at bolt top.
modelSpace.fixNode('FFF_FF0',boltTopNode.tag)

#oh.displayFEMesh()

# Loads

loadHandler= preprocessor.getLoadHandler
lPatterns= loadHandler.getLoadPatterns
## Load modulation.
ts= lPatterns.newTimeSeries("constant_ts","ts")
lPatterns.currentTimeSeries= "ts"
## Load case definition
lp0= lPatterns.newLoadPattern("default","0")

F= 13.0*kip2N
print('F= ', F/1e3, ' kN')
lp0.newNodalLoad(boltTopNode.tag,xc.Vector([0,0,F,0,0,0]))

lPatterns.addToDomain(lp0.name)
#oh.displayLoads()

# Solution
analysis= predefined_solutions.simple_static_linear(feProblem)
result= analysis.analyze(1)

# test= preprocessor.getSets.defSet('test')
# for e in uGrid.getElements:
#     pos= e.getPosCentroid(False)
#     if((pos.distPos3d(center)<=2*r) and pos.z>total_thickness/4.0):
#         test.getElements.append(e)

    

#oh.displayReactions()
oh.displayIntForcDiag('N',setToDisplay= setBolt)
oh.displayDispRot('uZ')# , setToDisplay= setBricks)
#oh.displayDispRot('uX', setToDisplay= test)
#oh.displayIntForc('N1', setToDisplay= quads)
oh.displayStresses('sigma_xx', setToDisplay= setBricks)
oh.displayStresses('sigma_yy', setToDisplay= setBricks)
oh.displayStresses('sigma_zz', setToDisplay= setBricks)
oh.displayStrains('epsilon_zz', setToDisplay= setBricks)
