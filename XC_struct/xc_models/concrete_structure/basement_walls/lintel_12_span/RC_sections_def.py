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
fiInf=28.65
nRef=0
fiRef=28.65
nLat=2
fiLat=9.525

beamRCsect=element_section_map.RCSlabBeamSection(name='beamRCsect',sectionDescr='beam elements',concrType=concrete, reinfSteelType=reinfSteel,width=wBeam,depth=hBeam,elemSetName=beam.name)

beamRCsect.dir1PositvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayerByNumFi_mm(nSup,fiSup,35,35,wBeam*1e3),])
beamRCsect.dir1NegatvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayerByNumFi_mm(nInf,fiInf,35,35,wBeam*1e3)])
if nRef>0:
    beamRCsect.dir1NegatvRebarRows.append(rcs.rebLayerByNumFi_mm(nRef,fiRef,100,35,wBeam*1e3))
if nLat>0:
    beamRCsect.dir1NegatvRebarRows.append(rcs.rebLayerByNumFi_mm(nLat,fiLat,hBeam/2.*1e3,35,wBeam*1e3))
beamRCsect.dir2PositvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayerByNumFi_mm(nSup,fiSup,35,35,wBeam*1e3)])
beamRCsect.dir2NegatvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayerByNumFi_mm(nInf,fiInf,35,35,wBeam*1e3)])
if nRef>0:
    beamRCsect.dir2NegatvRebarRows.append(rcs.rebLayerByNumFi_mm(nRef,fiRef,100,35,wBeam*1e3))
if nLat>0:
    beamRCsect.dir2NegatvRebarRows.append(rcs.rebLayerByNumFi_mm(nLat,fiLat,hBeam/2.*1e3,35,wBeam*1e3))

fiCercosCent=9.525
sepCercosCent=6*in2m
beamRCsect.dir1ShReinfY=rcs.ShearReinforcement(familyName= "sh",nShReinfBranches=2,areaShReinfBranch= math.pi*(fiCercosCent*1e-3)**2/4.,shReinfSpacing=sepCercosCent,angAlphaShReinf= math.pi/2.0,angThetaConcrStruts= math.pi/4.0)
beamRCsect.dir2ShReinfY=rcs.ShearReinforcement(familyName= "sh",nShReinfBranches=2,areaShReinfBranch= math.pi*(fiCercosCent*1e-3)**2/4.,shReinfSpacing=sepCercosCent,angAlphaShReinf= math.pi/2.0,angThetaConcrStruts= math.pi/4.0)


columnRCsect=element_section_map.RCSlabBeamSection(name='columnRCsect',sectionDescr='column',concrType=concrete, reinfSteelType=reinfSteel,width=wColumn,depth=dimYColumn,elemSetName=column.name)

columnRCsect.dir1PositvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayerByNumFi_mm(2,12.7,35,35,wColumn*1e3)])
columnRCsect.dir1NegatvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayerByNumFi_mm(2,12.7,35,35,wColumn*1e3)])
columnRCsect.dir2PositvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayerByNumFi_mm(2,12.7,35,35,wColumn*1e3)])
columnRCsect.dir2NegatvRebarRows= def_simple_RC_section.LongReinfLayers([rcs.rebLayerByNumFi_mm(2,12.7,35,35,wColumn*1e3)])



