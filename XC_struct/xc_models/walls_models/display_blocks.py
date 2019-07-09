execfile('./basement_wall.py')
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.CAD_model import vtk_CAD_graphic

defDisplay= vtk_CAD_graphic.RecordDefDisplayCAD()
defDisplay.cameraParameters= vtk_graphic_base.CameraParameters('ZPos') 
setToDisplay= totalSet
defDisplay.displayBlocks(setToDisplay,caption= setToDisplay.name+' set; blocks')
