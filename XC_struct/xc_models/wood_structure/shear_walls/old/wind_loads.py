# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division
import xc_base
import geom
import xc
from model import predefined_spaces
from solution import predefined_solutions
from materials.sections import section_properties
from materials import typical_materials

# Loads
from actions import load_cases as lcm
from actions import combinations as combs

# Design wind pressures

windwardWallPressure= 501 # Pa
leewardWallPressure= -595 # Pa
parapetWindwardWallPressure= 1494 # Pa
parapetLeewardWallPressure= -992 # Pa
flatRoof= -1272 # Pa

# Floor heights.
firstFlHeight= 3.4544 # m
secondFlHeight= 3.3528 # m
thirdFlHeight= 3.302 # m
parapetHeight= 0.6096 # m

# Forces per unit length on floors.
roofWinwardForcePerUnitLength= thirdFlHeight/2.0*windwardWallPressure+parapetHeight*(parapetWindwardWallPressure-parapetLeewardWallPressure)
thirdFlWinwardForcePerUnitLength= secondFlHeight/2.0*windwardWallPressure+thirdFlHeight/2.0*windwardWallPressure
secondFlWinwardForcePerUnitLength= firstFlHeight/2.0*windwardWallPressure+secondFlHeight/2.0*windwardWallPressure
# roofForcePerUnitLength= thirdFlHeight*(windwardWallPressure-leewardWallPressure)/2.0+parapetHeight*(parapetWindwardWallPressure-parapetLeewardWallPressure)
# thirdFlForcePerUnitLength= (secondFlHeight*(windwardWallPressure-leewardWallPressure)+thirdFlHeight*(windwardWallPressure-leewardWallPressure))/2.0
# secondFlForcePerUnitLength= (firstFlHeight*(windwardWallPressure-leewardWallPressure)+secondFlHeight*(windwardWallPressure-leewardWallPressure))/2.0

# Forces on floors
length= 45.53
secondFlWindwardForce= length*secondFlWinwardForcePerUnitLength
thirdFlWindwardForce= length*thirdFlWinwardForcePerUnitLength
roofWindwardForce= length*roofWinwardForcePerUnitLength

print('roof force per unit length: ', roofWinwardForcePerUnitLength/1e3, 'kN/m')
print('roof force per wall: ', roofWindwardForce/1e3/5.0, 'kN')
print('roof force per wall unit length: ', roofWindwardForce/1e3/5.0/10.0, 'kN/m')

# Problem type
sheathingBeam= xc.FEProblem()
sheathingBeam.title= 'Sheating design'
preprocessor= sheathingBeam.getPreprocessor   
nodes= preprocessor.getNodeHandler
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)

# Materials
diaphragm= section_properties.RectangularSection("diaphragm",b=.05,h=5.0)
plywood= typical_materials.MaterialData(name='Douglas-Fri Plywood',E=4.2e9,nu=0.2,rho=500)
section= diaphragm.defElasticShearSection2d(preprocessor,plywood)

L1_2nd_floor= 10.0752
L1= 13.2451
L2= 10.2413
L3= 10.5461
L4= 11.4789

# The z coordinate has only a "decorative" purpose 
zRoof= firstFlHeight + secondFlHeight + thirdFlHeight
zThirdFl= firstFlHeight + secondFlHeight
zSecondFl= firstFlHeight
pointHandler= preprocessor.getMultiBlockTopology.getPoints
roofPt1= pointHandler.newPntFromPos3d(geom.Pos3d(0.0,0.0,zRoof))
roofPt2= pointHandler.newPntFromPos3d(geom.Pos3d(L1,0.0,zRoof))
roofPt3= pointHandler.newPntFromPos3d(geom.Pos3d(L1+L2,0.0,zRoof))
roofPt4= pointHandler.newPntFromPos3d(geom.Pos3d(L1+L2+L3,0.0,zRoof))
roofPt5= pointHandler.newPntFromPos3d(geom.Pos3d(L1+L2+L3+L4,0.0,zRoof))

