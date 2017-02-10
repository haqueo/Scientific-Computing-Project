import math
# Here we write functions that will enable you to complete the exercises.

def match(str,pat):
    # matching of substring and pattern
    #    str: substring to match
    #    pat: pattern to match
    for j in range(len(pat)):
        # if str and pat match, return TRUE, otherwise FALSE
        if pat[j] == str[j]:
            pass
        else:
            return False
    return True

def RabinKarp(str,pat,base=256,modu=16647133):
    # Rabin-Karp string matching algorithm
    #    str:  text to be searched
    #    pat:  pattern to match
    #    base: base of the Rabin-fingerprint
    #    modu: modulus of the hash-function
    returnList = []
    ic = 0
    n  = len(str)
    m  = len(pat)
    # compute the hash values for pattern and initial string
    hp = 0
    for i in pat:
        hp = (base*hp + ord(i))%modu
    hs = 0
    for i in str[:m]:
        hs = (base*hs + ord(i))%modu
    # check for initial match
    if hs == hp and match(str[:m],pat):
        returnList.append(0)
        ic = 1

    # compute b^m
    bm = 1
    for i in range(m-1):
        bm = (bm*base)%modu
    # main loop
    for i in range(1, n - m + 1):
        hs = (base*(hs - bm*ord(str[i-1])) + ord(str[i+m-1]))%modu
        if hs == hp:
            if match(str[i:i+m],pat):
                returnList.append(i)
                ic += 1
    return returnList

def isPrime(p):
    # Function should return True if p is prime and False otherwise
    # input n >=1
    if p > 1:
        if p == 2:
            return True
        elif p % 2 == 0:
            return False
        else:
            for current in range(3, int(math.sqrt(p) + 1), 2):
                if p % current == 0:
                    return False
            return True
    return False


def primeList(N):
    # return a list of all the numbers up to and including N that are prime
    returnList = []
    number = 1

    while(number <= N):
        if (isPrime(number)):
            returnList.append(number)
            number +=1
        else:
            number +=1
    return returnList

def naiveSearch(str,pat):
    # naive string match by a sliding window
    #     str: string to be searched
    #     pat: pattern to match
    n  = len(str)
    m  = len(pat)
    ic = 0
    # main loop
    for i in range(n-m+1):
        # matching
        if match(str[i:i+m],pat):
            ic += 1
            print i,
    print "\n number of matches found: ", ic
    




