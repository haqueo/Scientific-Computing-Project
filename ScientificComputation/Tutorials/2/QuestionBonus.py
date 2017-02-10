import numpy as np
import sys
import math
import scipy as sp


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
    for i in range(1, n):
        if (criteria(i)):
            counter += i
    return counter


def powerMatrix(n):
    return np.array([[np.power(j + 1, i + 1) for j in range(n)] for i in range(n)])


def frange(start, step, end):
    counter = start

    while (counter < end):
        yield counter
        counter += step


if __name__ == '__main__':
    pi = math.pi

    function_name = str(sys.argv[1])

    if function_name == 'question_1':
        function_value = sumDiv(1000)
        print("n = %i returns %i") % (1000, function_value)
    elif function_name == 'question_2':
        function_value = powerMatrix(4)
    elif function_name == 'question_3':
        function_value = sp.sin([i for i in frange(0, 0.1, 3 * pi)])
    else:
        print("please enter input of the form 'question_i' for i =1,2,3")


    
