# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

import math
from rough_calculations import ng_basement_wall
import xc_base
import geom
import xc
from materials.aci import ACI_materials
from materials.aci import ACI_limit_state_checking
from materials import typical_materials
from geotechnics import earth_pressure as ep
from geotechnics import frictional_cohesional_soil as fcs
from actions import load_cases
from actions import combinations
from actions.earth_pressure import earth_pressure

INCH_2_METER= 0.0254
FEET_2_METER= 0.3048
cover= 55e-3

#Materials
concrete= ACI_materials.c4000
reinfSteel= ACI_materials.A615G60
execfile("./armatures_type.py")

wallHead= -(0.0*FEET_2_METER+1.0*INCH_2_METER)
topOfFoundation= -(11.0*FEET_2_METER+8*INCH_2_METER)
stemBottomWidth= 10*INCH_2_METER
stemTopWidth= stemBottomWidth
footingThickness= 14*INCH_2_METER
sectionName= "T3"
wall= ng_basement_wall.BasementWall(sectionName,cover,stemBottomWidth,stemTopWidth,footingThickness,concrete,reinfSteel)
wall.stemHeight= wallHead-topOfFoundation
wall.bToe= 1.5*FEET_2_METER
wall.bHeel= 1.5*FEET_2_METER
wall.beton= concrete
wall.exigeanceFisuration= 'B'
wall.stemReinforcement.setReinforcement(1,D1619_15.getCopy(ACI_limit_state_checking.RebarController('B')))
wall.stemReinforcement.setReinforcement(2,A13_15.getCopy(ACI_limit_state_checking.RebarController('B')))
wall.footingReinforcement.setReinforcement(3,D1619_15.getCopy(ACI_limit_state_checking.RebarController('B')))
wall.stemReinforcement.setReinforcement(4,A10_15.getCopy(ACI_limit_state_checking.RebarController('B')))
wall.stemReinforcement.setReinforcement(5,A19_30.getCopy(ACI_limit_state_checking.RebarController('B')))
wall.stemReinforcement.setReinforcement(6,A13_15.getCopy(ACI_limit_state_checking.RebarController('B')))
wall.footingReinforcement.setReinforcement(7,A10_15.getCopy(ACI_limit_state_checking.RebarController('B')))
wall.footingReinforcement.setReinforcement(8,D1619_15.getCopy(ACI_limit_state_checking.RebarController('B')))
wall.stemReinforcement.setReinforcement(11,A13_15.getCopy(ACI_limit_state_checking.RebarController('B')))


wallFEModel= wall.createFEProblem('Basement wall '+sectionName)
preprocessor= wallFEModel.getPreprocessor
nodes= preprocessor.getNodeHandler

#Soil
kS= 200*4.44822/(0.0254)**3 #Subgrade modulus (geotechnical report).
#print('kS= ', kS/1e6)
kX= typical_materials.defElasticMaterial(preprocessor, "kX",kS/10.0)
kY= typical_materials.defElasticMaterial(preprocessor, "kY",kS)
#kY= typical_materials.defElastNoTensMaterial(preprocessor, "kY",kS)
soilDensity= 125*0.453592/(0.3048)**3
#print('soil density= ',soilDensity)
backFillSoilModel= ep.RankineSoil(phi= math.radians(30),rho= soilDensity) #Characteristic values.
#print('Ka= ', backFillSoilModel.K0Jaky())
backFillDelta= 0.0 #2.0/3.0*backFillSoilModel.phi
foundationSoilModel= fcs.FrictionalCohesionalSoil(phi= math.radians(30), c= 0.0, rho= soilDensity)
sg_adm= 3000.0*47.880208 # Geothecnical exploration page 5

#Mesh.
wall.genMesh(nodes,[kX,kY])

#Sets.
totalSet= preprocessor.getSets.getSet("total")


#Actions.
loadCaseManager= load_cases.LoadCaseManager(preprocessor)
loadCaseNames= ['selfWeight','deadLoad','trafficLoad','liveLoad','snowLoad','windLoad','quakeLoad']
loadCaseManager.defineSimpleLoadCases(loadCaseNames)

#Self weight.
selfWeight= loadCaseManager.setCurrentLoadCase('selfWeight')
gravity=9.81 #Acceleration of gravity (m/s2)
wall.createSelfWeightLoads(rho= 2500,grav= gravity)

# Dead load.
# Dead load. Earth self weight.
gSoil= backFillSoilModel.rho*gravity
frontFillDepth= 1.0
deadLoad= loadCaseManager.setCurrentLoadCase('deadLoad')
wall.createDeadLoad(heelFillDepth= wall.stemHeight,toeFillDepth= frontFillDepth,rho= backFillSoilModel.rho, grav= gravity)

# Dead load. Earth pressure.
K0= backFillSoilModel.K0Jaky()
zGroundBackFill= 0.0 #Back fill
backFillPressureModel=  earth_pressure.EarthPressureModel( zGround= zGroundBackFill, zBottomSoils=[-10],KSoils= [K0],gammaSoils= [gSoil], zWater= -1e3, gammaWater= 1000*gravity)
wall.createBackFillPressures(backFillPressureModel, Delta= backFillDelta)
zGroundFrontFill= zGroundBackFill-wall.stemHeight+frontFillDepth #Front fill
frontFillPressureModel=  earth_pressure.EarthPressureModel(zGround= zGroundFrontFill, zBottomSoils=[-10],KSoils= [K0], gammaSoils= [gSoil], zWater= -1e3, gammaWater= 1000*gravity)
wall.createFrontFillPressures(frontFillPressureModel)

