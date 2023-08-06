import numpy as np
import talib as ta
from IQEngine.technical_index.baseindex.MA10 import *


def BOLL(CLOSE, M, N):
    a = MA10(CLOSE, M)
    upper = a + N * np.std(CLOSE, M)
    lower = a - N * np.std(CLOSE, M)
    return a, upper, lower


def talib_boll(close, m, n):
    return ta.BBANDS(close, timeperiod=m, nbdevup=n, nbdevdn=n, matype=0)
