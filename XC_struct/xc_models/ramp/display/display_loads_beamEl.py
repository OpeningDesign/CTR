# -*- coding: utf-8 -*-

from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.FE_model import quick_graphics as qg

execfile('../model_gen.py')
execfile('../load_state_data.py')

#available components: 'axialComponent', 'transComponent', 'transYComponent',
#                      'transZComponent'

loadCasesToDisplay=[Q3,Q4,Q5,Q6,Q7]
#loadCasesToDisplay=[LS1,LS2]
#loadCasesToDisplay=[Q9]
#End data

for lc in loadCasesToDisplay:
    for st in lc.setsToDispBeamLoads:
        lcs=qg.QuickGraphics(FEcase)
        capt=lc.loadCaseDescr + ', ' + st.description + ', '  + lc.unitsLoads
        lcs.dispLoadCaseBeamEl(loadCaseName=lc.loadCaseName,setToDisplay=st,fUnitConv=lc.unitsScaleLoads,elLoadComp=lc.compElLoad,elLoadScaleF=lc.vectorScaleLoads,nodLoadScaleF=lc.vectorScalePointLoads,viewDef= lc.cameraParameters,caption= capt,fileName=None)

