# -*- coding: utf-8 -*-

from postprocess.reports import graphical_reports as gr
from postprocess.xcVtk import vtk_graphic_base

execfile('../model_gen.py')
# Solution procedure
# solu= FEcase.getSoluProc
# solCtrl= solu.getSoluControl
# solModels= solCtrl.getModelWrapperContainer
# sm= solModels.newModelWrapper("sm")
# #cHandler= sm.newConstraintHandler("transformation_constraint_handler")
# cHandler= sm.newConstraintHandler("penalty_constraint_handler")
# cHandler.alphaSP= 1.0e18
# cHandler.alphaMP= 1.0e18
# numberer= sm.newNumberer("default_numberer")
# numberer.useAlgorithm("rcm")
# analysisAggregations= solCtrl.getAnalysisAggregationContainer
# analysisAggregation= analysisAggregations.newAnalysisAggregation("analysisAggregation","sm")

# solAlgo= analysisAggregation.newSolutionAlgorithm("ill-conditioning_soln_algo")
# integ= analysisAggregation.newIntegrator("ill-conditioning_integrator",xc.Vector([]))

# soe= analysisAggregation.newSystemOfEqn("band_arpack_soe")
# soe.shift= 0.0
# solver= soe.newSolver("band_arpack_solver")
# # soe= analysisAggregation.newSystemOfEqn("sym_band_eigen_soe")
# # solver= soe.newSolver("sym_band_eigen_solver")

# analysis= solu.newAnalysis("ill-conditioning_analysis","analysisAggregation","")
analOk= modelSpace.illConditioningAnalysis(1) #analysis.analyze(1)
eig1= analysis.getEigenvalue(1)

rlcd= gr.RecordDisp()
rlcd.cameraParameters= vtk_graphic_base.CameraParameters('Custom')
rlcd.cameraParameters.viewUpVc= [0,1,0]
rlcd.cameraParameters.posCVc= [-100,100,100]
rlcd.setsToDispEigenvectors=[xcTotalSet]

preprocessor.getDomain.getMesh.normalizeEigenvectors(1)
rlcd.displayEigenvectorsOnSets(eigenMode= 1)

