# -*- coding: utf-8 -*-
''' Main LVL bearing connection check.'''
from __future__ import division
from __future__ import print_function


inch2meter= 0.0254
pound2Newton=  4.4482216282509
pa2psi= 145.038e-6
psi2pa= 1.0/pa2psi
psf2pa= 47.880208 # N/m2

studSpacing= 12*inch2meter
joistSpacing= 24*inch2meter
tributaryArea= studSpacing*joistSpacing/2.0
deadLoad= 15*psf2pa*tributaryArea # Dead load.
liveLoad= 100*psf2pa*tributaryArea # Live load.
maxLoad= deadLoad+liveLoad # Bearing load.

connectionAllowableLoad= 365*pound2Newton
capacityFactor= maxLoad/connectionAllowableLoad

print('Max. load: ',maxLoad/1e3,'kN (', maxLoad/pound2Newton,'pounds)')
print('Connection allowable load: ',connectionAllowableLoad/1e3,'kN (', connectionAllowableLoad/pound2Newton,'pounds)')
print('Connection capacity factor: ',capacityFactor)


