

execfile('../model_gen.py') #FE model generation

from postprocess.xcVtk.CAD_model import vtk_CAD_graphic
defDisplay= vtk_CAD_graphic.RecordDefDisplayCAD()
#defDisplay.displayBlocks(xcSet=overallSet,fName= None,caption= 'Model grid')
'''
xcSet=columns
defDisplay.displayBlocks(xcSet=columns,fName= None,caption= xcSet.description)
xcSet=beams
defDisplay.displayBlocks(xcSet=beams,fName= None,caption= xcSet.description)
xcSet=slabs_H
defDisplay.displayBlocks(xcSet=slabs_H,fName= None,caption= xcSet.description)
xcSet=slabs_L
defDisplay.displayBlocks(xcSet=slabs_L,fName= None,caption= xcSet.description)
'''
defDisplay.displayBlocks(xcSet=ramp,fName= None,caption= 'Model grid')


