# -*- coding: utf-8 -*-
# AISC checking convenience functions.
from __future__ import division
from __future__ import print_function

def uls_check(profile, combinations, setToCheck, analysis):
    ''' Ad-hoc ultimate limit state checking routine.'''
    preprocessor= setToCheck.getPreprocessor
    nodes= preprocessor.getNodeHandler
    for comb in combinations:
        preprocessor.resetLoadCase()
        preprocessor.getLoadHandler.addToDomain(comb)
        result= analysis.analyze(1)
        nodes.calculateNodalReactions(True,1e-7)
        VMax= -1e23
        VMin= -VMax
        MMax= -1e23
        MMin= -MMax
        for e in setToCheck.elements:
          VMax= max(VMax,max(e.getV1, e.getV2))
          VMin= min(VMin,min(e.getV1, e.getV2))
          MMax= max(MMax,max(e.getM1, e.getM2))
          MMin= min(MMin,min(e.getM1, e.getM2))
        Vmax= max(abs(VMax),abs(VMin))
        Mmax= max(abs(MMax),abs(MMin))
        Phi_b= 0.90 # LRFD
        Mu= Phi_b*profile.getWz()*profile.steelType.fy
        if(Mmax<Mu):
            print('    '+comb, 'Mmax= ', Mmax/1e3, 'kN m < ',  Mu/1e3, 'kN m F= ', Mmax/Mu, ' => OK')
        else:
            print('    '+comb, 'Mmax= ', Mmax/1e3, 'kN m > ',  Mu/1e3, 'kN m F= ', Mmax/Mu, ' => KO')
        Phi_v= 1.0 # LRFD AISC Specification section G2.1a
        Vu= Phi_v*profile.getNominalShearStrengthWithoutTensionFieldAction()
        if(Vmax<Vu):
            print('    '+comb, 'Vmax= ', Vmax/1e3, 'kN < ',  Vu/1e3, 'kN F= ', Vmax/Vu, ' => OK')
        else:
            print('    '+comb, 'Vmax= ', Vmax/1e3, 'kN > ',  Vu/1e3, 'kN F= ', Vmax/Vu, ' => KO')

def sls_check(combinations, setToCheck, deflectionLimits, analysis):
    preprocessor= setToCheck.getPreprocessor
    for comb in combinations:
        preprocessor.resetLoadCase()
        preprocessor.getLoadHandler.addToDomain(comb)
        result= analysis.analyze(1)
        uy= 0.0
        lim= deflectionLimits[comb]
        for n in setToCheck.nodes:
            uy= max(abs(n.getDisp[1]), uy)
        if(uy<lim):
            print('    '+comb, 'uy= ', uy*1e3, 'mm < ', lim*1e3, 'mm F= ', uy/lim, ' => OK')
        else:
            print('    '+comb, 'uy= ', uy*1e3, 'mm > ', lim*1e3, 'mm F= ', uy/lim, ' => KO')
