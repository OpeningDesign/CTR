# -*- coding: utf-8 -*-
#from postprocess.reports import graphical_reports

execfile("../model_gen.py") #FE model generation
execfile('../load_state_data.py')


#ordered list of load cases (from those defined in ../load_state_data.py
#or redefined lately) to be displayed:
loadCasesToDisplay=[ULS01,ULS02_a,ULS02_b,ULS03_a,ULS03_b,ULS04_a,ULS04_b,ULS05_a,ULS05_b,ULS05_c,ULS05_d,ULS06_a,ULS06_b,ULS07_a,ULS07_b]
#loadCasesToDisplay=[ULS01]
                    
textfl=open(cfg.reportSimplLCFile,'w')  #tex file to be generated
for lc in loadCasesToDisplay:
    lc.simplLCReports(FEproblem=FEcase,pathGr= cfg.reportSimplLCGrPath,texFile=textfl,grWdt= cfg.grWidth,capStdTexts= cfg.capTexts)

textfl.close()

