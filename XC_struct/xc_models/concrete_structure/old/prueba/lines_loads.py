
# Lines 1 (Y direct)
k=zList.index(zBeamHigh)

linL1_rg=list()
i=xList.index(xWF[3])
j1=yList.index(yWF[4])
j2=yList.index(yWF[-1])
linL1_rg.append(gm.IJKRange((i,j1,k),(i,j2,k)))
i=xList.index(xWF[9])
linL1_rg.append(gm.IJKRange((i,j1,k),(i,j2,k)))

ptL1=gridGeom.getSetPntMultiRegion(linL1_rg,'ptL1')
lnL1=sets.get_lines_on_points(ptL1,'lnL1')


#Lines 2 (X direct)
k=zList.index(zBeamHigh) 

linL2_rg=list()
j=yList.index(yWF[4]-gap/2.0)
i1=xList.index(xWF[1])
i2=xList.index(xWF[3])
linL2_rg.append(gm.IJKRange((i1,j,k),(i2,j,k)))
j=yList.index(yWF[4])
i1=xList.index(xWF[9])
i2=xList.index(xWF[11])
linL2_rg.append(gm.IJKRange((i1,j,k),(i2,j,k)))
j=yList.index(yWF[3])
i1=xList.index(xWF[1])
i2=xList.index(xWF[3])
linL2_rg.append(gm.IJKRange((i1,j,k),(i2,j,k)))
i1=xList.index(xWF[10])
i2=xList.index(xWF[11])
linL2_rg.append(gm.IJKRange((i1,j,k),(i2,j,k)))

ptL2=gridGeom.getSetPntMultiRegion(linL2_rg,'ptL2')
lnL2=sets.get_lines_on_points(ptL2,'lnL2')

#Lines 3
k=zList.index(zBeamHigh)

linL3_rg=list()
i=xList.index(xWF[2])
j1=yList.index(yWF[1])
j2=yList.index(yWF[3])
linL3_rg.append(gm.IJKRange((i,j1,k),(i,j2,k)))
i=xList.index(xWF[4])
j1=yList.index(yWF[2])
j2=yList.index(yWF[4])
linL3_rg.append(gm.IJKRange((i,j1,k),(i,j2,k)))
i=xList.index(xWF[10])
j1=yList.index(yWF[1])
j2=yList.index(yWF[3])
linL3_rg.append(gm.IJKRange((i,j1,k),(i,j2,k)))
i=xList.index(xWF[8])
j1=yList.index(yWF[2])
j2=yList.index(yWF[4])
linL3_rg.append(gm.IJKRange((i,j1,k),(i,j2,k)))

ptL3=gridGeom.getSetPntMultiRegion(linL3_rg,'ptL3')
lnL3=sets.get_lines_on_points(ptL3,'lnL3')

#Lines 4
k=zList.index(zBeamHigh)

linL4_rg=list()
i=xList.index(xWF[10])
j1=yList.index(yWF[0])
j2=yList.index(yWF[1])
linL4_rg.append(gm.IJKRange((i,j1,k),(i,j2,k)))

ptL4=gridGeom.getSetPntMultiRegion(linL4_rg,'ptL4')
lnL4=sets.get_lines_on_points(ptL4,'lnL4')

#Lines 5
k=zList.index(zBeamHigh)

linL5_rg=list()
j=yList.index(yWF[2])
i1=xList.index(xWF[4])
i2=xList.index(xWF[6])
linL5_rg.append(gm.IJKRange((i1,j,k),(i2,j,k)))
i1=xList.index(xWF[7])
i2=xList.index(xWF[9])
linL5_rg.append(gm.IJKRange((i1,j,k),(i2,j,k)))

ptL5=gridGeom.getSetPntMultiRegion(linL5_rg,'ptL5')
lnL5=sets.get_lines_on_points(ptL5,'lnL5')

#Lines 6
k=zList.index(zBeamHigh)

