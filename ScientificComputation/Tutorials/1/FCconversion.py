import numpy as np
import scipy as sp

def F2C(F):
    # conversion from Fahrenheit to Celsius
    C = []      # start with empty list
    for degF in F:
        degC = 5.*(degF-32.)/9.
        C.append(degC)   # append new value to list
    return C

def C2F(C):
    # conversion from Celsius to Fahrenheit
    F = []      # start with empty list
    for degC in C:
        degF = 9.*degC/5. + 32.
        F.append(degF)   # append new value to list
    return F

if __name__ == '__main__':
    # main code

    F  = range(50,200,10)
    C  = F2C(F)
    FF = C2F(C)

    # doing it 'inline' ie list comprehension
    F_inl = [cdeg*9./5.+32. for cdeg in C]
    C_inl = [5.*(fdeg-32.)/9. for fdeg in F]

    firstPossibleValue = abs(min(C) - max(C_inl))
    secondPossibleValue = abs(max(C)-min(C_inl))

    largestDiff = max(firstPossibleValue,secondPossibleValue)

    print(largestDiff)