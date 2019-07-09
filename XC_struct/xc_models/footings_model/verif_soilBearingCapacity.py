# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import math
import os
import csv
import xc_base
import geom
import xc
from postprocess import limit_state_data as lsd

model_path="./"
#Project directory structure
execfile("project_directories.py")


csvFile= open('column_reactions.csv')
reader= csv.reader(csvFile)
loadsOnFooting= dict()
for row in reader:
    id= row[0]
    if id not in loadsOnFooting:
        loadsOnFooting[id]= dict()
    loadCaseName= row[2]
    if(loadCaseName.startswith('SLS')):
        load= xc.Vector([-float(row[3]),-float(row[4]),-float(row[5]),-float(row[6]),-float(row[7]),-float(row[8])])
        loadsOnFooting[id][loadCaseName]= load

admStress= 3000.0 * 0.04788026e3 #N/m2
csvFile= open('footings_geometry.csv')
reader= csv.reader(csvFile)
worstCases= dict()
for row in reader:
    id= row[0]
    if id not in worstCases:
        worstCases[id]= (0.0,None,None,0.0)
    B= float(row[6])
    area= B**2
    loads= loadsOnFooting[id]
    for key in loads:
        load= loads[key]
        P= load[2]
        Mx= load[3]
        ex= Mx/P
        My= load[4]
        ey= My/P
        despegue= ((abs(ex)>B/6.0 or abs(ey)>B/6.0))
        stress= P/area
        F= abs(stress/admStress)
        if(F>worstCases[id][0]):
            worstCases[id]= (F,id,key,P)

for key in worstCases:
    c= worstCases[key]
    if(c[0]>1.0):
        P= c[3]
        newArea= abs(P/admStress)
        newB= math.sqrt(newArea)
        print(c,newB,' m', newB/0.3048, ' ft')
