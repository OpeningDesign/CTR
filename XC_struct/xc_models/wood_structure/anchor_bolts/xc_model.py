# -*- coding: utf-8 -*-
'''Test taken from example 5-001 of SAP2000 verification manual.'''

from __future__ import division
from __future__ import print_function

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AOO)"
__copyright__= "Copyright 2015, LCPT and AOO"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

import xc_base
import geom
import xc
from solution import predefined_solutions
from model import predefined_spaces
from materials import typical_materials
from materials import steel_base
from materials.sections import section_properties
from postprocess import output_handler

# Problem type
feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor
nodes= preprocessor.getNodeHandler 
modelSpace= predefined_spaces.SolidMechanics3D(nodes)

# Geometry

inch2meter= 0.0254
foot2meter= 0.3048
psi2Pa= 6894.76
pci2Nm3= 271447.14116097
pound2N= 4.44822

width= 6*inch2meter
length= 4*foot2meter
height= 12*inch2meter
elem_size= 1.0*inch2meter

## Uniform grid
unifGrids= preprocessor.getMultiBlockTopology.getUniformGrids
uGrid= unifGrids.newUniformGrid()

uGrid.Lx= length
uGrid.Ly= width
uGrid.Lz= height
uGrid.nDivX= int(uGrid.Lx/elem_size)
uGrid.nDivY= int(uGrid.Ly/elem_size)
uGrid.nDivZ= int(uGrid.Lz/elem_size)

# Materials definition

## Reinforced concrete
concrete= typical_materials.defElasticIsotropic3d(preprocessor, "concrete",28.3e9,0.2,0.0)

## Anchor bolt
### Anchor bolt steel
anchorBoltSteel= steel_base.BasicSteel(E= 210e9,nu= 0.3, fy= 250e6, fu= 300e6, gammaM= 1.0)

### Cross section properties
diam= 0.25*inch2meter
boltSectionGeom= section_properties.CircularSection(name= 'boltSectionGeom', Rext= diam/2.0)
boltSection= boltSectionGeom.defElasticShearSection3d(preprocessor, anchorBoltSteel)



#########################################################
# Graphic stuff.
oh= output_handler.OutputHandler(modelSpace)

# Mesh generation
#
seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultMaterial= concrete.name
brick= seedElemHandler.newElement("Brick",xc.ID([0,0,0,0,0,0,0,0]))

uGrid.genMesh(xc.meshDir.I)

## Classify nodes
bottom_nodes= preprocessor.getSets.defSet('bottom_nodes')
lateral_nodes= preprocessor.getSets.defSet('lateral_nodes')
top_nodes= preprocessor.getSets.defSet('top_nodes')

for n in uGrid.getNodes:
    pos= n.getInitialPos3d
    if(pos.z<1e-3):
        bottom_nodes.getNodes.append(n)
    elif(abs(pos.z-height)<1e3):
        top_nodes.getNodes.append(n)
    if((pos.x<1e-3) or (abs(pos.x-length)<1e-3)):
        lateral_nodes.getNodes.append(n)

center= geom.Pos3d(length/2.0,width/2.0,height)
topCenterNode= top_nodes.getNearestNode(center)
topCenterNodePos= topCenterNode.getInitialPos3d

xcTotalSet= modelSpace.getTotalSet()
nodes.numDOFs= 6
print('numDOFs= ',preprocessor.getNodeHandler.numDOFs)
anchorTopNode= nodes.newNodeXYZ(topCenterNodePos.x,topCenterNodePos.y,topCenterNodePos.z+2.0*inch2meter)
print('anchor top node numDOFs= ', anchorTopNode.getNumberDOF)
anchorNodes= [anchorTopNode]
for i in range(1,5):
    pos= topCenterNodePos-i*geom.Vector3d(0.0,0.0,elem_size)
    existingNode= uGrid.getNearestNode(pos)
    newNode= nodes.newNodeXYZ(pos.x,pos.y,pos.z)
    anchorNodes.append(newNode)
    print(newNode.tag)
    
## Anchor elements definition
lin= preprocessor.getTransfCooHandler.newLinearCrdTransf3d('lin')
lin.xzVector= xc.Vector([1.0,0,0])
elements= preprocessor.getElementHandler
elements.defaultTransformation= "lin"
elements.defaultMaterial= boltSection.name
anchorElements= list()
n0= anchorNodes[0]
for i in range(1,len(anchorNodes)):
    n1= anchorNodes[i]
    print(n0.tag, n1.tag)
    beam3d= elements.newElement("ElasticBeam3d",xc.ID([n0.tag,n1.tag]))
    anchorElements.append(beam3d)
    n0= n1


# Constraints


## Fix horiz movement
for n in lateral_nodes.getNodes:
    modelSpace.fixNode("F0F",n.tag)

for n in bottom_nodes.getNodes:
    modelSpace.fixNode("000",n.tag)

oh.displayFEMesh()

quit()


constraints= preprocessor.getBoundaryCondHandler
#Constrain the displacement of node 1.

nod9.fix(xc.ID([0,1,2]),xc.Vector([0,0,0]))
nod10.fix(xc.ID([0,1,2]),xc.Vector([0,0,0]))
nod11.fix(xc.ID([0,1,2]),xc.Vector([0,0,0]))
nod12.fix(xc.ID([0,1,2]),xc.Vector([0,0,0]))

# Loads definition
loadHandler= preprocessor.getLoadHandler
lPatterns= loadHandler.getLoadPatterns
#Load modulation.
ts= lPatterns.newTimeSeries("constant_ts","ts")
lPatterns.currentTimeSeries= "ts"
#Load case definition
lp0= lPatterns.newLoadPattern("default","0")
#lPatterns.currentLoadPattern= "0"
lp0.newNodalLoad(13, xc.Vector([0,0,-1]))
lp0.newNodalLoad(14, xc.Vector([0,0,-1]))
lp0.newNodalLoad(15, xc.Vector([0,0,-1]))
lp0.newNodalLoad(16, xc.Vector([0,0,-1]))
#We add the load case to domain.
lPatterns.addToDomain(lp0.name)

# # Graphic stuff.
# oh= output_handler.OutputHandler(modelSpace)

# ## Uncomment to display the mesh
# oh.displayFEMesh()
# oh.displayLoads()

# Solution
analysis= predefined_solutions.simple_static_linear(feProblem)
result= analysis.analyze(1)

nodes.calculateNodalReactions(True,1e-7)
R9= nod9.getReaction
R10= nod10.getReaction
R11= nod11.getReaction
R12= nod12.getReaction


R= R9+R10+R11+R12
ratio1= (R-xc.Vector([0,0,4])).Norm()

''' 
print "R9= ",R9
print "R10= ",R10
print "R11= ",R11
print "R12= ",R12
print "R= ",R
print "ratio1= ",ratio1
   '''

