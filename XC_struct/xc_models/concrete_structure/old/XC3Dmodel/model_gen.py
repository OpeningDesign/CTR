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

#Displacements of the grid points in a range
#syntax: movePointsRange(ijkRange,vDisp)
#        ijkRange: range for the search
#        vDisp: xc vector displacement
# for i in range(1,len(xList)):
#     r= gm.IJKRange((i,0,lastZpos),(i,lastYpos,lastZpos))
#     gridGeom.movePointsRange(r,xc.Vector([0.0,0.0,-trSlope*xList[i]]))


#Slope (in X direction, Y direction or both) the grid points in a range
#syntax: slopePointsRange(ijkRange,slopeX,xZeroSlope,slopeY,yZeroSlope)
#     ijkRange: range for the search.
#     slopeX: slope in X direction, expressed as deltaZ/deltaX 
#                       (defaults to 0 = no slope applied)
#     xZeroSlope: coordinate X of the "rotation axis".
#     slopeY: slope in Y direction, expressed as deltaZ/deltaY)
#                       (defaults to 0 = no slope applied)
#     yZeroSlope: coordinate Y of the "rotation axis".

#Scale in X with origin xOrig (fixed axis: X=xOrig) to the points in a range
#Only X coordinate of points is modified in the following way:
#       x_scaled=xOrig+scale*(x_inic-xOrig)
#syntax: scaleCoorXPointsRange(ijkRange,xOrig,scale)
#     ijkRange: range for the search.
#     xOrig: origin X to apply scale (point in axis X=xOrig)
#            are not affected by the transformation 
#     scale: scale to apply to X coordinate

#Scale in Y with origin yOrig (fixed axis: Y=yOrig) to the points in a range
#Only Y coordinate of points is modified in the following way:
#       y_scaled=yOrig+scale*(y_inic-yOrig)
#syntax: scaleCoorYPointsRange(ijkRange,yOrig,scale)
#     ijkRange: range for the search.
#     yOrig: origin Y to apply scale (point in axis Y=yOrig)
#            are not affected by the transformation 
#     scale: scale to apply to Y coordinate

#Scale in Z with origin zOrig (fixed axis: Z=zOrig) to the points in a range
#Only Z coordinate of points is modified in the following way:
#       z_scaled=zOrig+scale*(z_inic-zOrig)
#syntax: scaleCoorZPointsRange(ijkRange,zOrig,scale)
#     ijkRange: range for the search.
#     zOrig: origin Z to apply scale (point in axis Z=zOrig)
#            are not affected by the transformation 
#     scale: scale to apply to Z coordinate

#Ranges for lines and surfaces
# extractIncludedIJranges(step): subranges index K=constant (default step=1)
# extractIncludedIKranges((step): subranges index J=constant (default step=1)
# extractIncludedJKranges((step): subranges index I=constant (default step=1)
# extractIncludedIranges(stepJ,stepK): subranges indexes J,K=constant (default
#                                      stpes= 1)
# idem for J and K ranges

#  Columns
k1=zList.index(0)
k2=zList.index(zCol)

colA_rg=[]
i=xList.index(xCols[0])
for y in yCols:
    j=yList.index(y)
    colA_rg.append(gm.IJKRange((i,j,k1),(i,j,k2)))
colB_rg=[]
i=xList.index(xCols[1])
for y in yCols:
    j=yList.index(y)
    colB_rg.append(gm.IJKRange((i,j,k1),(i,j,k2)))
colC_rg=[]
i=xList.index(xCols[2])
for y in yCols:
    j=yList.index(y)
    colC_rg.append(gm.IJKRange((i,j,k1),(i,j,k2)))
colD_rg=[]
i=xList.index(xCols[3])
for y in yCols:
    j=yList.index(y)
    colD_rg.append(gm.IJKRange((i,j,k1),(i,j,k2)))
colG_rg=[]
i=xList.index(xCols[4])
for y in yCols:
    j=yList.index(y)
    colG_rg.append(gm.IJKRange((i,j,k1),(i,j,k2)))
colF_rg=[]
i=xList.index(xCols[5])
for y in yCols:
    j=yList.index(y)
    colF_rg.append(gm.IJKRange((i,j,k1),(i,j,k2)))

#Beams
beamA_rg=[]
i=xList.index(xCols[0])
k=zList.index(zBeamHigh)
beamA_rg.append(gm.IJKRange((i,0,k),(i,yList.index(yCols[0]-gap/2.0),k)))
for j in range(len(yCols)-1):
    beamA_rg.append(gm.IJKRange((i,yList.index(yCols[j]+gap/2.),k),(i,yList.index(yCols[j+1]-gap/2.0),k)))
beamA_rg.append(gm.IJKRange((i,yList.index(yCols[-1]+gap/2.),k),(i,lastYpos,k)))

beamB_rg=[]
i=xList.index(xCols[1])
k=zList.index(zBeamHigh)
for j in range(1,len(yCols)-1):
    beamB_rg.append(gm.IJKRange((i,yList.index(yCols[j]+gap/2.),k),(i,yList.index(yCols[j+1]-gap/2.0),k)))
beamB_rg.append(gm.IJKRange((i,yList.index(yCols[-1]+gap/2.),k),(i,lastYpos,k)))

beamC_rg=[]
i=xList.index(xCols[2])
k=zList.index(zBeamHigh)
beamC_rg.append(gm.IJKRange((i,yList.index(yCols[-1]+gap/2.),k),(i,lastYpos,k)))

beamD_rg=[]
i=xList.index(xCols[3])
k=zList.index(zBeamHigh)
beamD_rg.append(gm.IJKRange((i,yList.index(yCols[-1]+gap/2.),k),(i,lastYpos,k)))

beamG_rg=[]
i=xList.index(xCols[4])
k=zList.index(zBeamHigh)
beamG_rg.append(gm.IJKRange((i,yList.index(yCols[-1]+gap/2.),k),(i,lastYpos,k)))

beamF_rg=[]
i=xList.index(xCols[5])
k=zList.index(zBeamHigh)
beamF_rg.append(gm.IJKRange((i,yList.index(yCols[-1]+gap/2.),k),(i,lastYpos,k)))

beam1_rg=[]
j=yList.index(yCols[0])
k=zList.index(zBeamHigh)
for i in range(1,len(xCols)-1):
    beam1_rg.append(gm.IJKRange((xList.index(xCols[i]+gap/2.),j,k),(xList.index(xCols[i+1]-gap/2.0),j,k)))
beam1_rg.append(gm.IJKRange((xList.index(xCols[-1]+gap/2.),j,k),(lastXpos,j,k)))

beam2H_rg=[]
j=yList.index(yCols[1])
k=zList.index(zBeamHigh)
i=1
beam2H_rg.append(gm.IJKRange((xList.index(xCols[i]+gap/2.),j,k),(xList.index(xCols[i+1]-gap/2.0),j,k)))
for i in range(3,len(xCols)-1):
    beam2H_rg.append(gm.IJKRange((xList.index(xCols[i]+gap/2.),j,k),(xList.index(xCols[i+1]-gap/2.0),j,k)))
