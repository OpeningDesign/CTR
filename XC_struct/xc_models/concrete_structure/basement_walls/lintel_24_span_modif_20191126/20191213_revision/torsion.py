import xc_base
import geom
import xc
from materials.ehe import EHE_materials
import math

fi_n_2=6.35e-3
area_n_2=math.pi*fi_n_2**2/4.
area_n_3=71e-6
area_n_4=129e-6
area_n_5=200e-6
area_n_6=284e-6
area_n_7=387e-6
area_n_8=509e-6



Td=66e3 #N.m  20.3 kN/m * 0.889 m * 7.315 /2  

hBeam=0.889   #35"
wBeam=0.254

A=hBeam*wBeam
u=2*(hBeam+wBeam)
c=0.03

he=max(A/u,2*c)   #ffective thickness

#Obtaining Tu1
concrete=EHE_materials.HA30
reinfSteel=EHE_materials.B500S

f1cd=0.6*abs(concrete.fcd())
K=1  #non pre-stressed structure
alpha=0.6 #stirrups only along the external circumference of the member
cotgTheta=1.0  # Theta=Angle between the concrete’s compression struts and the member’s axis.
Ae=(hBeam-he)*(wBeam-he)

Tu1=2*K*alpha*f1cd*Ae*he*(cotgTheta/(1+cotgTheta**2))

if Td <= Tu1:
    print "Td <= Tu1 -> Ok!"
else:
    print "Td > Tu1"

#Obtaining Tu2
#At=area_n_2
At=area_n_3  #Area of the reinforcements used as hoops or transverse reinforcement.
st=0.2032 #Longitudinal spacing between hoops or bars in the transverse reinforcement (8")

fytd=reinfSteel.fyd()

Tu2=2*Ae*At/st*fytd*cotgTheta

if Td <= Tu2:
    print "Td <= Tu2 -> Ok!"
else:
    print "Td > Tu2"

#Obtaining Tu3

A1=3*area_n_5+4*area_n_4+3*area_n_7
fy1d=reinfSteel.fyd()
ue=2*((hBeam-he)+(wBeam-he))

Tu3=2*Ae/ue*A1*fy1d*1/cotgTheta

if Td <= Tu3:
    print "Td <= Tu3 -> Ok!"
else:
    print "Td > Tu3"


