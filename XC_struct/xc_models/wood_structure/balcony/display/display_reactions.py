# -*- coding: utf-8 -*-
import os
from postprocess.xcVtk.FE_model import quick_graphics as QGrph
from postprocess.xcVtk import vtk_graphic_base

execfile('../model_gen.py')

#lcs=QGrph.LoadCaseResults(feProblem=FEcase,loadCaseName='LC1',loadCaseExpr='1.2*D+1.6*L+0.5*S')
#Allowable
#lcs=QGrph.LoadCaseResults(feProblem=FEcase,loadCaseName='LC1',loadCaseExpr='1.0*D+1.0*L+1.0*S')
lcs=QGrph.LoadCaseResults(feProblem=FEcase,loadCaseName='LC1',loadCaseExpr='1.0*D+1.0*S')
lcs.solve()
lcs.displayReactions(setToDisplay=overallSet)
