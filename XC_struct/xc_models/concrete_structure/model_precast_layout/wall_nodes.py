stBusq=overallSet
z=zBeamHigh
wallNorth=sets.get_nodes_wire(setBusq=stBusq,lstPtsWire=[geom.Pos3d(0,0,z),geom.Pos3d(xList[-1],0,z)])
wallSouth=sets.get_nodes_wire(setBusq=stBusq,lstPtsWire=[geom.Pos3d(0,yList[-1],z),geom.Pos3d(xList[-1],yList[-1],z)])
wallEast=sets.get_nodes_wire(setBusq=stBusq,lstPtsWire=[geom.Pos3d(0,0,z),geom.Pos3d(0,yList[-1],z)])
wallWest=sets.get_nodes_wire(setBusq=stBusq,lstPtsWire=[geom.Pos3d(xList[-1],0,z),geom.Pos3d(xList[-1],yList[-1],z)])
