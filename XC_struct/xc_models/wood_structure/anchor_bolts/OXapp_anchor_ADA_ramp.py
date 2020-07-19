# -*- coding: utf-8 -*-
# Verification test according to ACI 349.2 R-07.
# Guide to the Concrete Capacity Design (CCD) Method—Embedment Design Examples
# Example A3. Single stud, combined tension and shear.

from __future__ import division
from __future__ import print_function

import math
from materials.aci import ACI_materials
from materials.aci import ACI_limit_state_checking
in2m= 0.0254
m2in=1/in2m
ft2m= 0.3048
kip2N= 4.4482216e3
ksi2MPa= 6.89476
lb2N=4.4482216
N2lb=1/lb2N
N2kip=1/kip2N

# Data
Nua=17673  #applied factored external tension load using load factors from Appendix C of the Code. [N]
Vua=7269  #applied factored external shear load using load factors from Appendix C of the Code.[N]
stud= ACI_limit_state_checking.AnchorBolt(ca1=12*in2m,ca2=20*in2m,ha= 14*in2m, concrete= ACI_materials.c4000, steel= ACI_materials.A108, diam= 5/8*in2m, hef= 6.36*in2m, cast_in= True)

#Calculate the nominal strength of the anchor in tension (art. D.5.1)
Nsa=stud.getNominalSteelStrengthTension()
Nsa_kips=Nsa/kip2N

#Concrete breakout failure in tension (art. D.5.2.)
Nb= stud.getBasicConcreteBreakoutStrengthTension() # Basic concrete breakout strength
Nb_kips=Nb*N2kip
Ncb=stud.getConcrBreakoutStrengthTension()
Ncb_kips=Ncb*N2kip

#Pullout stregth of stud to check head of the stud (article D.5.3)
Abearing=0.92*(in2m)**2
Npn=stud.getPulloutStrengthTension(Abearing)
Npn_kips=Npn/kip2N

#Check ductility in tension
Ndd=stud.getStrengthDuctilityTension(Abearing,cracking=True)
Ndd_kips=Ndd/kip2N

'''
if Ndd >= Nua:
    print ('Ndd >= Nua -> ductility OK')
else:
    print ('Ndd < Nua -> NO ductility') 
'''
#Check design strength of stud in tension
Nnd=stud.getDesignStrengthTension(Abearing,ductility=True,loadCombAlt=False)
Nnd_kips=Nnd/kip2N
'''
if Nnd >= Nua:
    print ('Nnd >= Nua -> OK')
else:
    print ('Nnd < Nua -> change dimensions') 
'''


#SHEAR
#Calculate the nominal strength of the anchor in shear
Vsa=stud.getSteelStrengthShear()
Vsa_kips=Vsa/kip2N

#Concrete breakout failure in shear (art. D.6.2.)
Vcb=stud.getConcrBreakoutStrengthShear()
Vcb_kips=Vcb/kip2N
  
#Concrete pryout strength of anchor in shear (article D.6.3.)
Vcp=stud.getPryoutStrengthShear()
Vcp_kips=Vcp/kip2N
    
#Check ductility in shear
Vdd=stud.getStrengthDuctilityShear()
Vdd_kips=Vdd/kip2N

'''
if Vdd >= Vua:
    print ('Vdd >= Vua -> ductility OK')
else:
    print ('Vdd < Vua -> NO ductility') 
'''

# Check design strength of stud in shear
Vnd=stud.getDesignStrengthShear(ductility=True,loadCombAlt=False)
Vnd_kips=Vnd/kip2N

'''
if Vnd >= Vua:
    print ('Vnd >= Vua -> design strength checking OK')
else:
    print ('Vnd < Vua -> change stud dimensions') 
'''
#Art. D.7
'''
if Vua <= 0.2*Vnd:
    print ('Vua <= 0.2*Vnd -> full strength in tension is permitted')
if Nua <= 0.2*Nnd:
    print ('Nua <= 0.2*Nnd -> full strength in shear is permitted')
if Vua > 0.2*Vnd and Nua > 0.2*Nnd:
    if Nua/Nnd + Vua/Vnd <= 1.2:
        print ('Nua/Nnd + Vua/Vnd = ',round(Nua/Nnd + Vua/Vnd,2), ' <= 1.2')
'''
