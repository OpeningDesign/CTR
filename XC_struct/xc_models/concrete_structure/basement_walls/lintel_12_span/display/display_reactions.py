# -*- coding: utf-8 -*-
import os
from postprocess.xcVtk.FE_model import quick_graphics as QGrph
from postprocess.xcVtk import vtk_graphic_base

execfile('../model_gen.py')

lcs=QGrph.LoadCaseResults(feProblem=FEcase,loadCaseName='LC1',loadCaseExpr='1.2*D+1.6*L+0.5*S')
lcs.solve()
lcs.displayReactions(setToDisplay=overallSet,fConvUnits=1.0,scaleFactor=1.0,unitDescription= '[m,kN]',viewDef= vtk_graphic_base.CameraParameters('XYZPos'),fileName=None,defFScale=0.0)
