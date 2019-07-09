# -*- coding: utf-8 -*-
from postprocess.control_vars import *
from postprocess import limit_state_data as lsd
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.FE_model import vtk_display_limit_state as dls


model_path="./"
#Project directory structure
execfile(model_path+'project_directories.py')

modelDataInputFile=model_path+"footings_xc_model.py" #data for FE model generation
execfile(modelDataInputFile)


#Load properties to display:
fName= model_path+check_results_directory+'verifRsl_normStrsULS.py'
preprocessor= prep
execfile(fName)
execfile('./captionTexts.py')

limitStateLabel= lsd.normalStressesResistance.label

#Possible arguments: 'CF', 'N', 'My', 'Mz'
argument= 'CF'
setDisp= footingsSet 


# if("FCCP" in attributeName):
#   extrapolate_elem_attr.flatten_attribute(xcSet.getElements,attributeName,1,2)

dls.displayFieldDirs1and2(limitStateLabel,argument,setDisp,None,1.0,None,capTexts)


