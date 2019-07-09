# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
import csv
import xc_base
import geom
import xc

# Material definition
from materials import typical_materials
from materials.aci import ACI_materials

# Mesh definition
from model import predefined_spaces

#Loads
from actions import load_cases as lcm
from actions import combinations as combs

FEproblem= xc.FEProblem()
prep= FEproblem.getPreprocessor

#Material definition.
concrete= ACI_materials.c3500
nu= 0.3 # Poisson coefficient.
concreteDensity= 2500 # Density kg/m3.


#    A     B     C
#    +-----+-----+
#    | II  |  I  |
#    |     |O    |
#   D+-----+-----+E
#    |     |     |
#    | III | IV  |
#    +-----+-----+
#    F     G     H

columnBases= dict()
points= prep.getMultiBlockTopology.getPoints
surfaces= prep.getMultiBlockTopology.getSurfaces
footingSetList= list()
elementSize= 0.6

csvFile= open('footings_geometry.csv')
reader= csv.reader(csvFile)
for row in reader:
    id= row[0]
    footingSet= prep.getSets.defSet(id+'set')
    footingSetList.append(footingSet)
    center= geom.Pos3d(float(row[2]),float(row[3]),0.0)
    ptO= points.newPntFromPos3d(center)
    columnBases[id]= ptO
    thickness= float(row[5])
    materialName= id+'_material'
    footingRho= thickness*concreteDensity
    material= typical_materials.defElasticMembranePlateSection(prep,materialName,concrete.getEcm(),nu,footingRho,thickness)
    B= float(row[6])
    ptA= points.newPntFromPos3d(center+geom.Vector3d(-B/2.0,B/2.0,0.0))
    ptB= points.newPntFromPos3d(center+geom.Vector3d(0.0,B/2.0,0.0))
    ptC= points.newPntFromPos3d(center+geom.Vector3d(B/2.0,B/2.0,0.0))
    ptD= points.newPntFromPos3d(center+geom.Vector3d(-B/2.0,0.0,0.0))
    ptE= points.newPntFromPos3d(center+geom.Vector3d(B/2.0,0.0,0.0))
    ptF= points.newPntFromPos3d(center+geom.Vector3d(-B/2.0,-B/2.0,0.0))
    ptG= points.newPntFromPos3d(center+geom.Vector3d(0.0,-B/2.0,0.0))
    ptH= points.newPntFromPos3d(center+geom.Vector3d(B/2.0,-B/2.0,0.0))
    
    sI= surfaces.newQuadSurfacePts(ptO.tag,ptE.tag,ptC.tag,ptB.tag) #first quadrant
    sI.setProp('material',material)
    sI.setElemSizeIJ(elementSize,elementSize)
    footingSet.getSurfaces.append(sI)
    
    sII= surfaces.newQuadSurfacePts(ptD.tag,ptO.tag,ptB.tag,ptA.tag) #second quadrant
    sII.setProp('material',material)
    sII.setElemSizeIJ(elementSize,elementSize)
    footingSet.getSurfaces.append(sII)
    
    sIII= surfaces.newQuadSurfacePts(ptF.tag,ptG.tag,ptO.tag,ptD.tag) #third quadrant
    sIII.setProp('material',material)
    sIII.setElemSizeIJ(elementSize,elementSize)
    sIII.setProp('material',material)    
    footingSet.getSurfaces.append(sIII)
    
    sIV= surfaces.newQuadSurfacePts(ptG.tag,ptH.tag,ptE.tag,ptO.tag) #fourh quadrant
    sIV.setProp('material',material)
    sIV.setElemSizeIJ(elementSize,elementSize)
    footingSet.getSurfaces.append(sIV)

footingsSet= prep.getSets.defSet('footingsSet')
    
for fs in footingSetList:
    fs.fillDownwards()
    footingsSet+= fs

prep.getMultiBlockTopology.getSurfaces.conciliaNDivs()