beam2H_rg.append(gm.IJKRange((xList.index(xCols[-1]+gap/2.),j,k),(lastXpos,j,k)))

beam2L_rg=[]
j=yList.index(yCols[1])
k=zList.index(zBeamHigh)
i=2
beam2L_rg.append(gm.IJKRange((xList.index(xCols[i]+gap/2.),j,k),(xList.index(xCols[i+1]-gap/2.0),j,k)))

beam3H_rg=[]
j=yList.index(yCols[2])
k=zList.index(zBeamHigh)
i=1
beam3H_rg.append(gm.IJKRange((xList.index(xCols[i]+gap/2.),j,k),(xList.index(xCols[i+1]-gap/2.0),j,k)))
for i in range(3,len(xCols)-1):
    beam3H_rg.append(gm.IJKRange((xList.index(xCols[i]+gap/2.),j,k),(xList.index(xCols[i+1]-gap/2.0),j,k)))
beam3H_rg.append(gm.IJKRange((xList.index(xCols[-1]+gap/2.),j,k),(lastXpos,j,k)))

beam3L_rg=[]
j=yList.index(yCols[2])
k=zList.index(zBeamHigh)
i=2
beam3L_rg.append(gm.IJKRange((xList.index(xCols[i]+gap/2.),j,k),(xList.index(xCols[i+1]-gap/2.0),j,k)))

beam4H_rg=[]
j=yList.index(yCols[3])
k=zList.index(zBeamHigh)
i=1
beam4H_rg.append(gm.IJKRange((xList.index(xCols[i]+gap/2.),j,k),(xList.index(xCols[i+1]-gap/2.0),j,k)))
for i in range(3,len(xCols)-1):
    beam4H_rg.append(gm.IJKRange((xList.index(xCols[i]+gap/2.),j,k),(xList.index(xCols[i+1]-gap/2.0),j,k)))
beam4H_rg.append(gm.IJKRange((xList.index(xCols[-1]+gap/2.),j,k),(lastXpos,j,k)))

beam4L_rg=[]
j=yList.index(yCols[3])
k=zList.index(zBeamHigh)
i=2
beam4L_rg.append(gm.IJKRange((xList.index(xCols[i]+gap/2.),j,k),(xList.index(xCols[i+1]-gap/2.0),j,k)))

beam5H_rg=[]
j=yList.index(yCols[4])
k=zList.index(zBeamHigh)
i=1
beam5H_rg.append(gm.IJKRange((xList.index(xCols[i]+gap/2.),j,k),(xList.index(xCols[i+1]-gap/2.0),j,k)))
for i in range(3,len(xCols)-1):
    beam5H_rg.append(gm.IJKRange((xList.index(xCols[i]+gap/2.),j,k),(xList.index(xCols[i+1]-gap/2.0),j,k)))
beam5H_rg.append(gm.IJKRange((xList.index(xCols[-1]+gap/2.),j,k),(lastXpos,j,k)))

beam5L_rg=[]
j=yList.index(yCols[4])
k=zList.index(zBeamHigh)
i=2
beam5L_rg.append(gm.IJKRange((xList.index(xCols[i]+gap/2.),j,k),(xList.index(xCols[i+1]-gap/2.0),j,k)))


# Precast slabs

slabW1_rg=[]
j1=0
j2=yList.index(yCols[0]-gap/2.)
k=zList.index(zBeamHigh)
slabW1_rg.append(gm.IJKRange((0,j1,k),(xList.index(xRamp[0]),j2,k)))

slab12_rg=[]
j1=yList.index(yCols[0]+gap/2.)
j2=yList.index(yCols[1]-gap/2.)
k=zList.index(zBeamHigh)
slab12_rg.append(gm.IJKRange((0,j1,k),(xList.index(xRamp[0]),j2,k)))
slab12_rg.append(gm.IJKRange((xList.index(xRamp[0]),j1,k),(xList.index(xCols[0]-gap/2.),j2,k)))

slab23_rg=[]
j1=yList.index(yCols[1]+gap/2.)
j2=yList.index(yCols[2]-gap/2.)
k=zList.index(zBeamHigh)
slab23_rg.append(gm.IJKRange((0,j1,k),(xList.index(xCols[1]),j2,k)))

slab34_rg=[]
j1=yList.index(yCols[2]+gap/2.)
j2=yList.index(yStair1[0])
k=zList.index(zBeamHigh)
slab34_rg.append(gm.IJKRange((0,j1,k),(xList.index(xCols[1]),j2,k)))
j1=yList.index(yStair1[0])
j2=yList.index(yCols[3]-gap/2.)
slab34_rg.append(gm.IJKRange((xList.index(xCols[0]),j1,k),(xList.index(xCols[1]),j2,k)))

slab45_rg=[]
j1=yList.index(yCols[3]+gap/2.)
j2=yList.index(yCols[4]-gap/2.)
k=zList.index(zBeamHigh)
slab45_rg.append(gm.IJKRange((0,j1,k),(xList.index(xCols[1]),j2,k)))

slab5W_rg=[]
j1=yList.index(yCols[4]+gap/2.)
j2=yList.index(yFac[-1])
k=zList.index(zBeamHigh)
slab5W_rg.append(gm.IJKRange((0,j1,k),(xList.index(xCols[2]),j2,k)))
slab5W_rg.append(gm.IJKRange((xList.index(xCols[3]),j1,k),(xList.index(xFac[-1]),j2,k)))

slabBC_rg=[]
i1=xList.index(xStair2Elev[0])
i2=xList.index(xCols[2]-gap/2.)
k=zList.index(zBeamHigh)
slabBC_rg.append(gm.IJKRange((i1,0,k),(i2,yList.index(yCols[0]),k)))
i1=xList.index(xCols[1]+gap/2.)
i2=xList.index(xCols[2]-gap/2.)
k=zList.index(zBeamHigh)
slabBC_rg.append(gm.IJKRange((i1,yList.index(yCols[0]),k),(i2,yList.index(yCols[-1]),k)))

slabCD_H_rg=[]
i1=xList.index(xCols[2]+gap/2.0)
i2=xList.index(xCols[3]-gap/2.)
k=zList.index(zBeamHigh)
slabCD_H_rg.append(gm.IJKRange((i1,0,k),(i2,yList.index(yFac[1]),k)))
slabCD_L_rg=[]
k=zList.index(zBeamHigh)
slabCD_L_rg.append(gm.IJKRange((i1,yList.index(yFac[1]),k),(i2,lastYpos,k)))

slabDG_rg=[]
i1=xList.index(xCols[3]+gap/2.)
i2=xList.index(xCols[4]-gap/2.)
k=zList.index(zBeamHigh)
slabDG_rg.append(gm.IJKRange((i1,0,k),(i2,yList.index(yCols[-1]),k)))

slabGF_rg=[]
i1=xList.index(xCols[4]+gap/2.)
i2=xList.index(xCols[-1]-gap/2.)
k=zList.index(zBeamHigh)
slabGF_rg.append(gm.IJKRange((i1,0,k),(i2,yList.index(yCols[-1]),k)))

