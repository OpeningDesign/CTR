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

hucConnectorAllowableLoad= 1785.0*pound2Newton # HUC46 joist hanger strength.

deadLoad= 1.14e3 # Dead load
liveLoad= 4.56e3 # Live load
maxLoad= deadLoad+liveLoad # Bearing load.
hucCapacityFactor= maxLoad/hucConnectorAllowableLoad


print('Max. load: ',maxLoad/1e3,'kN (', maxLoad/pound2Newton,'pounds)')
print('HUC46 connector allowable load: ',hucConnectorAllowableLoad/1e3,'kN (', hucConnectorAllowableLoad/pound2Newton,'pounds)')
print('HUC46 connector capacity factor: ',hucCapacityFactor)


