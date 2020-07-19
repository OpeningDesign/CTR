#execfile('./xc_model.py')
execfile('./shear_walls_east_rev01.py')
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.CAD_model import vtk_CAD_graphic

displaySettings= vtk_CAD_graphic.DisplaySettingsBlockTopo()
displaySettings.cameraParameters= vtk_graphic_base.CameraParameters('Custom')
displaySettings.cameraParameters.viewUpVc= [0,0,1]
displaySettings.cameraParameters.posCVc= [0,-100,0]
setToDisplay= xcTotalSet
displaySettings.displayBlocks(setToDisplay,caption= setToDisplay.name+' set')
