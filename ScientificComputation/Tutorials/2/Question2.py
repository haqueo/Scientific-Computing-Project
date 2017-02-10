import numpy as np
def powerMatrix(n):
    return np.array([[np.power(j+1,i+1) for j in range(n)] for i in range(n)])
Ainv = np.linalg.inv(powerMatrix(3))
