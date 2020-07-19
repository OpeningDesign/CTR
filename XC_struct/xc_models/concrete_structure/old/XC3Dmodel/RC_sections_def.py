# -*- coding: utf-8 -*-

#import os
#import xc_base
#import geom
#import xc
from materials.sections.fiber_section import def_simple_RC_section as rcs
from postprocess import element_section_map


# **Concrete sections
#instances of element_section_map.RCSlabBeamSection that define the
#variables that make up THE TWO reinforced concrete sections in the two
#reinforcement directions of a slab or the front and back ending sections
#of a beam element

deckRCSects= element_section_map.RCSlabBeamSection(name='deckRCSects',sectionDescr='slab of shell elements',concrType=concrete, reinfSteelType=reinfSteel,depth=deckTh,elemSetName=decks.name)  
deckRCSects.dir1PositvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayer_mm(12,150,35)])
deckRCSects.dir1NegatvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayer_mm(12,200,35)])
deckRCSects.dir2PositvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayer_mm(16,250,35)])
deckRCSects.dir2NegatvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayer_mm(16,100,35)])
import math
areaFi8=math.pi*0.008**2/4.
shear1=rcs.ShearReinforcement(familyName= "shear1",nShReinfBranches= 1.0,areaShReinfBranch= areaFi8,shReinfSpacing= 0.20,angAlphaShReinf= math.pi/2.0,angThetaConcrStruts= math.radians(30))
shear2=rcs.ShearReinforcement(familyName= "shear2",nShReinfBranches= 1.0,areaShReinfBranch= areaFi8,shReinfSpacing= 0.15,angAlphaShReinf= math.pi/2.0,angThetaConcrStruts= math.radians(30))
deckRCSects.dir1ShReinfY=shear1
deckRCSects.dir2ShReinfY=shear2


footRCSects= element_section_map.RCSlabBeamSection(name='footRCSects',sectionDescr='footation',concrType=concrete, reinfSteelType=reinfSteel,depth=footTh,elemSetName=foot.name)
#D1: transversal rebars
#D2: longitudinal rebars
footRCSects.dir1PositvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayer_mm(12,150,35)])
footRCSects.dir1NegatvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayer_mm(12,150,35)])
footRCSects.dir2PositvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayer_mm(16,150,35)])
footRCSects.dir2NegatvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayer_mm(16,150,35)])

wallRCSects= element_section_map.RCSlabBeamSection(name='wallRCSects',sectionDescr='wall of shell elements',concrType=concrete, reinfSteelType=reinfSteel,depth=wallTh,elemSetName=wall.name)  
wallRCSects.dir1PositvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayer_mm(20,200,35)])
wallRCSects.dir1NegatvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayer_mm(25,150,35)])
wallRCSects.dir2PositvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayer_mm(16,150,35)])
wallRCSects.dir2NegatvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayer_mm(12,150,35)])


beamXRCsect=element_section_map.RCSlabBeamSection(name='beamXRCsect',sectionDescr='beam elements in X direction',concrType=concrete, reinfSteelType=reinfSteel,width=wbeamX,depth=hbeamX,elemSetName=beamX.name)
beamXRCsect.dir1PositvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayer_mm(20,50,35)])
beamXRCsect.dir1NegatvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayer_mm(22,50,35)])
beamXRCsect.dir2PositvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayer_mm(20,50,35)])
beamXRCsect.dir2NegatvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayer_mm(22,50,35)])


beamYRCsect=element_section_map.RCSlabBeamSection(name='beamYRCsect',sectionDescr='beam elements in Y direction',concrType=concrete, reinfSteelType=reinfSteel,width=wbeamY,depth=hbeamY,elemSetName=beamY.name)
beamYRCsect.dir1PositvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayer_mm(20,150,35)])
beamYRCsect.dir1NegatvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayer_mm(22,150,35)])
beamYRCsect.dir2PositvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayer_mm(20,150,35)])
beamYRCsect.dir2NegatvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayer_mm(22,150,35)])


columnZRCsect=element_section_map.RCSlabBeamSection(name='columnZRCsect',sectionDescr='columnZ',concrType=concrete, reinfSteelType=reinfSteel,width=wcolumnZ,depth=hcolumnZ,elemSetName=columnZ.name)
columnZRCsect.dir1PositvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayer_mm(20,150,35)])
columnZRCsect.dir1NegatvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayer_mm(22,150,35)])
columnZRCsect.dir2PositvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayer_mm(20,150,35)])
columnZRCsect.dir2NegatvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayer_mm(22,150,35)])



