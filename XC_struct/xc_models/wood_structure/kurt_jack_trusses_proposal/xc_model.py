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
from materials.sections import section_properties
from materials.awc_nds import AWCNDS_materials
from materials.awc_nds import structural_panels
from postprocess import output_handler
from solution import predefined_solutions
from actions import load_cases as lcm
from actions import combinations as combs

inchToMeter= 0.0254
pound2N=4.45
ft2m=0.3048
psiToPa= 6894.76
psf2N_m2= 0.047880258888889e3

FEcase= xc.FEProblem()
FEcase.title= 'Loads on jack trusses at south facade'
execfile('./xc_model_blocks.py')

xcTotalSet= preprocessor.getSets.getSet('total')

jackTrussesSet= preprocessor.getSets.defSet('jackTrussesSet')
girderSet= preprocessor.getSets.defSet('girderSet')
lvlBlindFasciaSet= preprocessor.getSets.defSet('lvlBlindFasciaSet')
regularTrussesSet= preprocessor.getSets.defSet('regularTrussesSet')
for l in xcTotalSet.getLines:
    l.setProp('spacing',12*inchToMeter)
    if(l.hasProp('labels')):
        labels= l.getProp('labels')
        if(labels.count('xc_jack_trusses')>0):
            if(abs(l.getTang(0.0)[1])<1e-3):
                l.setProp('spacing',24*inchToMeter)
            jackTrussesSet.getLines.append(l)
        elif(labels.count('xc_blue_girder')>0):
            girderSet.getLines.append(l)
        elif(labels.count('xc_lvl_blind_fascia')>0):
            lvlBlindFasciaSet.getLines.append(l)
        elif(labels.count('xc_regular_trusses')>0):
            regularTrussesSet.getLines.append(l)

supportSet= preprocessor.getSets.defSet('supportSet')
for p in xcTotalSet.getPoints:
    if(p.hasProp('labels')):
        labels= p.getProp('labels')
        if(labels.count('xc_supports')>0):
            supportSet.getPoints.append(p)

southFacadeLoads= preprocessor.getSets.defSet('southFacadeLoads')
for p in xcTotalSet.getPoints:
    if(p.hasProp('labels')):
        labels= p.getProp('labels')
        if(labels.count('xc_south_facade_loads')>0):
           southFacadeLoads.getPoints.append(p)

southFacadeLoads2= preprocessor.getSets.defSet('southFacadeLoads2')
for p in xcTotalSet.getPoints:
    if(p.hasProp('labels')):
        labels= p.getProp('labels')
        if(labels.count('xc_south_facade_loads2')>0):
           southFacadeLoads2.getPoints.append(p)
           
eastFacadeLoads= preprocessor.getSets.defSet('eastFacadeLoads')
for p in xcTotalSet.getPoints:
    if(p.hasProp('labels')):
        labels= p.getProp('labels')
        if(labels.count('xc_east_facade_loads')>0):
           eastFacadeLoads.getPoints.append(p)

# Problem type
preprocessor=FEcase.getPreprocessor
nodes= preprocessor.getNodeHandler
modelSpace= predefined_spaces.StructuralMechanics3D(nodes) 

# Materials

## LVL blind fascia: 1.55E (page 10 of the PDF document from "SolidStart")
LVL= typical_materials.MaterialData(name='LVL',E=2.0e6*psiToPa,nu=0.2,rho=500)
lvlBlindSectionGeometry= section_properties.RectangularSection("lvlBlind",b=1.75*inchToMeter,h=24.0*inchToMeter)
lvlBlindSection= lvlBlindSectionGeometry.defElasticShearSection3d(preprocessor,LVL)

## Materials LSL 1.55E (page 10 of the PDF document from "SolidStart")
lslJackTrussSection= structural_panels.LSL155HeaderSections['1.75x14'].defElasticShearSection3d(preprocessor)

## Girder material.
lvlGirderSectionGeometry= section_properties.RectangularSection("lvlGirder", b=1.25*inchToMeter, h=19.09*inchToMeter)
lvlGirderSection= lvlGirderSectionGeometry.defElasticShearSection3d(preprocessor, LVL)

