
from __future__ import division
from __future__ import print_function

import xc_base
import geom
import xc
from model import predefined_spaces
# Loads
from actions import load_cases as lcm
import check
from materials.awc_nds import AWCNDS_materials as mat

def genMesh(modelSpace, plateSection, studSpacing, trussSpacing):
    pointHandler= modelSpace.preprocessor.getMultiBlockTopology.getPoints
    infPoints= list()
    supPoints= list()
    for i in range(0,14):
        x= i*studSpacing
        infPoints.append(pointHandler.newPntFromPos3d(geom.Pos3d(x,0.0,0.0)))
        supPoints.append(pointHandler.newPntFromPos3d(geom.Pos3d(x,plateSection.h,0.0)))

    lines= modelSpace.preprocessor.getMultiBlockTopology.getLines
    infSet= modelSpace.preprocessor.getSets.defSet("inf")
    infLines= list()
    p0= infPoints[0]
    for p in infPoints[1:]:
        l= lines.newLine(p0.tag,p.tag)
        infLines.append(l)
        infSet.getLines.append(l)
        p0= p
    supSet= modelSpace.preprocessor.getSets.defSet("sup")
    supLines= list()
    p0= supPoints[0]
    for p in supPoints[1:]:
        l= lines.newLine(p0.tag,p.tag)
        supLines.append(l)
        supSet.getLines.append(l)
        p0= p
    infSet.fillDownwards()
    supSet.fillDownwards()

    # Mesh
    section= plateSection.defElasticShearSection2d(modelSpace.preprocessor)
    trfs= modelSpace.preprocessor.getTransfCooHandler
    lin= trfs.newLinearCrdTransf2d("lin")
    seedElemHandler= modelSpace.preprocessor.getElementHandler.seedElemHandler
    seedElemHandler.defaultMaterial= plateSection.xc_material.name
    seedElemHandler.defaultTransformation= "lin"
    elem= seedElemHandler.newElement("ElasticBeam2d",xc.ID([0,0]))

    xcTotalSet= modelSpace.preprocessor.getSets.getSet("total")
    mesh= infSet.genMesh(xc.meshDir.I)
    infSet.fillDownwards()
    mesh= supSet.genMesh(xc.meshDir.I)
    supSet.fillDownwards()

    ## Loaded nodes.
    loadedNodes= list()
    pos= supPoints[0].getPos+geom.Vector3d(studSpacing/2.0,0,0) #Position of the first loaded node
    xLast= supPoints[-1].getPos.x
    while pos.x<xLast:
        n= supSet.getNearestNode(pos)
        loadedNodes.append(supSet.getNearestNode(pos))
        pos+= geom.Vector3d(trussSpacing,0.0,0.0)
    print('loaded nodes: ', len(loadedNodes))

    ## Loaded elements.
    loadedElements= list()
    for e in supSet.elements:
        loadedElements.append(e)

    # Constraints
    supportedNodes= list()
    for p in infPoints:
        n= p.getNode()
        modelSpace.fixNode00F(n.tag)
        supportedNodes.append(n)

    for n in supSet.nodes:
        pos= n.getInitialPos3d
        nInf= infSet.getNearestNode(pos)
        modelSpace.constraints.newEqualDOF(nInf.tag,n.tag,xc.ID([1]))

    for p in supPoints[1:-1]:
        n= p.getNode()
        pos= n.getInitialPos3d
        nInf= infSet.getNearestNode(pos)
        modelSpace.constraints.newEqualDOF(nInf.tag,n.tag,xc.ID([0]))

    return infSet, supSet, supportedNodes, loadedNodes, loadedElements

def applyLoads(load, loadedNodes, loadedElements, trussSpacing, pointLoadFactor):
    ''' Apply load to nodes and elements.'''
    uniformLoadFactor= 1.0-pointLoadFactor
    pointLoad= pointLoadFactor*load
    for n in loadedNodes:
        n.newLoad(xc.Vector([0.0,-pointLoad,0.0]))
    uniformLoad= uniformLoadFactor*load/trussSpacing
    for e in loadedElements:
        e.vector2dUniformLoadGlobal(xc.Vector([0.0,-uniformLoad]))
    