slabFW_rg=[]
i1=xList.index(xCols[-1]+gap/2.)
i2=xList.index(xFac[3])
k=zList.index(zBeamHigh)
slabFW_rg.append(gm.IJKRange((i1,0,k),(i2,yList.index(yCols[-1]),k)))

slabsF_L_rg=[]
i1=xList.index(xFac[3])
i2=lastXpos
k=zList.index(zBeamHigh)
slabsF_L_rg.append(gm.IJKRange((i1,0,k),(i2,yList.index(yFac[2]),k)))


slabs5_L_rg=[]
j1=yList.index(yFac[2])
j2=lastYpos
k=zList.index(zBeamHigh)
slabs5_L_rg.append(gm.IJKRange((0,j1,k),(xList.index(xCols[2]),j2,k)))
slabs5_L_rg.append(gm.IJKRange((xList.index(xCols[3]),j1,k),(lastXpos,j2,k)))


#Lines generation
colA=gridGeom.genLinMultiRegion(lstIJKRange=colA_rg,setName='colA')
colB=gridGeom.genLinMultiRegion(lstIJKRange=colB_rg,setName='colB')
colC=gridGeom.genLinMultiRegion(lstIJKRange=colC_rg,setName='colC')
colD=gridGeom.genLinMultiRegion(lstIJKRange=colD_rg,setName='colD')
colG=gridGeom.genLinMultiRegion(lstIJKRange=colG_rg,setName='colG')
colF=gridGeom.genLinMultiRegion(lstIJKRange=colF_rg,setName='colF')
beamA=gridGeom.genLinMultiRegion(lstIJKRange=beamA_rg,setName='beamA')
beamB=gridGeom.genLinMultiRegion(lstIJKRange=beamB_rg,setName='beamB')
beamC=gridGeom.genLinMultiRegion(lstIJKRange=beamC_rg,setName='beamC')
beamD=gridGeom.genLinMultiRegion(lstIJKRange=beamD_rg,setName='beamD')
beamG=gridGeom.genLinMultiRegion(lstIJKRange=beamG_rg,setName='beamG')
beamF=gridGeom.genLinMultiRegion(lstIJKRange=beamF_rg,setName='beamF')
beam1=gridGeom.genLinMultiRegion(lstIJKRange=beam1_rg,setName='beam1')
beam2H=gridGeom.genLinMultiRegion(lstIJKRange=beam2H_rg,setName='beam2H')
beam2L=gridGeom.genLinMultiRegion(lstIJKRange=beam2L_rg,setName='beam2L')
beam3H=gridGeom.genLinMultiRegion(lstIJKRange=beam3H_rg,setName='beam3H')
beam3L=gridGeom.genLinMultiRegion(lstIJKRange=beam3L_rg,setName='beam3L')
beam4H=gridGeom.genLinMultiRegion(lstIJKRange=beam4H_rg,setName='beam4H')
beam4L=gridGeom.genLinMultiRegion(lstIJKRange=beam4L_rg,setName='beam4L')
beam5H=gridGeom.genLinMultiRegion(lstIJKRange=beam5H_rg,setName='beam5H')
beam5L=gridGeom.genLinMultiRegion(lstIJKRange=beam5L_rg,setName='beam5L')


#Surfaces generation
slabW1=gridGeom.genSurfMultiRegion(lstIJKRange=slabW1_rg,setName='slabW1')
slab12=gridGeom.genSurfMultiRegion(lstIJKRange=slab12_rg,setName='slab12')
slab23=gridGeom.genSurfMultiRegion(lstIJKRange=slab23_rg,setName='slab23')
slab34=gridGeom.genSurfMultiRegion(lstIJKRange=slab34_rg,setName='slab34')
slab45=gridGeom.genSurfMultiRegion(lstIJKRange=slab45_rg,setName='slab45')
slab5W=gridGeom.genSurfMultiRegion(lstIJKRange=slab5W_rg,setName='slab5W')
slabBC=gridGeom.genSurfMultiRegion(lstIJKRange=slabBC_rg,setName='slabBC')
slabCD_H=gridGeom.genSurfMultiRegion(lstIJKRange=slabCD_H_rg,setName='slabCD_H')
slabCD_L=gridGeom.genSurfMultiRegion(lstIJKRange=slabCD_L_rg,setName='slabCD_L')
slabDG=gridGeom.genSurfMultiRegion(lstIJKRange=slabDG_rg,setName='slabDG')
slabGF=gridGeom.genSurfMultiRegion(lstIJKRange=slabGF_rg,setName='slabGF')
slabFW=gridGeom.genSurfMultiRegion(lstIJKRange=slabFW_rg,setName='slabFW')

slabsF_L=gridGeom.genSurfMultiRegion(lstIJKRange=slabsF_L_rg,setName='slabsF_L')
slabs5_L=gridGeom.genSurfMultiRegion(lstIJKRange=slabs5_L_rg,setName='slabs5_L')

columns=colA+colB+colC+colD+colG+colF
columns.fillDownwards()
columns.description='Columns'
columns.color=cfg.colors['green01']
beams=beamA+beamB+beamC+beamD+beamG+beamF+beam1+beam2H+beam2L+beam3H+beam3L+beam4H+beam4L+beam5H+beam5L
beams.fillDownwards()
beams.description='Beams'
slabs_H=slabW1+slab12+slab23+slab34+slab45+slab5W+slabBC+slabCD_H+slabDG+slabGF+slabFW
slabs_H.fillDownwards()
slabs_H.description='Precast planks, top level'
slabs_L=slabCD_L+slabsF_L+slabs5_L
slabs_L.fillDownwards()
slabs_L.description='Precast planks, down level'
slabs=slabs_H+slabs_L
slabs.fillDownwards()
slabs.description='Precast planks'


#                         *** MATERIALS *** 
concrProp=tm.MaterialData(name='concrProp',E=concrete.Ecm(),nu=concrete.nuc,rho=concrete.density())

# Isotropic elastic section-material appropiate for plate and shell analysis
slabs_mat=tm.DeckMaterialData(name='slabs_mat',thickness= slabTh,material=concrProp)
slabs_mat.setupElasticSection(preprocessor=prep)   #creates the section-material

#Geometric sections
#rectangular sections
from materials.sections import section_properties as sectpr
geomSectBeams=sectpr.RectangularSection(name='geomSectBeams',b=beamWidth,h=beamHeight)
geomSectColumns=sectpr.RectangularSection(name='geomSectBeamY',b=colYdim,h=colXdim)

# Elastic material-section appropiate for 3D beam analysis, including shear
  # deformations.
  # Attributes:
  #   name:         name identifying the section
  #   section:      instance of a class that defines the geometric and
  #                 mechanical characteristiscs
  #                 of a section (e.g: RectangularSection, CircularSection,
  #                 ISection, ...)
  #   material:     instance of a class that defines the elastic modulus,
  #                 shear modulus and mass density of the material

