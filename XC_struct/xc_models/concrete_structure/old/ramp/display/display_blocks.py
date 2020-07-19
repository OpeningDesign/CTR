

execfile('../model_gen.py') #FE model generation

from postprocess.xcVtk.CAD_model import vtk_CAD_graphic
displaySettings= vtk_CAD_graphic.DisplaySettingsBlockTopo()
#displaySettings.displayBlocks(setToDisplay=overallSet,caption= 'Model grid')
'''
displaySettings.displayBlocks(setToDisplay=columns,caption= columns.description)
displaySettings.displayBlocks(setToDisplay=columns,caption= beams.description)
displaySettings.displayBlocks(setToDisplay=columns,caption= slabs_H.description)
displaySettings.displayBlocks(setToDisplay=columns,caption= slabs_L.description)
'''
displaySettings.displayBlocks(setToDisplay=ramp,caption= 'Model grid')


