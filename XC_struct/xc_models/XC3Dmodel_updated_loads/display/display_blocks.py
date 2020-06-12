

execfile('../model_gen.py') #FE model generation

from postprocess.xcVtk.CAD_model import vtk_CAD_graphic
displaySettings= vtk_CAD_graphic.DisplaySettingsBlockTopo()
#displaySettings.displayBlocks(setToDisplay=overallSet,caption= 'Model grid')
'''
displaySettings.displayBlocks(setToDisplay=columns,caption= columns.description)
displaySettings.displayBlocks(setToDisplay=beams,caption= beams.description)
displaySettings.displayBlocks(setToDisplay=slabs_H,caption= slabs_H.description)
displaySettings.displayBlocks(setToDisplay=slabs_L,caption= slabs_L.description)
'''
displaySettings.displayBlocks(setToDisplay=stag2Set,caption= 'Model grid')


