

execfile('../model_gen.py') #FE model generation

from postprocess.xcVtk.CAD_model import vtk_CAD_graphic
defDisplay= vtk_CAD_graphic.RecordDefDisplayCAD()
#defDisplay.displayBlocks(setToDisplay=overallSet,caption= 'Model grid')
'''
defDisplay.displayBlocks(setToDisplay=columns,caption= columns.description)
defDisplay.displayBlocks(setToDisplay=columns,caption= beams.description)
defDisplay.displayBlocks(setToDisplay=columns,caption= slabs_H.description)
defDisplay.displayBlocks(setToDisplay=columns,caption= slabs_L.description)
'''
defDisplay.displayBlocks(setToDisplay=ramp,caption= 'Model grid')


