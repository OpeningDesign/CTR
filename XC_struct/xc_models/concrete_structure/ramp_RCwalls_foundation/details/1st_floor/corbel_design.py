# -*- coding: utf-8 -*-

''' Verification test based on the EXAMPLE ACI 318-14 RC-BM-001 of
the program SAFE form Computers and Structures Inc.'''

 
from __future__ import division
from __future__ import print_function
from materials.aci import ACI_materials
from materials.aci import ACI_limit_state_checking as lsc
import os
from misc_utils import log_messages as lmsg

__author__= "Luis Claudio Pérez Tato (LCPT"
__copyright__= "Copyright 2019, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

concrete= ACI_materials.c4000
concrete.gammaC= 1.0
reinfSteel= ACI_materials.A615G60
reinfSteel.gammaS= 1.0

corbel= lsc.Corbel(concrete, reinfSteel, width= 1.0, thickness= 0.2, depth= 0.15, Asc= 1e-4, Ah= 1e-4)

Vd= 87.86e3
Nd= 0.2*Vd
av= 0.10

Vn_cap= corbel.getNominalVerticalLoadCapacity()
CF_v= corbel.getShearCapacityFactor(Vd)
Asc= corbel.getRequiredPrimaryReinforcement(Vd,Nd,av)
Asc_min= corbel.getMinimumPrimaryReinforcement(Vd,Nd,av)
Ah_min= corbel.getMinimumShearReinforcement(Vd,Nd,av)

print('Vn_cap= ', Vn_cap/1e3, 'kN')
print('CF_v= ', CF_v)
print('Asc= ', Asc*1e6,' mm2')
print('Asc_min= ', Asc_min*1e6,' mm2')
print('Ah_min= ', Ah_min*1e6,' mm2')
