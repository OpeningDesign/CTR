execfile('./footings_xc_model.py')
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.CAD_model import vtk_CAD_graphic

defDisplay= vtk_CAD_graphic.RecordDefDisplayCAD()
setToDisplay= xcTotalSet
defDisplay.displayBlocks(setToDisplay,caption= setToDisplay.name+' set; blocks')
