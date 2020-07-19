# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

'''
Design of the connection to resist the 5.3 kips uplift.
'''
inch2meter= 0.0254
kip2kN= 4.4482216
ksi2MPa= 6.89476

# Bolt diameter
boltDiameter= 5/8.0*inch2meter

# Plate geometry
plateThickness= 0.5*inch2meter
plateWidth= 4.0*inch2meter
plateArea= plateThickness*plateWidth
holeDiameter= boltDiameter+1/8.0*inch2meter
e1= 2*holeDiameter
e2= e1
p1= 3*holeDiameter
p2= 3*holeDiameter


# Material
## ASTM A36
Fy= 36*ksi2MPa*1e6
Fu= 58/36.0*Fy
Phi= 0.9 # reduction factor

# Shear lag factor
U= 1.0

# Loads
Pk= 5.3*kip2kN*1e3 # uplift force
Pd= 1.6*Pk

Anec= Pd/(Fy*Phi)
plateWidthNec= max(Anec/plateThickness,holeDiameter+2.0*e2)

# Net dimensions
## Net hole diameter
d_net= holeDiameter+1/16.0*inch2meter
## Net width
w= plateWidth-d_net
## Net area
A_n= w*plateThickness
## Effective area
A_e= U*A_n

# Weld
l= 0.85*plateWidth
a= Pd/(2.0*l*0.85*Fy)


print('plate thickness t= ', plateThickness*1e3, 'mm')
print('plate width w= ', plateWidth*1e3, 'mm')
print('e_1= ', e1*1e3, 'mm')
print('e_2= ', e2*1e3, 'mm')
print('distance between holes p_1=',p1*1e3,'mm')
print('bolt diameter d_h=', boltDiameter*1e3, 'mm')
print('uplift force: ', Pk/1e3, 'kN')
print('Fy= ', Fy/1e6, 'MPa')
print('Fu= ', Fu/1e6, 'MPa')
print('Anec= ', Anec, 'm2')
print('nec. plate width= ', plateWidthNec*1e3, 'mm')
print('net hole diameter d_net=', d_net*1e3,'mm')
print('net width w=', w*1e3,'mm')
print('net area A_n=', A_n*1e6,'mm2')
print('effective area A_e=', A_e*1e6,'mm2')
print('weld throat a=', a*1e3,'mm')
