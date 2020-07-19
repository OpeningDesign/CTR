# -*- coding: utf-8 -*-

import math
from rough_calculations import ng_retaining_wall
import xc_base
import geom
import xc
from materials.aci import ACI_materials
from materials.aci import ACI_limit_state_checking
from materials.sections import rebar_family
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

wallHead= -(2.0*FEET_2_METER+6.0*INCH_2_METER)
topOfFoundation= -(14.0*FEET_2_METER+0*INCH_2_METER)
stemBottomWidth= 10*INCH_2_METER
stemTopWidth= stemBottomWidth
footingThickness= stemBottomWidth+2*INCH_2_METER

sectionName= "RWcantilever"
wall= ng_retaining_wall.RetainingWall(sectionName,cover,stemBottomWidth,stemTopWidth,footingThickness, concrete, reinfSteel)
wall.stemHeight= wallHead-topOfFoundation
wall.bToe= 2.0*FEET_2_METER
wall.bHeel= 4.0*FEET_2_METER
wall.beton= concrete
wall.exigeanceFisuration= 'B'
wall.stemReinforcement.setReinforcement(1,A19_30.getCopy(ACI_limit_state_checking.RebarController('B')))
wall.stemReinforcement.setReinforcement(2,A13_30.getCopy(ACI_limit_state_checking.RebarController('B')))
wall.footingReinforcement.setReinforcement(3,D1619_15.getCopy(ACI_limit_state_checking.RebarController('B')))
wall.stemReinforcement.setReinforcement(4,A10_15.getCopy(ACI_limit_state_checking.RebarController('B')))
wall.stemReinforcement.setReinforcement(5,A16_30.getCopy(ACI_limit_state_checking.RebarController('B')))
wall.stemReinforcement.setReinforcement(6,A13_15.getCopy(ACI_limit_state_checking.RebarController('B')))
wall.footingReinforcement.setReinforcement(7,A10_15.getCopy(ACI_limit_state_checking.RebarController('B')))
wall.footingReinforcement.setReinforcement(8,D1619_15.getCopy(ACI_limit_state_checking.RebarController('B')))
wall.stemReinforcement.setReinforcement(11,A13_15.getCopy(ACI_limit_state_checking.RebarController('B')))


wallFEModel= wall.createFEProblem('Ramp wall')
preprocessor= wallFEModel.getPreprocessor
nodes= preprocessor.getNodeHandler

#Soil
kS= 200*4.44822/(0.0254)**3 #Subgrade modulus (geotechnical report).
#print 'kS= ', kS/1e6
kX= typical_materials.defElasticMaterial(preprocessor, "kX",kS/10.0)
kY= typical_materials.defElasticMaterial(preprocessor, "kY",kS)
#kY= typical_materials.defElastNoTensMaterial(preprocessor, "kY",kS)
soilDensity= 125*0.453592/(0.3048)**3
backFillSoilModel= ep.RankineSoil(phi= math.radians(30),rho= soilDensity) #Characteristic values.
backFillDelta= 0.0#2.0/3.0*backFillSoilModel.phi
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
gravity=9.81 #Aceleración de la gravedad (m/s2)
wall.createSelfWeightLoads(rho= 2500,grav= gravity)

#Dead load.
#  Dead load. Earth self weight.
gSoil= backFillSoilModel.rho*gravity
topOfFrontTerrain= -(12.0*FEET_2_METER+8*INCH_2_METER)
frontFillDepth= topOfFrontTerrain-topOfFoundation
deadLoad= loadCaseManager.setCurrentLoadCase('deadLoad')
wall.createDeadLoad(heelFillDepth= wall.stemHeight,toeFillDepth= frontFillDepth,rho= backFillSoilModel.rho, grav= gravity)

#  Dead load. Earth pressure.
Ka= backFillSoilModel.Ka()
zGroundBackFill= wallHead # Height of the back fill
backFillPressureModel=  earth_pressure.EarthPressureModel( zGround= zGroundBackFill, zBottomSoils=[-10],KSoils= [Ka],gammaSoils= [gSoil], zWater= -1e3, gammaWater= 1000*gravity)
wall.createBackFillPressures(backFillPressureModel, Delta= backFillDelta)
zGroundFrontFill= zGroundBackFill-wall.stemHeight+frontFillDepth #Front fill
frontFillPressureModel=  earth_pressure.EarthPressureModel(zGround= zGroundFrontFill, zBottomSoils=[-10],KSoils= [Ka], gammaSoils= [gSoil], zWater= -1e3, gammaWater= 1000*gravity)
wall.createFrontFillPressures(frontFillPressureModel)

#Live load. Traffic load.
trafficLoad= loadCaseManager.setCurrentLoadCase('trafficLoad')
trafficEarthPressure= earth_pressure.StripLoadOnBackfill(qLoad= 11.97e3,zLoad= 0.0, distWall= 1.0, stripWidth= 10)
wall.createPressuresFromLoadOnBackFill(trafficEarthPressure, Delta= backFillDelta)

#Accidental actions. Quake
quakeLoad= loadCaseManager.setCurrentLoadCase('quakeLoad')
kh=  0.03
kv=  0.7*kh
Aq= wall.getMononobeOkabeDryOverpressure(backFillSoilModel,kv,kh)
#print('Aq= ',Aq)
quakeEarthPressure= earth_pressure.UniformLoadOnStem(Aq)
wall.createEarthPressureLoadOnStem(quakeEarthPressure, Delta= backFillDelta)

#Load combinations
execfile("./load_combinations.py")

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
