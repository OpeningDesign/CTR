# -*- coding: utf-8 -*-

''' Fire design of the corridor joists.'''

 
from __future__ import division
from __future__ import print_function
from materials.awc_nds import AWCNDS_materials as mat
from materials.sections import section_properties as sp
from rough_calculations import ng_simple_beam as sb

__author__= "Luis Claudio Pérez Tato (LCPT"
__copyright__= "Copyright 2015, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

L= 40*47.88026 # Live load N/m2
D= 15*47.88026 # Dead load N/m2
joistSpacing= 32.0*0.0254 # Space between joists
#joistSection= sp.RectangularSection('joistSection',2.5*0.0254,10.0*0.0254)
joistSection= sp.RectangularSection('joistSection',3.5*0.0254,6*0.0254)
Ss= joistSection.getElasticSectionModulusZ()
Is= joistSection.Iz()

def getLVLFb(depth):
    '''Return allowable stress according to the document:
       LP SolidStart LVL Technical Guide2900Fb-2.0E
       page 4.
    '''
    retval= 2900
    in12= 12.0*0.0254
    in3_5= 3.5*0.0254
    if(depth>in12):
        retval*= pow((in12/depth),0.143)
    else:
        if(depth<in3_5):
            retval*= 1.147
        else:
            retval*= pow((in12/depth),0.111)
    return retval

# Tabulated design values
Fb= getLVLFb(joistSection.h)*6894.76 # Bending stress (Pa)
E= 2e6*6894.76 # Modulus of elasticity (Pa)
Fv= 285*6894.76 # Shear stress (Pa)

Cr= 1.0#1.15 # Repetitive member factor (AWC-NDS2018 supplement table 4F)
CD= mat.getLoadDurationFactor(10)
CM= mat.getWetServiceFactor('Fb',5)
Ct= mat.getTemperatureFactor('Fb','dry',mat.convertToFahrenheit(25))
CV= mat.getVolumeFactor(L,joistSection.b,joistSection.h)

# Span
l= 2.4#4.6#1.5 #4.6

# Deflection
WTL= joistSpacing*(D+L)
WLL= joistSpacing*(L)
beam= sb.SimpleBeam(E,Is,l)
deltaMaxTL= beam.getDeflectionUnderUniformLoad(WTL,beam.l/2.0)
deltaMaxLL= beam.getDeflectionUnderUniformLoad(WLL,beam.l/2.0)
deltaRef= l/480.0

# Bending 
Fb_adj= Fb*Cr*CD*CM*Ct*CV
Mu= Fb_adj*Ss
W= joistSpacing*(D+L)
Mmax= W*l**2/8.0


# Shear
As= joistSection.A()
Fv_adj= Fv*CD*CM*Ct
Av= (2/3.0)*As
Vu= Fv_adj*Av
Vmax= W*l/2.0



# Fire design
# Bending
a_eff= 0.7e-3*30+7e-3
burnedSection= sp.RectangularSection('s',joistSection.b-2*a_eff,joistSection.h-a_eff)
Ss= burnedSection.getElasticSectionModulusZ()

Cfire= mat.getFireDesignAdjustementFactor('Fb')
print('Cfire= ', Cfire)
Fb_adj= Cfire*Fb*CD*CM*Ct*CV
Mu= Fb_adj*Ss

# Shear
As= burnedSection.A()
Av= 2/3.0*As
Cfire= mat.getFireDesignAdjustementFactor('Fv')
Fv_adj= Cfire*Fv*CD*CM*Ct
Vu= Fv_adj*Av


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
print('Mu>Mmax= ',Mu>Mmax)

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
print('C_V=', CV)
print('joistSection.b= ',joistSection.b*1e3,' mm')
print('a_eff= ',a_eff*1e3,' mm')
print('burnedSection.b= ',burnedSection.b*1e3,' mm')
