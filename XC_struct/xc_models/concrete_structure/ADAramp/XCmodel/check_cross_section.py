execfile('./data.py')

fyd=250/1.05

def sigmaMax(N,M,thickness):
    sgMax=M*6/(thickness**2)+N/thickness
    return sgMax*1e-6   #MPa

def verif(sigmaX,sigmaZ,tao,fyd):
    sg_comp=(sigmaX**2+sigmaZ**2-sigmaX*sigmaZ+3*tao**2)**(0.5)
    if sg_comp <=fyd:
        print ('sg_comp= ', round(sg_comp,2) , '<=fyd -> Verification OK!')
    else:
        print ('sg_comp= ', round(sg_comp,2) , '>fyd -Cross-section is insufficient')

### Spacing = 2' L5x3-1/2x3/8
# Vertical flange.  
N1=143e3
M1=2.56e3
sigmaX=sigmaMax(N1,M1,angleTh)

Q1=90e3
tao=Q1/angleTh*1e-6

N2=0
M2=1.3e3
sigmaZ=sigmaMax(N2,M2,angleTh)

verif(sigmaX,sigmaZ,tao,fyd)

quit()
# Horizontal flange.  
N1=9.76e3
M1=3.05e3
sigmaX=sigmaMax(N1,M1,angleTh)

Q1=47.4e3
tao=Q1/angleTh*1e-6

N2=0
M2=1.14e3
sigmaZ=sigmaMax(N2,M2,angleTh)

verif(sigmaX,sigmaZ,tao,fyd)

# Anchor
'Rx =', -17673.47, 'Rz= ', 7269.56


### Spacing = 2' L5x3-1/2x1/2
# Vertical flange.  
N1=146e3
M1=2.57e3
sigmaX=sigmaMax(N1,M1,angleTh)
N2=
M2=
sigmaZ=sigmaMax(N2,M2,angleTh)

Q1=146e3
tao=Q1/angleTh*1e-6

# Horizontal flange.  
N1=9.93e3
M1=3.07e3
sigmaX=sigmaMax(N1,M1,angleTh)
N2=
M2=
sigmaZ=sigmaMax(N2,M2,angleTh)

Q1=48.2e3
tao=Q1/angleTh*1e-6

# Anchor
'Rx =', -18080, 'Rz= ', 7280