linL6_rg=list()
j=yList.index(yWF[1])
i1=xList.index(xWF[2])
i2=xList.index(xWF[10])
linL6_rg.append(gm.IJKRange((i1,j,k),(i2,j,k)))
# i1=xList.index(xWF[6])
# i2=xList.index(xWF[10])
# linL6_rg.append(gm.IJKRange((i1,j,k),(i2,j,k)))

ptL6=gridGeom.getSetPntMultiRegion(linL6_rg,'ptL6')
lnL6=sets.get_lines_on_points(ptL6,'lnL6')

#Lines 7
k=zList.index(zBeamHigh)

linL7_rg=list()
#i=xList.index(xWF[6]-gap/2.)
i=xList.index(xWF[6])
j1=yList.index(yWF[2])
j2=yList.index(yWF[-1])
linL7_rg.append(gm.IJKRange((i,j1,k),(i,j2,k)))
i=xList.index(xWF[7]+gap/2.)
linL7_rg.append(gm.IJKRange((i,j1,k),(i,j2,k)))

ptL7=gridGeom.getSetPntMultiRegion(linL7_rg,'ptL7')
lnL7=sets.get_lines_on_points(ptL7,'lnL7')

#Lines 8
k=zList.index(zBeamHigh)

linL8_rg=list()
k=zList.index(zBeamHigh) 
j=yList.index(yWF[2])
i1=xList.index(xWF[6])
i2=xList.index(xWF[7])
linL8_rg.append(gm.IJKRange((i1,j,k),(i2,j,k)))

j=yList.index(yWF[-1])
i1=xList.index(xWF[0])
i2=xList.index(xWF[6])
linL8_rg.append(gm.IJKRange((i1,j,k),(i2,j,k)))
i1=xList.index(xWF[7])
i2=xList.index(xWF[-1])
linL8_rg.append(gm.IJKRange((i1,j,k),(i2,j,k)))

ptL8=gridGeom.getSetPntMultiRegion(linL8_rg,'ptL8')
lnL8=sets.get_lines_on_points(ptL8,'lnL8')

#Lines 9
k=zList.index(zBeamHigh)

linL9_rg=list()
i=xList.index(xWF[-1])
j1=yList.index(yWF[0])
j2=yList.index(yWF[-1])
linL9_rg.append(gm.IJKRange((i,j1,k),(i,j2,k)))

ptL9=gridGeom.getSetPntMultiRegion(linL9_rg,'ptL9')
lnL9=sets.get_lines_on_points(ptL9,'lnL9')

#Lines 10 (X direct)
k=zList.index(zBeamHigh) 

linL10_rg=list()
j=yList.index(yWF[0])
i1=xList.index(xWF[5])
i2=xList.index(xWF[-1])
linL10_rg.append(gm.IJKRange((i1,j,k),(i2,j,k)))

ptL10=gridGeom.getSetPntMultiRegion(linL10_rg,'ptL10')
lnL10=sets.get_lines_on_points(ptL10,'lnL10')

#Lines 11 (X direct)
k=zList.index(zBeamHigh) 

linL11_rg=list()
j=yList.index(yWF[0])
i1=xList.index(xWF[0])
i2=xList.index(xWF[5])
linL11_rg.append(gm.IJKRange((i1,j,k),(i2,j,k)))

ptL11=gridGeom.getSetPntMultiRegion(linL11_rg,'ptL11')
lnL11=sets.get_lines_on_points(ptL11,'lnL11')

# Lines 12 (Y direct)

k=zList.index(zBeamHigh)

linL12_rg=list()
i=xList.index(xWF[0])
j1=yList.index(yWF[0])
j2=yList.index(yWF[4])
linL12_rg.append(gm.IJKRange((i,j1,k),(i,j2,k)))

ptL12=gridGeom.getSetPntMultiRegion(linL12_rg,'ptL12')
lnL12=sets.get_lines_on_points(ptL12,'lnL12')

