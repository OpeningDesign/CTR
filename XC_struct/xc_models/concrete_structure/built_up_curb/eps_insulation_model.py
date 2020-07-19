# -*- coding: utf-8 -*-

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

B= 2.0
eps_thickness= 6*inch2meter
concrete_thickness= 3*inch2meter

# Problem type
feProblem= xc.FEProblem()
preprocessor= feProblem.getPreprocessor
nodes= preprocessor.getNodeHandler

modelSpace= predefined_spaces.SolidMechanics2D(nodes)

points= preprocessor.getMultiBlockTopology.getPoints
pt1= points.newPntFromPos3d(geom.Pos3d(0.0,0.0,0.0))
pt2= points.newPntFromPos3d(geom.Pos3d(B,0.0,0.0))
pt3= points.newPntFromPos3d(geom.Pos3d(B,eps_thickness,0.0))
pt4= points.newPntFromPos3d(geom.Pos3d(0.0,eps_thickness,0.0))
pt5= points.newPntFromPos3d(geom.Pos3d(B,eps_thickness+concrete_thickness,0.0))
pt6= points.newPntFromPos3d(geom.Pos3d(0.0,eps_thickness+concrete_thickness,0.0))

surfaces= preprocessor.getMultiBlockTopology.getSurfaces
s1= surfaces.newQuadSurfacePts(pt1.tag,pt2.tag,pt3.tag,pt4.tag) #Eps
s2= surfaces.newQuadSurfacePts(pt4.tag,pt3.tag,pt5.tag,pt6.tag) #concrete

#########################################################
# Graphic stuff.
oh= output_handler.OutputHandler(modelSpace)

oh.displayBlocks()


# Materials definition
Ec= 3.6e6*psi2Pa
concrete= typical_materials.defElasticIsotropicPlaneStress(preprocessor, "concrete",Ec,0.2,2500)


#Eeps= 9308e3 #FOAMULAR C-300
Eeps= 13789e3 #FOAMULAR C-400
#Eeps= 18616e3 #FOAMULAR C-600
#Eeps= 25510e3 #FOAMULAR C-1000
eps= typical_materials.defElasticIsotropicPlaneStress(preprocessor, "eps",Eeps,0.2,2500)


# Mesh generation
elemSize= 0.01
s1.setElemSizeIJ(elemSize,elemSize)
s2.setElemSizeIJ(elemSize,elemSize)
divsOk= surfaces.conciliaNDivs()

seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultMaterial= eps.name
elem= seedElemHandler.newElement("FourNodeQuad",xc.ID([0,0,0,0]))
s1.genMesh(xc.meshDir.I)
seedElemHandler.defaultMaterial= concrete.name
s2.genMesh(xc.meshDir.I)


# Constraints

## Classify lines
vertical_lines= list()
base_line= None
top_line= None
lines= preprocessor.getMultiBlockTopology.getLines
for key in lines.getKeys():
    l= lines.get(key)
    tang= l.getTang(0.0)
    if(tang[0]==0.0): # vertical
        vertical_lines.append(l)
    else: # horizontal
        posCentroid= l.getPosCentroid()
        if(abs(posCentroid.y-pt1.getPos.y)<1e-3): # base
            base_line= l
        elif(abs(posCentroid.y-pt5.getPos.y)<1e-3):
            top_line= l

            

## Fix horiz movement
for l in vertical_lines:
    for n in l.getNodes:
        modelSpace.fixNode0F(n.tag)

## Elastic bearing
L= base_line.getLength()
numDiv= len(base_line.getNodes)-1
k= 10.0*680*pci2Nm3
kY= typical_materials.defElasticMaterial(preprocessor, "kY",k*L/numDiv)
for n in base_line.getNodes:
    fixNodeId, idElem= modelSpace.setUniaxialBearing2D(n.tag,"kY",[0,1])
#oh.displayFEMesh()


# Loads
r= 5*inch2meter #Radius of contact area
x0= B/2.0-r
x1= B/2.0+r
loaded_nodes= list()
for n in top_line.getNodes:
    pos= n.getInitialPos3d
    if((x0<=pos.x) and (pos.x<=x1)):
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
    lp0.newNodalLoad(n.tag,xc.Vector([0,-f]))

lPatterns.addToDomain(lp0.name)
oh.displayLoads()

# Solution
analysis= predefined_solutions.simple_static_linear(feProblem)
result= analysis.analyze(1)

# Sets
quads= preprocessor.getSets.defSet('quads')
for e in s1.getElements:
    quads.getElements.append(e)

#oh.displayReactions()
oh.displayDispRot('uY')
#oh.displayIntForc('N1', setToDisplay= quads)
