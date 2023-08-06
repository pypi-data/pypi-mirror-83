from MA import *
from BOLL import *
import numpy as np


def BOLL1(CLOSE, M, N):
    a = MA(CLOSE, M)
    return a


a = [1, 2, 3.9, 4, 5, 6, 7, 8, 9, 0]
s = np.array(a)
print(s)
# print(BOLL1(s, 4, 2))

print(talib_boll(s, 4, 2))
