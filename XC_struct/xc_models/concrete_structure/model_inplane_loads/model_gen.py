# -*- coding: utf-8 -*-
import os
import xc_base
import geom
import xc
import math
from model import predefined_spaces
from model.geometry import grid_model as gm
from materials import typical_materials as tm
from model.mesh import finit_el_model as fem
from postprocess import output_styles as outSty
from postprocess import output_handler as outHndl
from model.sets import sets_mng as sets
from actions import loads
from actions import load_cases as lcases
from actions import combinations as cc
from actions.earth_pressure import earth_pressure as ep
from postprocess.config import default_config
from solution import predefined_solutions

Klf_ft_2_N_m=4450/0.3048
    


# Default configuration of environment variables.
workingDirectory= default_config.findWorkingDirectory()+'/'
execfile(workingDirectory+'env_config.py')
execfile(workingDirectory+'data.py')
eSize= 0.5     #length of elements
#             *** GEOMETRIC model (points, lines, surfaces) - SETS ***
FEcase= xc.FEProblem()
preprocessor=FEcase.getPreprocessor
prep=preprocessor   #short name
nodes= prep.getNodeHandler
elements= prep.getElementHandler
elements.dimElem= 3
# Problem type
modelSpace= predefined_spaces.StructuralMechanics3D(nodes) #Defines the
sty=outSty.OutputStyle()
out=outHndl.OutputHandler(modelSpace,sty)
#grid model definition
gridGeom= gm.GridModel(prep,xList,yList,zList)
# Grid geometric entities definition (points, lines, surfaces)
# Points' generation
gridGeom.generatePoints()
#surfaces
hollowcore=gridGeom.genSurfMultiXYZRegion(
    [((xEW,yNW,0),(xGridA,yStair2_1,0)),
     ((xEW,yStair2_2,0),(xGridA,ySW,0)),
     ((xGridA,yRamp_1,0),(xRamp_1,ySW,0)),
     ((xRamp_1,yRamp_2,0),(xRamp_2,ySW,0)),
     ((xRamp_2,yStair1,0),(xStair1,ySW,0)),
     ((xStair1,yNW,0),(xWW,ySW,0))],
    'hollowcore')

#out.displayBlocks()

#                         *** MATERIALS ***
from materials.aci import ACI_materials as ACImat
concrete=ACImat.c4000

concrProp=tm.MaterialData(name='concrProp',E=concrete.Ecm(),nu=concrete.nuc,rho=concrete.density())
#     
hollowcore_mat=tm.DeckMaterialData(name='hollowcore_mat',thickness= slabTh,material=concrProp)
hollowcore_mat.setupElasticSection(preprocessor=prep)   #creates the section-material

hollowcore_mesh=fem.SurfSetToMesh(surfSet=hollowcore,matSect=hollowcore_mat,elemSize=eSize,elemType='ShellMITC4')
fem.multi_mesh(preprocessor=prep,lstMeshSets=[hollowcore_mesh])

#out.displayFEMesh()

#                       ***BOUNDARY CONDITIONS***
def getNodesYLine(coord,tol=0.01):
    '''coord=[x,[y1,y2]]
    '''
    pt1=geom.Pos3d(coord[0],coord[1][0],0)
    pt2=geom.Pos3d(coord[0],coord[1][1],0)
    nod=sets.get_nodes_wire(hollowcore,[pt1,pt2],tol)
    return nod
def getNodesXLine(coord,tol=0.01):
    '''coord=[[x1,x2],y]
    '''
    pt1=geom.Pos3d(coord[0][0],coord[1],0)
    pt2=geom.Pos3d(coord[0][1],coord[1],0)
    nod=sets.get_nodes_wire(hollowcore,[pt1,pt2],tol)
    return nod

