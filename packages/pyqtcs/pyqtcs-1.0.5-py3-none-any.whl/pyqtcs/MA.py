import talib as ta
import numpy as np


def MA(CLOSE, M):
    return np.average(CLOSE, M)
