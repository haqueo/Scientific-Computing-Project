import numpy as np
import matplotlib.pyplot as plt
from exerTools import RabinKarp, isPrime, primeList
# Exercise to find the distribution of primes in the first 100000 digits of primes

# exercise 2
# read 'Digits of Pi' file
f     = open('DigitsOfPi','r')
strPi = f.read()
f.close()


# generate a list of the primes up to 100000
listOfPrimes = primeList(10000)
occurencesy = [(lambda num: len(RabinKarp(strPi,str(num))))(prime) for prime in listOfPrimes]

plt.figure()
plt.loglog(listOfPrimes,occurencesy,basex=10)
plt.show()


# the figure shows lines of similar length, each dropping off significantly after each 1000 digits.
# this is because as you go up the next thousand digits, there is an extra digit in all the values of pi
# so to find a string of this length in the digit of pi becomes much harder
# a tenth less likely, in fact. this is shown directly by the figure.
