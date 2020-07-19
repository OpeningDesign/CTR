# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import math
import os
import csv
import xc_base
import geom
import xc
from postprocess import limit_state_data as lsd
from materials.aci import ACI_materials
from materials.aci import ACI_limit_state_checking

concrete= ACI_materials.c4000
concrete.gmmC= 1.0
reinfSteel= ACI_materials.A615G60

# Estimation of beam loads on walls from beam loads
# on columns.
csvFile= open('f_columns_reactions.csv')
reader= csv.reader(csvFile)
loadsOnWall= dict()
for row in reader:
    id= row[0]
    if id not in loadsOnWall:
        loadsOnWall[id]= dict()
    loadCaseName= row[2]
    if(loadCaseName.startswith('ULS')):
        load= xc.Vector([-0.5*float(row[3]),-0.5*float(row[4]),-0.5*float(row[5]),-0.5*float(row[6]),-0.5*float(row[7]),-0.5*float(row[8])])
        loadsOnWall[id][loadCaseName]= load

phi= 0.75 #Shear controlled failure
alphaAngle= math.radians(70.0)
betaAngle= math.pi/2.0-alphaAngle
nu= 1.4
entrega= 5.5*0.0254
potentialCrackLength= entrega/math.tan(betaAngle)
print('alphaAngle= ',math.degrees(alphaAngle))
print('betaAngle= ',math.degrees(betaAngle))
print('potentialCrackLength= ',potentialCrackLength, ' m', potentialCrackLength/0.0254, ' in')
Amax= 0.0 #Area of reinforcement.
Vdmax= 0.0 # Maximum shear-transfer
for beamKey in loadsOnWall:
    loadsFromBeam= loadsOnWall[beamKey]
    for loadCaseKey in loadsFromBeam:
        beamReaction= loadsFromBeam[loadCaseKey]
        verticalReaction= beamReaction[2]
        horizReaction= beamReaction[0]
        horizReaction= max(-0.35*verticalReaction,horizReaction)
        # verticalReaction*=0.1 Full dead load + live load governs
        Vd= horizReaction*math.cos(alphaAngle)-verticalReaction*math.sin(alphaAngle)
        Nd= horizReaction*math.sin(alphaAngle)+verticalReaction*math.cos(alphaAngle)
        # Shear friction reinforcement.
        Avf= Vd/(phi*reinfSteel.fyk*(nu*math.sin(alphaAngle)+math.cos(alphaAngle)))
        # Tension reinforcement.
        An= max(Nd,0.0)/(phi*reinfSteel.fyk*math.sin(alphaAngle))
        Amax= max(Amax,Avf+An)
        Vdmax= max(Vdmax,Vd)
        #print('beam: ', beamKey, ' load case: ', loadCaseKey, 'T= ', horizReaction/1000,' kN, R= ', verticalReaction/1000,' kN, Vd= ', Vd/1000,' kN, Nd= ', Nd/1000,' kN', Avf*1e4, ' cm2', An*1e4, ' cm2')

Ac= 2*0.3048*entrega/math.sin(betaAngle)
Vu= ACI_limit_state_checking.getMaximumShearTransferStrength(concrete,Ac)
        
tieRebarArea= ACI_materials.standard_bars_areas['#4']
tieArea= 2.0*tieRebarArea # Two legs
numberOfTies= math.ceil(Amax/tieArea)
tieSpacement= potentialCrackLength/numberOfTies
print('Amax= ',Amax*1e4, ' cm2')
print('number of ties: ',numberOfTies)
print('tie spacement: ', tieSpacement*1e2, ' cm (', tieSpacement/0.0254, 'in)')
print('Vdmax= ',Vdmax/1e3, ' kN')
print('Vu= ',Vu/1e3, ' kN')

