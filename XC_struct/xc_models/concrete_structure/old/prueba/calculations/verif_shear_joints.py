# -*- coding: utf-8 -*-
from __future__ import division
''' Verification test for the concrete shrinkage computation
   according to EHE-08. '''

import math
import xc_base
import geom
import xc
from materials.ehe import EHE_materials as EHEmat
from materials.ehe import EHE_limit_state_checking as EHEverif

'''
Verification of ultimate limit state due to longitudinal shear stress 
at joints between concretes according to art. 47 EHE.

Results are compared with those obtained in "Cálculo civil" app  
'''
ft2m=0.3048
in2m=0.0254

#Data
concrtype=EHEmat.HA25  #weakest EHE concrete type at joint
steelType=EHEmat.B500S  #reinforcing steel type
widthContact=0.35      #width in contact (parallel to Vd) [m]
unitAreaContact=widthContact #contact area per unit length
Vd=7e3                #Shear force [N/m]
Nd=1                  #Axial force (perpendicular to the plane of joint) [N/m]
                       #compression: Nd<0 
fiRebar=12             #diameter rebar [mm]
roughness='L'          #roughness of surface ('L'=low, 'H'=high)
dynamic='N'            #no low fatigue or dynamic stresses consideration
Ast=math.pi*(fiRebar*1e-3)**2/4
spacement=24*in2m         #rebars spacement [m]
angRebars=90           #Angle formed by the joining bars with the plane of the
                       #joint (degrees)

#End data

tao_rd=Vd/widthContact #design longitudinal shear stress at joint [N/m2]

areaContact=widthContact*1
sigma_cd=Nd/areaContact #External design tensile stress perpendicular to the
                        #plane of the joint [N/m]

shJoint=EHEverif.LongShearJoints(concrtype,steelType,unitAreaContact,roughness,dynamic,sigma_cd,Ast,spacement,angRebars)

beta=shJoint.getBetaCoef()

f_ctd=concrtype.fctd()   #[N/m2]

tao_u=shJoint.getUltShearStressWithReinf(tao_rd)

print 'tao_rd=',tao_rd*1e-6, ' MPa'
print 'tao_u=',tao_u*1e-6, ' MPa'
