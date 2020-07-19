# -*- coding: utf-8 -*-

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

def print_res(lcName,esize):
    print lcName
    for bound in bound_ret_walls:
        react=get_max_min_mean_react(bound[0],esize,bound[1])
        print bound[2], ' , ', react, '\\\\'
    for bound in bound_ramp:
        react=get_max_min_mean_react(bound[0],esize,bound[1])
        print bound[2], ' , ', react, '\\\\'
    for bound in bound_stair1:
        react=get_max_min_mean_react(bound[0],esize,bound[1])
        print bound[2], ' , ', react, '\\\\'
    for bound in bound_stair2:
        react=get_max_min_mean_react(bound[0],esize,bound[1])
        print bound[2], ' , ', react, '\\\\'
     
esize=0.5
loadHand.addToDomain(Wind_EW.name)
analysis= predefined_solutions.simple_static_linear(FEcase)
result= analysis.analyze(1)
preprocessor.getNodeHandler.calculateNodalReactions(True,1e-7)
meanReact(bound_ramp)
meanReact(bound_stair1)
meanReact(bound_stair2)
print_res(Wind_EW.name,esize)
loadHand.removeFromDomain(Wind_EW.name)
        
loadHand.addToDomain(Wind_NS.name)
analysis= predefined_solutions.simple_static_linear(FEcase)
result= analysis.analyze(1)
preprocessor.getNodeHandler.calculateNodalReactions(True,1e-7)
meanReact(bound_ramp)
meanReact(bound_stair1)
meanReact(bound_stair2)
print_res(Wind_NS.name,esize)
loadHand.removeFromDomain(Wind_NS.name)
        
loadHand.addToDomain(Wind_WE.name)
analysis= predefined_solutions.simple_static_linear(FEcase)
result= analysis.analyze(1)
preprocessor.getNodeHandler.calculateNodalReactions(True,1e-7)
meanReact(bound_ramp)
meanReact(bound_stair1)
meanReact(bound_stair2)
print_res(Wind_WE.name,esize)
loadHand.removeFromDomain(Wind_WE.name)
        
loadHand.addToDomain(Wind_SN.name)
analysis= predefined_solutions.simple_static_linear(FEcase)
result= analysis.analyze(1)
preprocessor.getNodeHandler.calculateNodalReactions(True,1e-7)
meanReact(bound_ramp)
meanReact(bound_stair1)
meanReact(bound_stair2)
print_res(Wind_SN.name,esize)
loadHand.removeFromDomain(Wind_SN.name)
        

