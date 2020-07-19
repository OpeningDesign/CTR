#choose load_cases_only_cantilever_loaded.py in model_gen.py before running it
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
    print('\\underline{shear checking:} \\\\')
    print('V$_{d,max}$= ', round(Vmax/1e3,2), ' kN \\\\ V$_{provided}$= ', round(Vu/1e3,2), ' kN \\\\ Capacity factor: F= ',round(Vmax/Vu,2),' \\\\')

def verifBending(Mmax,fy,Wz):
    Mu=Wz*fy/1.67
    print('\\underline{normal stresses checking:} \\\\')    
    print('M$_{d,max}$= ', round(Mmax/1e3,2), ' mkN \\\\ M$_{provided}$= ', round(Mu/1e3,2), ' mkN \\\\ Capacity factor: F= ',round(Mmax/Mu,2),' \\\\')

from solution import predefined_solutions
modelSpace.addNewLoadCaseToDomain('ULS02', '1.2*DeadC_LC+1.6*LiveC_LC+0.5*SnowC_LC')
analysis= predefined_solutions.simple_static_linear(FEcase)
result= analysis.analyze(1)
nodes.calculateNodalReactions(True,1e-7)
#
fy=strSteel.fy
## Verification of beam parallel to facade
print('\\textbf{Beam parallel to facade} \\\\')
st=beamXsteel
Vmax,Mmax=getMaxForces(st)
Avy=beamXsteel_mat.get('Avy')
Wz=beamXsteel_mat.getWz()
verifShear(Vmax,fy,Avy)
verifBending(Mmax,fy,Wz)

## Verification of West cantilever
print(' \\\\ \\textbf{West cantilever} \\\\')
st=WbeamYsteel
Vmax,Mmax=getMaxForces(st)
Avy=WbeamYsteel_mat.get('Avy')
Wz=WbeamYsteel_mat.getWz()
verifShear(Vmax,fy,Avy)
verifBending(Mmax,fy,Wz)

## Verification of central cantilever
print(' \\\\ \\textbf{Central cantilever} \\\\')
st=CbeamYsteel
Vmax,Mmax=getMaxForces(st)
Avy=CbeamYsteel_mat.get('Avy')
Wz=CbeamYsteel_mat.getWz()
verifShear(Vmax,fy,Avy)
verifBending(Mmax,fy,Wz)

## Verification of East cantilever
print(' \\\\ \\textbf{East cantilever} \\\\')
st=EbeamYsteel
Vmax,Mmax=getMaxForces(st)
Avy=EbeamYsteel_mat.get('Avy')
Wz=EbeamYsteel_mat.getWz()
verifShear(Vmax,fy,Avy)
verifBending(Mmax,fy,Wz)

## Verification column
print(' \\\\ \\textbf{Column} \\\\')
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

