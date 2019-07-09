# -*- coding: utf-8 -*-
from postprocess.control_vars import *
from postprocess import limit_state_data as lsd
from postprocess.xcVtk.FE_model import vtk_FE_graphic
from postprocess.xcVtk import control_var_diagram as cvd

execfile("../model_gen.py") #FE model generation

#Load properties to display:
execfile(cfg.verifCrackFreqFile)

#  Config
argument= 'wk'      #Available arguments: 'N', 'My','Mz','s_rmax','eps_sm','wk'
setsDispRes=[beamX]  #list of linear elements sets for which to display results 
setDisp=overallSet   #set of elements (any type) to be displayed
scaleFactor=1e2        #scale factor for the diagram (can be negative)
fUnitConv=1e3          #unit conversion factor (i.e m->mm => fUnitConv= 1e3)
#  End config 


diagram= cvd.ControlVarDiagram(scaleFactor=scaleFactor,fUnitConv=fUnitConv,sets=setsDispRes,attributeName=lsd.freqLoadsCrackControl.label,component=argument)
diagram.addDiagram()
defDisplay= vtk_FE_graphic.RecordDefDisplayEF()
defDisplay.setupGrid(setDisp)
defDisplay.defineMeshScene(None,defFScale=0.0)
defDisplay.appendDiagram(diagram) #Append diagram to the scene.
caption= cfg.capTexts[lsd.freqLoadsCrackControl.label] + ', ' + cfg.capTexts[argument] + '. '+ setsDispRes[0].description.capitalize() + ', ' 
defDisplay.displayScene(caption)



