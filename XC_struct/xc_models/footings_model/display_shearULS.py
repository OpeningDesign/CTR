# -*- coding: utf-8 -*-
from postprocess.control_vars import *
from postprocess import limit_state_data as lsd
from postprocess.xcVtk import vtk_graphic_base
from postprocess import output_handler


model_path="./"
#Project directory structure
execfile(model_path+'project_directories.py')

modelDataInputFile=model_path+"footings_xc_model.py" #data for FE model generation
execfile(modelDataInputFile)


#Load properties to display:
fName= model_path+check_results_directory+'verifRsl_shearULS.py'
preprocessor= prep
execfile(fName)
execfile('./captionTexts.py')

limitStateLabel= lsd.shearResistance.label

#Possible arguments: 'CF', 'N', 'Vy', 'My', 'Mz', 'Vu'
argument= 'Vu'
setDisp= footingsSet 


# if("FCCP" in attributeName):
#   extrapolate_elem_attr.flatten_attribute(xcSet.elements,attributeName,1,2)

oh= output_handler.OutputHandler(modelSpace)
oh.outputStyle.cameraParameters= cameraParameters
oh.displayFieldDirs1and2(limitStateLabel,argument,setToDisplay=setDisp,component=None, fileName= None)


