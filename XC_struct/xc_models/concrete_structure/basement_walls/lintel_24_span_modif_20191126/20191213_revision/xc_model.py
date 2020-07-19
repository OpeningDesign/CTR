# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

import math
import xc_base
import geom
import xc

from model import predefined_spaces
from materials.aci import ACI_materials
from materials import typical_materials
from postprocess import output_handler
from solution import predefined_solutions

inch2meter= 0.0254
pound2N=4.45
ft2m=0.3048
L= 8.8326

FEcase= xc.FEProblem()
execfile('./xc_model_blocks.py')


xcTotalSet= preprocessor.getSets.getSet('total')

concreteSet= preprocessor.getSets.defSet('concreteSet')
for s in xcTotalSet.getSurfaces:
    concreteSet.getSurfaces.append(s)

rebarSets= dict()
rebarSets[6]= preprocessor.getSets.defSet('rebars06')
rebarSets[6].setProp('rebarArea',ACI_materials.num2Area)
rebarSets[10]= preprocessor.getSets.defSet('rebars10')
rebarSets[10].setProp('rebarArea',ACI_materials.num3Area)
rebarSets[13]= preprocessor.getSets.defSet('rebars13')
rebarSets[13].setProp('rebarArea',ACI_materials.num4Area)
rebarSets[16]= preprocessor.getSets.defSet('rebars16')
rebarSets[16].setProp('rebarArea',ACI_materials.num5Area)
rebarSets[22]= preprocessor.getSets.defSet('rebars22')
rebarSets[22].setProp('rebarArea',ACI_materials.num6Area)
for l in xcTotalSet.getLines:
    if(l.hasProp('labels')):
        labels= l.getProp('labels')
        if(labels.count('rebar_segments_13')>0):
            rebarSets[13].getLines.append(l)
        elif(labels.count('rebar_segments_16')>0):
            rebarSets[16].getLines.append(l)
        elif(labels.count('rebar_segments_22')>0):
            rebarSets[22].getLines.append(l) 
        elif(labels.count('rebars_06')>0):
            rebarSets[06].getLines.append(l)
        elif(labels.count('rebars_10')>0):
            rebarSets[10].getLines.append(l)

linkSet= preprocessor.getSets.defSet('links')
for l in xcTotalSet.getLines:
    if(l.hasProp('labels')):
        labels= l.getProp('labels')
        if(labels.count('link_lines')>0):
            linkSet.getLines.append(l)

precastFloorPointSet= preprocessor.getSets.defSet('precastFloorPointSet')
for l in xcTotalSet.getLines:
    if(l.hasProp('labels')):
        labels= l.getProp('labels')
        if(labels.count('00FFFF_constraints')>0):
            precastFloorPointSet.getLines.append(l)

lintelEndPointsSet= preprocessor.getSets.defSet('lintelEndPointsSet')
for l in xcTotalSet.getLines:
    if(l.hasProp('labels')):
        labels= l.getProp('labels')
        if(labels.count('000FFF_constraints')>0):
            lintelEndPointsSet.getLines.append(l)
            
rebarEndPointsSet= preprocessor.getSets.defSet('rebarEndPointsSet')
for l in xcTotalSet.getLines:
    if(l.hasProp('labels')):
        labels= l.getProp('labels')
        if(labels.count('000000_constraints')>0):
            rebarEndPointsSet.getLines.append(l)

horizLoadedPointsSet= preprocessor.getSets.defSet('horizLoadedPointsSet')
for l in xcTotalSet.getLines:
    if(l.hasProp('labels')):
        labels= l.getProp('labels')
        if(labels.count('horiz_loads')>0):
            horizLoadedPointsSet.getLines.append(l)

# Problem type
preprocessor=FEcase.getPreprocessor
nodes= preprocessor.getNodeHandler
modelSpace= predefined_spaces.StructuralMechanics3D(nodes) 
## Graphic stuff.
oh= output_handler.OutputHandler(modelSpace)

# Materials
concrete=ACI_materials.c4000
reinfSteel=ACI_materials.A615G60
lintelThickness= 10*inch2meter
shellMaterial= typical_materials.defElasticMembranePlateSection(preprocessor, 'shellMaterial', concrete.Ecm(), 0.25, 0.0, lintelThickness)
trussMaterial= typical_materials.defElasticMaterial(preprocessor, 'trussMaterial',reinfSteel.Es)

# Mesh generation
elementSize= 10.0
for s in xcTotalSet.getSurfaces:
    s.setElemSizeIJ(elementSize,elementSize)
    if((s.nDivI!=1) or (s.nDivJ!=1)):
        print('tag: ', s.tag, ' nDivI= ', s.nDivI,' nDivJ= ', s.nDivJ) 
for l in xcTotalSet.getLines:
    l.setElemSize(elementSize)
    if(l.nDiv!=1):
        print('tag: ', l.tag, ' ', l.tipo(), ' nDiv= ', l.nDiv)

## Concrete  
seedElemHandler = preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultMaterial= shellMaterial.name
seedElem= seedElemHandler.newElement('ShellMITC4', xc.ID([0,0,0,0]))

preprocessor.getMultiBlockTopology.getSurfaces.conciliaNDivs()
concreteSet.genMesh(xc.meshDir.I)
concreteSet.fillDownwards()

## Reinforcement
seedElemHandler.defaultMaterial= trussMaterial.name
seedElemHandler.dimElem= 3
seedElem= seedElemHandler.newElement('Truss', xc.ID([0,0]))
seedElem.sectionArea= 1