EastW_nod=getNodesYLine([xEW,[yNW,ySW]])
WestW_nod=getNodesYLine([xWW,[yNW,ySW]])
gap=0.5
Ramp_nod_E=getNodesYLine([xGridA,[yNW+gap,yRamp_1-gap]])
Ramp_nod_E+=getNodesYLine([xRamp_1,[yRamp_1+gap,yRamp_2-gap]])
Ramp_nod_W=getNodesYLine([xRamp_2,[yStair1+gap,yRamp_2-gap]])
Stair1_nod_W=getNodesYLine([xStair1,[yNW+gap,yStair1-gap]])
Stair2_nod_W=getNodesYLine([xGridA,[yStair2_1+gap,yStair2_2-gap]])


nodY=EastW_nod+WestW_nod
for n in nodY:
    modelSpace.fixNode000_FFF(n.tag)

nodY=Ramp_nod_E+Ramp_nod_W+Stair1_nod_W+Stair2_nod_W

for n in nodY:
    modelSpace.fixNodeF00_FFF(n.tag)

#out.displayFEMesh()

NorthW_nod=getNodesXLine([[xEW,xWW],yNW])
SouthW_nod=getNodesXLine([[xEW,xWW],ySW])

Ramp_nod_N=getNodesXLine([[xGridA,xRamp_1],yRamp_1])
Ramp_nod_S=getNodesXLine([[xRamp_1,xRamp_2],yRamp_2])
Stair1_nod_S=getNodesXLine([[xRamp_2,xStair1],yStair1])
Stair2_nod_N=getNodesXLine([[xEW,xGridA],yStair2_1])
Stair2_nod_S=getNodesXLine([[xEW,xGridA],yStair2_2])

nodX=NorthW_nod+SouthW_nod
for n in nodX:
    modelSpace.fixNode000_FFF(n.tag)

nodX=Ramp_nod_N+Ramp_nod_S+Stair1_nod_S+Stair2_nod_N+Stair2_nod_S
for n in nodX:
    modelSpace.fixNode0F0_FFF(n.tag)
#out.displayFEMesh()

EastW_L=ySW-yNW-(yStair2_2-yStair2_1)
WestW_L=ySW-yNW
NorthW_L=xWW-xEW-(xStair1-xGridA)
SouthW_L=xWW-xEW
bound_ret_walls=[[EastW_nod,EastW_L,'East retaining wall'],[WestW_nod,WestW_L,'West retaining wall'],[NorthW_nod,NorthW_L,'North retaining wall'],[SouthW_nod,SouthW_L,'South retaining wall']] #[node list, wall length,description]
bound_ramp=[[Ramp_nod_E,yRamp_2-yRamp_1,'Ramp East wall'],
            [Ramp_nod_W,yRamp_2-yStair1,'Ramp West wall'],
            [Ramp_nod_N,xRamp_1-xGridA,'Ramp North wall'],
            [Ramp_nod_S,xRamp_2-xRamp_1,'Ramp South wall']]
bound_stair1=[[Stair1_nod_W,yStair1-yNW,'Stair 1 West wall'],
              [Stair1_nod_S,xStair1-xRamp_2,'Stair 1 South wall']]
bound_stair2=[[Stair2_nod_W,yStair2_2-yStair2_1,'Stair 2 West wall'],
              [Stair2_nod_N,xGridA-xEW,'Stair 2 North wall'],
              [Stair2_nod_S,xGridA-xEW,'Stair 2 South wall']]


def addLoadNodesXLine(shearWall,tol,direct):
    '''direct: load direction: 1:+Y, -1:-Y'''
    coor=shearWall[0]
    unifload=shearWall[1]*Klf_ft_2_N_m
    totalLoad=unifload*(coor[0][1]-coor[0][0])
    nod=getNodesXLine(coor,tol)
    nNod=len(nod)
    loadPerNode=totalLoad/nNod
    for n in nod:
        n.newLoad(xc.Vector([direct*loadPerNode,0,0,0,0,0]))
    
