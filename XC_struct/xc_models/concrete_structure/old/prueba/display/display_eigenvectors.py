# -*- coding: utf-8 -*-

from postprocess.reports import graphical_reports as gr
from postprocess.xcVtk import vtk_graphic_base

execfile('../model_gen.py')
# Solution procedure
analOK= modelSpace.illConditioningAnalysis(1)
eig1= modelSpace.analysis.getEigenvalue(1)

rlcd= gr.RecordDisp()
rlcd.cameraParameters= vtk_graphic_base.CameraParameters('Custom')
rlcd.cameraParameters.viewUpVc= [0,1,0]
rlcd.cameraParameters.posCVc= [-100,100,100]
rlcd.setsToDispEigenvectors=[xcTotalSet]

preprocessor.getDomain.getMesh.normalizeEigenvectors(1)
rlcd.displayEigenvectorsOnSets(eigenMode= 1)

