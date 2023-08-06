# -*- coding:utf-8 -*-

def MA(Series, M):
    """
    简单移动平均
    用法:MA(Series,M),Series的M日简单移动平均
    :param Series:
    :param M:
    :return:ma
    """
    len_series = len(Series)
    ma = []
    for i in range(len_series - M + 1):
        ma.append(Series[i:i + M].mean())
    return ma
