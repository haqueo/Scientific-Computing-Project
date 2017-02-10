from exerTools import RabinKarp, primeList, naiveSearch
import matplotlib.pyplot as plt
import time
f     = open('GeneticMaterialLarge','r')
strGM = f.read()
f.close()


p1  = 'CACAATATATGATCGC'
p2  = 'GTGCCAACATATTGTGCTCTCTATATAATGACTGCCTCT'
p3  = 'GCGAATATGGAAAAAAAGGCAGACACACACTTGTTGATTTCTTTATGCG'
pa  = 'ATTTCTACTGTAAAAATCTTTCTTTGTCCAAAAAATCTTTGATAGTGTTT'
pb  = 'CCCTATGTTTGTGTGCACGGACACGTGCTAAAGCCAAATATTTTGCTAGT'
pc  = 'CAATATATAACAAAAAATATTTTTCGGGCTTGCGTACTGTAAAGATGAAT'
p4  = pa + pb + pc


# Calculate the time the algorithm takes to find the supplied four patterns
# (labelled p1,p2,p3 and p4) in the genetic material string and plot the time against the
# length of the pattern using matplotlib.

ListOfPatterns = (p1,p2,p3,p4)
lengthOfPatterns = [len(string) for string in ListOfPatterns]
timetaken = []
naivetimetaken = []

for pattern in ListOfPatterns:

    t0 = time.time()
    RabinKarp(strGM,pattern,modu=3)
    t1 = time.time()

    timetaken.append(t1-t0)








#
# Repeat this calculation using the naiveSearch function
# and plot this on the same graph. Does this agree with the theoretical scaling results
# shown in lectures?


for pattern in ListOfPatterns:

    t0 = time.time()
    RabinKarp(strGM,pattern)
    t1 = time.time()

    naivetimetaken.append(t1-t0)


plt.figure()
plt.scatter(lengthOfPatterns,timetaken,label='RabinKarp search',color='r')
plt.scatter(lengthOfPatterns,naivetimetaken,label='naive search',color='g')
plt.legend(loc='best')
plt.show()

#I'd need to add more points to really be sure,
#but for large lengths (n) the RabinKarp search really does seem to be O(n),
#and the naive search does seem to be scaling higher.

#using the Rabin Karp with modu = 3
# we see, that the Rabin Karp search performs notably worse.
#this is because the modulus 3 is much too small, and causes lots of hash collisions
# this means you still have to complete the naive search on top of the hash calculations