beams_mat= tm.BeamMaterialData(name= 'beams_mat', section=geomSectBeams, material=concrProp)
beams_mat.setupElasticShear3DSection(preprocessor=prep)
columns_mat= tm.BeamMaterialData(name= 'columns_mat', section=geomSectColumns, material=concrProp)
columns_mat.setupElasticShear3DSection(preprocessor=prep)


#                         ***FE model - MESH***
# IMPORTANT: it's convenient to generate the mesh of surfaces before meshing
# the lines, otherwise, sets of shells can take also beam elements touched by
# them


beams_mesh=fem.LinSetToMesh(linSet=beams,matSect=beams_mat,elemSize=eSize,vDirLAxZ=xc.Vector([0,0,1]),elemType='ElasticBeam3d',dimElemSpace=3,coordTransfType='linear')
columns_mesh=fem.LinSetToMesh(linSet=columns,matSect=columns_mat,elemSize=eSize,vDirLAxZ=xc.Vector([0,1,0]),elemType='ElasticBeam3d',coordTransfType='linear')
slabs_mesh=fem.SurfSetToMesh(surfSet=slabs,matSect=slabs_mat,elemSize=eSize,elemType='ShellMITC4')
slabs_mesh.generateMesh(prep)     #mesh the set of surfaces

fem.multi_mesh(preprocessor=prep,lstMeshSets=[beams_mesh,columns_mesh])

column_sets=[colA,colB,colC,colD,colG,colF]
for st in column_sets:
    st.fillDownwards()

beam2=beam2H+beam2L
beam3=beam3H+beam3L
beam4=beam4H+beam4L
beam5=beam5H+beam5L
beams_sets=[beamA,beamB,beamC,beamD,beamG,beamF,beam1,beam2,beam3,beam4,beam5]
for st in beams_sets:
    st.fillDownwards()
slabs_sets=[slabW1,slab12,slab23,slab34,slab45,slab5W,slabBC,slabCD_H,slabCD_L,slabDG,slabGF,slabFW,slabCD_L,slabsF_L,slabs5_L]
for st in slabs_sets:
    st.fillDownwards()
slabs_H.fillDownwards()
slabs_L.fillDownwards()

'''
#                       ***BOUNDARY CONDITIONS***
# Regions resting on springs (Winkler elastic foundation)
#       wModulus: Winkler modulus of the foundation (springs in Z direction)
#       cRoz:     fraction of the Winkler modulus to apply for friction in
#                 the contact plane (springs in X, Y directions)
foot_wink=sprbc.ElasticFoundation(wModulus=20e7,cRoz=0.2)
foot_wink.generateSprings(xcSet=foot)
'''

# Springs (defined by Kx,Ky,Kz) to apply on nodes, points, 3Dpos, ...
# Default values for Kx, Ky, Kz are 0, which means that no spring is
# created in the corresponding direction
# spring_col=sprbc.SpringBC(name='spring_col',modelSpace=modelSpace,Kx=10e3,Ky=50e3,Kz=30e3)
# a=spring_col.applyOnNodesIn3Dpos(lst3DPos=[geom.Pos3d(0,LbeamY,0)])

#fixed DOF (ux:'0FF_FFF', uy:'F0F_FFF', uz:'FF0_FFF',
#           rx:'FFF_0FF', ry:'FFF_F0F', rz:'FFF_FF0')
# Base columns
for x in xCols:
    for y in yCols:
        n=nodes.getDomain.getMesh.getNearestNode(geom.Pos3d(x,y,0))
        modelSpace.fixNode('000_000',n.tag)
# Simple support beams on walls
z=zBeamHigh

x=xCols[0]
y=0
n=nodes.getDomain.getMesh.getNearestNode(geom.Pos3d(x,y,z))
modelSpace.fixNode('000_FFF',n.tag)

x=xList[-1]
for y in yCols:
    n=nodes.getDomain.getMesh.getNearestNode(geom.Pos3d(x,y,z))
    modelSpace.fixNode('000_FFF',n.tag)

y=yList[-1]
for x in xCols:
    n=nodes.getDomain.getMesh.getNearestNode(geom.Pos3d(x,y,z))
    modelSpace.fixNode('000_FFF',n.tag)

#Links between beams and columns
z=zCol
for x in xCols[2:6]:
    for y in yCols[0:5]:
        nCol=columns.nodes.getNearestNode(geom.Pos3d(x,y,z))
        nBeam1=beams.nodes.getNearestNode(geom.Pos3d(x-gap/2.0,y,z))
        nBeam2=beams.nodes.getNearestNode(geom.Pos3d(x+gap/2.0,y,z))
        modelSpace.setFulcrumBetweenNodes(nCol.tag,nBeam1.tag)
        modelSpace.setFulcrumBetweenNodes(nCol.tag,nBeam2.tag)
        #torsion
        modelSpace.fixNode('FFF_FF0',nCol.tag)
        modelSpace.fixNode('FFF_0FF',nBeam1.tag)
        modelSpace.fixNode('FFF_0FF',nBeam2.tag)
        
for x in xCols[2:6]:
    for y in yCols[4:5]:
        nCol=columns.nodes.getNearestNode(geom.Pos3d(x,y,z))
        nBeam1=beams.nodes.getNearestNode(geom.Pos3d(x,y+gap/2.0,z))
        modelSpace.setFulcrumBetweenNodes(nCol.tag,nBeam1.tag)
        #torsion
        modelSpace.fixNode('FFF_FF0',nCol.tag)
        modelSpace.fixNode('FFF_F0F',nBeam1.tag)

for x in xCols[1:2]:
    for y in yCols[0:5]:
        nCol=columns.nodes.getNearestNode(geom.Pos3d(x,y,z))
        nBeam1=beams.nodes.getNearestNode(geom.Pos3d(x+gap/2.0,y,z))
        modelSpace.setFulcrumBetweenNodes(nCol.tag,nBeam1.tag)
        #torsion
        modelSpace.fixNode('FFF_FF0',nCol.tag)
        modelSpace.fixNode('FFF_0FF',nBeam1.tag)

for x in xCols[1:2]:
    for y in yCols[1:2]:
        nCol=columns.nodes.getNearestNode(geom.Pos3d(x,y,z))
        nBeam1=beams.nodes.getNearestNode(geom.Pos3d(x,y+gap/2.0,z))
        modelSpace.setFulcrumBetweenNodes(nCol.tag,nBeam1.tag)
        #torsion
        modelSpace.fixNode('FFF_FF0',nCol.tag)
        modelSpace.fixNode('FFF_F0F',nBeam1.tag)
        
for x in xCols[1:2]:
    for y in yCols[2:5]:
        nCol=columns.nodes.getNearestNode(geom.Pos3d(x,y,z))
        nBeam1=beams.nodes.getNearestNode(geom.Pos3d(x,y-gap/2.0,z))
        nBeam2=beams.nodes.getNearestNode(geom.Pos3d(x,y+gap/2.0,z))
        modelSpace.setFulcrumBetweenNodes(nCol.tag,nBeam1.tag)
        modelSpace.setFulcrumBetweenNodes(nCol.tag,nBeam2.tag)
        #torsion
        modelSpace.fixNode('FFF_FF0',nCol.tag)
        modelSpace.fixNode('FFF_F0F',nBeam1.tag)
        modelSpace.fixNode('FFF_F0F',nBeam2.tag)
        
