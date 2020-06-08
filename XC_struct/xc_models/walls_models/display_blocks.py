execfile('./basement_wall.py')
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.CAD_model import vtk_CAD_graphic

displaySettings= vtk_CAD_graphic.DisplaySettingsBlockTopo()
displaySettings.cameraParameters= vtk_graphic_base.CameraParameters('ZPos') 
setToDisplay= totalSet
displaySettings.displayBlocks(setToDisplay,caption= setToDisplay.name+' set; blocks')
