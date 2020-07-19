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
from postprocess import output_handler
from solution import predefined_solutions

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2014, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

inch2meter= 0.0254
psi2Pa= 6894.76
pci2Nm3= 271447.14116097
pound2N= 4.44822

B= 1.25
eps_thickness= 6*inch2meter
concrete_thickness= 3*inch2meter
total_thickness= eps_thickness+concrete_thickness
elem_size= inch2meter

# Problem type
feProblem= xc.FEProblem()
preprocessor= feProblem.getPreprocessor
nodes= preprocessor.getNodeHandler

modelSpace= predefined_spaces.SolidMechanics3D(nodes)

unifGrids= preprocessor.getMultiBlockTopology.getUniformGrids
uGrid= unifGrids.newUniformGrid()

uGrid.Lx= B
uGrid.Ly= B
uGrid.Lz= total_thickness
print(uGrid.nDivX)
uGrid.nDivX= int(uGrid.Lx/elem_size)
print(uGrid.nDivX)
uGrid.nDivY= int(uGrid.Ly/elem_size)
uGrid.nDivZ= int(uGrid.Lz/elem_size)

#########################################################
# Graphic stuff.
oh= output_handler.OutputHandler(modelSpace)

#oh.displayBlocks()


# Materials definition
Ec= 3.6e6*psi2Pa
concrete= typical_materials.defElasticIsotropic3d(preprocessor, "concrete",Ec,0.2,2500)


#Eeps= 9308e3 #FOAMULAR C-300
Eeps= 13789e3 #FOAMULAR C-400
#Eeps= 18616e3 #FOAMULAR C-600
#Eeps= 25510e3 #FOAMULAR C-1000
eps= typical_materials.defElasticIsotropic3d(preprocessor, "eps",Eeps,0.2,2500)

# Mesh generation
seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultMaterial= eps.name
brick= seedElemHandler.newElement("Brick",xc.ID([0,0,0,0,0,0,0,0]))

numElem= uGrid.nDivX*uGrid.nDivY*uGrid.nDivZ
uGrid.genMesh(xc.meshDir.I)

for e in uGrid.getElements:
    z= e.getPosCentroid(False).z
    if(z>eps_thickness):
        e.physicalProperties.setMaterial(concrete)

# Constraints

## Classify nodes
bottom_nodes= list()
contour_nodes= list()
top_nodes= list()

for n in uGrid.getNodes:
    pos= n.getInitialPos3d
    if(pos.z<1e-3):
        bottom_nodes.append(n)
    elif(abs(pos.z-total_thickness)<1e3):
        top_nodes.append(n)
    if((pos.x<1e-3) or (pos.y<1e-3) or (abs(pos.x-B)<1e-3) or (abs(pos.y-B)<1e-3)):
        contour_nodes.append(n)
        
## Fix horiz movement
# for n in contour_nodes:
#     modelSpace.fixNode("00F",n.tag)

## Elastic bearing
S= B*B
numDiv= len(bottom_nodes)-1
k= 10.0*680*pci2Nm3
kZ= typical_materials.defElasticMaterial(preprocessor, "kZ",k*S/numDiv)
for n in bottom_nodes:
    modelSpace.fixNode("000",n.tag)
    #fixNodeId, idElem= modelSpace.setUniaxialBearing3D(n.tag,"kZ",[0,0,1])

#oh.displayFEMesh()
oh.displayLocalAxes()


# Loads
r= 5*inch2meter #Radius of contact area
center= geom.Pos3d(B/2.0,B/2.0,total_thickness)
loaded_nodes= list()
for n in top_nodes:
    pos= n.getInitialPos3d
    if(pos.distPos3d(center)<=r):
        loaded_nodes.append(n)

loadHandler= preprocessor.getLoadHandler
lPatterns= loadHandler.getLoadPatterns
## Load modulation.
ts= lPatterns.newTimeSeries("constant_ts","ts")
lPatterns.currentTimeSeries= "ts"
## Load case definition
lp0= lPatterns.newLoadPattern("default","0")

F= 7200.0*pound2N
print('F= ', F/1e3, ' kN')
f= F/len(loaded_nodes)
for n in loaded_nodes:
    lp0.newNodalLoad(n.tag,xc.Vector([0,0,-f]))

lPatterns.addToDomain(lp0.name)
oh.displayLoads()

# Solution
analysis= predefined_solutions.simple_static_linear(feProblem)
result= analysis.analyze(1)

test= preprocessor.getSets.defSet('test')
for e in uGrid.getElements:
    pos= e.getPosCentroid(False)
    if((pos.distPos3d(center)<=2*r) and pos.z>total_thickness/4.0):
        test.getElements.append(e)
        
quarter= preprocessor.getSets.defSet('quarter')
for e in uGrid.getElements:
    pos= e.getPosCentroid(False)
    if((pos.x<=B/2.0) and (pos.y<B/2.0)):
        quarter.getElements.append(e)

quarter.fillDownwards()

    

oh.displayReactions()
oh.displayDispRot('uZ', setToDisplay= quarter)
#oh.displayDispRot('uX', setToDisplay= test)
#oh.displayIntForc('N1', setToDisplay= quads)
oh.displayStresses('sigma_zz', setToDisplay= quarter)
