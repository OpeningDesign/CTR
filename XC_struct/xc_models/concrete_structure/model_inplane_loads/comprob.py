execfile('./model_gen.py')
def get_max_min_mean_react(lstNod,esize,Lwall):
    '''Return the maximum and minimum reactions (X Y directions) of the nodes
    in the list. Also return the mean reaction in X Y directions'''
    (maxRx,minRx,totalRx)=(0,0,0)
    (maxRy,minRy,totalRy)=(0,0,0)
    for n in lstNod:
        R=n.getReaction
        Rx=R[0]
        Ry=R[1]
        totalRx+=abs(Rx)
        totalRy+=abs(Ry)
        if Rx>maxRx:
            maxRx=Rx
        elif Rx<minRx:
            minRx=Rx
        if Ry>maxRy:
            maxRy=Ry
        elif Ry<minRy:
            minRy=Ry
    maxRx/=esize  #N/m
    minRx/=esize  #N/m
    maxRy/=esize  #N/m
    minRy/=esize  #N/m
    meanRx=totalRx/Lwall
    meanRy=totalRx/Lwall
    return (round(maxRx*1e-3,2),
            round(minRx*1e-3,2),
            round(maxRy*1e-3,2),
            round(minRy*1e-3,2))

loadHand.addToDomain(Wind_NS.name)
analysis= predefined_solutions.simple_static_linear(FEcase)
result= analysis.analyze(1)
preprocessor.getNodeHandler.calculateNodalReactions(True,1e-7)
Rx=0
Ry=0
for n in hollowcore.getNodes:
    R=n.getReaction
    Rx+=R[0]
    Ry+=R[1]
    
loadHand.removeFromDomain(Wind_NS.name)
 
print 'Rx=', Rx
print 'Ry=', Ry
