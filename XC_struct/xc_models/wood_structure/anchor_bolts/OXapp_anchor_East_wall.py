# -*- coding: utf-8 -*-
# Verification test according to ACI 349.2 R-07.
# Guide to the Concrete Capacity Design (CCD) Method—Embedment Design Examples
# OXapp East wall. Single stud, shear only

from __future__ import division
from __future__ import print_function

import math
from materials.aci import ACI_materials
from materials.aci import ACI_limit_state_checking
in2m= 0.0254
m2in=1/in2m
feet2meter= 0.3048
kip2N= 4.4482216e3
ksi2MPa= 6.89476
lb2N=4.4482216
N2lb=1/lb2N

# Data
Vua=1.6*5.3*kip2N  #applied factored external load using load factors from Appendix C of the Code.
stud= ACI_limit_state_checking.AnchorBolt(ca1= 8*in2m,ca2= 18*in2m,ha= 14*in2m, concrete= ACI_materials.c4000, steel= ACI_materials.A108, diam= 0.625*in2m, hef= 4.0*in2m, cast_in= False)

#Calculate the nominal strength of the anchor in shear
Vsa=stud.getSteelStrengthShear()
Vsa_kips=Vsa/kip2N
print("Check nominal strength of the anchor in shear:")
if Vsa > Vua:
    print('Vsa > Vua -> Ok!')
else:
    print('Vsa < Vua -> Change dimensions')

#Check concrete breakout failure in shear
Vcb=stud.getConcrBreakoutStrengthShear()
Vcb_kips=Vcb/kip2N

print("Check concrete breakout failure in shear:")
if Vcb > Vsa:
    print('Vcb > Vsa -> Ok!')
else:
    print('Vcb < Vsa -> Change dimensions')

#Check concrete pryout strength of anchor in shear
Vcp=stud.getPryoutStrengthShear()
Vcp_kips=Vcp/kip2N

print("Check concrete pryout strength of anchor in shear:")
if Vcp > Vsa:
    print('Vcp > Vsa -> Ok!')
else:
    print('Vcp < Vsa -> Change dimensions')

#Check pullout stregth of stud to check head of the stud
Abearing=0.67*(in2m)**2
Npn=stud.getPulloutStrengthTension(Abearing)
Npn_kips=Npn/kip2N
if 0.85*Npn > Vsa:
    print('0.85*Npn > Vsa -> Ok!')
else:
    print('0.85*Npn < Vsa -> Change dimensions')
