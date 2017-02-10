import pytest
from exerTools import RabinKarp

def test_RabinKarp1():
	assert len(RabinKarp('123124','1'))==2,   \
		"There are two occurences of 1 in the pattern."
def test_RabinKarp2():
	assert len(RabinKarp('abcdacdc','c'))==3,   \
		"There are three occurences of c in the pattern."
def test_RabinKarp3():
	assert len(RabinKarp('abcdacdc','e'))==0,   \
		"There are no occurences of e in the pattern."
def test_RabinKarp4():
	assert RabinKarp('123124','1')==[0,3],   \
		"The locations of 1 in this pattern start at 0 and at 3"
def test_RabinKarp5():
	assert RabinKarp('123124','123')==[0],   \
		"The location of 123 in this pattern starts at 0"
def test_RabinKarp6():
	assert RabinKarp('123124','124')==[3],   \
		"The location of 124 in this pattern starts at 3"