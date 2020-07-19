# -*- coding: utf-8 -*-
#from postprocess.reports import graphical_reports

execfile("../model_gen.py") #FE model generation

#Load properties to display:
execfile(workingDirectory+'load_state_data.py')



#ordered list of load cases (from those defined in ../load_state_data.py
#or redefined lately) to be displayed:
loadCasesToDisplay=ULSs
#loadCasesToDisplay=LSD_disp
outFile=cfg.projectDirTree.getReportSimplLCFile()
textfl=open(outFile,'w')  #tex file to be generated
for lc in loadCasesToDisplay:
    lc.simplLCReports(FEproblem=FEcase,texFile=textfl,cfg= cfg)

textfl.close()

