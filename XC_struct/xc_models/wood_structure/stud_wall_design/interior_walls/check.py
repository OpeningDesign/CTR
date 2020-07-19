# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from materials.awc_nds import AWCNDS_materials as mat
from solution import predefined_solutions
from actions import combinations as combs

OKGREEN= '\033[92m'
WARNING= '\033[93m'
FAIL= '\033[91m'
ENDC = '\033[0m'

kNToPound= 224.809
kNmTokipsft= 0.737562121169657
kNmToPoundft= kNmTokipsft*1000.0

# Load combination definition
combContainer= combs.CombContainer()

## Serviceability limit states.

### Equation 16-8
combContainer.SLS.qp.add('EQ1608', '1.0*deadLoad')
### Equation 16-9
combContainer.SLS.qp.add('EQ1609', '1.0*deadLoad+1.0*liveLoad')
### Equation 16-10
combContainer.SLS.qp.add('EQ1610', '1.0*deadLoad+1.0*snowLoad')
### Equation 16-11
combContainer.SLS.qp.add('EQ1611', '1.0*deadLoad+0.75*liveLoad+0.75*snowLoad')
### Equation 16-12
combContainer.SLS.qp.add('EQ1612', '1.0*deadLoad+0.6*windLoad')
### Equation 16-13
combContainer.SLS.qp.add('EQ1613', '1.0*deadLoad+0.45*windLoad+0.75*liveLoad+0.75*snowLoad')
### Equation 16-14-> doesn't apply
### Equation 16-15
combContainer.SLS.qp.add('EQ1615', '0.6*deadLoad+0.6*windLoad')
### Equation 16-16 -> doesn't apply
### LIVE load only.
combContainer.SLS.qp.add('LIVE', '1.0*liveLoad')

def checkPlates(combName, studSpacing, plateGeom, infSet, supSet, supportedNodes, loadDurationFactor):
    ## Bending stiffness
    uYMax= -1e6
    for n in infSet.nodes:
        uY= -n.getDisp[1]
        uYMax= max(uY,uYMax)

    r= studSpacing/uYMax
    print('**** uYMax('+combName+')= ', uYMax*1e3, ' mm (L/'+str(r)+')\n')

    ## Bending strength
    sgMax= -1e6
    for e in supSet.elements:
        e.getResistingForce()
        m1= e.getM1
        sg1= abs(m1/plateGeom.xc_material.sectionProperties.I*plateGeom.h/2)
        sgMax= max(sgMax,sg1)
        m2= e.getM2
        sg2= abs(m2/plateGeom.xc_material.sectionProperties.I*plateGeom.h/2)
        sgMax= max(sgMax,sg2)

    Fb_adj= plateGeom.getFbAdj()*loadDurationFactor
    FbCF= sgMax/Fb_adj
    print('sgMax= ', sgMax/1e6,' MPa')
    print('Fb_adj= ', Fb_adj/1e6,' MPa')
    if(Fb_adj>sgMax):
        print('**** CF= ', FbCF,'OK\n')
    else:
        print(FAIL+'**** CF= '+str(FbCF)+' KO\n'+ENDC)

    ## Shear strength
    tauMax= -1e6
    for e in supSet.elements:
        e.getResistingForce()
        v1= e.getV1
        tau1= abs(v1/plateGeom.xc_material.sectionProperties.A)
        tauMax= max(tauMax,tau1)
        v2= e.getV2
        tau2= abs(v2/plateGeom.xc_material.sectionProperties.A)
        tauMax= max(tauMax,tau2)

    tauMax*= (studSpacing-plateGeom.h)/studSpacing
    Fv_adj= plateGeom.getFvAdj()*loadDurationFactor
    FvCF= tauMax/Fv_adj
    print('tauMax= ', tauMax/1e6,' MPa')
    print('Fv_adj= ', Fv_adj/1e6,' MPa')
    if(Fv_adj>tauMax):
        print('**** CF= ', FvCF,'OK\n')
    else:
        print(FAIL+'**** CF= '+str(FvCF)+' KO\n'+ENDC)

    ## Compression perpendicular to grain

    ### Reactions
    preprocessor= infSet.getPreprocessor
    preprocessor.getNodeHandler.calculateNodalReactions(False,1e-7)
    RMax= -1e12;
    for n in supportedNodes:
        RMax= max(RMax,abs(n.getReaction[1]))
    sgMax= RMax/plateGeom.A()
    lb= (plateGeom.h)/0.0254 # Length in bearing parallel to the grain of the wood.
    Cb= (lb+0.375)/lb
    Fc_perp= plateGeom.getFc_perpAdj(Cb)*loadDurationFactor #Perpendicular to grain
    Fc_perpCF= sgMax/Fc_perp
    print('RMax= ', RMax/1e3, ' kN')
    print('sgMax= ', sgMax/1e6, ' MPa / ', sgMax/mat.psi2Pa,'psi')
    print('Fc_perp= ', Fc_perp/1e6, ' MPa / ', Fc_perp/mat.psi2Pa,'psi')
    if(Fc_perp>sgMax):
        print('**** CF= ', Fc_perpCF,'OK\n')
    else:
        print(FAIL+'**** CF= '+str(Fc_perpCF)+' KO\n'+ENDC)