# Lines 13 (Y direct)

k=zList.index(zBeamHigh)

linL13_rg=list()
i=xList.index(xWF[0])
j1=yList.index(yWF[4])
j2=yList.index(yWF[-1])
linL13_rg.append(gm.IJKRange((i,j1,k),(i,j2,k)))

ptL13=gridGeom.getSetPntMultiRegion(linL13_rg,'ptL13')
lnL13=sets.get_lines_on_points(ptL13,'lnL13')


#Lines for wind loads
lnL1W=lnL1+lnL2+lnL3+lnL4+lnL5+lnL6
lnL2W=lnL9

linL3W_rg=list()
j1=yList.index(yWF[2])
j2=yList.index(yWF[-1])
i=xList.index(xWF[7]+gap/2.)
linL3W_rg.append(gm.IJKRange((i,j1,k),(i,j2,k)))

ptL3W=gridGeom.getSetPntMultiRegion(linL3W_rg,'ptL3W')
lnL3W=sets.get_lines_on_points(ptL3W,'lnL3W')

linL4W_rg=list()
#i=xList.index(xWF[6]-gap/2.)
i=xList.index(xWF[6])
j1=yList.index(yWF[2])
j2=yList.index(yWF[-1])
linL4W_rg.append(gm.IJKRange((i,j1,k),(i,j2,k)))

ptL4W=gridGeom.getSetPntMultiRegion(linL4W_rg,'ptL4W')
lnL4W=sets.get_lines_on_points(ptL4W,'lnL4W')

lnL5W=lnL12+lnL13

#wind N-S
lnL7W=lnL8
lnL6W=lnL10+lnL11

#2019/10/07
#Lines E1A (X direct)
k=zList.index(zBeamHigh) 

linE1A_rg=list()
j=yList.index(yWF[1]+gap/2.)
i1=xList.index(xWF[0])
i2=xList.index(xWF[1])
linE1A_rg.append(gm.IJKRange((i1,j,k),(i2,j,k)))
ptE1A=gridGeom.getSetPntMultiRegion(linE1A_rg,'ptE1A')
lnE1A=sets.get_lines_on_points(ptE1A,'lnE1A')

#Lines E1B (X direct)
linE1B_rg=list()
j=yList.index(yQW[2])
i1=xList.index(xWF[0])
i2=xList.index(xWF[2])
linE1B_rg.append(gm.IJKRange((i1,j,k),(i2,j,k)))
ptE1B=gridGeom.getSetPntMultiRegion(linE1B_rg,'ptE1B')
lnE1B=sets.get_lines_on_points(ptE1B,'lnE1B')

#Lines E1C (X direct)
linE1C_rg=list()
j=yList.index(yWF[4]-gap/2.)
i1=xList.index(xWF[0])
i2=xList.index(xWF[2])
linE1C_rg.append(gm.IJKRange((i1,j,k),(i2,j,k)))
ptE1C=gridGeom.getSetPntMultiRegion(linE1C_rg,'ptE1C')
lnE1C=sets.get_lines_on_points(ptE1C,'lnE1C')


#Lines EC1B (X direct)
linEC1B_rg=list()
j=yList.index(yQW[2])
i1=xList.index(xWF[4])
i2=xList.index(xWF[6])
linEC1B_rg.append(gm.IJKRange((i1,j,k),(i2,j,k)))
ptEC1B=gridGeom.getSetPntMultiRegion(linEC1B_rg,'ptEC1B')
lnEC1B=sets.get_lines_on_points(ptEC1B,'lnEC1B')

#Lines EC1C (X direct)
linEC1C_rg=list()
j=yList.index(yWF[4]-gap/2.)
i1=xList.index(xWF[4])
i2=xList.index(xWF[6])
linEC1C_rg.append(gm.IJKRange((i1,j,k),(i2,j,k)))
ptEC1C=gridGeom.getSetPntMultiRegion(linEC1C_rg,'ptEC1C')
lnEC1C=sets.get_lines_on_points(ptEC1C,'lnEC1C')


