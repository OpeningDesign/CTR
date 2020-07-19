# -*- coding: utf-8 -*-

#OXapp. South basement walls (CMU+lintel)
# Verification on studs in anchorage angle profile to lintel
from __future__ import division
from __future__ import print_function

import math
from materials.aci import ACI_materials
from materials.aci import ACI_limit_state_checking

#units
in2m= 0.0254
m2in=1/in2m
feet2meter= 0.3048
kip2N= 4.4482216e3
ksi2MPa= 6.89476
lb2N=4.4482216
N2lb=1/lb2N

#    Data
## Applied factored external load (each stud)
Vua=1.6*3.2/2*kip2N
## Stud definition
stud= ACI_limit_state_checking.AnchorBolt(ca1= 5*in2m,ca2= 18*in2m,ha= 10*in2m, concrete= ACI_materials.c4000, steel= ACI_materials.A108, diam= 0.5*in2m, hef= 3.06*in2m, cast_in= False)
### where:
#### ca1: distance from the center of an anchor shaft to the edge of concrete in one direction. If shear is applied to anchor, ca1 is taken in the direction of the applied shear. If the tension is applied to the anchor, ca1 is the minimum edge distance.
### ca2: distance from center of an anchor shaft to the edge of concrete in the direction orthogonal to ca1.
### ha: thickness  of  member  in  which  an  anchor  is located, measured parallel to anchor axis.
### concrete: concrete material.
### steel: anchor steel.
### diam: anchor diameter.
### hef: effective embedment depth of anchor.
### cast_in: true if cast-in anchor false for post-installed anchors.

#Calculate the nominal strength of the anchor in shear  (art. D.6.1.)
Vsa=stud.getSteelStrengthShear()
#Concrete breakout failure in shear (art. D.6.2.)
Vcb=stud.getConcrBreakoutStrengthShear()
#Concrete pryout strength of anchor in shear (article D.6.3.)
Vcp=stud.getPryoutStrengthShear()
#Pullout stregth of stud to check head of the stud (article D.5.3)
Abearing=0.589*(in2m)**2
Npn=stud.getPulloutStrengthTension(Abearing)
#Check ductility
Vdd=stud.getStrengthDuctilityShear()
# Check design strength of stud in shear
Vnd=stud.getDesignStrengthShear(ductility=True,loadCombAlt=True)
if Vnd >= Vua:
    print ('Vnd >= Vua -> design strength checking OK')
else:
    print ('Vnd < Vua -> change stud dimensions') 
