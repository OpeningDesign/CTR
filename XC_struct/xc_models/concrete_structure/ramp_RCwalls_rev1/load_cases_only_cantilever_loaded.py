#only cantilever loaded
DeadC_LC=lcases.LoadCase(preprocessor=prep,name="DeadC_LC",loadPType="default",timeSType="constant_ts")
DeadC_LC.create()
DeadC_LC.addLstLoads([selfWeight,Dead2F,Dead1F,Earth1F,earthPressEastwall,earthPressWestwall,DeadSB,DeadCW,DeadCCC,DeadCE])
'''
modelSpace.addLoadCaseToDomain("DeadC_LC")
out.displayLoadVectors()
modelSpace.removeLoadCaseFromDomain("DeadC_LC")
'''

LiveC_LC=lcases.LoadCase(preprocessor=prep,name="LiveC_LC",loadPType="default",timeSType="constant_ts")
LiveC_LC.create()
LiveC_LC.addLstLoads([Live2F,Live1F,LiveSB,LiveCW,LiveCCC,LiveCE])
#modelSpace.addLoadCaseToDomain("LiveC_LC")
#out.displayLoadVectors()
#modelSpace.removeLoadCaseFromDomain("LiveC_LC")

SnowC_LC=lcases.LoadCase(preprocessor=prep,name="SnowC_LC",loadPType="default",timeSType="constant_ts")
SnowC_LC.create()
SnowC_LC.addLstLoads([Snow2F,Snow1F,SnowSB,SnowCW,SnowCCC,SnowCE])
#modelSpace.addLoadCaseToDomain("SnowC_LC")
#out.displayLoadVectors()
#modelSpace.removeLoadCaseFromDomain("SnowC_LC")