#Lines W1A (X direct)
linW1A_rg=list()
j=yList.index(yQW[0])
i1=xList.index(xWF[10])
i2=xList.index(xWF[12])
linW1A_rg.append(gm.IJKRange((i1,j,k),(i2,j,k)))
ptW1A=gridGeom.getSetPntMultiRegion(linW1A_rg,'ptW1A')
lnW1A=sets.get_lines_on_points(ptW1A,'lnW1A')

#Lines W1B (X direct)
linW1B_rg=list()
j=yList.index(yQW[2])
i1=xList.index(xWF[10])
i2=xList.index(xWF[12])
linW1B_rg.append(gm.IJKRange((i1,j,k),(i2,j,k)))
ptW1B=gridGeom.getSetPntMultiRegion(linW1B_rg,'ptW1B')
lnW1B=sets.get_lines_on_points(ptW1B,'lnW1B')

#Lines W1C (X direct)
linW1C_rg=list()
j=yList.index(yCols[3])
i1=xList.index(xWF[10])
i2=xList.index(xWF[12])
linW1C_rg.append(gm.IJKRange((i1,j,k),(i2,j,k)))
ptW1C=gridGeom.getSetPntMultiRegion(linW1C_rg,'ptW1C')
lnW1C=sets.get_lines_on_points(ptW1C,'lnW1C')

#Lines WC1A (X direct)
linWC1A_rg=list()
j=yList.index(yQW[1])
i1=xList.index(xWF[7])
i2=xList.index(xWF[8])
linWC1A_rg.append(gm.IJKRange((i1,j,k),(i2,j,k)))
ptWC1A=gridGeom.getSetPntMultiRegion(linWC1A_rg,'ptWC1A')
lnWC1A=sets.get_lines_on_points(ptWC1A,'lnWC1A')

#Lines WC1B (X direct)
linWC1B_rg=list()
j=yList.index(yQW[2])
i1=xList.index(xWF[7])
i2=xList.index(xWF[8])
linWC1B_rg.append(gm.IJKRange((i1,j,k),(i2,j,k)))
ptWC1B=gridGeom.getSetPntMultiRegion(linWC1B_rg,'ptWC1B')
lnWC1B=sets.get_lines_on_points(ptWC1B,'lnWC1B')

#Lines WC1C (X direct)
linWC1C_rg=list()
j=yList.index(yCols[3])
i1=xList.index(xWF[7])
i2=xList.index(xWF[8])
linWC1C_rg.append(gm.IJKRange((i1,j,k),(i2,j,k)))
ptWC1C=gridGeom.getSetPntMultiRegion(linWC1C_rg,'ptWC1C')
lnWC1C=sets.get_lines_on_points(ptWC1C,'lnWC1C')

# Lines N1B (Y direct)
k=zList.index(zBeamHigh)

linN1B_rg=list()
i=xList.index(xCols[3]-gap/2.)
j1=yList.index(yWF[0])
j2=yList.index(yWF[1])
linN1B_rg.append(gm.IJKRange((i,j1,k),(i,j2,k)))

ptN1B=gridGeom.getSetPntMultiRegion(linN1B_rg,'ptN1B')
lnN1B=sets.get_lines_on_points(ptN1B,'lnN1B')

# Lines N1C (Y direct)
k=zList.index(zBeamHigh)

linN1C_rg=list()
i=xList.index(xCols[2]-gap/2.)
j1=yList.index(yWF[0])
j2=yList.index(yWF[1])
linN1C_rg.append(gm.IJKRange((i,j1,k),(i,j2,k)))
ptN1C=gridGeom.getSetPntMultiRegion(linN1C_rg,'ptN1C')
lnN1C=sets.get_lines_on_points(ptN1C,'lnN1C')

