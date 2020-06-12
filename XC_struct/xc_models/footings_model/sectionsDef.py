# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division

import math
import os
import xc_base
import geom
import xc
# Macros
#from materials.ehe import auxEHE
from materials.sections.fiber_section import defSimpleRCSection
from materials.sections import section_properties
from postprocess import RC_material_distribution


from materials.aci import ACI_materials

from postprocess import limit_state_data as lsd
from postprocess import element_section_map


concrete= ACI_materials.c3000
concrete.gmmC= 1.0/0.75
reinfSteel= ACI_materials.A615G60
#Define available sections for the elements (spatial distribution of RC sections).
reinfConcreteSectionDistribution= RC_material_distribution.RCMaterialDistribution()
sections= reinfConcreteSectionDistribution.sectionDefinition

csvFile= open('footings_geometry.csv')
reader= csv.reader(csvFile)
rcSects= dict()
for row in reader:
    id= row[0]
    thickness= float(row[5])
    sName= id + '_sections'
    sDescr= id + ' footing sections.'
    rcSects[id]= defSimpleRCSection.RecordRCSlabBeamSection(name=sName,sectionDescr=sDescr,concrType=concrete, reinfSteelType=reinfSteel,depth= thickness)
csvFile.close()

for key in ['A1','A2','B1','B2']:
    rcS= rcSects[key]
    rcS.dir1PositvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n2s300r50])
    rcS.dir1NegatvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n7s300r50])
    rcS.dir2PositvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n2s300r45])
    rcS.dir2NegatvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n7s300r45])

for key in ['A3','A4','A5','B3','B4','B5']:
    rcS= rcSects[key]
    rcS.dir1PositvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n2s300r50])
    rcS.dir1NegatvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n8s300r50])
    rcS.dir2PositvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n2s300r45])
    rcS.dir2NegatvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n8s300r45])

for key in ['C1','D1','G1']:
    rcS= rcSects[key]
    rcS.dir1PositvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n2s300r50])
    rcS.dir1NegatvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n8s300r50])
    rcS.dir2PositvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n2s300r45])
    rcS.dir2NegatvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n8s300r45])

for key in ['C2','C3','C4','C5','D2','D3','D4','D5']:
    rcS= rcSects[key]
    rcS.dir1PositvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n2s300r50])
    rcS.dir1NegatvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n8s300r50])
    rcS.dir2PositvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n2s300r45])
    rcS.dir2NegatvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n8s300r45])

for key in ['G2','G3','G4','G5']:
    rcS= rcSects[key]
    rcS.dir1PositvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n2s300r50])
    rcS.dir1NegatvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n8s300r50])
    rcS.dir2PositvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n2s300r45])
    rcS.dir2NegatvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n8s300r45])

for key in ['F1','F2','F3','F4','F5']:
    rcS= rcSects[key]
    rcS.dir1PositvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n2s300r50])
    rcS.dir1NegatvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n8s300r50])
    rcS.dir2PositvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n2s300r45])
    rcS.dir2NegatvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n8s300r45])


for key in rcSects:
    rcS= rcSects[key]
    sections.append(rcS)
    
footingRCSect= defSimpleRCSection.RecordRCSlabBeamSection(name='footingRCSect',sectionDescr="footing.",concrType=concrete, reinfSteelType=reinfSteel,depth=0.50)
#[0]: longitudinal rebars
#[1]: transversal rebars
footingRCSect.dir1PositvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n2s150r50])
footingRCSect.dir1NegatvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n8s150r50])
footingRCSect.dir2PositvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n2s150r45])
footingRCSect.dir2NegatvRebarRows= def_simple_RC_section.LongReinfLayers([ACI_materials.n8s150r45])

sections.append(footingRCSect)

