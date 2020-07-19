# -*- coding: utf-8 -*-

#OXapp. South basement walls (CMU+lintel)
# Verification of weld between the two L profiles
from __future__ import division
from __future__ import print_function

from materials.eae import EAE_limit_state_checking
import math

in2m= 0.0254
m2in=1/in2m
feet2meter= 0.3048
kip2N= 4.4482216e3

Lw_paral=2*in2m #weld length parallel to shear
Lw_perp=5*in2m #weld length perpendicular to shear
throat=0.25*in2m  #throat width

A_weld=(2*Lw_paral+Lw_perp)*throat

Vd=1.6*3.2*kip2N
tao=Vd/A_weld

# * Weld perpendicular to shear:
tn= tao # Tangential stress normal to weld axis.
ta= 0 # Tangential stress parallel to weld axis.
n= 0 # Normal stress.
# ** equivalent stress.
sigmaCo= EAE_limit_state_checking.getFilletWeldYieldCriteriaLHS(n,tn,ta)
sigmaUlt= EAE_limit_state_checking.getFilletWeldYieldCriteriaRHSValue(430e6,275e6,1.25)
fcCond1= EAE_limit_state_checking.getFilletWeldCondition1CapacityFactor(n,tn,ta,430e6,275e6,1.25)
sigmaNUlt= EAE_limit_state_checking.getFilletWeldUltimateNormalStress(430e6,1.25)
fcCond2= EAE_limit_state_checking.getFilletWeldCondition2CapacityFactor(n,tn,430e6,1.25)
print ('fcCond1= ', fcCond1, '   fcCond2= ', fcCond2)


# * Weld parallel to shear:
tn= 0 # Tangential stress normal to weld axis.
ta= tao # Tangential stress parallel to weld axis.
n= 0 # Normal stress.
# ** equivalent stress.
sigmaCo= EAE_limit_state_checking.getFilletWeldYieldCriteriaLHS(n,tn,ta)
sigmaUlt= EAE_limit_state_checking.getFilletWeldYieldCriteriaRHSValue(430e6,275e6,1.25)
fcCond1= EAE_limit_state_checking.getFilletWeldCondition1CapacityFactor(n,tn,ta,430e6,275e6,1.25)
sigmaNUlt= EAE_limit_state_checking.getFilletWeldUltimateNormalStress(430e6,1.25)
fcCond2= EAE_limit_state_checking.getFilletWeldCondition2CapacityFactor(n,tn,430e6,1.25)
print ('fcCond1= ', fcCond1, '   fcCond2= ', fcCond2)