for key in rebarSets:
    rebarSet= rebarSets[key]
    seedElem.sectionArea= rebarSet.getProp('rebarArea')
    for l in rebarSet.getLines:
       l.genMesh(xc.meshDir.I)

# Constraints

def getPointsFromLines(lines):
    tags= set()
    retval= list()
    for l in lines:
        for p in [l.firstVertex, l.lastVertex]:
            if(not p.tag in tags):
                tags.add(p.tag)
                retval.append(p)
    return retval

## Precast floor constraints
precastFloorPoints= getPointsFromLines(precastFloorPointSet.getLines)

for p in precastFloorPoints:
    if(not p.hasNode):
        p.genMesh(xc.meshDir.I)
    n= p.getNode()
    modelSpace.fixNode('F0F_FFF',n.tag)

## Lintel ends floor constraints
lintelEndPoints= getPointsFromLines(lintelEndPointsSet.getLines)

for p in lintelEndPoints:
    if(not p.hasNode):
        print('point: '+str(p.tag)+' is not meshed')
        p.genMesh(xc.meshDir.I)
    n= p.getNode()
    modelSpace.fixNode('000_FFF',n.tag)
    
rebarEndPoints= getPointsFromLines(rebarEndPointsSet.getLines)
for p in rebarEndPoints:
    if(not p.hasNode):
        print('point: '+str(p.tag)+' is not meshed')
        p.genMesh(xc.meshDir.I)
    n= p.getNode()
    modelSpace.fixNode('000_000',n.tag)

## Links
for l in linkSet.getLines:
    n1= l.firstNode
    if(not n1):
        print('line: ',l.tag, ' is not connected at its origin.')
    n2= l.lastNode
    if(not n2):
        print('line: ',l.tag, ' is not connected at its end.')
    
    preprocessor.getBoundaryCondHandler.newRigidBeam(n2.tag,n1.tag)

# Loads

## Load pattern
lPatterns = preprocessor.getLoadHandler.getLoadPatterns  # Load pattern container.
### Variation of load with time.
ts = lPatterns.newTimeSeries("constant_ts","ts")  # Constant load, no variation.
lPatterns.currentTimeSeries= "ts"  # Time series to use for the new load patterns.
### Load pattern definition
lp0 = lPatterns.newLoadPattern("default","0")  # New load pattern named 0

# ## vertical loads
# deadL=110*pound2N/(ft2m)**2   #dead load (
# liveL=100*pound2N/(ft2m)**2    # live load (40 psf)
# snowL=42*pound2N/(ft2m)**2    # snow load (42 psf)
# verticalNodalLoad= (1.4*deadL+1.6*liveL)*L/len(precastFloorPoints)
# print(verticalNodalLoad/1e3)
# for p in precastFloorPoints:
#     n= p.getNode()
#     lp0.newNodalLoad(n.tag,xc.Vector([0.0,0.0,-verticalNodalLoad,0.0,0.0,0.0]))


## horizontal loads
earthPressure= 15e3 # N/m
horizLoadedPoints= getPointsFromLines(horizLoadedPointsSet.getLines)
horizontalNodalLoad= earthPressure*L/len(horizLoadedPoints)
print(horizontalNodalLoad/1e3)
for p in horizLoadedPoints:
    if(not p.hasNode):
        p.genMesh(xc.meshDir.I)
    n= p.getNode()
    lp0.newNodalLoad(n.tag,xc.Vector([0.0,-horizontalNodalLoad,0.0,0.0,0.0,0.0]))

## We add the load case to domain.
lPatterns.addToDomain(lp0.getName())

def softenConcrete():
    vCompDisp= modelSpace.getIntForceComponentFromName('N1')
    for e in concreteSet.elements:
        e.getResistingForce()
        physProp= e.getPhysicalProperties
        N1= physProp.getMeanGeneralizedStressByName(vCompDisp)
        for mat in physProp.getVectorMaterials:
            if(N1>0):
                mat.E/=10.0

# *********Solution*********
analysis = predefined_solutions.simple_static_linear(FEcase)
result = analysis.analyze(1)
# softenConcrete()
# result = analysis.analyze(1)
# softenConcrete()
# result = analysis.analyze(1)
# softenConcrete()
# result = analysis.analyze(1)
# softenConcrete()
# result = analysis.analyze(1)
# softenConcrete()
# result = analysis.analyze(1)

# Graphics

## Fill sets
for key in rebarSets:
    s= rebarSets[key]
    s.fillDownwards()
    
#oh.displayBlocks()
#oh.displayLocalAxes()
#oh.displayFEMesh()
oh.displayLoads()

#oh.displayDispRot(itemToDisp='uY')
# oh.displayDispRot(itemToDisp='uZ')
# oh.displayIntForc(itemToDisp= 'N1', setToDisplay= concreteSet)
# oh.displayIntForcDiag(itemToDisp= 'N', setToDisplay= rebarSets[22])
# oh.displayIntForcDiag(itemToDisp= 'N', setToDisplay= rebarSets[16])
# oh.displayIntForcDiag(itemToDisp= 'N', setToDisplay= rebarSets[13])
# oh.displayIntForcDiag(itemToDisp= 'N', setToDisplay= rebarSets[10])
# oh.displayIntForcDiag(itemToDisp= 'N', setToDisplay= rebarSets[06])
oh.displayReactions()
#oh.displayIntForc('M2', setToDisplay= concreteSet)