for x in xCols[0:1]:
    for y in yCols[0:5]:
        nCol=columns.nodes.getNearestNode(geom.Pos3d(x,y,z))
        nBeam1=beams.nodes.getNearestNode(geom.Pos3d(x,y-gap/2.0,z))
        nBeam2=beams.nodes.getNearestNode(geom.Pos3d(x,y+gap/2.0,z))
        modelSpace.setFulcrumBetweenNodes(nCol.tag,nBeam1.tag)
        modelSpace.setFulcrumBetweenNodes(nCol.tag,nBeam2.tag)
        #torsion
        modelSpace.fixNode('FFF_FF0',nCol.tag)
        modelSpace.fixNode('FFF_F0F',nBeam1.tag)
        modelSpace.fixNode('FFF_F0F',nBeam2.tag)

# Simple support precast planks on walls
#East
stBusq=slabW1+slab12+slab23+slab34+slab45+slab5W
z=zBeamHigh
nod=sets.get_nodes_wire(setBusq=stBusq,lstPtsWire=[geom.Pos3d(0,0,z),geom.Pos3d(0,yFac[-1],z)])
for n in nod:
    modelSpace.fixNode('FF0_FFF',n.tag)
stBusq=slabs5_L
z=zBeamHigh
nod=sets.get_nodes_wire(setBusq=stBusq,lstPtsWire=[geom.Pos3d(0,yFac[-1],z),geom.Pos3d(0,yList[-1],z)])
for n in nod:
    modelSpace.fixNode('FF0_FFF',n.tag)
#North
stBusq=slabBC+slabCD_H+slabDG+slabGF+slabFW
y=0
z=zBeamHigh
nod=sets.get_nodes_wire(setBusq=stBusq,lstPtsWire=[geom.Pos3d(0,y,z),geom.Pos3d(xFac[-1],y,z)])
for n in nod:
    modelSpace.fixNode('FF0_FFF',n.tag)
stBusq=slabsF_L
z=zBeamHigh
nod=sets.get_nodes_wire(setBusq=stBusq,lstPtsWire=[geom.Pos3d(xFac[-1],y,z),geom.Pos3d(xList[-1],y,z)])
for n in nod:
    modelSpace.fixNode('FF0_FFF',n.tag)
#West
stBusq=slabsF_L+slabs5_L
x=xList[-1]
z=zBeamHigh
nod=sets.get_nodes_wire(setBusq=stBusq,lstPtsWire=[geom.Pos3d(x,yCols[-1],z),geom.Pos3d(x,yList[-1],z)])
for n in nod:
    modelSpace.fixNode('FF0_FFF',n.tag)
#South
stBusq=slabCD_L
y=yList[-1]
z=zBeamHigh
nod=sets.get_nodes_wire(setBusq=stBusq,lstPtsWire=[geom.Pos3d(xCols[2],y,z),geom.Pos3d(xCols[3],y,z)])
for n in nod:
    modelSpace.fixNode('FF0_FFF',n.tag)
#Ramp
stBusq=slabW1+slab12
x=xRamp[0]
z=zBeamHigh
nod=sets.get_nodes_wire(setBusq=stBusq,lstPtsWire=[geom.Pos3d(x,yList[0],z),geom.Pos3d(x,yCols[1],z)])
for n in nod:
    modelSpace.fixNode('FF0_FFF',n.tag)
#Cantilever
stBusq=slab5W
x=xFac[-1]
z=zBeamHigh
nod=sets.get_nodes_wire(setBusq=stBusq,lstPtsWire=[geom.Pos3d(x,yCols[4],z),geom.Pos3d(x,yFac[-1],z)])
for n in nod:
    modelSpace.fixNode('FF0_FFF',n.tag)

'''
# Links beams to precast planks
gluedDOFs= [0,1,2,3,4]

stbeams=beam1+beam2+beam3+beam4+beam5
stslabs=slabBC+slabCD_L+slabDG+slabGF+slabFW+slabsF_L
stbeams.fillDownwards()
stslabs.fillDownwards()
nod_stbeams=stbeams.nodes
nod_stslabs=stslabs.nodes
for n in nod_stbeams:
    n1=nod_stslabs.getNearestNode(n.getCurrentPos3d(0))
    modelSpace.constraints.newEqualDOF(n.tag,n1.tag,xc.ID(gluedDOFs))
    
stbeams=beam1
stslabs=slabCD_H
stbeams.fillDownwards()
stslabs.fillDownwards()
nod_stbeams=stbeams.nodes
nod_stslabs=stslabs.nodes
for n in nod_stbeams:
    n1=nod_stslabs.getNearestNode(n.getCurrentPos3d(0))
    modelSpace.constraints.newEqualDOF(n.tag,n1.tag,xc.ID(gluedDOFs))

stbeams=beamA+beamB
stslabs=slabW1+slab12+slab23+slab34+slab45
stbeams.fillDownwards()
stslabs.fillDownwards()
nod_stbeams=stbeams.nodes
nod_stslabs=stslabs.nodes
for n in nod_stbeams:
    n1=nod_stslabs.getNearestNode(n.getCurrentPos3d(0))
    modelSpace.constraints.newEqualDOF(n.tag,n1.tag,xc.ID(gluedDOFs))
    
stbeams=beamA+beamB+beamC
stslabs=slab5W+slabs5_L
stbeams.fillDownwards()
stslabs.fillDownwards()
nod_stbeams=stbeams.nodes
nod_stslabs=stslabs.nodes
for n in nod_stbeams:
    n1=nod_stslabs.getNearestNode(n.getCurrentPos3d(0))
    modelSpace.constraints.newEqualDOF(n.tag,n1.tag,xc.ID(gluedDOFs))

    
stbeams=beamD+beamG+beamF
stslabs=slab5W+slabs5_L
stbeams.fillDownwards()
stslabs.fillDownwards()
nod_stbeams=stbeams.nodes
nod_stslabs=stslabs.nodes
for n in nod_stbeams:
    n1=nod_stslabs.getNearestNode(n.getCurrentPos3d(0))
    modelSpace.constraints.newEqualDOF(n.tag,n1.tag,xc.ID(gluedDOFs))

# Support of slabCD_H on slabCD_L
i1=xList.index(xCols[1]+gap/2.)
i2=xList.index(xCols[2]-gap/2.)
j1=yList.index(yCols[0])
j2=yList.index(yFac[1])
k=zList.index(zBeamHigh)
st1=gridGeom.getSetSurfOneRegion(gm.IJKRange((i1,j1,k),(i2,j2,k)),'st1')
nod_st1=st1.nodes
nod_st2=slabCD_L.nodes
for n in nod_st1:
    n1=nod_st2.getNearestNode(n.getCurrentPos3d(0))
    modelSpace.constraints.newEqualDOF(n.tag,n1.tag,xc.ID(gluedDOFs))
'''
execfile(workingDirectory+'lines_loads.py')
#                       ***ACTIONS***

