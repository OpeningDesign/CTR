import xc_base
import geom
import xc
from model import predefined_spaces as psp
from model.geometry import grid_model as gm
from model.mesh import finit_el_model as fem
from model.sets import sets_mng as sets
from materials import typical_materials as tm
from actions import loads
from actions import load_cases as lcases
from postprocess.config import default_config

workingDirectory= default_config.findWorkingDirectory()+'/'
execfile(workingDirectory+'data.py')

FEcase= xc.FEProblem()
preprocessor=FEcase.getPreprocessor
prep=preprocessor   #short name
nodes= prep.getNodeHandler
elements= prep.getElementHandler
elements.dimElem= 3
# Problem type
modelSpace= psp.StructuralMechanics3D(nodes) #Defines the
# grid model definition
gridGeom= gm.GridModel(prep,xList,yList,zList)
gridGeom.generatePoints()

# idem for J and K ranges
floor=gridGeom.genSurfOneXYZRegion(xyzRange=((0,0,rimHeigth),(rimSpan,floorWidth,rimHeigth)),setName='floor')
rim=gridGeom.genSurfOneXYZRegion(xyzRange=((0,0,0),(rimSpan,0,rimHeigth)),setName='rim')
#                         *** MATERIALS *** 
wood=tm.MaterialData(name='wood',E=Ewood,nu=nuWood,rho=rhoWood)
# Isotropic elastic section-material appropiate for plate and shell analysis
floor_mat=tm.DeckMaterialData(name='floor_mat',thickness= floorTh,material=wood)
floor_mat.setupElasticSection(prep)
rim_mat=tm.DeckMaterialData(name='rim_mat',thickness= rimTh,material=wood)
rim_mat.setupElasticSection(prep)


#                         ***FE model - MESH***
floor_mesh=fem.SurfSetToMesh(surfSet=floor,matSect=floor_mat,elemSize=eSize,elemType='ShellMITC4')
floor_mesh.generateMesh(prep)
rim_mesh=fem.SurfSetToMesh(surfSet=rim,matSect=rim_mat,elemSize=eSize,elemType='ShellMITC4')
rim_mesh.generateMesh(prep)

overallSet=floor+rim

#Boundary conditions
Bnd1=sets.get_nodes_wire(setBusq=overallSet, lstPtsWire=[geom.Pos3d(0,0,0),geom.Pos3d(0,0,rimHeigth),geom.Pos3d(0,floorWidth,rimHeigth)])
for n in Bnd1:
    modelSpace.fixNode('000_FFF',n.tag)
Bnd2=sets.get_nodes_wire(setBusq=overallSet, lstPtsWire=[geom.Pos3d(rimSpan,0,0),geom.Pos3d(rimSpan,0,rimHeigth),geom.Pos3d(rimSpan,floorWidth,rimHeigth)])
for n in Bnd2:
    modelSpace.fixNode('000_FFF',n.tag)

loadSet=gridGeom.getSetSurfOneRegion(ijkRange=gm.IJKRange((1,0,1),(2,1,1)), setName='loadSet')

#Loads
total=loads.UniformLoadOnSurfaces(name= 'total',xcSet=loadSet,loadVector=xc.Vector([0,0,-pointLoad/(studXdim*studYdim),0,0,0]),refSystem='Global')


#    ***LOAD CASES***
ULS1=lcases.LoadCase(preprocessor=prep,name="ULS1",loadPType="default",timeSType="constant_ts")
ULS1.create()
ULS1.addLstLoads([total])

