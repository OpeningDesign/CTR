ft2m=0.3048
in2m=0.0254
# Supporting walls, dimensions Y direction
dimW0_W1=4.14
dimW1_W2=3.5
dimW2_W3=3.5
dimW3_Slab=4.2

#dimensions X direction
ramp_width=5.9

rampTh=0.15

L_ramp=dimW0_W1+dimW1_W2+dimW2_W3+dimW3_Slab

Lslope8=8*ft2m
Lslope15=L_ramp-2*Lslope8

ySlopeChange=[Lslope8,L_ramp-Lslope8]

yWalls=[dimW0_W1]
yWalls.append(yWalls[-1]+dimW1_W2)
yWalls.append(yWalls[-1]+dimW2_W3)

foundWidth=3*ft2m
foundHigh=1*ft2m+2*in2m

H_slab_cim=foundHigh/2.0+(14*12-12*12-8)*in2m

H_ramp=2*Lslope8*0.08+Lslope15*0.15

yCim=list()
for w in yWalls:
    yCim.append(w-foundWidth/2.)
    yCim.append(w+foundWidth/2.)


# coordinates in global X,Y,Z axes for the grid generation

xList=[0,ramp_width]

yListaux=[0]+ySlopeChange+yWalls+yCim+[L_ramp]
yList=[]
for i in yListaux:
    if i not in yList:
        yList.append(i)
yList.sort()

zList=[-H_slab_cim,H_ramp]

#auxiliary data
lastXpos=len(xList)-1
lastYpos=len(yList)-1
lastZpos=len(zList)-1

unifLoad=1915  # live load (uniform) [Pa]
concLoad=13340 #concentrated load [N]


'''
#unif. live load rooms[Pa]
unifLLrooms=1915
#unif. live load terrace [Pa] pedestrian
unifLLterrace=4788

#snow load [Pa]
unifSL=2873

'''

H_wall1=H_slab_cim+H_ramp-0.08*Lslope8-0.15*(4.14-Lslope8)
H_wall2=H_wall1-3.5*0.15
H_wall3=H_wall2-3.5*0.15