# Mesh generation.
nodos= prep.getNodeHandler
modelSpace= predefined_spaces.StructuralMechanics3D(nodos)
nodos.newSeedNode()
seedElemHandler= prep.getElementHandler.seedElemHandler

for fs in footingSetList:
    for s in fs.getSurfaces:
         seedElemHandler.defaultMaterial= s.getProp('material').name
         elem= seedElemHandler.newElement("ShellMITC4",xc.ID([0,0,0,0]))
         s.genMesh(xc.meshDir.I)

footingsSet.fillDownwards()
footingsSet.name= 'footingsSet'

xcTotalSet= prep.getSets.getSet('total')

# Constraints.
fixedNodes= list()
kS= 200*4.44822/(0.0254**3)#kSd/m/f
print ('kS= ', kS/1e6)
kV= typical_materials.defElasticMaterial(prep, "kV",kS)
#kV= typical_materials.defElastNoTensMaterial(preprocessor, "kV",kS)
kH= typical_materials.defElasticMaterial(prep, "kH",kS/10.0)
xcTotalSet.computeTributaryAreas(False)
# Springs on nodes.
elasticBearingNodes= footingsSet.getNodes

for n in elasticBearingNodes:
    tA= n.getTributaryArea()
    kV.E= kS*tA
    kH.E= kS/10.0*tA
    fixedNode, newElem= modelSpace.setBearing(n.tag,['kH','kH','kV'])
    fixedNodes.append(fixedNode)

  #Loads
loadManager= prep.getLoadHandler
loadCases= loadManager.getLoadPatterns
#Load modulation.
ts= loadCases.newTimeSeries("constant_ts","ts")
loadCases.currentTimeSeries= "ts"

#Load case definition
loadCaseManager= lcm.LoadCaseManager(prep)
loadCaseNames= ['ULS01','ULS02_a','ULS02_b','ULS03_a','ULS03_b','ULS04_a','ULS04_b','ULS05_a','ULS05_b','ULS05_c','ULS05_d','ULS06_a','ULS06_b','ULS07_a','ULS07_b']
loadCaseManager.defineSimpleLoadCases(loadCaseNames)

csvFile= open('column_reactions.csv')
reader= csv.reader(csvFile)
loadPatterns= dict()
for row in reader:
    id= row[0]
    loadCaseName= row[2]
    if(loadCaseName.startswith('ULS')):
        cLC= loadCaseManager.setCurrentLoadCase(loadCaseName)
        loadPatterns[loadCaseName]= cLC
        pt= columnBases[id]
        n= pt.getNode()
        cLC.newNodalLoad(n.tag,xc.Vector([-float(row[3]),-float(row[4]),-float(row[5]),-float(row[6]),-float(row[7]),-float(row[8])]))

#Load combinations
combContainer= combs.CombContainer()

#Permanent and transitory situations.
combContainer.ULS.perm.add('combULS01','1.0*ULS01')
combContainer.ULS.perm.add('combULS02_a','1.0*ULS02_a')
combContainer.ULS.perm.add('combULS02_b','1.0*ULS02_b')
combContainer.ULS.perm.add('combULS03_a','1.0*ULS03_a')
combContainer.ULS.perm.add('combULS03_b','1.0*ULS03_b')
combContainer.ULS.perm.add('combULS04_a','1.0*ULS04_a')
combContainer.ULS.perm.add('combULS04_b','1.0*ULS04_b')
combContainer.ULS.perm.add('combULS05_a','1.0*ULS05_a')
combContainer.ULS.perm.add('combULS05_b','1.0*ULS05_b')
combContainer.ULS.perm.add('combULS05_c','1.0*ULS05_c')
combContainer.ULS.perm.add('combULS05_d','1.0*ULS05_d')
combContainer.ULS.perm.add('combULS06_a','1.0*ULS06_a')
combContainer.ULS.perm.add('combULS06_b','1.0*ULS06_b')
combContainer.ULS.perm.add('combULS07_a','1.0*ULS07_a')
combContainer.ULS.perm.add('combULS07_b','1.0*ULS07_b')


