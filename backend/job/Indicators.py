import sys

import os
from job.logger import logger

import backtrader as bt
import akshare as ak
import pandas as pd
from datetime import datetime
import itertools
from job.Stock import HKStock, emptyBT
from backtrader.indicators import (
    # MovingAverageSimple as SMA,
    ExponentialMovingAverage as EMA,
    # WeightedMovingAverage as SMA,
)

from backtrader.talib import SMA  # type:ignore


class emptyIndicator(bt.Indicator):
    params = (("value", 5),)

    lines = ("tutorialline",)

    def __init__(self) -> None:
        self.lines.tutorialline = self.data.open(0)  # type: ignore


class emptyStrategy(bt.Strategy):
    """
    空白strategy模板，负责测试indicator。
    """

    def __init__(self) -> None:
        self.indi_value = list()
        self.indi = emptyIndicator()

    def next(self):
        pass


class cusIndi_YDTC(bt.Indicator):
    """
    来自同花顺指标 诱多退场

    VAR1:=REF((L+O+C+H)/4,1) //REF(i,j) J个周期前的I指标

    VAR2:=SMA(ABS(VAR1-H)13,1/SMA(MAX(VAR1-H.0).10.1);

    VAR3:=EMA(VAR2.10):

    VAR4:=HHV(H.33):

    VAR5:=EMA(F(H>=VAR4VAR3.0),3)*-1

    主力退场:IF(VAR5>REF(VAR5 D,VAR5.0)LINETHICK2.Color0066BB

    主力诱多:IF(VAR5<REF(VAR5 1VAR5.0LINETHICK2 ColoIFF8800

    """

    lines = ("Leave", "Enter", "var2", "var7", "var6", "var1")
    params = (("period", 33),)
    plotinfo = dict(subplot=True)  # 控制画图的参数

    def __init__(
        self,
    ) -> None:
        self.addminperiod(self.params.period)  # type: ignore
        var1 = (
            self.data.close(-1)
            + self.data.open(-1)
            + self.data.high(-1)
            + self.data.low(-1)
        ) / 4  # 这里的-1是指前一天的数据, 且没问题

        var2 = SMA(abs(var1 - self.data.high), timeperiod=13)  # type: ignore
        # var6 = var2
        # var7 = SMA(bt.Max(var1 - self.data.high, 0), period=10)  # type: ignore
        # var6 var7 都不对，abs是对的
        # 他妈的， 同花顺算得有问题， 他们的代码是错的
        var2 = bt.DivByZero(var2, SMA(bt.Max(var1 - self.data.high, 0), period=10), zero=1)  # type: ignore
        var3 = EMA(var2, period=10)  # type: ignore

        var4 = bt.indicators.Highest(self.data.open, period=33)  # type: ignore
        var5 = EMA(bt.If(self.data.high > var4, var3 * -1, 0), period=3)  # type: ignore

        self.l.Leave = bt.If(var5 > var5(-1), var5, 0)
        self.l.Enter = bt.If(var5 < var5(-1), var5, 0)
        self.l.var1 = var1


if __name__ == "__main__":
    logger.info("running test on " + __file__)
    a = HKStock(stockNum="09866")
    a.get_daily_data()
    # logger.info(a.daily_data_pd)
    # logger.info(AK_to_BT(a.daily_data_pd))
    cb = emptyBT()
    cb.cerebro.addstrategy(emptyStrategy)
    cb.add_data(HKStock.AK_to_BT(a.daily_data_pd))
    cb.run()
    print(cb.get_indi()[0], type(cb.get_indi()[0]))
    cb.cerebro.plot()
