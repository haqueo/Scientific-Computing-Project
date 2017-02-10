import numpy as np
import matplotlib.pyplot as plt

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
    CCP = np.clip(tmp,0,max(tmp));

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
          Cnew[i,it-1] = tmp
    PPrice = Cnew[0,0]

    return PPrice,CPrice

if __name__ == '__main__':

    # parameters
    riskfree = 0.01
    volat    = 0.3
    optType  = 'European'
    Current  = np.arange(45,65,1)
    for i in range(30):
        days   = 5*i
        Strike = 55
        CPrice = np.zeros(len(Current))
        j = 0
        for CC in Current:
            P,C = CoxRossRubinstein(volat,riskfree,days,CC,\
                            Strike,optType)
            CPrice[j] = C
            j += 1

        plt.plot(Current,CPrice)
    plt.savefig('Straddle.png')
    plt.draw()
    plt.show()
