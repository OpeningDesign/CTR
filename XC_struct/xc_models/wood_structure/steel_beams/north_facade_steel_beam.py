# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

import math
import vtk
import xc_base
import geom
import xc
from solution import predefined_solutions
from model import predefined_spaces
from materials import typical_materials
from materials.astm_aisc import ASTM_materials

from materials.sections import structural_steel as steel
from actions import load_cases as lcm
from actions import combinations as combs
from datetime import date
import aisc_checking

#Units
foot2m= 0.3048
inch2m= 0.0254

# Problem type
steelBeam= xc.FEProblem()
steelBeam.title= 'Steel beams at 2nd floor. North facade'
preprocessor= steelBeam.getPreprocessor
nodes= preprocessor.getNodeHandler

# Materials
## Steel material
steel= ASTM_materials.A572
steel.gammaM= 1.00
## Profile geometry
# profile= ASTM_materials.CShape(steel,'C380X50.4')
# numberOfProfiles= 2 # 2 UPN profiles!!
# profile= ASTM_materials.WShape(steel,'W16X57')
profile= ASTM_materials.WShape(steel,'W12X87')
numberOfProfiles= 1 # 1 W profiles
xcSection= profile.defElasticShearSection2d(preprocessor)

# Model geometry

## Points.
span= 23.0*foot2m+(9.0+7/8.0)*inch2m
pointHandler= preprocessor.getMultiBlockTopology.getPoints
p0= pointHandler.newPntFromPos3d(geom.Pos3d(0.0,0.0,0.0))
p1= pointHandler.newPntFromPos3d(geom.Pos3d(span,0.0,0.0))

## Lines
lineHandler= preprocessor.getMultiBlockTopology.getLines
l1= lineHandler.newLine(p0.tag,p1.tag)
l1.nDiv= 10

# Mesh
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)
trfs= preprocessor.getTransfCooHandler
lin= trfs.newLinearCrdTransf2d("lin")
seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultMaterial= xcSection.name
seedElemHandler.defaultTransformation= "lin"
elem= seedElemHandler.newElement("ElasticBeam2d",xc.ID([0,0]))

xcTotalSet= preprocessor.getSets.getSet('total')
mesh= xcTotalSet.genMesh(xc.meshDir.I)

# Constraints
modelSpace.fixNode00F(p0.getNode().tag)
modelSpace.fixNodeF0F(p1.getNode().tag)

# Actions

## Load cases
loadCaseManager= lcm.LoadCaseManager(preprocessor)
loadCaseNames= ['deadLoad','liveLoad','snowLoad','windLoad']
loadCaseManager.defineSimpleLoadCases(loadCaseNames)

def defineLoad(loadCaseName, loadValue):
    print(loadCaseName, loadValue/1e3, 'kN')
    cLC= loadCaseManager.setCurrentLoadCase(loadCaseName)
    loadVector= xc.Vector([0.0,-loadValue])
    for e in xcTotalSet.elements:
        e.vector2dUniformLoadGlobal(loadVector)

### Load values from "E_reactions.ods"    
### Dead load
selfWeight= numberOfProfiles*profile.getRho()*9.81
defineLoad('deadLoad',(selfWeight+14.25e3)/numberOfProfiles)
### Live load
defineLoad('liveLoad',21.74e3/numberOfProfiles)
### Snow load
defineLoad('snowLoad',9.52e3/numberOfProfiles)
### Wind load
defineLoad('windLoad',-6.01e3/numberOfProfiles)

## Load combinations
combContainer= combs.CombContainer()
### Serviceability limit states.
combContainer.SLS.qp.add('SLS01', '1.0*liveLoad')
combContainer.SLS.qp.add('SLS02', '1.0*deadLoad+1.0*liveLoad')
combContainer.SLS.qp.add('SLS03', '1.0*deadLoad+1.0*snowLoad')
### Ultimate limit state.
combContainer.ULS.perm.add('ULS01', '1.4*deadLoad')
combContainer.ULS.perm.add('ULS02', '1.2*deadLoad + 1.6*liveLoad + 0.5*snowLoad')
combContainer.ULS.perm.add('ULS03', '1.2*deadLoad + 1.6*snowLoad + 0.5*liveLoad ')
combContainer.ULS.perm.add('ULS04', '1.2*deadLoad + 1.6*snowLoad + 0.5*windLoad')
combContainer.ULS.perm.add('ULS05', '1.2*deadLoad + 1.0*windLoad + 0.5*liveLoad ')
combContainer.ULS.perm.add('ULS06', '1.2*deadLoad + 0.5*liveLoad + 0.2*snowLoad')
combContainer.ULS.perm.add('ULS07', '0.9*deadLoad + 1.0*windLoad')
### Dump combination definition into XC.
combContainer.dumpCombinations(preprocessor)

# Solution
## Linear static analysis.
analysis= predefined_solutions.simple_static_linear(steelBeam)

# Checking
## Check deflection limit
deflectionLimits= dict()
deflectionLimits['SLS01']= span/540.0
deflectionLimits['SLS02']= span/240.0
deflectionLimits['SLS03']= span/240.0
midSpan1= span/2
n1= l1.getNearestNode(geom.Pos3d(midSpan1,0.0,0.0))

print(date.today(), steelBeam.title)
print('  cheking profile: ', profile.name, profile.getRho(), 'kg/m')
print('  L= ', span, 'm')

print('  Serviceability limit states.')
aisc_checking.sls_check(combContainer.SLS.qp, xcTotalSet, deflectionLimits, analysis)

## Check flexural and shear strength.
print('  Ultimate limit states.')
aisc_checking.uls_check(profile, combContainer.ULS.perm, xcTotalSet, analysis)


