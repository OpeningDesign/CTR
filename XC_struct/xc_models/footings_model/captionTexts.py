# -*- coding: utf-8 -*-

#Texts for captions (without punctuation marks)
#prefix 'fatg_' corresponds to fatigue verifications
capTexts={
    'FEmesh': 'FE mesh',
    'ULS_normalStressesResistance': 'ULS normal stresses check',
    'ULS_shearResistance': 'ULS shear check',
    'getMaxSteelStress': 'steel maximum stress',
    'SLS_frequentLoadsCrackControl': 'SLS cracking, frequent actions',
    'SLS_quasiPermanentLoadsLoadsCrackControl': 'SLS cracking, quasi-permanent actions',
}

#captions for reults of simple load cases (English version)
enCapTextsSimplLC={
    'uX':'displacement in global X direction',
    'uY':'displacement in global Y direction',
    'uZ':'displacement in global Z direction',
    'rotX':"rotation around global X axis",
    'rotY':"rotation around global Y axis",
    'rotZ':"rotation around global Z axis",
    'N1':'internal axial force in local direction 1',
    'N2':'internal axial force in local direction 2',
    'M1':'bending moment around local axis 1',
    'M2':'bending moment around local axis 2',
    'Q1':'internal shear force in local direction 1',
    'Q2':'internal shear force in local direction 2',
    'N':'internal axial force',
    'Qy':'internal shear force in local direction y',
    'Qz':'internal shear force in local direction z',
    'My':'bending moment around local axis y',
    'Mz':'bending moment around local axis z',
    'T':'internal torsional moment'
}

capTexts={
    'uX':'déplacement en direction X',
    'uY':'déplacement en direction Y',
    'uZ':'déplacement en direction Z',
    'rotX':"rotation autour de l'axe X",
    'rotY':"rotation autour de l'axe Y",
    'rotZ':"rotation autour de l'axe Z",
    'CF':'facteur de capacité',
    'getCF':'facteur de capacité',
    'N':'effort normal associé au facteur de capacité',
    'N1':'effort normal direction 1',
    'N2':'effort normal direction 2',
    'M1':'moment de flexion direction 1',
    'M2':'moment de flexion adirection 2',
    'Q1':'effort tranchant direction 1',
    'Q2':'effort tranchant direction 2',
    'Qy':'effort tranchant direction y',
    'Qz':'effort tranchant direction z',
    'My':'moment de flexion associé au facteur de capacité',
    'Mz':'moment de flexion associé au facteur de capacité',
    'Mu':'valeur ultime du moment de flexion',
    'theta':'',
    'Vy':'effort tranchant associé au facteur de capacité',
    'Vz':'effort tranchant associé au facteur de capacité',
    'Vcu':'',
    'Vsu':'',
    'Vu':"valeur ultime de l'effort tranchant",
    'LocalAxes': 'axes locaux',
    'FEmesh': 'maillage',
    'ULS_normalStressesResistance': 'Vérification ELU contraintes normales',
    'normalStressCheck': 'Vérification ELU contraintes normales',
    'ULS_shearResistance': 'Vérification ELU effort tranchant',
    'getMaxSteelStress': "contrainte maximale dans l'armature",
    'SLS_frequentLoadsCrackControl': 'Vérification ELS fissuration, cas de charge fréquents',
    'SLS_quasiPermanentLoadsLoadsCrackControl': 'Vérification ELS fissuration, cas de charge quasi-permanents',
    
}

fatg_capTexts={
    'ULS_fatigueResistance': 'Vérification ELU fatigue',
    'getAbsSteelStressIncrement': "vérification de l'armature. Différence de contrainte $\delta_{sd}(Q_{fat})$ sous les actions de fatigue",
    'concreteBendingCF':'vérification du béton. Facteur de capacité contraintes de compression',
    'concreteLimitStress':'vérification du béton. Limites contraintes de compression',
    'concreteShearCF':'vérification du béton. Facteur de capacité effort tranchant',
    'shearLimit': 'vérification du béton. Limites effort tranchant',
    'Mu': 'moment de flexion ultime',
    'Vu': 'effort tranchant ltime',

}
