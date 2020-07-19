# -*- coding: utf-8 -*-
in2mm=25.4
import os
import math
from postprocess.xcVtk.FE_model import quick_graphics as QGrph
from postprocess.xcVtk import vtk_graphic_base

#Data
Gwood=0.5   #specific gravity of the wood based on ovendry weight and volume at 12\% moisture content.
Kfactor=29.5  #coefficient depending on the species specific gravity
#end data

execfile('../model_gen.py')

lcs=QGrph.LoadCaseResults(feProblem=FEcase,loadCaseName='ULS1',loadCaseExpr='1.0*D+1.0*L+1.0*S')
lcs.solve()

nodes.calculateNodalReactions(True,1e-7)


def getN(ry,rz):
    return math.sqrt(ry**2+rz**2)
def getAng(ry,rz):
    ang=math.atan(ry/rz)
    return abs(ang)
def getLmin(angN,N,withdrFactor,lateralRes):
    D=withdrFactor*(math.sin(angN))**2
    C=lateralRes*(math.cos(angN))**2
    Lmin=(N*C)/(lateralRes*withdrFactor-N*D)
    return Lmin
def getWithdrRes(withdrFactor,L):
    return round(abs(withdrFactor*L),2)

def printResNode(n,withdrFactor,lateralRes):
    r=n.getReaction
    ry=-1*(round(r[1],2))  #withdrawal
    rz=-1*round(r[2],2)  #lateral
    N=round(getN(ry,rz),2)
    theta=getAng(ry,rz)
    Lmin=round(getLmin(theta,N,withdrFactor,lateralRes),2)
    withdrRes=getWithdrRes(withdrFactor,Lmin)
    print n.tag, ' & ', ry,  ' & ', rz , ' & ', round(theta,3), ' & ',N, ' & ', lateralRes,' & ',Lmin ,' & ', withdrRes,' \\\\ '

print 'Node & R$_y$ & R$_z$ & N & $\\theta$ & lat. Resist. & L$_{min}$ & withdrawal Resist.\\'
Dscrew=3/8.*in2mm   #shank diameter of the lag screw (mm)
lateralRes=round(Kfactor*Dscrew**2,2)
withdrFactor=125.4*Gwood**(3/2.)*Dscrew**(3/4.)
for n in anchorBase.getNodes:
    printResNode(n,withdrFactor,lateralRes)
print '\\hline'


Dscrew=0.875*in2mm   #shank diameter of the lag screw (mm)
lateralRes=round(Kfactor*Dscrew**2,2)
withdrFactor=125.4*Gwood**(3/2.)*Dscrew**(3/4.)
for n in anchorTop.getNodes:
    printResNode(n,withdrFactor,lateralRes)
    
