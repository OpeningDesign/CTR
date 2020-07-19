# -*- coding: utf-8 -*-

import os
import xc_base
import geom
import xc
import math
from model import predefined_spaces
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
from materials.astm_aisc import ASTM_materials
#from materials.sia262 import SIA262_materials
from materials.ec3 import EC3_materials
from postprocess.config import default_config
from postprocess import output_styles as outSty
from postprocess import output_handler as outHndl

execfile('./data.py')
# Default configuration of environment variables.
FEcase= xc.FEProblem()
preprocessor=FEcase.getPreprocessor
prep=preprocessor   #short name
nodes= prep.getNodeHandler
elements= prep.getElementHandler
elements.dimElem= 3
# Problem type
modelSpace= predefined_spaces.StructuralMechanics3D(nodes)
sty=outSty.OutputStyle()
out=outHndl.OutputHandler(modelSpace,sty)

xList=[0,angleWidth-angleTh/2]
yList=[0,spcAnch/2,spcAnch,spcAnch*1.5,spcAnch*2]
zList=[0,zAnchor,angleHeight-angleTh/2]
gridGeom= gm.GridModel(prep,xList,yList,zList)
gridGeom.generatePoints()

support=gridGeom.genSurfMultiRegion([gm.IJKRange((0,0,0),(1,4,0)),gm.IJKRange((0,0,0),(0,4,2))],'support')

#out.displayBlocks()

#                         *** MATERIALS *** 
steel=ASTM_materials.A36

# Isotropic elastic section-material appropiate for plate and shell analysis
support_mat=tm.DeckMaterialData(name='support_mat',thickness= angleTh,material=steel)
support_mat.setupElasticSection(preprocessor=prep)
#                         ***FE model - MESH***
support_mesh=fem.SurfSetToMesh(surfSet=support,matSect=support_mat,elemSize=eSize,elemType='ShellMITC4')
support_mesh.generateMesh(prep)

#                       ***BOUNDARY CONDITIONS***
n_anch1=nodes.getDomain.getMesh.getNearestNode(geom.Pos3d(0,0,zAnchor))
modelSpace.fixNode('000_FFF',n_anch1.tag)
n_anch2=nodes.getDomain.getMesh.getNearestNode(geom.Pos3d(0,spcAnch,zAnchor))
modelSpace.fixNode('000_FFF',n_anch2.tag)
n_anch3=nodes.getDomain.getMesh.getNearestNode(geom.Pos3d(0,2*spcAnch,zAnchor))
modelSpace.fixNode('000_FFF',n_anch3.tag)

n_bottom=sets.get_nodes_wire(support,[geom.Pos3d(0,0,0),geom.Pos3d(0,spcAnch*2,0)],tol=0.001)
for n in n_bottom:
    modelSpace.fixNode('0FF_FFF',n.tag)

#out.displayFEMesh()

#                       ***ACTIONS***
pntAux=gridGeom.getSetPntRange(gm.IJKRange((1,0,0),(1,4,0)),'pntAux')
linLoaded=sets.get_lines_on_points(pntAux,'linLoaded',True)

Qd=loads.UniformLoadOnLines(name='Qd',xcSet=linLoaded,loadVector=xc.Vector([0,0,-combLoad,0,0,0]))

ULS01=lcases.LoadCase(preprocessor=prep,name="ULS01",loadPType="default",timeSType="constant_ts")
ULS01.create()
ULS01.addLstLoads([Qd])
modelSpace.addLoadCaseToDomain("ULS01")
#out.displayLoadVectors()
modelSpace.removeLoadCaseFromDomain("ULS01")

setOutVert=gridGeom.getSetSurfOneRegion(gm.IJKRange((0,1,0),(0,2,2)),'setOutVert')
setOutVert.description='Vertical flange'
setOutHor=gridGeom.getSetSurfOneRegion(gm.IJKRange((0,1,0),(1,2,0)),'setOutHor')
setOutHor.description='Horizontal flange'

#out.displayFEMesh(setOutput)
#out.displayFEMesh()
#out.displayFEMesh(setOutVert)
#out.displayFEMesh(setOutHor)

from solution import predefined_solutions
modelSpace.removeAllLoadPatternsFromDomain()
modelSpace.addLoadCaseToDomain('ULS01')
analysis= predefined_solutions.simple_static_linear(FEcase)
result= analysis.analyze(1)
out.displayDispRot('uZ')

out.displayIntForc('N1',setOutVert)
out.displayIntForc('M1',setOutVert)
out.displayIntForc('Q1',setOutVert)
out.displayIntForc('N2',setOutVert)
out.displayIntForc('M2',setOutVert)
out.displayIntForc('Q2',setOutVert)

out.displayIntForc('N1',setOutHor)
out.displayIntForc('M1',setOutHor)
out.displayIntForc('Q1',setOutHor)
out.displayIntForc('N2',setOutHor)
out.displayIntForc('M2',setOutHor)
out.displayIntForc('Q2',setOutHor)


modelSpace.preprocessor.getNodeHandler.calculateNodalReactions(True,1e-7)
Rx=n_anch2.getReaction[0]
Ry=n_anch2.getReaction[1]
Rz=n_anch2.getReaction[2]

print ('Rx =', Rx, 'Rz= ', Rz)
