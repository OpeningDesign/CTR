# -*- coding: utf-8 -*-
import os
from postprocess.xcVtk.FE_model import quick_graphics as QGrph
import csv

execfile('../model_gen.py')
execfile('../load_state_data.py')
execfile('../wall_nodes.py')

#ordered list of load cases (from those defined in ../load_state_data.py
#or redefined lately) to be displayed:
loadCases=[D,L,S,W_WE,W_NS]

#End data


northReactions= dict()
southReactions= dict()
eastReactions= dict()
westReactions= dict()

for lc in loadCases:
    northReactions[lc.loadCaseName]= 0.0
    southReactions[lc.loadCaseName]= 0.0
    eastReactions[lc.loadCaseName]= 0.0
    westReactions[lc.loadCaseName]= 0.0

for lc in loadCases:
    lcs=QGrph.LoadCaseResults(FEcase)
    #solve for load case
    lcs.solve(loadCaseName=lc.loadCaseName,loadCaseExpr=lc.loadCaseExpr)
    #Reaction on column bases
    nodes.calculateNodalReactions(False,1e-7)
    for n in wallNorth:
        reac= n.getReaction
        northReactions[lc.loadCaseName]+= reac[2]
    for n in wallSouth:
        reac= n.getReaction
        southReactions[lc.loadCaseName]+= reac[2]
    for n in wallEast:
        reac= n.getReaction
        eastReactions[lc.loadCaseName]+= reac[2]
    for n in wallWest:
        reac= n.getReaction
        westReactions[lc.loadCaseName]+= reac[2]

csvFile= open("wall_reactions.csv", "w")
writer= csv.writer(csvFile)

for key in northReactions:
    reac= northReactions[key]
    row= ['North', key, reac]
    writer.writerow(row)
for key in southReactions:
    reac= southReactions[key]
    row= ['South', key, reac]
    writer.writerow(row)
for key in eastReactions:
    reac= eastReactions[key]
    row= ['East', key, reac]
    writer.writerow(row)
for key in westReactions:
    reac= westReactions[key]
    row= ['West', key, reac]
    writer.writerow(row)

csvFile.close()



            
