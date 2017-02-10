#Question 1

#Write a main function that sums all numbers divisible by 3 or 5 less than n, but not by both.
#Useful functions you may want to use
#This main function should read n from the command line and print the sum (preferably with some text).

import sys

def criteria(n):

    if (n % 3 == 0 and n % 5 == 0):
        return False
    elif (n % 3 == 0):
        return True
    elif (n % 5 == 0):
        return True
    else:
        return False



def sumDiv(n):

    counter = 0
    for i in range(1,n):
        if (criteria(i)):
            counter += i
    return counter



if __name__ == '__main__':
    n = int(sys.argv[1])
    print("n = %i returns %i") % (n,sumDiv(n))