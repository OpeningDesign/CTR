# -*- coding: utf-8 -*-

execfile('./xc_model.py')

# Graphic output
from postprocess.xcVtk.FE_model import quick_graphics as QGrph
from postprocess.reports import graphical_reports as gr
from postprocess.xcVtk import vtk_graphic_base

lc= gr.getRecordLoadCaseDispFromLoadPattern(cLC)
lc.setsToDispDspRot=[infSet]#[overallSet]
lc.setsToDispIntForc=[]
lc.unitsScaleLoads=1e-3
lc.unitsScaleDispl=1e3
lc.unitsDispl='[mm]'
lc.unitsScaleMom=1e-3
lc.unitsMom='[m.kN]'
lc.unitsScaleForc=1e-3
lc.unitsForc='[kN]'
lc.listDspRot=['uY']
lc.cameraParameters= vtk_graphic_base.CameraParameters('ZPos')

lc.displayDispRot()#itemToDisp='uY',setToDisplay=infSet,fConvUnits=1e3,unitDescription='mm',fileName=None,defFScale=1)
