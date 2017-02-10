import numpy as np
def CoxRossRubinstein(volat,riskfree,days,Current, \
					  Strike,optType):
	# Cox-Ross-Rubinstein (CRR) algorithm for option
	# pricing using a binomial tree structure and
	# arbitrage arguments

	# time step (approx. 250 trading days in a year)
	dt = 1./250.
	# up/down factor (based on volatility)
	u = np.exp(volat*np.sqrt(dt))
	d = 1/u
	# risk-free factor
	Rf = np.exp(riskfree*dt)

	# mapping matrix for underlying asset
	PP      = np.zeros((days+1,days+1))
	PP[0,0] = u
	PP     += np.diag(d*np.ones(days),-1)
	# price vector at root of binomial tree
	P       = np.zeros((days+1,1))
	P[0]    = Current

	# build underlying-asset binomial tree
	SS = P.copy()
	for i in range(0,days):
		P  = np.matmul(PP,P)
		SS = np.hstack((SS,P))

	# evaluation for call options on expiration
	tmp = SS[:,-1]-Strike
	CCC = np.clip(tmp,0,max(tmp))

	# evaluation for put options on expiration
	tmp = Strike-SS[:,-1]
	CCP = np.clip(tmp,0,max(tmp));

	# reverse binomial tree for call option price
	Cnew       = np.zeros((days+1,days+1))
	Cnew[:,-1] = CCC
	for it in range(days,-1,-1):
		for i in range(0,it):
			Cu = Cnew[i,it]
			Cd = Cnew[i+1,it]
			nn = (Cu-Cd)/((u-d)*SS[i,it])
			bb = (u*Cd - d*Cu)/((u-d)*Rf)
			tmp = nn*SS[i,it]+bb
			if (optType == 'American'):
				tmp2 = SS[i,it]-Strike
				tmp  = max(tmp,tmp2)
			Cnew[i,it-1] = tmp
	CPrice = Cnew[0,0]

	# reverse binomial tree for put option price
	Cnew       = np.zeros((days+1,days+1))
	Cnew[:,-1] = CCP
	for it in range(days,-1,-1):
		for i in range(0,it):
			Cu = Cnew[i,it]
			Cd = Cnew[i+1,it]
			nn = (Cu-Cd)/((u-d)*SS[i,it])
			bb = (u*Cd - d*Cu)/((u-d)*Rf)
			tmp = nn*SS[i,it]+bb
			if (optType == 'American'):
				tmp2 = Strike-SS[i,it]
				tmp  = max(tmp,tmp2)
			Cnew[i,it-1] = tmp
	PPrice = Cnew[0,0]

	return PPrice,CPrice