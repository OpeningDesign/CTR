execfile('./model_gen.py')

def getMaxForces(setElem):
    VMax= -1e23
    VMin= -VMax
    MMax= -1e23
    MMin= -MMax
    for e in setElem.elements:
        VMax= max(VMax,max(e.getVy1, e.getVy2))
        VMin= min(VMin,min(e.getVy1, e.getVy2))
        MMax= max(MMax,max(e.getMz1, e.getMz2))
        MMin= min(MMin,min(e.getMz1, e.getMz2))
    Vmax= max(VMax,abs(VMin))
    Mmax= max(MMax,abs(MMin))
    return(Vmax,Mmax)

def getMaxForcesOrt(setElem):
    VMax= -1e23
    VMin= -VMax
    MMax= -1e23
    MMin= -MMax
    for e in setElem.elements:
        VMax= max(VMax,max(e.getVz1, e.getVz2))
        VMin= min(VMin,min(e.getVz1, e.getVz2))
        MMax= max(MMax,max(e.getMy1, e.getMy2))
        MMin= min(MMin,min(e.getMy1, e.getMy2))
    Vmax= max(VMax,abs(VMin))
    Mmax= max(MMax,abs(MMin))
    return(Vmax,Mmax)

def verifShear(Vmax,fy,Avy):
    Vu=fy/math.sqrt(3.0)*Avy/1.67
    print('Vmax= ', Vmax/1e3, ' kN Vu= ', Vu/1e3, ' kN; F= ',Vmax/Vu)

def verifBending(Mmax,fy,Wz):
    Mu=Wz*fy/1.67
    print('Mmax= ', Mmax/1e3, ' kN m Mu= ', Mu/1e3, ' kN m; F= ',Mmax/Mu)

from solution import predefined_solutions
modelSpace.addNewLoadCaseToDomain('ULS02', '1.2*Dead_LC+1.6*Live_LC+0.5*Snow_LC')
analysis= predefined_solutions.simple_static_linear(FEcase)
result= analysis.analyze(1)
nodes.calculateNodalReactions(True,1e-7)
#
fy=strSteel.fy
## Verification of beam parallel to facade
print 'Beam parallel to facade'
st=beamXsteel
Vmax,Mmax=getMaxForces(st)
Avy=beamXsteel_mat.get('Avy')
Wz=beamXsteel_mat.getWz()
verifShear(Vmax,fy,Avy)
verifBending(Mmax,fy,Wz)

## Verification of West cantilever
print 'West cantilever'
st=WbeamYsteel
Vmax,Mmax=getMaxForces(st)
Avy=WbeamYsteel_mat.get('Avy')
Wz=WbeamYsteel_mat.getWz()
verifShear(Vmax,fy,Avy)
verifBending(Mmax,fy,Wz)

## Verification of central cantilever
print 'Central cantilever'
st=CbeamYsteel
Vmax,Mmax=getMaxForces(st)
Avy=CbeamYsteel_mat.get('Avy')
Wz=CbeamYsteel_mat.getWz()
verifShear(Vmax,fy,Avy)
verifBending(Mmax,fy,Wz)

## Verification of East cantilever
print 'East cantilever'
st=EbeamYsteel
Vmax,Mmax=getMaxForces(st)
Avy=EbeamYsteel_mat.get('Avy')
Wz=EbeamYsteel_mat.getWz()
verifShear(Vmax,fy,Avy)
verifBending(Mmax,fy,Wz)

## Verification column
print 'Column'
st=columnZsteel

Vmax,Mmax=getMaxForces(st)
Avy=columnZsteel_mat.get('Avy')
Wy=columnZsteel_mat.getWy()
verifShear(Vmax,fy,Avy)
verifBending(Mmax,fy,Wz)

Vmax,Mmax=getMaxForcesOrt(st)
Avz=columnZsteel_mat.get('Avz')
Wy=columnZsteel_mat.getWy()
verifShear(Vmax,fy,Avz)
verifBending(Mmax,fy,Wy)

