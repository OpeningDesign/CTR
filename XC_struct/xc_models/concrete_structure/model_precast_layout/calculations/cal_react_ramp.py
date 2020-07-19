import os
from postprocess.xcVtk.FE_model import quick_graphics as QGrph
import csv

execfile('../model_gen.py')
execfile('../load_state_data.py')

length=yCols[1]
Reactions= dict()
for l in LC:
    Reactions[l.loadCaseName]= 0.0

for l in LC:
    lcs=QGrph.LoadCaseResults(FEcase,l.loadCaseName,l.loadCaseExpr)
    lcs.solve()
    nodes.calculateNodalReactions(False,1e-7)
    for n in nodRamp:
        reac= n.getReaction
        Reactions[l.loadCaseName]+= reac[2]/length

csvFile= open("ramp_wall_react.csv", "w")
writer= csv.writer(csvFile)

for key in Reactions:
    reac= round(Reactions[key],2)
    row= ['Rz [N/m]', key, reac]
    writer.writerow(row)

csvFile.close()

