# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import xc_base
import geom
from geom_utils import DxfReader

layerNamesToImport= ['xc.*']


dxfReader= DxfReader.DXFReader("model.dxf",layerNamesToImport)

dxfReader.exportToDXF('pp.dxf')

