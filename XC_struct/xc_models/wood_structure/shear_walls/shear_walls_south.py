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

leewardWallPressure= 595 # Pa
parapetWindwardWallPressure= 1494 # Pa
parapetLeewardWallPressure= -992 # Pa
flatRoof= -1272 # Pa

# Floor heights.
firstFlHeight= 3.4544 # m
secondFlHeight= 3.3528 # m
thirdFlHeight= 3.302 # m
parapetHeight= 0.6096 # m

# Forces per unit length on floor.
roofLeewardForcePerUnitLength= thirdFlHeight/2.0*leewardWallPressure+parapetHeight*(parapetWindwardWallPressure-parapetLeewardWallPressure)
thirdFlLeewardForcePerUnitLength= secondFlHeight/2.0*leewardWallPressure+thirdFlHeight/2.0*leewardWallPressure
secondFlLeewardForcePerUnitLength= firstFlHeight/2.0*leewardWallPressure+secondFlHeight/2.0*leewardWallPressure

# Forces on floors
length= 22.0
secondFlLeewardForce= length*secondFlLeewardForcePerUnitLength
thirdFlLeewardForce= length*thirdFlLeewardForcePerUnitLength
roofLeewardForce= length*roofLeewardForcePerUnitLength

print('roof force per unit length: ', roofLeewardForcePerUnitLength/1e3, 'kN/m')
print('roof force per wall: ', roofLeewardForce/1e3/5.0, 'kN')
print('roof force per wall unit length: ', roofLeewardForce/1e3/5.0/10.0, 'kN/m')

roofReaction= roofLeewardForce
thirdFlReaction= thirdFlLeewardForce+roofReaction
secondFlReaction= secondFlLeewardForce+thirdFlReaction

print('roofLeewardForcePerUnitLength= ',roofLeewardForcePerUnitLength/1e3,' kN/m')
print('thirdFlLeewardForcePerUnitLength= ',thirdFlLeewardForcePerUnitLength/1e3,' kN/m')
print('secondFlLeewardForcePerUnitLength= ',secondFlLeewardForcePerUnitLength/1e3,' kN/m')
print('roofReaction= ', roofReaction/1e3, ' roofLeewardForce= ', roofLeewardForce/1e3)
print('thirdFlReaction= ', thirdFlReaction/1e3, ' thirdFlLeewardForce= ', thirdFlLeewardForce/1e3)
print('secondFlReaction= ', secondFlReaction/1e3, ' secondFlLeewardForce= ', secondFlLeewardForce/1e3)

