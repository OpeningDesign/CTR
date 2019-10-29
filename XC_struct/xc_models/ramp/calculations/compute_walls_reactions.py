# -*- coding: utf-8 -*-
import os
from postprocess.xcVtk.FE_model import quick_graphics as QGrph
import csv

execfile('../model_gen.py')
execfile('../load_state_data.py')


#ordered list of load cases (from those defined in ../load_state_data.py
#or redefined lately) to be displayed:
loadCases=[D,Lunif]#,LconcSpan1,LconcSpan2,LconcSpan3]

#End data

csvFileWall1= open("wall_Wall1_reactions.csv", "w")
writerWall1 = csv.writer(csvFileWall1)
csvFileWall2= open("wall_Wall2_reactions.csv", "w")
writerWall2 = csv.writer(csvFileWall2)
csvFileWall3= open("wall_Wall3_reactions.csv", "w")
writerWall3 = csv.writer(csvFileWall3)

for lc in loadCases:
    lcs=QGrph.LoadCaseResults(FEcase)
    #solve for load case
    lcs.solve(loadCaseName=lc.loadCaseName,loadCaseExpr=lc.loadCaseExpr)
    #Reaction on column bases
    nodes.calculateNodalReactions(False,1e-7)
    for l in  linWall1.getLines:
        for n in l.nodes:
            reac= n.getReaction
            row= [n.tag, lc.loadCaseName, reac[2]]
            writerWall1.writerow(row)
    for l in  linWall2.getLines:
        for n in l.nodes:
            reac= n.getReaction
            row= [n.tag, lc.loadCaseName, reac[2]]
            writerWall2.writerow(row)
    for l in  linWall3.getLines:
        for n in l.nodes:
            reac= n.getReaction
            row= [n.tag, lc.loadCaseName, reac[2]]
            writerWall3.writerow(row)

csvFileWall1.close()
csvFileWall2.close()
csvFileWall3.close()




            
