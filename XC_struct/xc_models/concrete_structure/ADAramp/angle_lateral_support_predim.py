# OXaoo - ADA ramp. Lateral support by means of an steel angle anchored to the 
# concrete wall


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
psf2Nsm=47.88   #pound per square feet to N per square meter
plf2Nlm=lb2N/ft2m   #pound per linear feet to N per linear meter
#Data
#steel profile
angleL=5*in2m   #angle side L5*5*3/8
angleTh=3/8*in2m   #angle thickness L5*5*3/8
angleW=12.3*plf2Nlm  #angle weight [N/m]
#angleIx=8.76*in2m**4 #moment of inertia [m4]
#angleSx=2.41*in2m**3 #elastic section modulus [m3]
#angleRx=1.55*in2m   # radius of gyration [m]
angleXbar=1.37*in2m  #distance from the outside face to the baricenter [m]
#Geometry
rampWidth=68*in2m
rampThickness=6*in2m
#Materials
concrete= ACI_materials.c4000
studSteel= ACI_materials.A108
#Loads
grav=9.81
rampSelfWeight=rampThickness*rampWidth/2*concrete.density()*grav #(N/m)
angleSelfWeight=angleW
deadLoad=20*psf2Nsm*rampWidth/2
liveLoad=100*psf2Nsm*rampWidth/2
snowLoad=42*psf2Nsm*rampWidth/2

#Combination
combLoad=1.2*(rampSelfWeight+deadLoad)+1.6*liveLoad+0.5*snowLoad #[N/m]

#End data

#Verification of the capacity of the flange section.
Md=combLoad*(angleL-angleXbar)  #[m.N/m]

Vd=combLoad+angleW  #[N/m]

sigmBend=6*Md/(angleTh**2)  #maximum stress due to the bending moment [N/m2]
print('maximum stress due to bending moment =', sigmBend*1e-6, ' MPa')

tao=Vd/angleTh   # shear stress [N/m2]
print('maximum shear stress =', tao*1e-6, ' MPa')

#
stud= ACI_limit_state_checking.AnchorBolt(ca1= 24*in2m,ca2= 24*in2m,ha= 10*in2m, concrete= ACI_materials.c4000, steel= ACI_materials.A108, diam= 0.625*in2m, hef= 3.0*in2m, cast_in= False)
nStuds=1 # number of studs per meter
Vua=Vd/nStuds

#Calculate the nominal strength of the anchor in shear
Vsa=stud.getSteelStrengthShear()
Vsa_kips=Vsa/kip2N
print("Check nominal strength of the anchor in shear:")
if Vsa > Vua:
    print('Vsa= > Vua -> Ok!')
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
