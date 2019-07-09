# Links beams to precast planks
stbeams=beam1+beam2+beam3+beam4+beam5
stslabs=slabBC+slabCD_L+slabDG+slabGF+slabFW+slabsF_L
stbeams.fillDownwards()
stslabs.fillDownwards()
nod_stbeams=stbeams.getNodes
nod_stslabs=stslabs.getNodes
for n in nod_stbeams:
    n1=nod_stslabs.getNearestNode(n.getCurrentPos3d(0))
    modelSpace.fixNode('F0F_F00',n1.tag)
    
stbeams=beam1
stslabs=slabCD_H
stbeams.fillDownwards()
stslabs.fillDownwards()
nod_stbeams=stbeams.getNodes
nod_stslabs=stslabs.getNodes
for n in nod_stbeams:
    n1=nod_stslabs.getNearestNode(n.getCurrentPos3d(0))
    modelSpace.fixNode('00F_FFF',n1.tag)

stbeams=beamA+beamB
stslabs=slabW1+slab12+slab23+slab34+slab45
stbeams.fillDownwards()
stslabs.fillDownwards()
nod_stbeams=stbeams.getNodes
nod_stslabs=stslabs.getNodes
for n in nod_stbeams:
    n1=nod_stslabs.getNearestNode(n.getCurrentPos3d(0))
    modelSpace.fixNode('00F_FFF',n1.tag)
    
stbeams=beamA+beamB+beamC
stslabs=slab5W+slabs5_L
stbeams.fillDownwards()
stslabs.fillDownwards()
nod_stbeams=stbeams.getNodes
nod_stslabs=stslabs.getNodes
for n in nod_stbeams:
    n1=nod_stslabs.getNearestNode(n.getCurrentPos3d(0))
    modelSpace.fixNode('00F_FFF',n1.tag)
    
stbeams=beamD+beamG+beamF
stslabs=slab5W+slabs5_L
stbeams.fillDownwards()
stslabs.fillDownwards()
nod_stbeams=stbeams.getNodes
nod_stslabs=stslabs.getNodes
for n in nod_stbeams:
    n1=nod_stslabs.getNearestNode(n.getCurrentPos3d(0))
    modelSpace.fixNode('00F_FFF',n1.tag)


# Support of slabCD_H on slabCD_L
i1=xList.index(xCols[1]+gap/2.)
i2=xList.index(xCols[2]-gap/2.)
j1=yList.index(yCols[0])
j2=yList.index(yFac[1])
k=zList.index(zHlwHigh)
st1=gridGeom.getSetSurfOneRegion(gm.IJKRange((i1,j1,k),(i2,j2,k)),'st1')
nod_st1=st1.getNodes
nod_st2=slabCD_L.getNodes
for n in nod_st1:
    n1=nod_st2.getNearestNode(n.getCurrentPos3d(0))
    modelSpace.fixNode('00F_FFF',n1.tag)


