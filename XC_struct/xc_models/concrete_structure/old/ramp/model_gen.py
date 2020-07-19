# -*- coding: utf-8 -*-

import os
import xc_base
import geom
import xc
import math
from model import predefined_spaces as psp
from model.geometry import grid_model as gm
from model.mesh import finit_el_model as fem
from model.boundary_cond import spring_bound_cond as sprbc
from model.sets import sets_mng as sets
from materials import typical_materials as tm
from actions import loads
from actions import load_cases as lcases
from actions import combinations as cc
from actions.earth_pressure import earth_pressure as ep
from model.geometry import geom_utils as gut
from materials.ehe import EHE_materials
#from materials.sia262 import SIA262_materials
from materials.ec3 import EC3_materials

# Default configuration of environment variables.
from postprocess.config import default_config



workingDirectory= default_config.findWorkingDirectory()+'/'
execfile(workingDirectory+'env_config.py')
execfile(workingDirectory+'data.py')

#Auxiliary data
#Materials
concrete=EHE_materials.HA30
reinfSteel=EHE_materials.B500S
# concrete=SIA262_materials.c30_37
# reinfSteel=SIA262_materials.B500B

eSize= 0.35     #length of elements

#             *** GEOMETRIC model (points, lines, surfaces) - SETS ***
FEcase= xc.FEProblem()
preprocessor=FEcase.getPreprocessor
prep=preprocessor   #short name
nodes= prep.getNodeHandler
elements= prep.getElementHandler
elements.dimElem= 3
# Problem type
modelSpace= psp.StructuralMechanics3D(nodes) #Defines the
# dimension of the space: nodes by three coordinates (x,y,z) and 
# six DOF for each node (Ux,Uy,Uz,thetaX,thetaY,thetaZ)


# grid model definition
gridGeom= gm.GridModel(prep,xList,yList,zList)

# Grid geometric entities definition (points, lines, surfaces)
# Points' generation
gridGeom.generatePoints()



#Slope (in X direction, Y direction or both) the grid points in a range
#syntax: slopePointsRange(ijkRange,slopeX,xZeroSlope,slopeY,yZeroSlope)
#     ijkRange: range for the search.
#     slopeX: slope in X direction, expressed as deltaZ/deltaX 
#                       (defaults to 0 = no slope applied)
#     xZeroSlope: coordinate X of the "rotation axis".
#     slopeY: slope in Y direction, expressed as deltaZ/deltaY)
#                       (defaults to 0 = no slope applied)
#     yZeroSlope: coordinate Y of the "rotation axis".

#First 8% slope range
j1=0
j2=lastYpos
slope8a_rg=gm.IJKRange((0,j1,lastZpos),(lastXpos,j2,lastZpos))
gridGeom.slopePointsRange(ijkRange=slope8a_rg,slopeX=0,xZeroSlope=0,slopeY=-0.08,yZeroSlope=0)
j1=yList.index(ySlopeChange[0])
j2=lastYpos
slope15_rg=gm.IJKRange((0,j1,lastZpos),(lastXpos,j2,lastZpos))
gridGeom.slopePointsRange(ijkRange=slope15_rg,slopeX=0,xZeroSlope=0,slopeY=-0.15+0.08,yZeroSlope=ySlopeChange[0])
j1=yList.index(ySlopeChange[1])
j2=lastYpos
slope8b_rg=gm.IJKRange((0,j1,lastZpos),(lastXpos,j2,lastZpos))
gridGeom.slopePointsRange(ijkRange=slope8b_rg,slopeX=0,xZeroSlope=0,slopeY=0.15-0.08,yZeroSlope=ySlopeChange[1])

#Ranges for lines and surfaces
ramp_rg=gm.IJKRange((0,0,lastZpos),(lastXpos,lastYpos,lastZpos))
#Surfaces generation
ramp=gridGeom.genSurfOneRegion(ijkRange=ramp_rg,setName='ramp')

ramp.description='Ramp'

ramp.fillDownwards()

