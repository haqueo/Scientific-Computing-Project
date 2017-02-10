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
    alpha = (1.-d/Rf)/(u-d)
    beta  = (u/Rf-1.)/(u-d)

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
    CCP = np.clip(tmp,0,max(tmp))

    # reverse binomial tree for call option price
    Cnew       = np.zeros((days+1,days+1))
    Cnew[:,-1] = CCC
    for it in range(days,-1,-1):
        for i in range(0,it):
            Cu = Cnew[i,it]
            Cd = Cnew[i+1,it]
            tmp = alpha*Cu + beta*Cd
            if (optType == 'American'):
                tmp2 = SS[i,it]-Strike
                tmp  = max(tmp,tmp2)
            elif (optType == 'Bermuda'):
                if (it % 21 == 0):
                    tmp3 = SS[i, it] - Strike
                    tmp = max(tmp, tmp3)
            Cnew[i,it-1] = tmp
    CPrice = Cnew[0,0]


    # reverse binomial tree for put option price
    Cnew       = np.zeros((days+1,days+1))
    Cnew[:,-1] = CCP
    for it in range(days,-1,-1):
      for i in range(0,it):
          Cu = Cnew[i,it]
          Cd = Cnew[i+1,it]
          tmp = alpha*Cu + beta*Cd
          if (optType == 'American'):
              tmp2 = Strike-SS[i,it]
              tmp  = max(tmp,tmp2)
          if (optType == 'Bermuda'):
              if (it % 21) == 0:
                  tmp3 = Strike - SS[i, it]
                  tmp = max(tmp, tmp3)
          Cnew[i,it-1] = tmp
    PPrice = Cnew[0,0]

    return PPrice,CPrice


if __name__ == '__main__':

    import pandas as pd

    # read S&P 500 prices from file
    df    = pd.read_csv('./data/SP500Prices.csv')
    AdjC  = df['AdjClose']
    Price = np.array(AdjC[::-1])

    # calculate logarithmic returns
    returns = []
    for i in range(0,len(Price)):
        r = np.log(Price[i]/Price[i-1])
        returns.append(r)

    # compute daily volatility
    volat_d = np.std(returns)
    # adjust to annualized volatility
    volat   = volat_d*np.sqrt(250)

    # input to CRR-function
    Current  = Price[-1]
    days     = 10
    riskfree = 0.01
    Strike   = 2170
    Strike   = 2150

    # test
    riskfree = 0.05
    volat    = 0.2
    days     = 250
    Current  = 50
    Strike   = 60

    optType  = 'European'
    # optType  = 'American'

    # compute put and call option values
    P,C = CoxRossRubinstein(volat,riskfree,days,Current,\
                            Strike,optType)

    # output
    print('Historical volatility = %0.5f' % volat)
    print('Current price         = %.2f' % Current)
    print('Strike price          = %4i' % Strike)
    print('Option type           = %s' % optType)
    print('days till expiration  = %3i\n' % days)
    print('SPX call option       = %.2f' % C)
    print('SPX  put option       = %.2f' % P)