def printCombinationResults(prb,comb, studSpacing, plateGeom, infSet, supSet, supportedNodes, loadDurationFactor):
    preprocessor= prb.getPreprocessor
    preprocessor.resetLoadCase()
    preprocessor.getLoadHandler.addToDomain(comb)
    # Solution
    solution= predefined_solutions.SolutionProcedure()
    analysis= solution.simpleStaticLinear(prb)
    result= analysis.analyze(1)
    print('********** combination: '+comb)
    checkPlates(comb,studSpacing, plateGeom, infSet, supSet, supportedNodes, loadDurationFactor)
    preprocessor.getLoadHandler.removeFromDomain(comb)
        
class CombInformation:
    snowLoadDurationFactor= 1.15
    snowLoadCombinations= ['EQ1610','EQ1611','EQ1613']
    windLoadDurationFactor= 1.6
    windLoadCombinations= ['EQ1612','EQ1613','EQ1615']
    combsToStudy= ['EQ1608','EQ1609','EQ1610','EQ1611','EQ1612','EQ1613','EQ1615','LIVE']
    def printResults(self, prb, studSpacing, trussSpacing, plateGeom, infSet, supSet, supportedNodes):
        # Data
        print('Wood material: ', plateGeom.wood.name,' grade:', plateGeom.wood.grade)
        print('plate thickness= ', plateGeom.h*1e3, ' mm')
        print('stud spacing= ', studSpacing, ' m')
        print('truss spacing= ', trussSpacing, ' m\n')
        for comb in self.combsToStudy:
            loadDurationFactor= 1.0
            if(comb in self.snowLoadCombinations):
                loadDurationFactor= self.snowLoadDurationFactor
            elif( comb in self.windLoadCombinations):
                loadDurationFactor= self.windLoadDurationFactor
            printCombinationResults(prb,comb,studSpacing, plateGeom, infSet, supSet, supportedNodes, loadDurationFactor)

def checkStuds(stud, N, M, loadDurationFactor, repetitiveMemberFactor):
    ## stresses
    fc= N/stud.section.A()
    fb1= M/stud.section.getElasticSectionModulusZ()
    fb2= 0.0

    E_adj= stud.section.getEminAdj()
    Fc_adj= stud.section.getFcAdj()*loadDurationFactor
    Fb_adj= stud.section.getFbAdj()*repetitiveMemberFactor*loadDurationFactor

    #Checking
    Cp= stud.getColumnStabilityFactor(c= 0.8, E_adj= E_adj,Fc_adj= Fc_adj)
    Fc_adj*= Cp
    capacity= stud.section.A()*Fc_adj
    FcE1= stud.getFcE1(E_adj= E_adj)
    FcE2= stud.getFcE2(E_adj= E_adj)
    RB= stud.getBendingSlendernessRatioB()
    FbE= stud.getFbE(E_adj= E_adj)
    CF= stud.getCapacityFactor(E_adj, Fc_adj, Fb_adj, Fb_adj, fc,fb1, fb2)
    print('axial load:', N/1e3, ' kN', N/1e3*kNToPound, ' lb')
    print('bending moment:', M/1e3, ' kN m', M/1e3*kNmToPoundft, ' lb ft')
    print ('compression stress: ', fc/1e6, ' MPa', fc/mat.psi2Pa, ' psi')
    print('unbraced length x:', stud.getUnbracedLengthB(), ' m')
    print('unbraced length y:', stud.unbracedLengthH, ' m')
    print('Fc\'= ', Fc_adj/1e6,' MPa')
    print('Fb\'= ', Fb_adj/1e6,' MPa')
    print('E\'= ', E_adj/1e9,' GPa')
    print('stud stability factor Cp= ', Cp)
    print('stud capacity = ', capacity/1e3, ' kN')
    print('FcE1= ', FcE1/1e6,' MPa')
    print('FcE2= ', FcE2/1e6,' MPa')
    print('RB= ', RB,' m')
    print('FbE= ', FbE/1e6,' MPa')
    print('capacity factor CF= ', CF)
