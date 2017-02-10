import pandas as pd
import numpy as np
from CRR import CoxRossRubinstein

if __name__ == '__main__':
    # read S&P 500 prices from file
    df = pd.read_csv('./data/AAPL14-15.csv')
    AdjC = df['AdjClose']
    Price = np.array(AdjC[::-1])

    returns = []
    for i in range(0, len(Price)):
        r = np.log(Price[i] / Price[i - 1])
        returns.append(r)

    volat_d = np.std(returns)
    volat = volat_d * np.sqrt(252)

    # input to CRR function

    Current = 100.06
    days = 252
    Strike = 90
    riskfree = 0.01

    Pam,Cam = CoxRossRubinstein(volat,riskfree,days,Current,Strike,'American')
    Peu,Ceu = CoxRossRubinstein(volat,riskfree,days,Current,Strike,'European')
    Pbe,Cbe = CoxRossRubinstein(volat,riskfree,days,Current,Strike,'Bermuda')

    print(Pam, Cam)
    print(Peu,Ceu)
    print(Pbe,Cbe)
    # You would choose the american option as there is more flexibility for the same price
    print(Price[0])





