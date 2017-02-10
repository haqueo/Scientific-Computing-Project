import math
import scipy as sp
import matplotlib.pyplot as plt

def frange(start,step,end):
    counter = start

    while(counter<end):
        yield counter
        counter += step

if __name__ == '__main__':
    pi = math.pi
    y = sp.sin([i for i in frange(0,0.1,3*pi)])

    plt.figure()
    plt.plot(y)
    plt.show()

