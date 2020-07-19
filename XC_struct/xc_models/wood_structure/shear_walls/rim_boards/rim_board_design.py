# -*- coding: utf-8 -*-
''' Design of rim boards for shear transmission on shear walls
    according to the data from:

    LP® SOLIDSTART® OSB & LSLRIM BOARD U.S. (ASD) TECHNICAL GUIDE
    APA Rated OSB and 1.35E LSL
'''

from __future__ import print_function
from __future__ import division
import csv

psi2Pa= 6894.76
inch2meter= 25.4e-3

boardThickness= 1.0*inch2meter
CD= 1.6 # Load duration factor. 
Fv_osb= CD*270.0*psi2Pa
q_osb= Fv_osb*boardThickness
Fv_lvl= CD*410.0*psi2Pa

with open('nominal_unit_shear_capacities_rev03.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    headers = next(csv_reader, None)
    shearPerUnitLengthIndex= headers.index('Shear/m')
    units = next(csv_reader, None)
    for row in csv_reader:
        name= row[0]
        if(name!=''):
            shearPerUnitLength= float(row[shearPerUnitLengthIndex])*1e3
            requiredOSBThickness= shearPerUnitLength/Fv_osb
            requiredLVLThickness= shearPerUnitLength/Fv_lvl
            print(name, shearPerUnitLength/1e3,'kN/m, required OSB thickness: ', requiredOSBThickness*1e3,'mm, required LVL thickness: ', requiredLVLThickness*1e3,'mm')
