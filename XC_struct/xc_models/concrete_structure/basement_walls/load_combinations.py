#Load combinations
combContainer= combinations.CombContainer()

#Quasi-permanent situations.
combContainer.SLS.qp.add('ELS00', '1.0*selfWeight+1.0*deadLoad+0.5*trafficLoad')

# Service limit states.
# 'selfWeight','deadLoad','trafficLoad','liveLoad','snowLoad','windLoad','quakeLoad']
#Equation 16-8
combContainer.ULS.perm.add('EQ1608', '1.0*selfWeight+1.0*deadLoad')
#Equation 16-9
combContainer.ULS.perm.add('EQ1609A', '1.0*selfWeight+1.0*deadLoad+1.0*trafficLoad')
combContainer.ULS.perm.add('EQ1609B', '1.0*selfWeight+1.0*deadLoad+1.0*liveLoad')
#Equation 16-10
combContainer.ULS.perm.add('EQ1610', '1.0*selfWeight+1.0*deadLoad+1.0*snowLoad')
#Equation 16-11
combContainer.ULS.perm.add('EQ1611A', '1.0*selfWeight+1.0*deadLoad+0.75*trafficLoad+0.75*snowLoad')
combContainer.ULS.perm.add('EQ1611B', '1.0*selfWeight+1.0*deadLoad+0.75*liveLoad+0.75*snowLoad')
#Equation 16-12
combContainer.ULS.perm.add('EQ1612', '1.0*selfWeight+1.0*deadLoad+0.6*windLoad')
#Equation 16-13
combContainer.ULS.perm.add('EQ1613A', '1.0*selfWeight+1.0*deadLoad+0.45*windLoad+0.75*trafficLoad+0.75*snowLoad')
combContainer.ULS.perm.add('EQ1613B', '1.0*selfWeight+1.0*deadLoad+0.45*windLoad+0.75*liveLoad+0.75*snowLoad')
#Equation 16-14-> doesn' apply
#Equation 16-15
combContainer.ULS.perm.add('EQ1615', '0.6*selfWeight+0.6*deadLoad+0.6*windLoad')
#Equation 16-16 -> doesn't apply


#Strength ultimate states. (type 2).
# 'selfWeight','deadLoad','trafficLoad','liveLoad','snowLoad','windLoad','quakeLoad']
#Equation 16-1
combContainer.ULS.perm.add('EQ1601', '1.4*selfWeight+1.4*deadLoad')
#Equation 16-2
combContainer.ULS.perm.add('EQ1602A', '1.2*selfWeight+1.2*deadLoad+1.6*trafficLoad+0.5*snowLoad')
combContainer.ULS.perm.add('EQ1602B', '1.2*selfWeight+1.2*deadLoad+1.6*liveLoad+0.5*snowLoad')
#Equation 16-3
combContainer.ULS.perm.add('EQ1603A', '1.2*selfWeight+1.2*deadLoad+1.6*snowLoad+0.5*trafficLoad')
combContainer.ULS.perm.add('EQ1603B', '1.2*selfWeight+1.2*deadLoad+1.6*snowLoad+0.5*liveLoad')
combContainer.ULS.perm.add('EQ1603C', '1.2*selfWeight+1.2*deadLoad+1.6*snowLoad+0.5*windLoad')
#Equation 16-4
combContainer.ULS.perm.add('EQ1604A', '1.2*selfWeight+1.2*deadLoad+1.0*windLoad+0.5*trafficLoad+0.5*snowLoad')
combContainer.ULS.perm.add('EQ1604B', '1.2*selfWeight+1.2*deadLoad+1.0*windLoad+0.5*liveLoad+0.5*snowLoad')
#Equation 16-5
combContainer.ULS.perm.add('EQ1605A', '1.2*selfWeight+1.2*deadLoad+0.5*trafficLoad+0.7*snowLoad')
combContainer.ULS.perm.add('EQ1605B', '1.2*selfWeight+1.2*deadLoad+0.5*liveLoad+0.7*snowLoad')
#Equation 16-6 -> doesn't apply
#Equation 16-7 -> doesn't apply
