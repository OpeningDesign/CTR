# -*- coding: utf-8 -*-

from postprocess.reports import graphical_reports as gr
from postprocess.xcVtk import vtk_graphic_base

execfile('xc_model.py')
# Solution procedure

numEigenModes= 15
analOk= modelSpace.zeroEnergyModes(numEigenModes)

rlcd= gr.RecordDisp()
rlcd.cameraParameters= vtk_graphic_base.CameraParameters('Custom')
rlcd.cameraParameters.viewUpVc= [0,1,0]
rlcd.cameraParameters.posCVc= [-100,100,100]
rlcd.setsToDispEigenvectors=[xcTotalSet]

for i in range(1,numEigenModes):
   print('eig'+str(i)+'= '+str(modelSpace.analysis.getEigenvalue(i)))
   preprocessor.getDomain.getMesh.normalizeEigenvectors(i)
   rlcd.displayEigenvectorsOnSets(eigenMode= i)

