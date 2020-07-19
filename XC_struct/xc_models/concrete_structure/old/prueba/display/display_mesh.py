# -*- coding: utf-8 -*-

execfile("../model_gen.py") #FE model generation
#execfile("../pp.py")
from postprocess.xcVtk.FE_model import vtk_FE_graphic

#  caption:  text to write in the graphic
#  defFScale: factor to apply to current displacement of nodes so that the
#             display position of each node equals to the initial position plus
#             its displacement multiplied by this factor. (Defaults to 0.0,
#             i.e. display of initial/undeformed shape)

#  nodeSize:  size of the points that represent nodes (defaults to 0.01)
#  scaleConstr: scale of SPContraints symbols (defaults to 0.2)

displaySettings= vtk_FE_graphic.DisplaySettingsFE()
#setsTodisp=[beams,columns,slabs]
#setsTodisp=[beams+columns]
#setsTodisp=[slab5W]
#setsTodisp=[slabs]
#setsTodisp=[beams,columns]
#setsTodisp=[columns]
#setsTodisp=[slabs,beams,columns]
#setsTodisp=[slabs]
#setsTodisp=[slabs5_L]
# sett=beams+columns
# sett.color=cfg.colors['brown04']
# setsTodisp=[sett]
#setsTodisp=[slabW1,slab12,slab23,slab34,slab45,slab5W,slabBC,slabCD_H,slabCD_L,slabDG,slabGF,slabFW]
#setsTodisp=[slabsBC_L,slabCD_L,slabsF_L]
setsTodisp=[rampNeighboursPlanksSet]
displaySettings.displayMesh(xcSets=setsTodisp,caption='Precast beams and columns',nodeSize=0.5,scaleConstr=1.0)