## Regular trusses.
lvlRegTrussSectionGeometry= section_properties.RectangularSection("lvlRegTruss", b=1.25*inchToMeter, h=12.50*inchToMeter)
lvlRegTrussSection= lvlRegTrussSectionGeometry.defElasticShearSection3d(preprocessor, LVL)

# Mesh generation.
lin= preprocessor.getTransfCooHandler.newLinearCrdTransf3d('lin')
lin.xzVector= xc.Vector([1.0,0,0])

seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultTransformation= "lin"

def createMesh(xcSet, section):
    seedElemHandler.defaultMaterial= section.name

    for l in xcSet.getLines:
        vDir= l.getTang(0.0)
        lin.xzVector= xc.Vector([vDir[1], -vDir[0], vDir[2]])
        elem= seedElemHandler.newElement("ElasticBeam3d",xc.ID([0,0]))
        l.genMesh(xc.meshDir.I)
    xcSet.fillDownwards()

    
## Jack trusses.
createMesh(jackTrussesSet, lslJackTrussSection)
## Girder.
createMesh(girderSet, lvlGirderSection)
## Blind fascia.
createMesh(lvlBlindFasciaSet,lvlBlindSection)
## Regular trusses.
createMesh(regularTrussesSet, lvlRegTrussSection)

## "Remove" torsional stiffness
for e in xcTotalSet.elements:
    sp= e.sectionProperties
    sp.J/=100.0
    e.setSectionProperties(sp)
    

# Constraints
for p in supportSet.getPoints:
    if(not p.hasNode):
        lmsg.warning('point: '+str(p)+' not meshed.')
    n= p.getNode()
    modelSpace.fixNode('000_FFF',n.tag)
    
## Graphic stuff.
oh= output_handler.OutputHandler(modelSpace)

# Loads
loadCaseManager= lcm.LoadCaseManager(preprocessor)
loadCaseNames= ['deadLoad', 'liveLoad', 'windLoad', 'snowLoad']
loadCaseManager.defineSimpleLoadCases(loadCaseNames)

def loadOnLines(xcSet, loadVector):
    for l in xcSet.getLines:
        spacing= l.getProp('spacing')
        #print('spacing= '+str(spacing)+' load= '+str(spacing*loadVector))
        for e in l.getElements:
            e.vector3dUniformLoadGlobal(spacing*loadVector)

### Dead load.
cLC= loadCaseManager.setCurrentLoadCase('deadLoad')

#### Dead load on elements.
deadL= 15*psf2N_m2
uniformLoad= xc.Vector([0.0,0.0,-deadL])
loadOnLines(jackTrussesSet,uniformLoad)
loadOnLines(girderSet,uniformLoad)
loadOnLines(lvlBlindFasciaSet,uniformLoad)
loadOnLines(regularTrussesSet,uniformLoad)

#### Dead load on nodes.
for p in southFacadeLoads.getPoints:
    if(not p.hasNode):
        lmsg.warning('point: '+str(p)+' not meshed.')
    n= p.getNode()
    n.newLoad(xc.Vector([0.0,0.0,-726.74*pound2N,0.0,0.0,0.0]))
    
for p in southFacadeLoads2.getPoints:
    if(not p.hasNode):
        lmsg.warning('point: '+str(p)+' not meshed.')
    n= p.getNode()
    n.newLoad(xc.Vector([0.0,0.0,-726.74*pound2N*2.4291/.6096/2.0,0.0,0.0,0.0]))

for p in eastFacadeLoads.getPoints:
    if(not p.hasNode):
        lmsg.warning('point: '+str(p)+' not meshed.')
    n= p.getNode()
    n.newLoad(xc.Vector([0.0,0.0,-1044.55*pound2N,0.0,0.0,0.0]))

### Live load.
cLC= loadCaseManager.setCurrentLoadCase('liveLoad')

#### Live load on elements.
liveL= 40.0*psf2N_m2
uniformLoad= xc.Vector([0.0,0.0,-liveL])
loadOnLines(jackTrussesSet,uniformLoad)
loadOnLines(girderSet,uniformLoad)
loadOnLines(lvlBlindFasciaSet,uniformLoad)
loadOnLines(regularTrussesSet,uniformLoad)

