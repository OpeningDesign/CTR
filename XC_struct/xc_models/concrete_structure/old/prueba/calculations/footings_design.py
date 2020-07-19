# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

import math
import csv
from materials.aci import ACI_materials as aci
from scipy.optimize import brentq

class ACIIsolatedFooting(object):
    ''' Design of Isolated Square and Rectangular Footings(ACI 318-14)

    :ivar id: identifier.
    :ivar b: rectangular column dimension in concrete footing design (m).
    :ivar c: rectangular column dimension in concrete footing design (m).
    :ivar concrete: footing concrete.
    :ivar ulsLoads: design loads (ultimate limit state).
    :ivar slsLoads: service loads (serviceability limit state).
    :ivar phi: shear resistance factor.
    :ivar lamb_da: modification factor for lightweight concrete.
    :ivar q_allow: allowable soil pressure.
    '''
    axialForceIndex= 5
    def __init__(self, id= None, b= 0.5, c= 0.5, concrete= aci.A36M, ulsLoads= None, slsLoads= None, q= None):
        '''
        Constructor.


        :param b: rectangular column dimension in concrete footing design (m).
        :param c: rectangular column dimension in concrete footing design (m).
        :param ulsLoads: design loads (ultimate limit state).
        :param slsLoads: service loads (serviceability limit state).
        '''
        self.id= id
        self.b= b
        self.c= c
        self.concrete= concrete
        self.ulsLoads= ulsLoads
        self.slsLoads= slsLoads
        self.q_allow= q # allowable soil pressure.
        self.phi= 0.75 #shear resistance factor.
        self.lamb_da= 1.0 # normal weight concrete.

    def getFactoredAxialForce(self):
        ''' Return the column to footing factored axial force.'''
        retval= float(self.ulsLoads[0][self.axialForceIndex])
        for l in self.ulsLoads:
            retval= max(retval,float(l[self.axialForceIndex]))
        return retval

    def getServiceAxialForce(self):
        ''' Return the column to footing service axial force.'''
        retval= float(self.slsLoads[0][self.axialForceIndex])
        combName= self.slsLoads[0][2]
        for l in self.slsLoads:
            tmp= float(l[self.axialForceIndex])
            if(retval<tmp):
                retval= tmp
                combName= l[2]
        print('P= ', retval/1e3, ' combination: ', combName)
        return retval

    def getTwoWayVc(self):
        ''' Return shear strength in concrete design for
            two-way shear.'''
        fcklb_inch2= abs(self.concrete.fck*aci.fromPascal) #Pa -> lb/inch2
        return 4.0*self.lamb_da*math.sqrt(fcklb_inch2)*aci.toPascal #lb/inch2 -> Pa
    def hf_func(self, Pu, vc):
        ''' Returns the function to find the root for.'''
        tmp= Pu/self.phi/self.getTwoWayVc()
        def hf(d):
            return 4.0*d*d+2.0*(self.b+self.c)*d-tmp
        return hf
    
    def computeApproximateFootingDepth(self):
        ''' Find an approximate footing depth.'''
        Pu= self.getFactoredAxialForce()
        vc= self.getTwoWayVc()
        print('Pu= ', Pu/1e3, ' kN')
        f= self.hf_func(Pu,vc)
        d= brentq(f, 0.0, 100.0, args=())
        return d+4.0*2.54/100.0

    def computeArea(self):
        '''Find required area of footing base.'''
        P= self.getServiceAxialForce()
        print('P= ', P/1e3, ' kN')
        return P/self.q_allow

    def computeB(self):
        '''Find required square side.'''
        return math.sqrt(self.computeArea())
    
csvFile= open('column_reactions.csv')
reader= csv.reader(csvFile)

b= 16*2.54/100.0 #column dimensions.
c= 16*2.54/100.0
q_allow= 3000.0*47.880208 # Geothecnical exploration page 5

footings= [ACIIsolatedFooting('A1',b,c, aci.A36M), ACIIsolatedFooting('A2',b,c, aci.A36M), ACIIsolatedFooting('A3',b,c, aci.A36M), ACIIsolatedFooting('A4',b,c, aci.A36M), ACIIsolatedFooting('A5',b,c, aci.A36M), ACIIsolatedFooting('B1',b,c, aci.A36M), ACIIsolatedFooting('B2',b,c, aci.A36M), ACIIsolatedFooting('B3',b,c, aci.A36M), ACIIsolatedFooting('B4',b,c, aci.A36M), ACIIsolatedFooting('B5',b,c, aci.A36M), ACIIsolatedFooting('C1',b,c, aci.A36M), ACIIsolatedFooting('C2',b,c, aci.A36M), ACIIsolatedFooting('C3',b,c, aci.A36M), ACIIsolatedFooting('C4',b,c, aci.A36M), ACIIsolatedFooting('C5',b,c, aci.A36M), ACIIsolatedFooting('D1',b,c, aci.A36M), ACIIsolatedFooting('D2',b,c, aci.A36M), ACIIsolatedFooting('D3',b,c, aci.A36M), ACIIsolatedFooting('D4',b,c, aci.A36M), ACIIsolatedFooting('D5',b,c, aci.A36M), ACIIsolatedFooting('G1',b,c, aci.A36M), ACIIsolatedFooting('G2',b,c, aci.A36M), ACIIsolatedFooting('G3',b,c, aci.A36M), ACIIsolatedFooting('G4',b,c, aci.A36M), ACIIsolatedFooting('G5',b,c, aci.A36M), ACIIsolatedFooting('F1',b,c, aci.A36M), ACIIsolatedFooting('F2',b,c, aci.A36M), ACIIsolatedFooting('F3',b,c, aci.A36M), ACIIsolatedFooting('F4',b,c, aci.A36M), ACIIsolatedFooting('F5',b,c, aci.A36M)]

ulsLoadDict= dict()
slsLoadDict= dict()
for f in footings:
    ulsLoadDict[f.id]= list()
    slsLoadDict[f.id]= list()
    
#Populate load dictionary.
for row in reader:
    if(row[2].startswith('ULS')):
        ulsLoadDict[row[0]].append(row)
    elif(row[2].startswith('SLS')):
        slsLoadDict[row[0]].append(row)

csvFile= open("footings_dimensions.csv", "w")
writer = csv.writer(csvFile)

for f in footings:
    f.ulsLoads= ulsLoadDict[f.id]
    f.slsLoads= slsLoadDict[f.id]
    f.q_allow= q_allow
    writer.writerow([f.id, f.computeApproximateFootingDepth(), f.computeB()])

csvFile.close()