#Inertial load (density*acceleration) applied to the elements in a set
grav=9.81 #Gravity acceleration (m/s2)
#selfWeight=loads.InertialLoad(name='selfWeight', lstMeshSets=[beamXconcr_mesh,beamY_mesh,columnZconcr_mesh,deck_mesh,wall_mesh,foot_mesh], vAccel=xc.Vector( [0.0,0.0,-grav]))
selfWeightBeamCols=loads.InertialLoad(name='selfWeightBeamCols', lstMeshSets=[beams_mesh,columns_mesh], vAccel=xc.Vector( [0.0,0.0,-grav]))


'''
# Point load acting on one or several nodes
#     name:       name identifying the load
#     lstNod:     list of nodes  on which the load is applied
#     loadVector: xc.Vector with the six components of the load: 
#                 xc.Vector([Fx,Fy,Fz,Mx,My,Mz]).

nodPLoad=sets.get_lstNod_from_lst3DPos(preprocessor=prep,lst3DPos=[geom.Pos3d(0,yList[lastYpos]/2.0,zList[lastZpos]),geom.Pos3d(xList[lastXpos],yList[lastYpos]/2.0,zList[lastZpos])])
QpuntBeams=loads.NodalLoad(name='QpuntBeams',lstNod=nodPLoad,loadVector=xc.Vector([0,0,-Qbeam,0,0,0]))
'''
# Uniform loads applied on shell elements
#    name:       name identifying the load
#    xcSet:     set that contains the surfaces
#    loadVector: xc.Vector with the six components of the load: 
#                xc.Vector([Fx,Fy,Fz,Mx,My,Mz]).
#    refSystem: reference system in which loadVector is defined:
#               'Local': element local coordinate system
#               'Global': global coordinate system (defaults to 'Global)

selfWeightSlabs= loads.UniformLoadOnSurfaces(name= 'selfWeightSlabs',xcSet=slabs,loadVector=xc.Vector([0,0,-Whollowdeck,0,0,0]),refSystem='Global')

LLunif_rooms_1floor=loads.UniformLoadOnSurfaces(name= 'LLunif_rooms_1floor',xcSet=slabs_H,loadVector=xc.Vector([0,0,-unifLLrooms,0,0,0]),refSystem='Global')
LLunif_terrace_1floor=loads.UniformLoadOnSurfaces(name= 'LLunif_rooms_1floor',xcSet=slabs_L,loadVector=xc.Vector([0,0,-unifLLterrace,0,0,0]),refSystem='Global')

SL_terrace_1floor=loads.UniformLoadOnSurfaces(name= 'SL_terrace_1floor',xcSet=slabs_L,loadVector=xc.Vector([0,0,-unifSL,0,0,0]),refSystem='Global')

#staggered patterns
from actions.utils import staggered_patterns as sptt
auxInd=list()
for x in xCols:
    auxInd.append(xList.index(x))
lIndX=[0]+auxInd+[xList.index(xFac[-1])]+[lastXpos]
auxInd=list()
for y in yCols:
    auxInd.append(yList.index(y))
lIndY=[0]+auxInd+[yList.index(yFac[-1])]+[lastYpos]
indZ=zList.index(zBeamHigh)
stag1_rg=sptt.staggeredPatternType1(lIndX,lIndY,indZ)
stag1Set=gridGeom.getSetSurfMultiRegion(stag1_rg,'stag1Set')
stag1Set.fillDownwards()
LLstag_rooms_1floor=loads.UniformLoadOnSurfaces(name= 'LLstag_rooms_1floor',xcSet=stag1Set,loadVector=xc.Vector([0,0,-unifLLrooms,0,0,0]),refSystem='Global')

indZ=zList.index(zBeamHigh)
stag2_rg=sptt.staggeredPatternType1(lIndX,lIndY,indZ)
stag2Set=gridGeom.getSetSurfMultiRegion(stag2_rg,'stag2Set')
stag2Set.fillDownwards()
LLstag_terrace_1floor=loads.UniformLoadOnSurfaces(name= 'LLstag_terrace_1floor',xcSet=stag2Set,loadVector=xc.Vector([0,0,-unifLLterrace,0,0,0]),refSystem='Global')
'''


#Uniform load on beams
# syntax: UniformLoadOnBeams(name, xcSet, loadVector,refSystem)
#    name:       name identifying the load
#    xcSet:      set that contains the lines
#    loadVector: xc.Vector with the six components of the load: 
#                xc.Vector([Fx,Fy,Fz,Mx,My,Mz]).
#    refSystem: reference system in which loadVector is defined:
#               'Local': element local coordinate system
#               'Global': global coordinate system (defaults to 'Global)
unifLoadBeamsY=loads.UniformLoadOnBeams(name='unifLoadBeamsY', xcSet=beamY, loadVector=xc.Vector([0,0,-qunifBeam,0,0,0]),refSystem='Global')

# Strain gradient on shell elements
#     name:  name identifying the load
#     xcSet: set that contains the surfaces
#     nabla: strain gradient in the thickness of the elements:
#            nabla=espilon/thickness    

#strGrad=loads.StrainLoadOnShells(name='strGrad', xcSet=deck,epsilon=0.001)
'''

# Uniform load applied to all the lines (not necessarily defined as lines
# for latter generation of beam elements, they can be lines belonging to 
# surfaces for example) found in the xcSet
# The uniform load is introduced as point loads in the nodes
#     name:   name identifying the load
#     xcSet:  set that contains the lines
#     loadVector: xc.Vector with the six components of the load: 
#                 xc.Vector([Fx,Fy,Fz,Mx,My,Mz]).

DL_lnL1=loads.UniformLoadOnLines(name='DL_lnL1',xcSet=lnL1,loadVector=xc.Vector([0,0,-1*D_lnL1,0,0,0]))
LL_lnL1=loads.UniformLoadOnLines(name='LL_lnL1',xcSet=lnL1,loadVector=xc.Vector([0,0,-1*L_lnL1,0,0,0]))
SL_lnL1=loads.UniformLoadOnLines(name='SL_lnL1',xcSet=lnL1,loadVector=xc.Vector([0,0,-1*S_lnL1,0,0,0]))

DL_lnL2=loads.UniformLoadOnLines(name='DL_lnL2',xcSet=lnL2,loadVector=xc.Vector([0,0,-1*D_lnL2,0,0,0]))
LL_lnL2=loads.UniformLoadOnLines(name='LL_lnL2',xcSet=lnL2,loadVector=xc.Vector([0,0,-1*L_lnL2,0,0,0]))
SL_lnL2=loads.UniformLoadOnLines(name='SL_lnL2',xcSet=lnL2,loadVector=xc.Vector([0,0,-1*S_lnL2,0,0,0]))

