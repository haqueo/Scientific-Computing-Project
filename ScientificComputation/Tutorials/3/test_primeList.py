import pytest
from exerTools import primeList

def test_primeList1():
	numOfPrimes = len(primeList(100))
	assert numOfPrimes==25, \
    	"In the first 100 numbers there are 25 primes not %s prime(s). Check you are finding them all." % str(numOfPrimes)
def test_primeList2():
	numOfPrimes = len(primeList(101))
	assert numOfPrimes==26, \
    	"In the first 100 numbers there are 26 primes not %s prime(s). If the last test passed \
then you probably aren't including N when you search for primes up to and including N." % str(numOfPrimes)
def test_primeList3():
	tenthPrime = primeList(100)[9]
	assert tenthPrime==29, \
    	"The 10th prime number is 29 not %s" % str(tenthPrime)