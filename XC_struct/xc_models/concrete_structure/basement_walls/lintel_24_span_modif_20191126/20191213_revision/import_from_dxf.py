# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

from import_export import dxf_reader
from import_export import neutral_mesh_description as nmd

layerNamesToImport= ['concrete_cells','rebars_10','rebars_06','link_lines','rebar_segments_13','rebar_segments_16','rebar_segments_22', '000FFF_constraints', '00FFFF_constraints', '000000_constraints', 'horiz_loads']

def getRelativeCoo(pt):
  return [pt[0],pt[1],pt[2]] #No modification.

fileName= 'lintel_model.dxf'
#fileName= 'pp.dxf'
dxfImport= dxf_reader.DXFImport(fileName, layerNamesToImport,getRelativeCoo, importLines= True, polylinesAsSurfaces= False, threshold= 0.001, tolerance= .001)

#Block topology
blocks= dxfImport.exportBlockTopology('test')

fileName= 'xc_model_blocks'
ieData= nmd.XCImportExportData()
ieData.outputFileName= fileName
ieData.problemName= 'FEcase'
ieData.blockData= blocks

ieData.writeToXCFile()
