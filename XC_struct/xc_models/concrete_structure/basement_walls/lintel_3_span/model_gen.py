# -*- coding: utf-8 -*-
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
from materials.ehe import EHE_materials

workingDirectory= default_config.findWorkingDirectory()+'/'
execfile(workingDirectory+'data.py')
execfile(workingDirectory+'env_config.py')

FEcase= xc.FEProblem()
preprocessor=FEcase.getPreprocessor
prep=preprocessor   #short name
nodes= prep.getNodeHandler
elements= prep.getElementHandler
elements.dimElem= 3
# Problem type
modelSpace= psp.StructuralMechanics3D(nodes) 
# grid model definition
gridGeom= gm.GridModel(prep,xList,yList,zList)
gridGeom.generatePoints()


beamCent=gridGeom.genLinOneXYZRegion(xyzRange=((0,0,zBeam),(0,yBeamCent,zBeam)),setName='beamCent')
beamExtr=gridGeom.genLinOneXYZRegion(xyzRange=((0,yBeamCent,zBeam),(0,yBeamEnd,zBeam)),setName='beamExtr')

column=gridGeom.genLinOneXYZRegion(xyzRange=((0,yBeamEnd,0),(0,yBeamEnd,zColumn)),setName='column')
#                         *** MATERIALS *** 
concrete=EHE_materials.HA30
reinfSteel=EHE_materials.B500S
concrProp=tm.MaterialData(name='concrProp',E=concrete.Ecm(),nu=concrete.nuc,rho=concrete.density())

from materials.sections import section_properties as sectpr

geomSectBeam=sectpr.RectangularSection(name='geomSectBeam',b=wBeam,h=hBeam)
geomSectColumn=sectpr.RectangularSection(name='geomSectColumn',b=wColumn,h=dimYColumn)

# Elastic material-section
beamConcr_mat= tm.BeamMaterialData(name= 'beamConcr_mat', section=geomSectBeam, material=concrProp)
beamConcr_mat.setupElasticShear3DSection(preprocessor=prep)
columnConcr_mat= tm.BeamMaterialData(name= 'columnConcr_mat', section=geomSectColumn, material=concrProp)
columnConcr_mat.setupElasticShear3DSection(preprocessor=prep)

#                         ***FE model - MESH***
#deck_mesh=fem.SurfSetToMesh(surfSet=deck,matSect=deck_mat,elemSize=eSize,elemType='ShellMITC4')
#deck_mesh.generateMesh(prep)
# vDirLAxZ parallel to width
beamCent_mesh=fem.LinSetToMesh(linSet=beamCent,matSect=beamConcr_mat,elemSize=eSize,vDirLAxZ=xc.Vector([0,0,1]),elemType='ElasticBeam3d',dimElemSpace=3,coordTransfType='linear')
beamExtr_mesh=fem.LinSetToMesh(linSet=beamExtr,matSect=beamConcr_mat,elemSize=eSize,vDirLAxZ=xc.Vector([0,0,1]),elemType='ElasticBeam3d',dimElemSpace=3,coordTransfType='linear')

columnConcr_mesh=fem.LinSetToMesh(linSet=column,matSect=columnConcr_mat,elemSize=eSize,vDirLAxZ=xc.Vector([1,0,0]),elemType='ElasticBeam3d',dimElemSpace=3,coordTransfType='linear')
fem.multi_mesh(preprocessor=prep,lstMeshSets=[beamCent_mesh,beamExtr_mesh,columnConcr_mesh])

beam=beamCent+beamExtr

#Boundary conditions

#Movimiento Y impedido pilar
for n in column.getNodes:
    modelSpace.fixNode('F0F_0FF',n.tag)

#Simetría
p=gridGeom.getPntXYZ((0,0,zBeam))
n=p.getNode()
modelSpace.fixNode('F0F_000',n.tag)

#Empotramiento base pilar
p=gridGeom.getPntXYZ((0,yBeamEnd,0))
n=p.getNode()
modelSpace.fixNode('000_000',n.tag)

#Apoyo viga en pilar
p1=gridGeom.getPntXYZ((0,yBeamEnd,zBeam))
n1=p1.getNode()
modelSpace.fixNode('FFF_F0F',n.tag)

p2=gridGeom.getPntXYZ((0,yBeamEnd,zColumn))
n2=p2.getNode()
#modelSpace.setRigidRodBetweenNodes(n1.tag,n2.tag)
modelSpace.constraints.newEqualDOF(n1.tag,n2.tag,xc.ID([0]))
modelSpace.constraints.newEqualDOF(n1.tag,n2.tag,xc.ID([1]))
modelSpace.constraints.newEqualDOF(n1.tag,n2.tag,xc.ID([2]))

#Loads
grav=9.81
selfWeight=loads.InertialLoad(name='selfWeight', lstMeshSets=[beamCent_mesh,beamExtr_mesh,columnConcr_mesh], vAccel=xc.Vector( [0.0,0.0,-grav]))
selfW_wall=(wallHeight-hBeam)*concrete.density()*grav*wallTh
Dwall=loads.UniformLoadOnBeams(name='Dwall', xcSet=beam, loadVector=xc.Vector([0,0,-selfW_wall,0,0,0]),refSystem='Global')
selfW_hollow=sectAreaSlab*concrete.density()*grav*spanSlab/2.
Dhollow=loads.UniformLoadOnBeams(name='Dhollow', xcSet=beam, loadVector=xc.Vector([0,0,-selfW_hollow,0,0,0]),refSystem='Global')
fill_slab=deadL*spanSlab/2.
Dslab=loads.UniformLoadOnBeams(name='Dslab', xcSet=beam, loadVector=xc.Vector([0,0,-fill_slab,0,0,0]),refSystem='Global')
live_slab=liveL*spanSlab/2.
live=loads.UniformLoadOnBeams(name='live', xcSet=beam, loadVector=xc.Vector([0,0,-live_slab,0,0,0]),refSystem='Global')
snow_slab=snowL*spanSlab/2.
snow=loads.UniformLoadOnBeams(name='snow', xcSet=beam, loadVector=xc.Vector([0,0,-snow_slab,0,0,0]),refSystem='Global')

#    ***LOAD CASES***
DeadL=lcases.LoadCase(preprocessor=prep,name="DeadL",loadPType="default",timeSType="constant_ts")
DeadL.create()
DeadL.addLstLoads([selfWeight,Dwall,Dhollow,Dslab])

LiveL=lcases.LoadCase(preprocessor=prep,name="LiveL",loadPType="default",timeSType="constant_ts")
LiveL.create()
LiveL.addLstLoads([live])

SnowL=lcases.LoadCase(preprocessor=prep,name="SnowL",loadPType="default",timeSType="constant_ts")
SnowL.create()
SnowL.addLstLoads([snow])

overallSet=beam+column

#    ***LIMIT STATE COMBINATIONS***
from actions import combinations as cc

combContainer= cc.CombContainer()  #Container of load combinations
# COMBINATIONS OF ACTIONS FOR ULTIMATE LIMIT STATES
    # name:        name to identify the combination
    # perm:        combination for a persistent or transient design situation
    # acc:         combination for a accidental design situation
    # fatigue:     combination for a fatigue design situation
    # earthquake:  combination for a seismic design situation
#Persistent and transitory situations.
combContainer.ULS.perm.add('ELU01', '1.4*DeadL')
combContainer.ULS.perm.add('ELU02', '1.2*DeadL+1.6*LiveL+0.5*SnowL')
combContainer.ULS.perm.add('ELU03', '1.2*DeadL+1.0*LiveL+1.6*SnowL')
