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
execfile(workingDirectory + 'data.py')

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
deck=gridGeom.genSurfOneXYZRegion(xyzRange=((0,0,0),(length,width,0)),setName='deck')

#                         *** MATERIALS *** 
alumin=tm.MaterialData(name='alumin',E=Ealum,nu=nualum,rho=rhoalum)
# Isotropic elastic section-material appropiate for plate and shell analysis
deck_mat=tm.DeckMaterialData(name='deck_mat',thickness= deckTh,material=alumin)
deck_mat.setupElasticSection(prep)
tie_mat=tm.defElasticMaterial(prep,"tie_mat",Ealum)

#                         ***FE model - MESH***
deck_mesh=fem.SurfSetToMesh(surfSet=deck,matSect=deck_mat,elemSize=eSize,elemType='ShellMITC4')
deck_mesh.generateMesh(prep)

#Ties
anchorTop=prep.getSets.defSet('anchorTop')
elements.defaultMaterial="tie_mat"
pt1_1=gridGeom.getPntXYZ((0,width,0))
n1_1=pt1_1.getNode()
n1_2=nodes.newNodeXYZ(0,0,heigth)
modelSpace.fixNode('000_000',n1_2.tag)
tie1=elements.newElement("Truss",xc.ID([n1_1.tag,n1_2.tag]))
tie1.sectionArea= tieArea

pt2_1=gridGeom.getPntXYZ((length,width,0))
n2_1=pt2_1.getNode()
n2_2=nodes.newNodeXYZ(length,0,heigth)
modelSpace.fixNode('000_000',n2_2.tag)
tie2=elements.newElement("Truss",xc.ID([n2_1.tag,n2_2.tag]))
tie2.sectionArea= tieArea
ties=prep.getSets.defSet('ties')
ties.getElements.append(tie1)
ties.getElements.append(tie2)

ties.fillDownwards()
anchorTop.getNodes.append(n1_2)
anchorTop.getNodes.append(n2_2)

#Boundary conditions
anchorBase=prep.getSets.defSet('anchorBase')
pntAnchorBase=gridGeom.getSetPntXYZRange(xyzRange=((0,0,0),(length,0,0)), setName='pntAnchorBase')
for p in pntAnchorBase.getPoints:
    n=p.getNode()
    modelSpace.fixNode('000_FFF',n.tag)
    anchorBase.getNodes.append(n)
    
#Loads
selfWeight=loads.UniformLoadOnSurfaces(name= 'selfWeight',xcSet=deck,loadVector=xc.Vector([0,0,-deckingW,0,0,0]),refSystem='Global')

live=loads.UniformLoadOnSurfaces(name= 'liveL',xcSet=deck,loadVector=xc.Vector([0,0,-liveL,0,0,0]),refSystem='Global')

snow=loads.UniformLoadOnSurfaces(name= 'snowL',xcSet=deck,loadVector=xc.Vector([0,0,-snowL,0,0,0]),refSystem='Global')

#    ***LOAD CASES***
D=lcases.LoadCase(preprocessor=prep,name="D",loadPType="default",timeSType="constant_ts")
D.create()
D.addLstLoads([selfWeight])

L=lcases.LoadCase(preprocessor=prep,name="L",loadPType="default",timeSType="constant_ts")
L.create()
L.addLstLoads([live])

S=lcases.LoadCase(preprocessor=prep,name="S",loadPType="default",timeSType="constant_ts")
S.create()
S.addLstLoads([snow])

overallSet= modelSpace.setSum('overallSet',[deck,ties])
