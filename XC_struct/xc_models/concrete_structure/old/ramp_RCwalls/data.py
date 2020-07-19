# -*- coding: utf-8 -*-

ft2m=0.3048
in2m=0.0254

#Geometry
wallThBasement=round(10*in2m,2)
wallThFirstFloor=round(8*in2m,2)
wallLength=round((8+58+8)*ft2m+19.5*in2m,2)
Laux=round((wallLength-(13+2*14)*ft2m-(3+2*8+2*4)*in2m)/2.,2)
LwallBasement=wallLength
LwallFirstFloor=round(wallLength-Laux,2)

yHall=round(5.5*ft2m,2)
xHall=round(-5.0*ft2m,2)
distXwalls=19*ft2m

yCantilv=round(-(2.0*ft2m+11*in2m),2)
foundElev=round(-14*ft2m,2)
rampStartElev=round(-(2*ft2m+6*in2m),2)
rampEndElev=round(-(12*ft2m+8*in2m),2)
firstFloorElev=0
secondFloorElev=round(11*ft2m+4*in2m,2)

eSize= 0.35     #length of elements

xEastWall=0
xWestWall=distXwalls
#Materials
from materials.aci import ACI_materials as ACImat
concrete=ACImat.c4000
reinfSteel=ACImat.A615G60
from materials.astm_aisc import ASTM_materials as ASTMmat
strSteel=ASTMmat.A36
strSteel.gammaM= 1.00
# coordinates in global X,Y,Z axes for the grid generation

xList=[xHall,xEastWall,xWestWall]
xList.sort()

yDeck=round(LwallFirstFloor/2.,2)
yList=[yCantilv,0,yHall,yDeck,LwallFirstFloor,LwallBasement]
yList.sort()

zList=[foundElev,firstFloorElev,secondFloorElev]
zList.sort()

#Loads
# earth pressure
firad=math.radians(30)  #internal friction angle (radians)
KearthPress=1-math.sin(firad)
densSoil=1000       #mass density of the soil (kg/m3)
Earth_E1F=20e3   #horizontal force [N/m] due to earth pressure over East wall 

Dead_WE2F=(31.71+4.91)*1e3  #dead load West & East walls 2 floor [N/m]
Live_WE2F=(24.71+8.32)*1e3
Snow_WE2F=13.38*1e3
Wind_WE2F=-8.46*1e3  #vertical
WindH_E2F=1.7*1e3  #horizontal

Dead_E1F=42.85*1e3  #dead load East wall 1 floor [N/m]
Live_E1F=10.77*1e3
Snow_E1F=-0.08*1e3
Wind_E1F=-0.5*1e3

Dead_stbeam=7.35e3  #dead load steel beam North facade [N/m]
Live_stbeam=2*2.33e3
Snow_stbeam=1.75e3

Dead_Wcant=30.78e3  #dead load steel cantilever (West side)
Live_Wcant=23.78e3
Snow_Wcant=10.35e3

Dead_Ccant=44.65e3  #dead load steel cantilever (Central)
Live_Ccant=39.04e3
Snow_Ccant=15.49e3

ratio=(xEastWall-xHall)/(xWestWall-xEastWall)

Dead_Ecant=ratio*Dead_Wcant  #dead load steel cantilever (East side)
Live_Ecant=ratio*Live_Wcant  
Snow_Ecant=ratio*Snow_Wcant  

