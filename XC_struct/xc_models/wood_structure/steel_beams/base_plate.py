# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

#Units
foot2m= 0.3048
inch2m= 0.0254

side= 2*6.5*0.0254
area= side**2

Vd= 211.165823593e3 # 211 kN
Rd= Vd

sigma_c= Rd/area

print('area A= '+str(area)+' m2')
print('sigma_c= '+str(sigma_c/1e6)+' MPa')
