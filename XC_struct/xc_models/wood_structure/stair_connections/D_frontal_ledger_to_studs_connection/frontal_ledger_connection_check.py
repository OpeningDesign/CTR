# -*- coding: utf-8 -*-
''' Main LVL bearing connection check.'''
from __future__ import division
from __future__ import print_function

import math

inch2meter= 0.0254
pound2Newton=  4.4482216282509
pa2psi= 145.038e-6
psi2pa= 1.0/pa2psi
psf2pa= 47.880208 # N/m2

studSpacing= 12*inch2meter
landingWidth= 1.9 # meters
deadLoad= 1197*studSpacing*landingWidth/2.0 # Dead load.
liveLoad= 4788*studSpacing*landingWidth/2.0 # Live load.
maxShearLoad= deadLoad+liveLoad # Bearing load.

connectionAllowableShearLoad= 555*pound2Newton
shearCapacityFactor= maxShearLoad/connectionAllowableShearLoad

print('Max. load: ',maxShearLoad/1e3,'kN (', maxShearLoad/pound2Newton,'pounds)')
print('Connection allowable shear load: ',connectionAllowableShearLoad/1e3,'kN (', connectionAllowableShearLoad/pound2Newton,'pounds)')
print('Connection shear capacity factor: ',shearCapacityFactor)

# Bracing force estimation .01*studLoad according to the
# publication Bracing for Stability
# https://www.aisc.org/globalassets/aisc/research-library/bracing-for-stability.pdf
numberOfScrews= 3
studLoad= 10e3 # N
threadPenetration= (6.0-2.0)*inch2meter
connectionAllowableWithdrawalLoad= numberOfScrews*min(187*pound2Newton*threadPenetration/inch2meter,495*pound2Newton)
ratio= connectionAllowableWithdrawalLoad/studLoad
bracingCapacityFactor= .01/ratio

capacityFactor= math.sqrt(shearCapacityFactor**2+bracingCapacityFactor**2)


print('Connection allowable withdrawal load: ',connectionAllowableWithdrawalLoad/1e3,'kN (', connectionAllowableWithdrawalLoad/pound2Newton,'pounds)')
print('ratio: ',ratio*100,'%')
print('Connection bracing capacity factor: ',bracingCapacityFactor)

