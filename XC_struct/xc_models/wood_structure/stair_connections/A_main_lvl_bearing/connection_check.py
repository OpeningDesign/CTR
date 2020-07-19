# -*- coding: utf-8 -*-
''' Main LVL bearing connection check.'''
from __future__ import division
from __future__ import print_function


inch2meter= 0.0254
pound2Newton=  4.4482216282509
pa2psi= 145.038e-6
psi2pa= 1.0/pa2psi

a= 2.5*inch2meter # Bearing length.
b= 5.25*inch2meter # LVL main header width.

bearingSurface= a*b
deadLoad= 2.0e3 # Dead load
liveLoad= 8.0e3 # Live load
maxLoad= deadLoad+liveLoad # Bearing load.
bearingStress= maxLoad/bearingSurface
Cr= 1.0 # Repetitive member factor (NDS table 4A page 32)
CM= 1.0 # Wet service factor (NDS table 4A page 32)
# Flat use factor: doesn't apply
# Size factor: doesn't apply
# Load duration factor: doesn't apply (NDS section 4.3.2)
# Beam stability factor: doesn't apply.
# Bearing area factor: doesn't apply -it's a member end- (NDS section 3.10.4)

bearingStrength= Cr*CM*425*psi2pa # Spruce-pine-fir national design specification (NDS table 4A page 37)


print('bearing stress: ',bearingStress/1e6,'MPa (', bearingStress*pa2psi,'psi)')
print('bearing strength: ',bearingStrength/1e6,'MPa (', bearingStrength*pa2psi,'psi)')
print('capacity factor: ',bearingStress/bearingStrength)