DL_lnL3=loads.UniformLoadOnLines(name='DL_lnL3',xcSet=lnL3,loadVector=xc.Vector([0,0,-1*D_lnL3,0,0,0]))
LL_lnL3=loads.UniformLoadOnLines(name='LL_lnL3',xcSet=lnL3,loadVector=xc.Vector([0,0,-1*L_lnL3,0,0,0]))
SL_lnL3=loads.UniformLoadOnLines(name='SL_lnL3',xcSet=lnL3,loadVector=xc.Vector([0,0,-1*S_lnL3,0,0,0]))

DL_lnL4=loads.UniformLoadOnLines(name='DL_lnL4',xcSet=lnL4,loadVector=xc.Vector([0,0,-1*D_lnL4,0,0,0]))
LL_lnL4=loads.UniformLoadOnLines(name='LL_lnL4',xcSet=lnL4,loadVector=xc.Vector([0,0,-1*L_lnL4,0,0,0]))
SL_lnL4=loads.UniformLoadOnLines(name='SL_lnL4',xcSet=lnL4,loadVector=xc.Vector([0,0,-1*S_lnL4,0,0,0]))

DL_lnL5=loads.UniformLoadOnLines(name='DL_lnL5',xcSet=lnL5,loadVector=xc.Vector([0,0,-1*D_lnL5,0,0,0]))
LL_lnL5=loads.UniformLoadOnLines(name='LL_lnL5',xcSet=lnL5,loadVector=xc.Vector([0,0,-1*L_lnL5,0,0,0]))
SL_lnL5=loads.UniformLoadOnLines(name='SL_lnL5',xcSet=lnL5,loadVector=xc.Vector([0,0,-1*S_lnL5,0,0,0]))

DL_lnL6=loads.UniformLoadOnLines(name='DL_lnL6',xcSet=lnL6,loadVector=xc.Vector([0,0,-1*D_lnL6,0,0,0]))
LL_lnL6=loads.UniformLoadOnLines(name='LL_lnL6',xcSet=lnL6,loadVector=xc.Vector([0,0,-1*L_lnL6,0,0,0]))
SL_lnL6=loads.UniformLoadOnLines(name='SL_lnL6',xcSet=lnL6,loadVector=xc.Vector([0,0,-1*S_lnL6,0,0,0]))

DL_lnL7=loads.UniformLoadOnLines(name='DL_lnL7',xcSet=lnL7,loadVector=xc.Vector([0,0,-1*D_lnL7,0,0,0]))
LL_lnL7=loads.UniformLoadOnLines(name='LL_lnL7',xcSet=lnL7,loadVector=xc.Vector([0,0,-1*L_lnL7,0,0,0]))
SL_lnL7=loads.UniformLoadOnLines(name='SL_lnL7',xcSet=lnL7,loadVector=xc.Vector([0,0,-1*S_lnL7,0,0,0]))

DL_lnL8=loads.UniformLoadOnLines(name='DL_lnL8',xcSet=lnL8,loadVector=xc.Vector([0,0,-1*D_lnL8,0,0,0]))

DL_lnL9=loads.UniformLoadOnLines(name='DL_lnL9',xcSet=lnL9,loadVector=xc.Vector([0,0,-1*D_lnL9,0,0,0]))
LL_lnL9=loads.UniformLoadOnLines(name='LL_lnL9',xcSet=lnL9,loadVector=xc.Vector([0,0,-1*L_lnL9,0,0,0]))
SL_lnL9=loads.UniformLoadOnLines(name='SL_lnL9',xcSet=lnL9,loadVector=xc.Vector([0,0,-1*S_lnL9,0,0,0]))

DL_lnL10=loads.UniformLoadOnLines(name='DL_lnL10',xcSet=lnL10,loadVector=xc.Vector([0,0,-1*D_lnL10,0,0,0]))
LL_lnL10=loads.UniformLoadOnLines(name='LL_lnL10',xcSet=lnL10,loadVector=xc.Vector([0,0,-1*L_lnL10,0,0,0]))
SL_lnL10=loads.UniformLoadOnLines(name='SL_lnL10',xcSet=lnL10,loadVector=xc.Vector([0,0,-1*S_lnL10,0,0,0]))

DL_lnL11=loads.UniformLoadOnLines(name='DL_lnL11',xcSet=lnL11,loadVector=xc.Vector([0,0,-1*D_lnL11,0,0,0]))

DL_lnL12=loads.UniformLoadOnLines(name='DL_lnL12',xcSet=lnL12,loadVector=xc.Vector([0,0,-1*D_lnL12,0,0,0]))
LL_lnL12=loads.UniformLoadOnLines(name='LL_lnL12',xcSet=lnL12,loadVector=xc.Vector([0,0,-1*L_lnL12,0,0,0]))
SL_lnL12=loads.UniformLoadOnLines(name='SL_lnL12',xcSet=lnL12,loadVector=xc.Vector([0,0,-1*S_lnL12,0,0,0]))

DL_lnL13=loads.UniformLoadOnLines(name='DL_lnL13',xcSet=lnL13,loadVector=xc.Vector([0,0,-1*D_lnL13,0,0,0]))
LL_lnL13=loads.UniformLoadOnLines(name='LL_lnL13',xcSet=lnL13,loadVector=xc.Vector([0,0,-1*L_lnL13,0,0,0]))
SL_lnL13=loads.UniformLoadOnLines(name='SL_lnL13',xcSet=lnL13,loadVector=xc.Vector([0,0,-1*S_lnL13,0,0,0]))

#Wind W-E
WL_WE_lnL1W=loads.UniformLoadOnLines(name='WL_WE_lnL1W',xcSet=lnL1W,loadVector=xc.Vector([0,0,WWE_lnL1W,0,0,0]))
WL_WE_lnL2W=loads.UniformLoadOnLines(name='WL_WE_lnL2W',xcSet=lnL2W,loadVector=xc.Vector([0,0,WWE_lnL2W,0,0,0]))
WL_WE_lnL3W=loads.UniformLoadOnLines(name='WL_WE_lnL3W',xcSet=lnL3W,loadVector=xc.Vector([0,0,WWE_lnL3W,0,0,0]))
WL_WE_lnL4W=loads.UniformLoadOnLines(name='WL_WE_lnL4W',xcSet=lnL4W,loadVector=xc.Vector([0,0,WWE_lnL4W,0,0,0]))
WL_WE_lnL5W=loads.UniformLoadOnLines(name='WL_WE_lnL5W',xcSet=lnL5W,loadVector=xc.Vector([0,0,WWE_lnL5W,0,0,0]))

#Wind N-S
WL_NS_lnL1W=loads.UniformLoadOnLines(name='WL_NS_lnL1W',xcSet=lnL1W,loadVector=xc.Vector([0,0,WNS_lnL1W,0,0,0]))
WL_NS_lnL6W=loads.UniformLoadOnLines(name='WL_NS_lnL6W',xcSet=lnL6W,loadVector=xc.Vector([0,0,WNS_lnL6W,0,0,0]))
WL_NS_lnL7W=loads.UniformLoadOnLines(name='WL_NS_lnL7W',xcSet=lnL7W,loadVector=xc.Vector([0,0,WNS_lnL7W,0,0,0]))

