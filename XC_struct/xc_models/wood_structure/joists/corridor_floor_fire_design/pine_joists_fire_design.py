# -*- coding: utf-8 -*-

''' Fire design of the corridor joists.'''

 
from __future__ import division
from __future__ import print_function
from materials.awc_nds import AWCNDS_materials as mat
from materials.awc_nds import dimensional_lumber as dl
from materials.sections import section_properties as sp
from rough_calculations import ng_simple_beam as sb

__author__= "Luis Claudio Pérez Tato (LCPT"
__copyright__= "Copyright 2015, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

inch2meter= 0.0254
psi2Pa= 6894.75

L= 40*47.88026 # Live load N/m2
D= 15*47.88026 # Dead load N/m2
joistSpacing= 32.0*inch2meter # Space between joists

# Ryan asks for a cheaper solution 20191203 and 20200117
wood= dl.SouthernPineWood(name='SouthernPine', grade= 'no_1', sub_grade= '')
joistSection= mat.DimensionLumberSection(name= '4x6', woodMaterial= wood)

Ss= joistSection.getElasticSectionModulusZ()
Is= joistSection.Iz()

# Tabulated design values
Fb= joistSection.getFb() # Bending stress (Pa)
E= joistSection.wood.E # Modulus of elasticity (Pa)
Fv= joistSection.wood.Fv # Shear stress (Pa)

Cr= 1.0#1.15 # Repetitive member factor (AWC-NDS2018 supplement table 4F)
CD= mat.getLoadDurationFactor(10)
CM= mat.getWetServiceFactor('Fb',5)
Ct= mat.getTemperatureFactor('Fb','dry',mat.convertToFahrenheit(25))

# Span
l= 2.4#4.6#1.5 #4.6

## Deflection
WTL= joistSpacing*(D+L)
WLL= joistSpacing*(L)
beam= sb.SimpleBeam(E,Is,l)
deltaMaxTL= beam.getDeflectionUnderUniformLoad(WTL,beam.l/2.0)
deltaMaxLL= beam.getDeflectionUnderUniformLoad(WLL,beam.l/2.0)
deltaRef= l/480.0

## Bending 
Fb_adj= Fb*Cr*CD*CM*Ct
Mu= Fb_adj*Ss
W= joistSpacing*(D+L)
Mmax= W*l**2/8.0


## Shear
As= joistSection.A()
Fv_adj= Fv*CD*CM*Ct
Av= (2/3.0)*As
Vu= Fv_adj*Av
Vmax= W*l/2.0

## Bearing
osbPanelThickness= (1.0+1.0/8.0)*inch2meter
bearingArea= joistSection.b*osbPanelThickness
Rmax= Vmax # Reaction
bearingStress= Rmax/bearingArea
Fc_perp= 550*psi2Pa
CF= bearingStress/Fc_perp



# Fire design
## Bending
a_eff= 0.7e-3*30+7e-3
burnedSection= mat.CustomLumberSection(name= '4x6',b= joistSection.b-2*a_eff, h= joistSection.h-a_eff, woodMaterial= wood)

Ss= burnedSection.getElasticSectionModulusZ()

Cfire= mat.getFireDesignAdjustementFactor('Fb')
print('Cfire= ', Cfire)
Fb_adj= Cfire*Fb*CD*CM*Ct
Mu= Fb_adj*Ss

## Shear
As= burnedSection.A()
Av= 2/3.0*As
Cfire= mat.getFireDesignAdjustementFactor('Fv')
Fv_adj= Cfire*Fv*CD*CM*Ct
Vu= Fv_adj*Av


print('b= ', joistSection.b*1000, 'mm (',joistSection.b/inch2meter,'in)')
print('h= ', joistSection.h*1000, 'mm (',joistSection.h/inch2meter,'in)')
print('I= ', Is,' m4')
print('**** Deflection ****')
r= l/deltaMaxLL
deltaRefLL= l/540.0
print('deltaMaxLL= ', deltaMaxLL*1e3, ' mm (L/'+str(r)+')')
print('deltaMaxLL<deltaRefLL= ',deltaMaxLL<deltaRefLL)
r= l/deltaMaxTL
print('deltaMaxTL= ', deltaMaxTL*1e3, ' mm (L/'+str(r)+')')
deltaRefTL= l/360.0
print('deltaMaxTL<deltaRefTL= ',deltaMaxTL<deltaRefTL)

print('**** Bending strength ****')
print('Fb= ', Fb/1e6, ' MPa')
print('Fb\'= ', Fb_adj/1e6, ' MPa')
print('D= ',D/1e3,' kN/m2')
print('L= ',L/1e3,' kN/m2')
print('W= ',W/1e3,' kN/m')
print('Mu= ',Mu/1e3,' kN m')
print('Mmax= ',Mmax/1e3,' kN m')
print('F= ', Mmax/Mu,' Mu>Mmax= ',Mu>Mmax)

print('**** Shear strength ****')
print('Fv= ', Fv/1e6, ' MPa')
print('Fv\'= ', Fv_adj/1e6, ' MPa')
print('As= ', As*1e4, ' cm2')
print('Vu= ',Vu/1e3,' kN')
print('Vmax= ',Vmax/1e3,' kN')
print('Vu>Vmax= ',Vu>Vmax)
print('S= ', joistSection.getElasticSectionModulusZ()/1e-6,' m3')
print('Ss= ', Ss/1e-6,' m3')
print('C_D=', CD)
print('C_M=', CM)
print('C_t=', Ct)
print('joistSection.b= ',joistSection.b*1e3,' mm')
print('a_eff= ',a_eff*1e3,' mm')
print('burnedSection.b= ',burnedSection.b*1e3,' mm')

print('**** Bearing stress ****')
print('Reaction R=', Rmax/1e3,' kN')
print('Bearing area A=', bearingArea*1e4,' cm2')
print('Bearing stress sg= ', bearingStress/1e6, ' MPa')
print('Fc_perp= ', Fc_perp/1e6, ' MPa')
print('CF= ', CF)