def defineLoads(modelSpace, loadedNodes, loadedElements, deadLoad, liveLoad, snowLoad, windLoad, trussSpacing, pointLoadFactor):
    ''' Define the loads and load combinations.'''
    # Actions
    ## Load cases
    loadCaseManager= lcm.LoadCaseManager(modelSpace.preprocessor)
    loadCaseNames= ['deadLoad','liveLoad','snowLoad','windLoad']
    loadCaseManager.defineSimpleLoadCases(loadCaseNames)
    
    ## Load values.
    cLC= loadCaseManager.setCurrentLoadCase('deadLoad')
    applyLoads(deadLoad, loadedNodes, loadedElements, trussSpacing, pointLoadFactor)
    cLC= loadCaseManager.setCurrentLoadCase('liveLoad')
    applyLoads(liveLoad, loadedNodes, loadedElements, trussSpacing, pointLoadFactor)
    cLC= loadCaseManager.setCurrentLoadCase('snowLoad')
    applyLoads(snowLoad, loadedNodes, loadedElements, trussSpacing, pointLoadFactor)
    cLC= loadCaseManager.setCurrentLoadCase('windLoad')
    applyLoads(windLoad, loadedNodes, loadedElements, trussSpacing, pointLoadFactor)    

class DoublePlate(object):
    def __init__(self, title, material, studSpacing, trussSpacing, pointLoadFactor):
        '''Constructor.'''
        self.prb= xc.FEProblem()
        self.prb.title= title
        self.material = material
        preprocessor= self.prb.getPreprocessor   
        self.nodes= preprocessor.getNodeHandler
        self.modelSpace= predefined_spaces.StructuralMechanics2D(self.nodes)
        self.studSpacing= studSpacing
        self.trussSpacing= trussSpacing
        self.pointLoadFactor= pointLoadFactor
        
    def check(self, deadLoad, liveLoad, snowLoad, windLoad):
        # Create model
        infSet, supSet, supportedNodes, loadedNodes, loadedElements= genMesh(self.modelSpace, self.material, self.studSpacing, self.trussSpacing)
        
        defineLoads(self.modelSpace, loadedNodes, loadedElements, deadLoad, liveLoad, snowLoad, windLoad, self.trussSpacing, self.pointLoadFactor)
        
        # Load combination definition
        combContainer= check.combContainer
        combContainer.dumpCombinations(self.modelSpace.preprocessor)

        # Checking
        ci= check.CombInformation()
        ci.printResults(self.prb, self.studSpacing, self.trussSpacing, self.material, infSet, supSet, supportedNodes)

class Stud(object):
    def __init__(self, title, studSection, studSpacing, wallHeight):
        '''Constructor.'''
        self.title= title
        self.studSpacing= studSpacing
        self.wallHeight= wallHeight
        self.studHeight= self.wallHeight-3*2*mat.in2meter
        self.stud= mat.ColumnMember(0.3,self.studHeight, studSection)
        self.repetitiveMemberFactor= 1.15
    def printHeader(self):
        print('***** ', self.title ,' ******')
        print('wall height= ',self.wallHeight, ' m')
        print('stud height= ',self.studHeight, ' m')
        print('stud spacing= ',self.studSpacing, ' m')
        print('sections dimensions: ', str(self.stud.section.b*1e3)+'x'+str(self.stud.section.h*1e3), ' mm')
       
    def check(self, deadLoad, liveLoad, snowLoad, windLoad):
        
        snowLoadDurationFactor= 1.15
        snowLoadCombinations= ['EQ1610','EQ1611','EQ1613']
        windLoadDurationFactor= 1.6
        windLoadCombinations= ['EQ1612','EQ1613','EQ1615']
        # Load combination definition
        combContainer= check.combContainer

        # Checking
        for key in combContainer.SLS.qp:
            expr= combContainer.SLS.qp[key].expr
            value= eval(expr)
            print(key, value)
            N= value[1]*self.studSpacing
            M= value[0]*self.studHeight**2/8.0
            
            loadDurationFactor= 1.0
            if(key in snowLoadCombinations):
                loadDurationFactor= snowLoadDurationFactor
            elif( key in windLoadCombinations):
                loadDurationFactor= windLoadDurationFactor
            print('*************** comb: ', key)
            check.checkStuds(self.stud, N, M,loadDurationFactor,self.repetitiveMemberFactor)