'''
# Point load distributed over the shell elements in xcSet whose 
# centroids are inside the prism defined by the 2D polygon prismBase
# and one global axis.
# syntax: PointLoadOverShellElems(name, xcSet, loadVector,prismBase,prismAxis,refSystem):
#    name: name identifying the load
#    xcSet: set that contains the shell elements
#    loadVector: xc vector with the six components of the point load:
#                   xc.Vector([Fx,Fy,Fz,Mx,My,Mz]).
#    prismBase: 2D polygon that defines the n-sided base of the prism.
#                   The vertices of the polygon are defined in global 
#                   coordinates in the following way:
#                      - for X-axis-prism: (y,z)
#                      - for Y-axis-prism: (x,z)
#                      - for Z-axis-prism: (x,y)
#    prismAxis: axis of the prism (can be equal to 'X', 'Y', 'Z')
#                   (defaults to 'Z')
#    refSystem:  reference system in which loadVector is defined:
#                   'Local': element local coordinate system
#                   'Global': global coordinate system (defaults to 'Global')

prBase=gut.rect2DPolygon(xCent=LbeamX/2.,yCent=LbeamY/2.,Lx=0.5,Ly=1.0)
wheelDeck1=loads.PointLoadOverShellElems(name='wheelDeck1', xcSet=decklv1, loadVector=xc.Vector([0,0,-Qwheel]),prismBase=prBase,prismAxis='Z',refSystem='Global')

# ---------------------------------------------------------------

# Point loads defined in the object lModel, distributed over the shell 
# elements under the wheels affected by them.

# syntax: VehicleDistrLoad(name,xcSet,loadModel, xCentr,yCentr,hDistr,slopeDistr)
#      name: name identifying the load
#      xcSet: set that contains the shell elements
#      lModel: instance of the class LoadModel with the definition of
#               vehicle of the load model.
#      xCent: global coord. X where to place the centroid of the vehicle
#      yCent: global coord. Y where  to place the centroid of the vehicle
#      hDistr: height considered to distribute each point load with
#               slope slopeDistr 
#      slopeDistr: slope (H/V) through hDistr to distribute the load of 
#               a wheel

from actions.roadway_trafic import IAP_load_models as slm
from actions.roadway_trafic import load_model_base as lmb
vehicleDeck1=lmb.VehicleDistrLoad(name='vehicleDeck1',xcSet=decklv1,loadModel=slm.IAP_carril_virt3_fren, xCentr=LbeamX/2,yCentr=LbeamY/2.,hDistr=0.25,slopeDistr=1.0)


#    ***LOAD CASES***

'''
#Dead load
DeadL=lcases.LoadCase(preprocessor=prep,name="DeadL")
DeadL.create()
DeadL.addLstLoads([DL_lnL1,DL_lnL2,DL_lnL3,DL_lnL4,DL_lnL5,DL_lnL6,DL_lnL7,DL_lnL8,DL_lnL9,DL_lnL10,DL_lnL11,DL_lnL12,DL_lnL13,selfWeightSlabs,selfWeightBeamCols])

#live load (uniform on rooms)
LiveL_ru=lcases.LoadCase(preprocessor=prep,name="LiveL_ru")
LiveL_ru.create()
LiveL_ru.addLstLoads([LL_lnL1,LL_lnL2,LL_lnL3,LL_lnL4,LL_lnL5,LL_lnL6,LL_lnL7,LL_lnL9,LL_lnL10,LL_lnL12,LL_lnL13,LLunif_rooms_1floor])

#live load (staggered pattern on rooms)
LiveL_rs=lcases.LoadCase(preprocessor=prep,name="LiveL_rs")
LiveL_rs.create()
LiveL_rs.addLstLoads([LL_lnL1,LL_lnL2,LL_lnL3,LL_lnL4,LL_lnL5,LL_lnL6,LL_lnL7,LL_lnL9,LL_lnL10,LL_lnL12,LL_lnL13,LLstag_rooms_1floor])

#live load (uniform on patios)
LiveL_pu=lcases.LoadCase(preprocessor=prep,name="LiveL_pu")
LiveL_pu.create()
LiveL_pu.addLstLoads([LLunif_terrace_1floor])

#live load (staggered pattern on patios)
LiveL_ps=lcases.LoadCase(preprocessor=prep,name="LiveL_ps")
LiveL_ps.create()
LiveL_ps.addLstLoads([LLstag_terrace_1floor])

SnowL=lcases.LoadCase(preprocessor=prep,name="SnowL")
SnowL.create()
SnowL.addLstLoads([SL_lnL1,SL_lnL2,SL_lnL3,SL_lnL4,SL_lnL5,SL_lnL6,SL_lnL7,SL_lnL9,SL_lnL10,SL_lnL12,SL_lnL13,SL_terrace_1floor])

Wind_WE=lcases.LoadCase(preprocessor=prep,name="Wind_WE")
Wind_WE.create()
Wind_WE.addLstLoads([WL_WE_lnL1W,WL_WE_lnL2W,WL_WE_lnL3W,WL_WE_lnL4W,WL_WE_lnL5W])

Wind_NS=lcases.LoadCase(preprocessor=prep,name="Wind_NS")
Wind_NS.create()
Wind_NS.addLstLoads([WL_NS_lnL1W,WL_NS_lnL6W,WL_NS_lnL7W])

overallSet=colA+colB+colC+colD+colG+colF+beamA+beamB+beam1+beam2H+beam2L+beam3H+beam3L+beam4H+beam4L+beam5H+beam5L+slabW1+slab12+slab23+slab34+slab45+slab5W+slabBC+slabCD_H+slabCD_L+slabDG+slabGF+slabFW+slabsF_L+slabs5_L

preprocessor.getDomain.getMesh.getNumFreeNodes()
'''
for n in slabs.nodes:
    print n.getCurrentPos3d(0).z
'''
slabs.fillDownwards()
slabs.description='Precast planks'
slabs.name='hollowcore'
columns.fillDownwards()
columns.name='columns'
columns.description='Columns'
beams.fillDownwards()
beams.description='1st floor beams'
beams.name='beams'
slabs_H.fillDownwards()
slabs_L.fillDownwards()

column_sets=[colA,colB,colC,colD,colG,colF]
for st in column_sets:
    st.fillDownwards()

beams_sets=[beamA,beamB,beamC,beamD,beamG,beamF,beam1,beam2,beam3,beam4,beam5]
for st in beams_sets:
    st.fillDownwards()
slabs_sets=[slabW1,slab12,slab23,slab34,slab45,slab5W,slabBC,slabCD_H,slabCD_L,slabDG,slabGF,slabFW,slabCD_L,slabsF_L,slabs5_L]
for st in slabs_sets:
    st.fillDownwards()


j=yList.index(yCols[0])
k=zList.index(zBeamHigh)
steel_beam_rg=gm.IJKRange((xList.index(xCols[1]+gap/2.),j,k),(xList.index(xCols[2]-gap/2.0),j,k))
steel_beam=gridGeom.getSetLinOneRegion(steel_beam_rg,'steel_beam')

#execfile(workingDirectory+'print_links_slabs_beams.py')