def addLoadNodesYLine(shearWall,tol,direct):
    '''direct: load direction: 1:+X, -1:-X'''
    coor=shearWall[0]
    unifload=shearWall[1]*Klf_ft_2_N_m
    totalLoad=unifload*(coor[1][1]-coor[1][0])
    nod=getNodesYLine(coor,tol)
    nNod=len(nod)
    loadPerNode=totalLoad/nNod
    for n in nod:
        n.newLoad(xc.Vector([0,direct*loadPerNode,0,0,0,0]))
    
    
 #Loads
loadHand=preprocessor.getLoadHandler

tol=0.3

def meanReact(boundNodLst):
    for bound in boundNodLst:
        lstNodes=bound[0]
        nNodes=len(lstNodes)
        totalRx=0
        totalRy=0
        for n in lstNodes:
            totalRx+=n.getReaction[0]
            totalRy+=n.getReaction[1]
        for n in lstNodes:
            n.setReaction(xc.Vector([totalRx/nNodes,totalRy/nNodes,0,0,0,0]))

#Wind East_West (lines X direction)
Wind_EW=lcases.LoadCase(preprocessor=prep,name="Wind_EW",loadPType="default",timeSType="constant_ts")
Wind_EW.create()
for wall in ShearXwalls:
    addLoadNodesXLine(wall,tol,1)
loadHand.addToDomain(Wind_EW.name)
out.displayLoads()
analysis= predefined_solutions.simple_static_linear(FEcase)
result= analysis.analyze(1)
preprocessor.getNodeHandler.calculateNodalReactions(True,1e-7)

meanReact(bound_ramp)
meanReact(bound_stair1)
meanReact(bound_stair2)
out.displayReactions(fileName='windEW.jpg')

loadHand.removeFromDomain(Wind_EW.name)


#Wind North_South (lines Y direction)
Wind_NS=lcases.LoadCase(preprocessor=prep,name="Wind_NS",loadPType="default",timeSType="constant_ts")
Wind_NS.create()
for wall in ShearYwalls:
    addLoadNodesYLine(wall,tol,1)

loadHand.addToDomain(Wind_NS.name)
out.displayLoads()
analysis= predefined_solutions.simple_static_linear(FEcase)
result= analysis.analyze(1)
preprocessor.getNodeHandler.calculateNodalReactions(True,1e-7)

meanReact(bound_ramp)
meanReact(bound_stair1)
meanReact(bound_stair2)
out.displayReactions(fileName='windNS.jpg')

loadHand.removeFromDomain(Wind_NS.name)


#Wind West_East (lines X direction)
Wind_WE=lcases.LoadCase(preprocessor=prep,name="Wind_WE",loadPType="default",timeSType="constant_ts")
Wind_WE.create()
for wall in ShearXwalls:
    addLoadNodesXLine(wall,tol,-1)

loadHand.addToDomain(Wind_WE.name)
out.displayLoads()
analysis= predefined_solutions.simple_static_linear(FEcase)
result= analysis.analyze(1)
preprocessor.getNodeHandler.calculateNodalReactions(True,1e-7)

meanReact(bound_ramp)
meanReact(bound_stair1)
meanReact(bound_stair2)
out.displayReactions(fileName='windWE.jpg')

loadHand.removeFromDomain(Wind_WE.name)


#Wind South_North (lines Y direction)
Wind_SN=lcases.LoadCase(preprocessor=prep,name="Wind_SN",loadPType="default",timeSType="constant_ts")
Wind_SN.create()
for wall in ShearYwalls:
    addLoadNodesYLine(wall,tol,-1)

loadHand.addToDomain(Wind_SN.name)
out.displayLoads()
analysis= predefined_solutions.simple_static_linear(FEcase)
result= analysis.analyze(1)
preprocessor.getNodeHandler.calculateNodalReactions(True,1e-7)

meanReact(bound_ramp)
meanReact(bound_stair1)
meanReact(bound_stair2)
out.displayReactions(fileName='windSN.jpg')

loadHand.removeFromDomain(Wind_SN.name)