thirdFlPt1= pointHandler.newPntFromPos3d(geom.Pos3d(0.0,0.0,zThirdFl))
thirdFlPt2= pointHandler.newPntFromPos3d(geom.Pos3d(L1,0.0,zThirdFl))
thirdFlPt3= pointHandler.newPntFromPos3d(geom.Pos3d(L1+L2,0.0,zThirdFl))
thirdFlPt4= pointHandler.newPntFromPos3d(geom.Pos3d(L1+L2+L3,0.0,zThirdFl))
thirdFlPt5= pointHandler.newPntFromPos3d(geom.Pos3d(L1+L2+L3+L4,0.0,zThirdFl))

secondFlPt1= pointHandler.newPntFromPos3d(geom.Pos3d(0.0,0.0,zSecondFl))
secondFlPt2a= pointHandler.newPntFromPos3d(geom.Pos3d(L1_2nd_floor,0.0,zSecondFl))
secondFlPt2b= pointHandler.newPntFromPos3d(geom.Pos3d(L1,0.0,zSecondFl))
secondFlPt3= pointHandler.newPntFromPos3d(geom.Pos3d(L1+L2,0.0,zSecondFl))
secondFlPt4= pointHandler.newPntFromPos3d(geom.Pos3d(L1+L2+L3,0.0,zSecondFl))
secondFlPt5= pointHandler.newPntFromPos3d(geom.Pos3d(L1+L2+L3+L4,0.0,zSecondFl))

lines= preprocessor.getMultiBlockTopology.getLines
roofl1= lines.newLine(roofPt1.tag,roofPt2.tag)
roofl2= lines.newLine(roofPt2.tag,roofPt3.tag)
roofl3= lines.newLine(roofPt3.tag,roofPt4.tag)
roofl4= lines.newLine(roofPt4.tag,roofPt5.tag)
roofLines= [roofl1,roofl2,roofl3,roofl4]
roofSet= preprocessor.getSets.defSet("roofSet")
for l in roofLines:
    roofSet.getLines.append(l)

thirdFll1= lines.newLine(thirdFlPt1.tag,thirdFlPt2.tag)
thirdFll2= lines.newLine(thirdFlPt2.tag,thirdFlPt3.tag)
thirdFll3= lines.newLine(thirdFlPt3.tag,thirdFlPt4.tag)
thirdFll4= lines.newLine(thirdFlPt4.tag,thirdFlPt5.tag)
thirdFlLines= [thirdFll1,thirdFll2,thirdFll3,thirdFll4]
thirdFlSet= preprocessor.getSets.defSet("thirdFlSet")
for l in thirdFlLines:
    thirdFlSet.getLines.append(l)

secondFll1= lines.newLine(secondFlPt1.tag,secondFlPt2a.tag)
secondFll2a= lines.newLine(secondFlPt2a.tag,secondFlPt2b.tag)
secondFll2b= lines.newLine(secondFlPt2b.tag,secondFlPt3.tag)
secondFll3= lines.newLine(secondFlPt3.tag,secondFlPt4.tag)
secondFll4= lines.newLine(secondFlPt4.tag,secondFlPt5.tag)
secondFlLines= [secondFll1,secondFll2a,secondFll2b,secondFll3,secondFll4]
secondFlSet= preprocessor.getSets.defSet("secondFlSet")
for l in secondFlLines:
    secondFlSet.getLines.append(l)

# Mesh
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)
# nodes.newSeedNode() DEPRECATED
trfs= preprocessor.getTransfCooHandler
lin= trfs.newLinearCrdTransf2d("lin")
seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultMaterial= section.name
seedElemHandler.defaultTransformation= "lin"
elem= seedElemHandler.newElement("ElasticBeam2d",xc.ID([0,0]))

roofMesh= roofSet.genMesh(xc.meshDir.I)
roofSet.fillDownwards()
thirdFlMesh= thirdFlSet.genMesh(xc.meshDir.I)
thirdFlSet.fillDownwards()
secondFlMesh= secondFlSet.genMesh(xc.meshDir.I)
secondFlSet.fillDownwards()

# Constraints
for p in [roofPt2,roofPt3,roofPt4]:
    n= p.getNode()
    modelSpace.fixNode00F(n.tag)
for p in [thirdFlPt2,thirdFlPt3,thirdFlPt4]:
    n= p.getNode()
    modelSpace.fixNode00F(n.tag)
