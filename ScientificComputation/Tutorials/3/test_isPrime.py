import pytest
from exerTools import isPrime
import time
def test_isPrime1():
    assert isPrime(1)==0, \
    	"1 is not a prime. Check that you deal with 1 properly."
def test_isPrime2():
    assert isPrime(2)==1,  \
    	"2 is a prime"
def test_isPrime3():
	assert isPrime(1500450271)==1, \
    	"1500450271 is a prime"