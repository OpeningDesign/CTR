ft2m=0.3048
in2m=0.0254
# Columns, dimensions X direction
dimWA=20*ft2m+2*in2m
dimAB=26*ft2m
dimBC=23*ft2m
dimCD=35*ft2m
dimDG=31*ft2m
dimGF=25*ft2m
dimFW=23*ft2m+2*in2m

#Columns, dimensions Y direction
dimW1=8.890
dim12=8.306
dim23=8.306
dim34=8.306
dim45=8.306
dim5W=6.096

xCols=[dimWA]
xCols.append(xCols[-1]+dimAB)
xCols.append(xCols[-1]+dimBC)
xCols.append(xCols[-1]+dimCD)
xCols.append(xCols[-1]+dimDG)
xCols.append(xCols[-1]+dimGF)

yCols=[dimW1]
yCols.append(yCols[-1]+dim12)
yCols.append(yCols[-1]+dim23)
yCols.append(yCols[-1]+dim34)
yCols.append(yCols[-1]+dim45)

xWalls=[0,xCols[-1]+dimFW]
yWalls=[0,yCols[-1]+dim5W]

xRamp=[7.828]
yRamp=[16.02]
yStair1=[30.373,33.183]

xStair2Elev=[16.66]
yStair2Elev=[8.875]

#Facades
xFac=[0,xCols[2],xCols[3],53.52]
yFac=[0,10.975,44.77]   

#Wall frames
xWF=[0,xCols[0],xCols[0]+3.5,10.2,10.2+1.6/2.,xCols[1],xCols[2],xCols[3],xFac[-1]-10.2-0.8,xFac[-1]-10.2,xFac[-1]-9.6,xFac[-1]-10.2+4.2,xFac[-1]]


yWF=[0,yCols[0],yCols[0]+2,yCols[3]-4.5,yCols[3],yFac[-1]]


gap=0.2

xGaps=[]
for i in xCols:
    xGaps.append(i-gap/2.)
    xGaps.append(i+gap/2.)
yGaps=[]
for i in yCols:
    yGaps.append(i-gap/2.)
    yGaps.append(i+gap/2.)

#Beam section
beamWidth=0.609
beamHeight=0.787

#Column section
colXdim=16*in2m
colYdim=16*in2m

#!!!!! Modify according to problem!!!
hHollowCore=12*in2m
H1stFloor=10*ft2m+8*in2m
deltaFloors=1*ft2m+2*in2m
Hfound=3*ft2m+18*in2m
zCol=Hfound+H1stFloor
zBeamHigh=zCol-hHollowCore/2.
#zBeamLow=zBeamHigh-deltaFloors
zHlwHigh=zCol+hHollowCore/2.
zHlwLow=zHlwHigh-deltaFloors

# coordinates in global X,Y,Z axes for the grid generation
xListaux=xCols+xWalls+xRamp+xStair2Elev+xFac+xWF+xGaps+xWalls
xList=[]
for i in xListaux:
    if i not in xList:
        xList.append(i)
xList.sort()
yListaux=yCols+yWalls+yRamp+yStair1+yStair2Elev+yFac+yWF+yGaps
yList=[]
for i in yListaux:
    if i not in yList:
        yList.append(i)
yList.sort()

zList=[0,zBeamHigh,zHlwLow,zCol,zHlwHigh]
zList.sort()
#auxiliary data
lastXpos=len(xList)-1
lastYpos=len(yList)-1
lastZpos=len(zList)-1



# precast slabs
slabTh=0.15


#Weight hollowcore deck 30+5 [Pa]
import math
Width_hollo=1.219
Area_hollo=Width_hollo*0.3048-4*math.pi*0.236**2/4.
Whollowdeck=5.19e3
W_hollo=25e3*Area_hollo
W_compress=25e3*Width_hollo*0.05      #compression layer
Whollowdeck=(W_hollo+W_compress)/Width_hollo
'''
#Dead load facades [N/ml]
DLfac=7352+2035+4876
#Dead load interior wall frames [N/ml]
DLwf=4070+9746

#Live load facades [N/ml]
LLfac=5269+21065
#Live load interior wall frames [N/ml]
LLwf=10538+42130

#Snow load facades [N/ml]
SLfac=15801
#Snow load interior wall frames [N/ml]
SLwf=31603
'''


#unif. live load rooms[Pa]
unifLLrooms=1915
#unif. live load terrace [Pa] pedestrian
unifLLterrace=4788

#snow load [Pa]
unifSL=2873

#Linear loads from wood frames bearing on 1st floor
#D: dead load (N)
#L: live load (N)
#S: snow load (N)

D_lnL1=22.1e3
L_lnL1=48840
S_lnL1=29300

D_lnL2=12.12e3
L_lnL2=10770
S_lnL2=6460

D_lnL3=16.33e3
L_lnL3=26810
S_lnL3=16090

D_lnL4=15.32e3
L_lnL4=22980
S_lnL4=13790

D_lnL5=10.55e3
L_lnL5=4790
S_lnL5=2870

D_lnL6=16.14e3
L_lnL6=26090
S_lnL6=15660

D_lnL7=23.05e3
L_lnL7=24420
S_lnL7=14650

D_lnL8=7.35e3

D_lnL9=25.31e3
L_lnL9=33040
S_lnL9=19820

D_lnL10=22.23e3
L_lnL10=21310
S_lnL10=12780

D_lnL11=7.35e3

D_lnL12=22.67e3
L_lnL12=22980
S_lnL12=13790

D_lnL13=23.05e3
L_lnL13=24420
S_lnL13=14650

#Wind W-E (Z direction)
WWE_lnL1W=5.8e3
WWE_lnL2W=27.1e3
WWE_lnL3W=-23.5e3
WWE_lnL4W=34.85e3
WWE_lnL5W=-15.73e3
#Wind N-S (Z direction)
WNS_lnL1W=5.8e3
WNS_lnL6W=18.74e3
WNS_lnL7W=-17.5e3
