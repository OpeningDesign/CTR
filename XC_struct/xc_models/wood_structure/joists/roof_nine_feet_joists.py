# -*- coding: utf-8 -*-

''' Fire design of the corridor joists.'''

 
from __future__ import division
from __future__ import print_function
from materials.sections import section_properties as sp
from materials.awc_nds import dimensional_lumber as dl
from rough_calculations import ng_simple_beam as sb
from materials.awc_nds import AWCNDS_materials
from materials.awc_nds import structural_panels

__author__= "Luis Claudio Pérez Tato (LCPT"
__copyright__= "Copyright 2015, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

inch2meter= 0.0254

L= 42*47.88026 # Snow load N/m2
D= 18*47.88026 # Dead load N/m2
joistSpacing= 24.0*inch2meter # Space between joists
#joistSection= sp.RectangularSection('joistSection',2.5*inch2meter,10.0*inch2meter)
#joistSection= structural_panels.LVLHeaderSections['3.5x7-1/4']
wood= dl.SouthernPineWood(name='SouthernPine', grade= 'no_1', sub_grade= '')
joistSection= AWCNDS_materials.DimensionLumberSection(name= '4x6', woodMaterial= wood)
Ss= joistSection.getElasticSectionModulusZ()
Is= joistSection.Iz()

# Tabulated design values
Fb= joistSection.getFb() # Bending stress (Pa)
E= joistSection.wood.E # Modulus of elasticity (Pa)
Fv= joistSection.wood.Fv # Shear stress (Pa)

Cr= 1.0#1.15 # Repetitive member factor (AWC-NDS2018 supplement table 4F)
CD= AWCNDS_materials.getLoadDurationFactor(10)
CM= AWCNDS_materials.getWetServiceFactor('Fb',5)
Ct= AWCNDS_materials.getTemperatureFactor('Fb','dry',AWCNDS_materials.convertToFahrenheit(25))

# Span
l= 10*0.3048 #9*0.3048+6.75*inch2meter (10 feet more or less).

## Deflection
WTL= joistSpacing*(D+L)
WLL= joistSpacing*(L)
beam= sb.SimpleBeam(E,Is,l)
deltaMaxTL= beam.getDeflectionUnderUniformLoad(WTL,beam.l/2.0)
deltaMaxLL= beam.getDeflectionUnderUniformLoad(WLL,beam.l/2.0)

## Bending 
Fb_adj= Fb*Cr*CD*CM*Ct
Mu= Fb_adj*Ss
W= WTL
Mmax= W*l**2/8.0


## Shear
As= joistSection.A()
Fv_adj= Fv*CD*CM*Ct
Av= (2/3.0)*As
Vu= Fv_adj*Av
Vmax= W*l/2.0


print('**** Deflection ****')
r= l/deltaMaxLL
deltaRefLL= l/360.0
print('deltaMaxLL= ', deltaMaxLL*1e3, ' mm (L/'+str(r)+') L= ', l)
print('deltaMaxLL<deltaRefLL= ',deltaMaxLL<deltaRefLL)
r= l/deltaMaxTL
print('deltaMaxTL= ', deltaMaxTL*1e3, ' mm (L/'+str(r)+')')
deltaRefTL= l/240.0
print('deltaMaxTL<deltaRefTL= ',deltaMaxTL<deltaRefTL)

print('**** Bending strength ****')
print('Fb= ', Fb/1e6, ' MPa')
print('Fb\'= ', Fb_adj/1e6, ' MPa')
print('D= ',D/1e3,' kN/m2')
print('L= ',L/1e3,' kN/m2')
print('W= ',W/1e3,' kN/m')
print('Mu= ',Mu/1e3,' kN m', Mu/4.44822/0.3048, ' lb.ft')
print('Mmax= ',Mmax/1e3,' kN m')
print('Mu>Mmax= ',Mu>Mmax)

print('**** Shear strength ****')
print('Fv= ', Fv/1e6, ' MPa')
print('Fv\'= ', Fv_adj/1e6, ' MPa')
print('As= ', As*1e4, ' cm2')
print('Vu= ',Vu/1e3,' kN', Vu/4.44822, ' lb')
print('Vmax= ',Vmax/1e3,' kN')
print('Vu>Vmax= ',Vu>Vmax)
print('S= ', joistSection.getElasticSectionModulusZ()/1e-6,' m3')
print('Ss= ', Ss/1e-6,' m3')
print('C_D=', CD)
print('C_M=', CM)
print('C_t=', Ct)


# # Fire design
# ## Bending
# a_eff= 0.7e-3*30+7e-3
# burnedSection= sp.RectangularSection('s',joistSection.b-2*a_eff,joistSection.h-a_eff)
# Ss= burnedSection.getElasticSectionModulusZ()

# Cfire= AWCNDS_materials.getFireDesignAdjustementFactor('Fb')
# print('Cfire= ', Cfire)
# Fb_adj= Cfire*Fb*CD*CM*Ct
# Mu= Fb_adj*Ss

# ## Shear
# As= burnedSection.A()
# Av= 2/3.0*As
# Cfire= AWCNDS_materials.getFireDesignAdjustementFactor('Fv')
# Fv_adj= Cfire*Fv*CD*CM*Ct
# Vu= Fv_adj*Av

# print('**** Bending strength ****')
# print('Fb= ', Fb/1e6, ' MPa')
# print('Fb\'= ', Fb_adj/1e6, ' MPa')
# print('D= ',D/1e3,' kN/m2')
# print('L= ',L/1e3,' kN/m2')
# print('W= ',W/1e3,' kN/m')
# print('Mu= ',Mu/1e3,' kN m', Mu/4.44822/0.3048, ' lb.ft')
# print('Mmax= ',Mmax/1e3,' kN m')
# print('Mu>Mmax= ',Mu>Mmax)

# print('**** Shear strength ****')
# print('Fv= ', Fv/1e6, ' MPa')
# print('Fv\'= ', Fv_adj/1e6, ' MPa')
# print('As= ', As*1e4, ' cm2')
# print('Vu= ',Vu/1e3,' kN', Vu/4.44822, ' lb')
# print('Vmax= ',Vmax/1e3,' kN')
# print('Vu>Vmax= ',Vu>Vmax)
# print('S= ', joistSection.getElasticSectionModulusZ()/1e-6,' m3')
# print('Ss= ', Ss/1e-6,' m3')
# print('C_D=', CD)
# print('C_M=', CM)
# print('C_t=', Ct)

# print('**** Reaction ****')
# RD= joistSpacing*D*l/2.0/joistSpacing # N/m
# RL= joistSpacing*L*l/2.0/joistSpacing # N/m
# print('R_D=', RD/1e3, ' kN/m')
# print('R_L=', RL/1e3, ' kN/m')
