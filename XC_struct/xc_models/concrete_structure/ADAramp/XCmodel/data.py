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
spcAnch=2*ft2m #spacing between anchorages
#steel profile
angleTh=3/8*in2m        #angle thickness L5x3-1/2x3/8
#angleTh=1/2*in2m        #angle thicknessL5x3-1/2x1/2
angleHeight=3.5*in2m    #height of the L profile (in contact with wall)
angleWidth=5*in2m       #width of the L profile (supporting the slab)
zAnchor=(angleHeight-angleTh/2)-1.5*in2m  #z coordinate of the anchor

#Geometry
rampWidth=4*ft2m+6*in2m
rampThickness=6*in2m
#Materials
concrete= ACI_materials.c4000
studSteel= ACI_materials.A108
#Loads
angleW=12.3*plf2Nlm  #angle weight [N/m]
grav=9.81
rampSelfWeight=rampThickness*rampWidth/2*concrete.density()*grav #(N/m)
angleSelfWeight=angleW
deadLoad=20*psf2Nsm*rampWidth/2
liveLoad=100*psf2Nsm*rampWidth/2
snowLoad=42*psf2Nsm*rampWidth/2

#Combination
combLoad=1.2*(rampSelfWeight+deadLoad)+1.6*liveLoad+0.5*snowLoad #[N/m]
# for live load, because the critical situation is when concrete is not cured
# we suppose snow can be cummulated
eSize=angleHeight/3
#End data


