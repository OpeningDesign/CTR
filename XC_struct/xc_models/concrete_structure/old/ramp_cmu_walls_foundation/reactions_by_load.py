# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division

execfile('ramp_cover_reactions.py')
#execfile('ramp_cover_reactions_alcove.py')

from postprocess import get_reactions as gr
import pickle

supportNodes= list()


reactions= dict()

reactions['RA']= dict()
reactions['RB']= dict()

RAs= reactions['RA']
RBs= reactions['RB']

def resultLoadCase(prb,nmbLoadCase):
    preprocessor= prb.getPreprocessor   
    preprocessor.resetLoadCase()
    preprocessor.getLoadHandler.addToDomain(nmbLoadCase)
    #Solución
    solution= predefined_solutions.SolutionProcedure()
    analysis= solution.simpleStaticLinear(prb)
    result= analysis.analyze(1)
    nodes.calculateNodalReactions(True,1e-7)
    ra= p0.getNode().getReaction[1]
    rb= p3.getNode().getReaction[1]
    print(nmbLoadCase,' RA= ', p0.getNode().getReaction[1]/1e3, ' kN/m, RB= ', p3.getNode().getReaction[1]/1e3,' kN/m')
    #print(nmbLoadCase,' RA= ', p0.getNode().getReaction[1]/1e3,' RB= ', (p3a.getNode().getReaction[1]+p3b.getNode().getReaction[1])/1e3, ' kN/m, RC= ', p4.getNode().getReaction[1]/1e3,' kN/m')
    RAs['nmbLoadCase']= ra
    RBs['nmbLoadCase']= rb
    preprocessor.getLoadHandler.removeFromDomain(nmbLoadCase)

f = open('ramp_cover_reactions.p', 'wb')
pickle.dump(reactions, f)
f.close()

for name in loadCaseNames:
    resultLoadCase(precastPlanks,name)
