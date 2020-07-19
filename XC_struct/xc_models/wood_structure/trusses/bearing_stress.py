# -*- coding: utf-8 -*-
''' bearing stress checking according to
    American Wood Council National Design Specification 2018.'''

from __future__ import print_function
from __future__ import division

inchToMeter= 2.54/100.0
pa2psi= 145.038e-6
psi2pa= 1.0/pa2psi

a= 2.0*inchToMeter # Entrega de la cercha.
b= 4.0*inchToMeter # Truss bottom chord width.

bearingSurface= a*b
maxLoad= 25.9e3/2.0 # Bearing load zone AB internal wall
bearingStress= maxLoad/bearingSurface
Cr= 1.0 # Repetitive member factor (NDS table 4A page 32)
CM= 1.0 # Wet service factor (NDS table 4A page 32)
# Flat use factor: doesn't apply
# Size factor: doesn't apply
# Load duration factor: doesn't apply (NDS section 4.3.2)
# Beam stability factor: doesn't apply.
# Bearing area factor: doesn't apply -it's a member end- (NDS section 3.10.4)

bearingStrength= Cr*CM*405*psi2pa # National design specification (NDS table 4A page 35)


print('bearing stress: ',bearingStress/1e6,'MPa (', bearingStress*pa2psi,'psi)')
print('bearing strength: ',bearingStrength/1e6,'MPa (', bearingStrength*pa2psi,'psi)')
print('capacity factor: ',bearingStress/bearingStrength)