for p in [secondFlPt2a,secondFlPt3,secondFlPt4]:
    n= p.getNode()
    modelSpace.fixNode00F(n.tag)

# Actions
loadCaseManager= lcm.LoadCaseManager(preprocessor)
loadCaseNames= ['windLoad']
loadCaseManager.defineSimpleLoadCases(loadCaseNames)

# Wind load.
cLC= loadCaseManager.setCurrentLoadCase('windLoad')
for e in roofSet.getElements:
    e.vector2dUniformLoadGlobal(xc.Vector([0.0,-roofWinwardForcePerUnitLength]))
for e in thirdFlSet.getElements:
    e.vector2dUniformLoadGlobal(xc.Vector([0.0,-thirdFlWinwardForcePerUnitLength]))
for e in secondFlSet.getElements:
    e.vector2dUniformLoadGlobal(xc.Vector([0.0,-secondFlWinwardForcePerUnitLength]))

#We add the load case to domain.
preprocessor.getLoadHandler.getLoadPatterns.addToDomain('windLoad')

# Solution
# Linear static analysis.
analisis= predefined_solutions.simple_static_linear(sheathingBeam)
result= analisis.analyze(1)

nodes.calculateNodalReactions(True,1e-7)
loadOnSecondFlPt2b= roofPt2.getNode().getReaction[1]+thirdFlPt2.getNode().getReaction[1]

# We remove the load case to domain.
preprocessor.getLoadHandler.getLoadPatterns.removeFromDomain('windLoad')
# We add the load to the load case.
cLC.newNodalLoad(secondFlPt2b.getNode().tag,xc.Vector([0.0,-loadOnSecondFlPt2b,0.0]))
#We add the load case to domain.
preprocessor.getLoadHandler.getLoadPatterns.addToDomain('windLoad')
# And we solve
analisis= predefined_solutions.simple_static_linear(sheathingBeam)
result= analisis.analyze(1)
                 
nodes.calculateNodalReactions(True,1e-7)
roofR= 0.0
roofReactions= list()
for p in [roofPt2,roofPt3,roofPt4]:
    R= p.getNode().getReaction[1]
    print('roof R= ',R/1e3,' kN')
    roofR+= R
    roofReactions.append(R)
    
thirdFlR= 0.0
thirdFlReactions= list()
for p in [thirdFlPt2,thirdFlPt3,thirdFlPt4]:
    R= p.getNode().getReaction[1]
    print('third floor R= ',R/1e3,' kN')
    thirdFlR+= R
    thirdFlReactions.append(R)

secondFlR= 0.0
secondFlReactions= list()
for p in [secondFlPt2a,secondFlPt3,secondFlPt4]:
    R= p.getNode().getReaction[1]
    print('second floor R= ',R/1e3,' kN')
    secondFlR+= R
    secondFlReactions.append(R)

thirdFlReactions[0]+= roofReactions[0]
thirdFlReactions[1]+= roofReactions[1]
thirdFlReactions[2]+= roofReactions[2]

#secondFlReactions[0]+= thirdFlReactions[0] # Already added.
secondFlReactions[1]+= thirdFlReactions[1]
secondFlReactions[2]+= thirdFlReactions[2]

print('loadOnSecondFlPt2b= ', loadOnSecondFlPt2b/1e3, ' kN')
print('roofR= ', roofR/1e3, ' roofWindwardForce= ', roofWindwardForce/1e3)
print('thirdFlR= ', thirdFlR/1e3, ' thirdFlWindwardForce= ', thirdFlWindwardForce/1e3)
print('secondFlR= ', (secondFlR-loadOnSecondFlPt2b)/1e3, ' secondFlWindwardForce= ', secondFlWindwardForce/1e3)

print('roof: ', roofReactions[0]/1e3, roofReactions[1]/1e3, roofReactions[2]/1e3)
print('thirdFl: ', thirdFlReactions[0]/1e3, thirdFlReactions[1]/1e3, thirdFlReactions[2]/1e3)
print('secondFl: ', secondFlReactions[0]/1e3, secondFlReactions[1]/1e3, secondFlReactions[2]/1e3)
