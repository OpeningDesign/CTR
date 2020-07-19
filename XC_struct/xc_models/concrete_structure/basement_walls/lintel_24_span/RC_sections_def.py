# -*- coding: utf-8 -*-

#import os
#import xc_base
#import geom
#import xc
from materials.sections.fiber_section import def_simple_RC_section as rcs
from postprocess import element_section_map

from materials.aci import ACI_materials
ft2m=0.3048
in2m=0.0254

concrete= ACI_materials.c3000
concrete.gmmC= 1.0/0.75
reinfSteel= ACI_materials.A615G60

# **Concrete sections
#instances of element_section_map.RCSlabBeamSection that define the
#variables that make up THE TWO reinforced concrete sections in the two
#reinforcement directions of a slab or the front and back ending sections
#of a beam element
nSup=2
fiSup=15.875
nInf=3
fiInf=22.225
nRef=2
fiRef=25.4
nLat=2
fiLat=12.7

beamCentRCsect=element_section_map.RCSlabBeamSection(name='beamCentRCsect',sectionDescr='beam elements',concrType=concrete, reinfSteelType=reinfSteel,width=wBeam,depth=hBeam,elemSetName=beamCent.name)

beamCentRCsect.dir1PositvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayerByNumFi_mm(nSup,fiSup,35,35,wBeam*1e3),rcs.rebLayerByNumFi_mm(nLat,fiLat,hBeam/3.*1e3,35,wBeam*1e3)])
beamCentRCsect.dir1NegatvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayerByNumFi_mm(nInf,fiInf,35,35,wBeam*1e3),rcs.rebLayerByNumFi_mm(nLat,fiLat,hBeam/3.*1e3,35,wBeam*1e3)])
if nRef>0:
    beamCentRCsect.dir1NegatvRebarRows.append(rcs.rebLayerByNumFi_mm(nRef,fiRef,100,35,wBeam*1e3))
beamCentRCsect.dir2PositvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayerByNumFi_mm(nSup,fiSup,35,35,wBeam*1e3),rcs.rebLayerByNumFi_mm(nLat,fiLat,hBeam/3.*1e3,35,wBeam*1e3)])
beamCentRCsect.dir2NegatvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayerByNumFi_mm(nInf,fiInf,35,35,wBeam*1e3),rcs.rebLayerByNumFi_mm(nLat,fiLat,hBeam/3.*1e3,35,wBeam*1e3)])
if nRef>0:
    beamCentRCsect.dir2NegatvRebarRows.append(rcs.rebLayerByNumFi_mm(nRef,fiRef,100,35,wBeam*1e3))

fiCercosCent=6.35
sepCercosCent=8*in2m
beamCentRCsect.dir1ShReinfY=rcs.ShearReinforcement(familyName= "sh",nShReinfBranches=2,areaShReinfBranch= math.pi*(fiCercosCent*1e-3)**2/4.,shReinfSpacing=sepCercosCent,angAlphaShReinf= math.pi/2.0,angThetaConcrStruts= math.pi/4.0)
beamCentRCsect.dir2ShReinfY=rcs.ShearReinforcement(familyName= "sh",nShReinfBranches=2,areaShReinfBranch= math.pi*(fiCercosCent*1e-3)**2/4.,shReinfSpacing=sepCercosCent,angAlphaShReinf= math.pi/2.0,angThetaConcrStruts= math.pi/4.0)

beamExtrRCsect=element_section_map.RCSlabBeamSection(name='beamExtrRCsect',sectionDescr='beam elements',concrType=concrete, reinfSteelType=reinfSteel,width=wBeam,depth=hBeam,elemSetName=beamExtr.name)
beamExtrRCsect.dir1PositvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayerByNumFi_mm(nSup,fiSup,35,35,wBeam*1e3),rcs.rebLayerByNumFi_mm(nLat,fiLat,hBeam/3.*1e3,35,wBeam*1e3)])
beamExtrRCsect.dir1NegatvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayerByNumFi_mm(nInf,fiInf,35,35,wBeam*1e3),rcs.rebLayerByNumFi_mm(nLat,fiLat,hBeam/3.*1e3,35,wBeam*1e3)])
beamExtrRCsect.dir2PositvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayerByNumFi_mm(nSup,fiSup,35,35,wBeam*1e3),rcs.rebLayerByNumFi_mm(nLat,fiLat,hBeam/3.*1e3,35,wBeam*1e3)])
beamExtrRCsect.dir2NegatvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayerByNumFi_mm(nInf,fiInf,35,35,wBeam*1e3),rcs.rebLayerByNumFi_mm(nLat,fiLat,hBeam/3.*1e3,35,wBeam*1e3)])

fiCercosExtr=9.525
sepCercosExtr=8*in2m
beamExtrRCsect.dir1ShReinfY=rcs.ShearReinforcement(familyName= "sh",nShReinfBranches=2,areaShReinfBranch= math.pi*(fiCercosExtr*1e-3)**2/4.,shReinfSpacing=sepCercosExtr,angAlphaShReinf= math.pi/2.0,angThetaConcrStruts= math.pi/4.0)
beamExtrRCsect.dir2ShReinfY=rcs.ShearReinforcement(familyName= "sh",nShReinfBranches=2,areaShReinfBranch= math.pi*(fiCercosExtr*1e-3)**2/4.,shReinfSpacing=sepCercosExtr,angAlphaShReinf= math.pi/2.0,angThetaConcrStruts= math.pi/4.0)

columnRCsect=element_section_map.RCSlabBeamSection(name='columnRCsect',sectionDescr='column',concrType=concrete, reinfSteelType=reinfSteel,width=wColumn,depth=dimYColumn,elemSetName=column.name)

columnRCsect.dir1PositvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayerByNumFi_mm(2,12.7,35,35,wColumn*1e3)])
columnRCsect.dir1NegatvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayerByNumFi_mm(2,12.7,35,35,wColumn*1e3)])
columnRCsect.dir2PositvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayerByNumFi_mm(2,12.7,35,35,wColumn*1e3)])
columnRCsect.dir2NegatvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayerByNumFi_mm(2,12.7,35,35,wColumn*1e3)])



