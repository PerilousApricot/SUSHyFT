from math import *

from sys import *

def quicksumtable( table, i ) :

    isum = 0
    for itable in table :
        numbers = itable[2]
        isum = isum + numbers[i]
    return isum