#                         *** MATERIALS *** 
concrProp=tm.MaterialData(name='concrProp',E=concrete.Ecm(),nu=concrete.nuc,rho=concrete.density())

# Isotropic elastic section-material appropiate for plate and shell analysis
ramp_mat=tm.DeckMaterialData(name='ramp_mat',thickness=rampTh,material=concrProp)
ramp_mat.setupElasticSection(preprocessor=prep)   #creates the section-material

#                         ***FE model - MESH***
# IMPORTANT: it's convenient to generate the mesh of surfaces before meshing
# the lines, otherwise, sets of shells can take also beam elements touched by
# them
ramp_mesh=fem.SurfSetToMesh(surfSet=ramp,matSect=ramp_mat,elemSize=eSize,elemType='ShellMITC4')
ramp_mesh.generateMesh(prep)     #mesh the set of surfaces

ramp.fillDownwards()


#                       ***BOUNDARY CONDITIONS***
#fixed DOF (ux:'0FF_FFF', uy:'F0F_FFF', uz:'FF0_FFF',
#           rx:'FFF_0FF', ry:'FFF_F0F', rz:'FFF_FF0')
j=0
linWall0_rg=gm.IJKRange((0,j,lastZpos),(lastXpos,j,lastZpos))
aux1=gridGeom.getSetPntRange(linWall0_rg,'aux1')
linWall0=sets.get_lines_on_points(aux1,'linWall0')
for l in  linWall0.getLines:
    for n in l.nodes:
        modelSpace.fixNode('000_FFF',n.tag)

j=yList.index(yWalls[0])
linWall1_rg=gm.IJKRange((0,j,lastZpos),(lastXpos,j,lastZpos))
aux2=gridGeom.getSetPntRange(linWall1_rg,'aux2')
linWall1=sets.get_lines_on_points(aux2,'linWall1')
for l in  linWall1.getLines:
    for n in l.nodes:
        modelSpace.fixNode('FF0_FFF',n.tag)

j=yList.index(yWalls[1])
linWall2_rg=gm.IJKRange((0,j,lastZpos),(lastXpos,j,lastZpos))
aux3=gridGeom.getSetPntRange(linWall2_rg,'aux3')
linWall2=sets.get_lines_on_points(aux3,'linWall2')
for l in  linWall2.getLines:
    for n in l.nodes:
        modelSpace.fixNode('FF0_FFF',n.tag)

j=yList.index(yWalls[2])
linWall3_rg=gm.IJKRange((0,j,lastZpos),(lastXpos,j,lastZpos))
aux4=gridGeom.getSetPntRange(linWall3_rg,'aux4')
linWall3=sets.get_lines_on_points(aux4,'linWall3')
for l in  linWall3.getLines:
    for n in l.nodes:
        modelSpace.fixNode('FF0_FFF',n.tag)

j=lastYpos
linWall4_rg=gm.IJKRange((0,j,lastZpos),(lastXpos,j,lastZpos))
aux5=gridGeom.getSetPntRange(linWall4_rg,'aux5')
linWall4=sets.get_lines_on_points(aux5,'linWall4')
for l in  linWall4.getLines:
    for n in l.nodes:
        modelSpace.fixNode('000_FFF',n.tag)

#                       ***ACTIONS***

#Inertial load (density*acceleration) applied to the elements in a set
grav=9.81 #Gravity acceleration (m/s2)
#selfWeight=loads.InertialLoad(name='selfWeight', lstMeshSets=[beamXconcr_mesh,beamY_mesh,columnZconcr_mesh,deck_mesh,wall_mesh,foot_mesh], vAccel=xc.Vector( [0.0,0.0,-grav]))
selfWeight=loads.InertialLoad(name='selfWeight', lstMeshSets=[ramp_mesh], vAccel=xc.Vector( [0.0,0.0,-grav]))


# Point load acting on one or several nodes
#     name:       name identifying the load
#     lstNod:     list of nodes  on which the load is applied
#     loadVector: xc.Vector with the six components of the load: 
#                 xc.Vector([Fx,Fy,Fz,Mx,My,Mz]).

