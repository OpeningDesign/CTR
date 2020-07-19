# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
import sys
import os
import csv

arg1= str(sys.argv[1])
fileName= os.path.splitext(arg1)[0]

outputFileNameReactions= fileName+'_reactions.csv'
csvFileReactions= open(outputFileNameReactions,'w')
writerReactions= csv.writer(csvFileReactions)
outputFileNameDispl= fileName+'_displ.txt'
writerDispl= open(outputFileNameDispl,'w')
writerReactions.writerow(['comb','floor','truss','Rx', 'Ry', 'Rz', 'Rx', 'Ry','Rz', 'truss', 'Rx', 'Ry', 'Rz','Rx', 'Ry', 'Rz'])
writerReactions.writerow(['','','name','(kN)', '(kN)', '(kN)', '(kN)', '(kN)','(kN)', 'name', '(kN)', '(kN)', '(kN)','(kN)', '(kN)', '(kN)'])

execfile(str(sys.argv[1]))

def writeResults(combName, floor, trusses):
    for t in trusses:
        d= t.getDeflection()
        writerDispl.write(combName+' '+t.name+': '+str(d[0]*1e3)+' mm (L/'+str(int(d[1]))+'; L= '+str(t.span())+' m) ----')
    writerDispl.write('\n')
    preprocessor.getNodeHandler.calculateNodalReactions(False,1e-7)
    outputRow= [combName, floor]
    for t in trusses:
        r= t.getReactions()
        outputRow.extend([t.name, r[0][0]/1e3, r[0][1]/1e3, r[0][2]/1e3,r[1][0]/1e3, r[1][1]/1e3, r[1][2]/1e3])
    writerReactions.writerow(outputRow)    


def resultComb(prb,nmbComb):
    preprocessor.resetLoadCase()
    preprocessor.getLoadHandler.addToDomain(nmbComb)
    #Solución
    solution= predefined_solutions.SolutionProcedure()
    analysis= solution.simpleStaticLinear(prb)
    result= analysis.analyze(1)
    reportResults(nmbComb)
    preprocessor.getLoadHandler.removeFromDomain(nmbComb)


for comb in ['EQ1608','EQ1609','EQ1610','EQ1611','EQ1612','EQ1613','EQ1615','LIVE']:
  resultComb(feProblem,comb)

writerDispl.close()
csvFileReactions.close()
