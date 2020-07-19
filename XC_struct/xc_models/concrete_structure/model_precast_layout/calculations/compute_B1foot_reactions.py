# -*- coding: utf-8 -*-
import os
from postprocess.xcVtk.FE_model import quick_graphics as QGrph
import csv

execfile('../model_gen.py')
execfile('../load_state_data.py')
execfile('../base_nodes_columns.py')

#ordered list of load cases (from those defined in ../load_state_data.py
#or redefined lately) to be displayed:
ulsLoadCases=[ULS01,ULS02_a,ULS02_b,ULS03_a,ULS03_b,ULS04_a,ULS04_b,ULS05_a,ULS05_b,ULS05_c,ULS05_d,ULS06_a,ULS06_b,ULS07_a,ULS07_b]
slsLoadCases=[SLS01,SLS02_a,SLS02_b,SLS03_a,SLS03_b,SLS04_a,SLS04_b,SLS05_a,SLS05_b]
loadCases= ulsLoadCases+slsLoadCases

#End data

csvFile= open("columnB1_reactions.csv", "w")
writer = csv.writer(csvFile)

for lc in loadCases:
    lcs=QGrph.LoadCaseResults(FEcase,loadCaseName=lc.loadCaseName,loadCaseExpr=lc.loadCaseExpr)
    #solve for load case
    lcs.solve()
    #Reaction on column bases
    nodes.calculateNodalReactions(False,1e-7)
    reac= n_colB1.getReaction
    row= [n_colB1.getProp('id'), n_colB1.tag, lc.loadCaseName, reac[0], reac[1], reac[2], reac[3], reac[4], reac[5]]
    writer.writerow(row)

csvFile.close()



            