# Dead load from building.
buildingDeadLoad= 31.54e3 #North
print('buildingDeadLoad= ', buildingDeadLoad/1e3, ' kN/m')
wall.createLoadOnTopOfStem(xc.Vector([0.0,-buildingDeadLoad,0.0]))

#Live load. Traffic load.
trafficLoad= loadCaseManager.setCurrentLoadCase('trafficLoad')
trafficEarthPressure= earth_pressure.StripLoadOnBackfill(qLoad= 11.97e3,zLoad= 0.0, distWall= 1.0, stripWidth= 10)
wall.createPressuresFromLoadOnBackFill(trafficEarthPressure, Delta= backFillDelta)

# Live load from the building.
liveLoad= loadCaseManager.setCurrentLoadCase('liveLoad')
buildingLiveLoad= 21.67e3 #North
print('buildingLiveLoad= ', buildingLiveLoad/1e3, ' kN/m')
wall.createLoadOnTopOfStem(xc.Vector([0.0,-buildingLiveLoad,0.0]))

# Snow load from the building.
snowLoad= loadCaseManager.setCurrentLoadCase('snowLoad')
buildingSnowLoad= 10.06e3 #North
print('buildingSnowLoad= ', buildingSnowLoad/1e3, ' kN/m')
wall.createLoadOnTopOfStem(xc.Vector([0.0,-buildingSnowLoad,0.0]))

# Wind load from the building.
windLoad= loadCaseManager.setCurrentLoadCase('windLoad')
buildingWindLoad= 15.12e3 #North
print('buildingWindLoad= ', buildingWindLoad/1e3, ' kN/m')
wall.createLoadOnTopOfStem(xc.Vector([0.0,-buildingWindLoad,0.0]))

# Accidental actions. Quake
quakeLoad= loadCaseManager.setCurrentLoadCase('quakeLoad')
kh=  0.03
kv=  0.7*kh
Aq= wall.getMononobeOkabeDryOverpressure(backFillSoilModel,kv,kh)
#print('Aq= ',Aq)
quakeEarthPressure= earth_pressure.UniformLoadOnStem(Aq)
wall.createEarthPressureLoadOnStem(quakeEarthPressure, Delta= backFillDelta)

#Load combinations
execfile("./load_combinations.py")

#Quasi-permanent situations.
combContainer.SLS.qp.add('ELS00', '1.0*selfWeight+1.0*deadLoad+0.5*trafficLoad')

# #Stability ultimate states. (type 1)
# combContainer.ULS.perm.add('SR1A', '1.1*selfWeight+1.35*deadLoad+1.5*trafficLoad')
# combContainer.ULS.perm.add('SR2', '1.1*selfWeight+1.35*deadLoad')
# combContainer.ULS.perm.add('SR3A', '1.1*selfWeight+0.8*deadLoad+1.5*trafficLoad')
# combContainer.ULS.perm.add('SR4', '1.1*selfWeight+0.8*deadLoad')
# combContainer.ULS.perm.add('SR5A', '0.9*selfWeight+1.35*deadLoad+1.5*trafficLoad')
# combContainer.ULS.perm.add('SR6', '0.9*selfWeight+1.35*deadLoad')
# combContainer.ULS.perm.add('SR7A', '0.9*selfWeight+0.8*deadLoad+1.5*trafficLoad')
# combContainer.ULS.perm.add('SRS1', '1.0*selfWeight+1.0*deadLoad+0.3*trafficLoad+1.0*quakeLoad')

#Strength ultimate states. (type 2).
# 'selfWeight','deadLoad','trafficLoad','liveLoad','snowLoad','windLoad','quakeLoad']
#Equation 16.1
combContainer.ULS.perm.add('SR101', '1.4*selfWeight+1.4*deadLoad')
#Equation 16.2
combContainer.ULS.perm.add('SR102A', '1.2*selfWeight+1.2*deadLoad+1.6*trafficLoad+0.5*snowLoad')
combContainer.ULS.perm.add('SR102B', '1.2*selfWeight+1.2*deadLoad+1.6*liveLoad+0.5*snowLoad')
#Equation 16.3
combContainer.ULS.perm.add('SR103A', '1.2*selfWeight+1.2*deadLoad+1.6*snowLoad+0.5*trafficLoad')
combContainer.ULS.perm.add('SR103B', '1.2*selfWeight+1.2*deadLoad+1.6*snowLoad+0.5*liveLoad')
combContainer.ULS.perm.add('SR103C', '1.2*selfWeight+1.2*deadLoad+1.6*snowLoad+0.5*windLoad')
#Equation 16.4
combContainer.ULS.perm.add('SR104A', '1.2*selfWeight+1.2*deadLoad+1.0*windLoad+0.5*trafficLoad+0.5*snowLoad')
combContainer.ULS.perm.add('SR104B', '1.2*selfWeight+1.2*deadLoad+1.0*windLoad+0.5*liveLoad+0.5*snowLoad')
#Equation 16.5
combContainer.ULS.perm.add('SR105A', '1.2*selfWeight+1.2*deadLoad+0.5*trafficLoad+0.7*snowLoad')
combContainer.ULS.perm.add('SR105B', '1.2*selfWeight+1.2*deadLoad+0.5*liveLoad+0.7*snowLoad')
#Equation 16.6 -> doesn't apply
#Equation 16.7 -> doesn't apply

def getLoadCasesForDisplaying():
  retval=[]
  for lcName in loadCaseNames:
    lc= loadCaseManager.loadPatterns[lcName]
    rlcd= gr.getRecordLoadCaseDispFromLoadPattern(lc)
    rlcd.cameraParameters= cp
    rlcd.setsToDispLoads=[totalSet]
    rlcd.setsToDispBeamLoads=[totalSet]
    retval.append(rlcd)
  return retval
