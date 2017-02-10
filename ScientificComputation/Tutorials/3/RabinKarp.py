import sys
import time

def RabinKarp(str,pat,base=256,modu=16647133):
    # Rabin-Karp string matching algorithm
    #    str:  text to be searched
    #    pat:  pattern to match
    #    base: base of the Rabin-fingerprint
    #    modu: modulus of the hash-function
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
        print 0
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
                print i,
                ic += 1
    print "\n number of matches found: ", ic

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

if __name__ == '__main__':

    # read 'Genetic Material' file
    f     = open('GeneticMaterialLarge','r')
    strGM = f.read()
    f.close()
    strGM = strGM.replace("\n","")

    # patterns to search for
    p1  = 'CACAATATATGATCGC'
    p2  = 'GTGCCAACATATTGTGCTCTCTATATAATGACTGCCTCT'
    p3  = 'GCGAATATGGAAAAAAAGGCAGACACACACTTGTTGATTTCTTTATGCG'
    pa  = 'ATTTCTACTGTAAAAATCTTTCTTTGTCCAAAAAATCTTTGATAGTGTTT'
    pb  = 'CCCTATGTTTGTGTGCACGGACACGTGCTAAAGCCAAATATTTTGCTAGT'
    pc  = 'CAATATATAACAAAAAATATTTTTCGGGCTTGCGTACTGTAAAGATGAAT'
    p4  = pa + pb + pc
    patGM = p2

    # read 'Digits of Pi' file
    f     = open('DigitsOfPi','r')
    strPi = f.read()
    f.close()

    # pattern to search for
    p1 = '160496'
    p2 = '2479114016957900338356'
    patPi = p1

    # scan the Genetic Material file
    t0    = time.time()
    RabinKarp(strGM,patGM)
    t1    = time.time()
    total = t1-t0
    print 'Genetic Material (Rabin-Karp algorithm): ',total

    t0    = time.time()
    naiveSearch(strGM,patGM)
    t1    = time.time()
    total = t1-t0
    print 'Genetic Material (naive search): ',total
    #
    # # scan the Digits of Pi file
    t0    = time.time()
    RabinKarp(strPi,patPi)
    t1    = time.time()
    total = t1-t0
    print 'Digits of Pi (Rabin-Karp algorithm): ',total

    t0    = time.time()
    naiveSearch(strPi,patPi)
    t1    = time.time()
    total = t1-t0
    print 'Digits of Pi (naive search): ',total
