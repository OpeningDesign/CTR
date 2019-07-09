# -*- coding: utf-8 -*-

import sys

wallDefinition= sys.argv[1]

print(wallDefinition)
execfile(wallDefinition)

from postprocess.reports import common_formats as fmt

reactions= {}
forces= None


#Serviceability analysis.
combContainer.dumpCombinations(preprocessor)
sls_results= wall.performSLSAnalysis(['ELS00'])
print 'SLS results= ', sls_results.rotation, sls_results.rotationComb
wall.setSLSInternalForcesEnvelope(sls_results.internalForces)

#ULS stability analysis.
sr= wall.performStabilityAnalysis(['EQ1608','EQ1609A', 'EQ1609B', 'EQ1610', 'EQ1611A', 'EQ1611B', 'EQ1612', 'EQ1613A', 'EQ1613B', 'EQ1615'],foundationSoilModel, sg_adm)

#ULS strength analysis.
uls_results= wall.performULSAnalysis(['EQ1601', 'EQ1602A', 'EQ1602B', 'EQ1603A', 'EQ1603B', 'EQ1603C', 'EQ1604A', 'EQ1604B', 'EQ1605A', 'EQ1605B'])
wall.setULSInternalForcesEnvelope(uls_results.internalForces)

pth= "./results/"
# fsr= open(pth+'verification_results.tex','w')
# sr.writeOutput(fsr)
# fsr.close()

wall.writeResult(pth)
wall.drawSchema(pth)
