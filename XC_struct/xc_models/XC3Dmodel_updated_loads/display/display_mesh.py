# -*- coding: utf-8 -*-

execfile("../model_gen.py") #FE model generation
#execfile("../pp.py")
from postprocess.xcVtk.FE_model import vtk_FE_graphic

#  caption:  text to write in the graphic
#  defFScale: factor to apply to current displacement of nodes so that the
#             display position of each node equals to the initial position plus
#             its displacement multiplied by this factor. (Defaults to 0.0,
#             i.e. display of initial/undeformed shape)
#  fName:     name of the graphic file to create (defaults to None -> screen
#             window).
#  nodeSize:  size of the points that represent nodes (defaults to 0.01)
#  scaleConstr: scale of SPContraints symbols (defaults to 0.2)

defDisplay= vtk_FE_graphic.RecordDefDisplayEF()
#setsTodisp=[beams,columns,slabs]
#setsTodisp=[beams+columns]
#setsTodisp=[slab5W]
#setsTodisp=[slabs]
#setsTodisp=[beams,columns]
setsTodisp=[stag2Set]
# sett=beams+columns
# sett.color=cfg.colors['brown04']
# setsTodisp=[sett]
defDisplay.displayMesh(xcSets=setsTodisp,fName= None,caption='Precast beams and columns',nodeSize=0.5,scaleConstr=1.0)
