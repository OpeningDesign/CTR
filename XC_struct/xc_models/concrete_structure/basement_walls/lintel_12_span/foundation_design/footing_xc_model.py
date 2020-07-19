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
from postprocess import RC_material_distribution
from materials.sections.fiber_section import def_simple_RC_section
from postprocess import element_section_map

from materials.aci import ACI_limit_state_checking

# Mesh definition
from model import predefined_spaces

#Loads
from actions import load_cases as lcm
from actions import combinations as combs
from postprocess import output_handler
from postprocess import limit_state_data as lsd

FEproblem= xc.FEProblem()
prep= FEproblem.getPreprocessor
nodes= prep.getNodeHandler
modelSpace= predefined_spaces.StructuralMechanics3D(nodes)

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
elementSize= 0.3

id= '00'
footingSet= prep.getSets.defSet(id+'set')
center= geom.Pos3d(0.0,0.0,0.0)
ptO= points.newPntFromPos3d(center)
columnBases[id]= ptO
thickness= 0.3556
materialName= id+'_material'
footingRho= thickness*concreteDensity
material= typical_materials.defElasticMembranePlateSection(prep,materialName,concrete.getEcm(),nu,footingRho,thickness)
footingSet.setProp('material',material)
B= 1.65
L= 4*0.3048
ptA= points.newPntFromPos3d(center+geom.Vector3d(-B/2.0,L/2.0,0.0))
ptB= points.newPntFromPos3d(center+geom.Vector3d(0.0,L/2.0,0.0))
ptC= points.newPntFromPos3d(center+geom.Vector3d(B/2.0,L/2.0,0.0))
ptD= points.newPntFromPos3d(center+geom.Vector3d(-B/2.0,0.0,0.0))
ptE= points.newPntFromPos3d(center+geom.Vector3d(B/2.0,0.0,0.0))
ptF= points.newPntFromPos3d(center+geom.Vector3d(-B/2.0,-L/2.0,0.0))
ptG= points.newPntFromPos3d(center+geom.Vector3d(0.0,-L/2.0,0.0))
ptH= points.newPntFromPos3d(center+geom.Vector3d(B/2.0,-L/2.0,0.0))
sI= surfaces.newQuadSurfacePts(ptO.tag,ptE.tag,ptC.tag,ptB.tag) #first quadrant
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

#footingSet.fillDownwards()

prep.getMultiBlockTopology.getSurfaces.conciliaNDivs()

#########################################################
# Graphic stuff.
oh= output_handler.OutputHandler(modelSpace)

#oh.displayBlocks()

# Mesh generation.

seedElemHandler= prep.getElementHandler.seedElemHandler

seedElemHandler.defaultMaterial= footingSet.getProp('material').name
elem= seedElemHandler.newElement("ShellMITC4",xc.ID([0,0,0,0]))
footingSet.genMesh(xc.meshDir.I)

footingSet.fillDownwards()
#oh.displayFEMesh()

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
elasticBearingNodes= footingSet.nodes

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
loadCaseName= 'ULS01'
loadCaseManager.defineSimpleLoadCases([loadCaseName])
cLC= loadCaseManager.setCurrentLoadCase(loadCaseName)
n= ptO.getNode()
reaction= xc.Vector([0.0,0.0,-273e3,0.0,0.0,0.0])
cLC.newNodalLoad(n.tag,reaction)
loadCases.addToDomain(loadCaseName)
#oh.displayLoads()

#Load combinations
combContainer= combs.CombContainer()

## Permanent and transitory situations.
combContainer.ULS.perm.add('combULS01','1.0*ULS01')

# Check soil bearing capacity.
stress= -reaction[2]/B/L/1.2 # Design value/1.2 approx. characteristic value
admStress= 3000.0 * 0.04788026e3 #N/m2
F= abs(stress/admStress)
print('soil bearing capacity factor; F= ',F)

# Check reinforced concrete strength

## Define reinforced concrete section.
concrete= ACI_materials.c3000
concrete.gmmC= 1.0/0.75
reinfSteel= ACI_materials.A615G60
## Define sections for the elements (spatial distribution of RC sections).
reinfConcreteSectionDistribution= RC_material_distribution.RCMaterialDistribution()
sections= reinfConcreteSectionDistribution.sectionDefinition

id= '00'
sName= id + '_sections'
sDescr= id + ' footing sections.'
rcSection= element_section_map.RCSlabBeamSection(name=sName,sectionDescr=sDescr,concrType=concrete, reinfSteelType=reinfSteel,depth= thickness)

rcSection.dir1PositvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n2s300r50])
rcSection.dir1NegatvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n5s300r50])
rcSection.dir2PositvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n2s300r45])
rcSection.dir2NegatvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n5s300r45])

sections.append(rcSection)
reinfConcreteSectionDistribution.assign(elemSet= footingSet.elements, setRCSects= rcSection)

## Elements with an assigned section.
elementsWithSection= reinfConcreteSectionDistribution.getElementSet(prep)

loadCombinations= prep.getLoadHandler.getLoadCombinations

## Limit states to calculate internal forces for.
limitStates= [lsd.normalStressesResistance, # Normal stresses resistance.
lsd.shearResistance, # Shear stresses resistance (IS THE SAME AS NORMAL STRESSES, THIS IS WHY IT'S COMMENTED OUT).
lsd.freqLoadsCrackControl, # RC crack control under frequent loads
lsd.quasiPermanentLoadsCrackControl, # RC crack control under quasi-permanent loads
lsd.fatigueResistance # Fatigue resistance.
] 

for ls in limitStates:
  ls.saveAll(combContainer=combContainer,setCalc= elementsWithSection,fConvIntForc= 1.0)
  print('combinations for ', ls.label, ': ', loadCombinations.getKeys())

## Check normal stresses on each element.
limitStateLabel= lsd.normalStressesResistance.label
lsd.normalStressesResistance.controller= ACI_limit_state_checking.BiaxialBendingNormalStressController(limitStateLabel)
lsd.normalStressesResistance.check(reinfConcreteSectionDistribution)

# ## Checking shear.
# limitStateLabel= lsd.shearResistance.label
# lsd.shearResistance.controller= ACI_limit_state_checking.ShearController(limitStateLabel)
# lsd.shearResistance.check(reinfConcreteSectionDistribution)
