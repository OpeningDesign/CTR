# -*- coding: utf-8 -*-
''' Main LVL bearing connection check.'''
from __future__ import division
from __future__ import print_function


inch2meter= 0.0254
pound2Newton=  4.4482216282509
pa2psi= 145.038e-6
psi2pa= 1.0/pa2psi

# Standard LSC installation.
# 1 3/4" X 11 7/8" LVL STRINGERS -> DF/SP Allowable Loads

lscStringerAllowableLoad= 755*pound2Newton # LSC stringer connector strength.
hucqConnectorAllowableLoad= 2500*pound2Newton # HUCQ 1.81/11-SDS joist hanger strength.

deadLoad= 2.0*0.84e3 # Dead load
liveLoad= 2.0*3.36e3 # Live load
maxLoad= deadLoad+liveLoad # Bearing load.
lscCapacityFactor= 0.2*maxLoad/lscStringerAllowableLoad
hucqCapacityFactor= maxLoad/hucqConnectorAllowableLoad


print('Max. load: ',maxLoad/1e3,'kN (', maxLoad/pound2Newton,'pounds)')
print('LSC stringer connector allowable load: ',lscStringerAllowableLoad/1e3,'kN (', lscStringerAllowableLoad/pound2Newton,'pounds)')
print('HUCQ 1.81/11-SDS connector allowable load: ',hucqConnectorAllowableLoad/1e3,'kN (', hucqConnectorAllowableLoad/pound2Newton,'pounds)')
print('LSC connector capacity factor: ',lscCapacityFactor)
print('HUCQ connector capacity factor: ',hucqCapacityFactor)


