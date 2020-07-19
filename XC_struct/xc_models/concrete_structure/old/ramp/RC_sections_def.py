# -*- coding: utf-8 -*-

#import os
#import xc_base
#import geom
#import xc
from materials.sections.fiber_section import def_simple_RC_section as rcs
from postprocess import element_section_map

from materials.aci import ACI_materials
from postprocess import RC_material_distribution

concrete= ACI_materials.c3000
concrete.gmmC= 1.0/0.75
reinfSteel= ACI_materials.A615G60
#Define available sections for the elements (spatial distribution of RC sections).
reinfConcreteSectionDistribution= RC_material_distribution.RCMaterialDistribution()
sections= reinfConcreteSectionDistribution.sectionDefinition

# **Concrete sections
#instances of element_section_map.RCSlabBeamSection that define the
#variables that make up THE TWO reinforced concrete sections in the two
#reinforcement directions of a slab or the front and back ending sections
#of a beam element

rampRCSects= element_section_map.RCSlabBeamSection(name='rampRCSects',sectionDescr='slab of shell elements',concrType=concrete, reinfSteelType=reinfSteel,depth=rampTh,elemSetName=ramp.name)  
rampRCSects.dir1PositvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n3s300r50]) #tranv. sup.
rampRCSects.dir1NegatvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n3s300r45]) #transv. inf.
rampRCSects.dir2PositvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n3s300r50]) #long. sup.
rampRCSects.dir2NegatvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n3s150r50]) #long. inf.