#### Live load on nodes.
for p in eastFacadeLoads.getPoints:
    if(not p.hasNode):
        lmsg.warning('point: '+str(p)+' not meshed.')
    n= p.getNode()
    n.newLoad(xc.Vector([0.0,0.0,-1107.39*pound2N,0.0,0.0,0.0]))

### Wind load.
cLC= loadCaseManager.setCurrentLoadCase('windLoad')

#### Wind load on nodes.
for p in eastFacadeLoads.getPoints:
    if(not p.hasNode):
        lmsg.warning('point: '+str(p)+' not meshed.')
    n= p.getNode()
    n.newLoad(xc.Vector([0.0,0.0,488.33*pound2N,0.0,0.0,0.0]))

### Snow load.
cLC= loadCaseManager.setCurrentLoadCase('snowLoad')

#### Snow load on nodes.
for p in eastFacadeLoads.getPoints:
    if(not p.hasNode):
        lmsg.warning('point: '+str(p)+' not meshed.')
    n= p.getNode()
    n.newLoad(xc.Vector([0.0,0.0,-772.87*pound2N,0.0,0.0,0.0]))

# Load combination definition
combContainer= combs.CombContainer()

## Serviceability limit states.

### Equation 16-8
combContainer.SLS.qp.add('EQ1608', '1.0*deadLoad')
### Equation 16-9
combContainer.SLS.qp.add('EQ1609', '1.0*deadLoad+1.0*liveLoad')
### Equation 16-10
combContainer.SLS.qp.add('EQ1610', '1.0*deadLoad+1.0*snowLoad')
### Equation 16-11
combContainer.SLS.qp.add('EQ1611', '1.0*deadLoad+0.75*liveLoad+0.75*snowLoad')
### Equation 16-12
combContainer.SLS.qp.add('EQ1612', '1.0*deadLoad+0.6*windLoad')
### Equation 16-13
combContainer.SLS.qp.add('EQ1613', '1.0*deadLoad+0.45*windLoad+0.75*liveLoad+0.75*snowLoad')
### Equation 16-14-> doesn't apply
### Equation 16-15
combContainer.SLS.qp.add('EQ1615', '0.6*deadLoad+0.6*windLoad')
### Equation 16-16 -> doesn't apply
### LIVE load only.
combContainer.SLS.qp.add('LIVE', '1.0*liveLoad')

combContainer.dumpCombinations(preprocessor)

preprocessor.getLoadHandler.addToDomain('EQ1611')

# Solution
# Linear static analysis.
analysis= predefined_solutions.simple_static_linear(FEcase)
result= analysis.analyze(1)



# Graphics

#oh.displayBlocks()
#oh.displayLocalAxes(setToDisplay= girderSet)
#oh.displayLocalAxes(setToDisplay= lvlBlindFasciaSet)
oh.displayLocalAxes()

#oh.displayFEMesh()
oh.displayLoads()#setToDisplay= lvlBlindFasciaSet)

#oh.displayDispRot(itemToDisp='uY')
#oh.displayDispRot(itemToDisp='uZ')
# oh.displayIntForcDiag(itemToDisp= 'Mz', setToDisplay= jackTrussesSet)
# oh.displayIntForcDiag(itemToDisp= 'Vy', setToDisplay= jackTrussesSet)
# oh.displayIntForcDiag(itemToDisp= 'Mz', setToDisplay= girderSet)
# oh.displayReactions(setToDisplay= girderSet)
#oh.displayIntForcDiag(itemToDisp= 'Vy', setToDisplay= regularTrussesSet+jackTrussesSet+girderSet)
#oh.displayIntForcDiag(itemToDisp= 'Vy', setToDisplay= lvlBlindFasciaSet)
#oh.displayIntForcDiag(itemToDisp= 'Vy', setToDisplay= girderSet)
#oh.displayIntForcDiag(itemToDisp= 'Mz', setToDisplay= regularTrussesSet)
#oh.displayReactions(setToDisplay= regularTrussesSet)
#oh.displayIntForcDiag(itemToDisp= 'Vy', setToDisplay= regularTrussesSet)
#oh.displayIntForc('Q1')
