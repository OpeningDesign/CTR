# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
import csv
import math
from fractions import Fraction

execfile('sectionsDef.py')

def Float2Arch(meters):
    FEET_TO_METER= .3048
    ft= int(meters // FEET_TO_METER)
    rest= meters-ft*FEET_TO_METER
    if(abs(rest-FEET_TO_METER)<1e-3):
        ft+= 1
        rest= 0
    inch= str(round(rest/FEET_TO_METER * 12))
    return '{0}\'-{1}"'.format(ft,inch)

def rebarFormat(numBars,rebarNumber):
    n= int(math.ceil(numBars))
    return '('+str(n)+')-'+rebarNumber+ '\'s E.W. BOTTOM'

outputFile= open("footing_schedule.csv", "w")
writer= csv.writer(outputFile)

csvFile= open('footings_geometry.csv')
reader= csv.reader(csvFile)
for row in reader:
    id= row[0]
    outputRow= list()
    outputRow.append(id)
    B= float(row[6])
    strB= Float2Arch(float(row[6]))
    outputRow.append(strB)
    outputRow.append(strB)
    thickness= Float2Arch(float(row[5]))
    outputRow.append(thickness)
    reinforcement= rcSects[id]
    rebarsSpacement= reinforcement.dir1NegatvRebarRows[0].rebarsSpacing
    numBars= B/rebarsSpacement
    rebarArea= reinforcement.dir1NegatvRebarRows[0].areaRebar
    rebarNumber= ACI_materials.findNumberByArea(rebarArea)
    outputRow.append(rebarFormat(numBars,rebarNumber))
    writer.writerow(outputRow)