nodPLoad=sets.get_lstNod_from_lst3DPos(preprocessor=prep,lst3DPos=[geom.Pos3d(ramp_width/2.0,yWalls[0]/2.0,zList[lastZpos])])
QpuntSpan1=loads.NodalLoad(name='QpuntSpan1',lstNod=nodPLoad,loadVector=xc.Vector([0,0,-concLoad,0,0,0]))
nodPLoad=sets.get_lstNod_from_lst3DPos(preprocessor=prep,lst3DPos=[geom.Pos3d(ramp_width/2.0,yWalls[0]+dimW1_W2/2.0,zList[lastZpos])])
QpuntSpan2=loads.NodalLoad(name='QpuntSpan2',lstNod=nodPLoad,loadVector=xc.Vector([0,0,-concLoad,0,0,0]))
nodPLoad=sets.get_lstNod_from_lst3DPos(preprocessor=prep,lst3DPos=[geom.Pos3d(ramp_width/2.0,yWalls[1]+dimW2_W3/2.0,zList[lastZpos])])
QpuntSpan3=loads.NodalLoad(name='QpuntSpan3',lstNod=nodPLoad,loadVector=xc.Vector([0,0,-concLoad,0,0,0]))




# Uniform loads applied on shell elements
#    name:       name identifying the load
#    xcSet:     set that contains the surfaces
#    loadVector: xc.Vector with the six components of the load: 
#                xc.Vector([Fx,Fy,Fz,Mx,My,Mz]).
#    refSystem: reference system in which loadVector is defined:
#               'Local': element local coordinate system
#               'Global': global coordinate system (defaults to 'Global)

unifLoadRamp= loads.UniformLoadOnSurfaces(name= 'unifLoadRamp',xcSet=ramp,loadVector=xc.Vector([0,0,-unifLoad,0,0,0]),refSystem='Global')

#    ***LOAD CASES***

#Dead load
DeadL=lcases.LoadCase(preprocessor=prep,name="DeadL",loadPType="default",timeSType="constant_ts")
DeadL.create()
DeadL.addLstLoads([selfWeight])

LiveLunif=lcases.LoadCase(preprocessor=prep,name="LiveLunif",loadPType="default",timeSType="constant_ts")
LiveLunif.create()
LiveLunif.addLstLoads([unifLoadRamp])

LiveLconcSpan1=lcases.LoadCase(preprocessor=prep,name="LiveLconcSpan1",loadPType="default",timeSType="constant_ts")
LiveLconcSpan1.create()
LiveLconcSpan1.addLstLoads([QpuntSpan1])

LiveLconcSpan2=lcases.LoadCase(preprocessor=prep,name="LiveLconcSpan2",loadPType="default",timeSType="constant_ts")
LiveLconcSpan2.create()
LiveLconcSpan2.addLstLoads([QpuntSpan2])

LiveLconcSpan3=lcases.LoadCase(preprocessor=prep,name="LiveLconcSpan3",loadPType="default",timeSType="constant_ts")
LiveLconcSpan3.create()
LiveLconcSpan3.addLstLoads([QpuntSpan3])

#    ***LIMIT STATE COMBINATIONS***
combContainer= cc.CombContainer()  #Container of load combinations

# COMBINATIONS OF ACTIONS FOR ULTIMATE LIMIT STATES
    # name:        name to identify the combination
    # perm:        combination for a persistent or transient design situation
    # acc:         combination for a accidental design situation
    # fatigue:     combination for a fatigue design situation
    # earthquake:  combination for a seismic design situation
#Persistent and transitory situations.
combContainer.ULS.perm.add('ELU01', '1.4*DeadL')
combContainer.ULS.perm.add('ELU02', '1.2*DeadL+1.6*LiveLunif')
combContainer.ULS.perm.add('ELU03', '1.2*DeadL+1.6*LiveLconcSpan1')
combContainer.ULS.perm.add('ELU04', '1.2*DeadL+1.6*LiveLconcSpan2')
combContainer.ULS.perm.add('ELU05', '1.2*DeadL+1.6*LiveLconcSpan3')
