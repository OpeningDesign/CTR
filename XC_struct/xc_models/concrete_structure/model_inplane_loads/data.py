# -*- coding: utf-8 -*-

#Coordinates
xEW=0
xGridA=5.94
xRamp_1=7.57
xRamp_2=13.57
xStair1=16.5
xWW=55.6

yNW=0
yRamp_1=2
yStair1=8.4
yRamp_2=15.7
yStair2_1=30.2
yStair2_2=32.9
ySW=47.5

#material
slabTh=0.15


xList=[xEW,xGridA,xRamp_1,xRamp_2,xStair1,xWW]
yList=[yNW,yRamp_1,yStair1,yRamp_2,yStair2_1,yStair2_2,ySW]
zList=[0]

disp=0.5 #ficticious displacement
#Shear walls Y direction: [[x,[y1,y2]],in_plan_load] (Klb/ft)
WLS1_a=[[10.2,[35.2,43.6]],1.16]
WLS1_b=[[42.2,[35.2,43.6]],1.16]
WL4=[[44.1,[0+disp,8.3+disp]],0.84]
WLN1B=[[31.5,[0+disp,8.5+disp]],1.16]
WLN1C=[[24.1,[0+disp,8.5+disp]],1.16]
WLN1D=[[xRamp_1-disp,[0+disp,15.7+disp]],1.16]

ShearYwalls=[WLS1_a,WLS1_b,WL4,WLN1B,WLN1C,WLN1D]

#Shear walls X direction: [[[x1,x2],y],in_plan_load] (Klb/ft)
WLE1A=[[[0+disp,7.6-disp],9],1.31*7.6/(7.6-2*disp)]
WLE1B=[[[0+disp,9.2+disp],22.4],0.06]
WL15=[[[0+disp,9.2+disp],32.9+disp],0.99]
WLEC1A=[[[7.5,13.7],15.5+disp],1.11]
WLEC1B=[[[11.2,20.2],23.2],0.09]
WLEC1C=[[[11.2,20.2],33.2],1.15]
WLW1A=[[[43.4,52.4],12.2],0.1]
WLW1B=[[[43.4,52.4],22.4],0.01]
WLW1C=[[[43.4,52.4],33.2],0.11]

WLWC1A=[[[32.2,41.4],15.6],0.59]
WLWC1B=[[[32.2,41.4],22.9],0.09]
WLWC1C=[[[32.2,41.4],33.2],1.15]

ShearXwalls=[WLE1A,WLE1B,WL15,WLEC1A,WLEC1B,WLEC1C,WLW1A,WLW1B,WLW1C,WLWC1A,WLWC1B,WLWC1C]

