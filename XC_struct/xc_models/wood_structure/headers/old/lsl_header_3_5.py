# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division
import xc_base
import geom
import xc
from model import predefined_spaces
from solution import predefined_solutions
from materials.sections import section_properties
from materials import typical_materials

# Loads
from actions import load_cases as lcm

# Units
inchToMeter= 2.54/100.0
footToMeter= 0.3048
poundToN= 4.44822
psiToPa= 6894.76

# Problem type
lslHeader= xc.FEProblem()
lslHeader.title= 'Header L= 3.75 feet on first floor'
preprocessor= lslHeader.getPreprocessor
nodes= preprocessor.getNodeHandler
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)

# Materials LSL 1.55E (page 4 of the PDF document from "SolidStart")
sectionGeometry= section_properties.RectangularSection("header",b=3.5*inchToMeter,h=(11+7.0/8)*inchToMeter)
LSL= typical_materials.MaterialData(name='LSL',E=1.55e6*psiToPa,nu=0.2,rho=500)
section= sectionGeometry.defElasticShearSection2d(preprocessor,LSL)

# Header geometry
headerSpan= 3.75*footToMeter
centerSpacing= 24.0*inchToMeter # Distance between trusses
## Key points
pointHandler= preprocessor.getMultiBlockTopology.getPoints
p0= pointHandler.newPntFromPos3d(geom.Pos3d(0.0,0.0,0.0))
p1= pointHandler.newPntFromPos3d(geom.Pos3d(headerSpan,0.0,0.0))

## Lines
lineHandler= preprocessor.getMultiBlockTopology.getLines
l1= lineHandler.newLine(p0.tag,p1.tag)
l1.setElemSize(centerSpacing)

# Mesh
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)
trfs= preprocessor.getTransfCooHandler
lin= trfs.newLinearCrdTransf2d("lin")
seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultMaterial= section.name
seedElemHandler.defaultTransformation= "lin"
elem= seedElemHandler.newElement("ElasticBeam2d",xc.ID([0,0]))

xcTotalSet= preprocessor.getSets.getSet('total')

mesh= xcTotalSet.genMesh(xc.meshDir.I)

# Constraints
modelSpace.fixNode00F(p0.getNode().tag)
modelSpace.fixNode00F(p1.getNode().tag)

# Actions
loadCaseManager= lcm.LoadCaseManager(preprocessor)
loadCaseNames= ['load']
loadCaseManager.defineSimpleLoadCases(loadCaseNames)

## Loads on nodes.
cLC= loadCaseManager.setCurrentLoadCase('load')
punctualLoad= xc.Vector([0.0,-3*9.64e3,0.0]) # Loads at first floor (see CD reactions.ods).
for n in xcTotalSet.nodes:
    n.newLoad(punctualLoad)


#We add the load case to domain.
preprocessor.getLoadHandler.getLoadPatterns.addToDomain('load')

# Solution
# Linear static analysis.
analysis= predefined_solutions.simple_static_linear(lslHeader)
result= analysis.analyze(1)

# Checking
nodes.calculateNodalReactions(True,1e-7)
Vmax= max(p0.getNode().getReaction[1],p1.getNode().getReaction[1])
eMidSpan= xcTotalSet.getNearestElement(geom.Pos3d(headerSpan/2.0,0.0,0.0))
Mmax= max(abs(eMidSpan.getM1),abs(eMidSpan.getM2))
print('Uniform load: ', 2.0*Vmax/headerSpan/1e3, ' kN/m')

## Shear
Vu= 11360.0*poundToN
print('Vmax= ', Vmax/1e3, ' kN Vu= ', Vu/1e3, ' kN; F= ',Vmax/Vu)

## Bending
Mu= 16198.0*poundToN*footToMeter
print('Mmax= ', Mmax/1e3, ' kN.m Mu= ', Mu/1e3, ' kN.m; F= ',Mmax/Mu)

## Deflection
ratioI= sectionGeometry.Iz()/(488*(0.0254)**4)
nMidSpan= l1.getNearestNode(geom.Pos3d(headerSpan/2.0,0.0,0.0))
dMidSpan= ratioI*nMidSpan.getDisp[1]
ratio1= abs(dMidSpan)/headerSpan
print('dY= ',dMidSpan*1e3,' mm; ratio= L/', 1.0/ratio1, 'L= ', headerSpan, ' m')
