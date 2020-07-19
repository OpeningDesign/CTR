execfile('./footings_xc_model.py')
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.CAD_model import vtk_CAD_graphic

displaySettings= vtk_CAD_graphic.DisplaySettingsBlockTopo()
setToDisplay= xcTotalSet
displaySettings.displayBlocks(setToDisplay,caption= setToDisplay.name+' set; blocks')
