#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
修复在mac下不能导入libs的问题
"""
import sys

import os
from job.logger import logger

import backtrader as bt
import akshare as ak
from datetime import datetime
import pandas as pd

"""
将AKshare拿到的数据（pd）转换为Backtrader可以获得的数据
传入的参数和return的data是独立的
"""


class HKStock:
    def __init__(self, stockNum: str = "", stockName: str = "") -> None:
        if stockNum != "":
            self.stockNum = stockNum
        elif stockName != "":  # 支持模糊搜索
            self.stockList_pd = ak.stock_hk_spot_em()
            """
            序号     代码   名称    最新价    涨跌额    涨跌幅     今开     最高     最低     昨收         成交量        成交额
            0        1  08619     WAC HOLDINGS  0.172  0.071  70.30  0.103  0.200  0.103  0.101  38284000.0  5958708.0
            """
            # print(self.stockList_pd)
            try:
                self.stockNum = self.stockList_pd[
                    self.stockList_pd["名称"].str.contains(stockName)
                ].iat[0, 1]
            except:
                logger.error(
                    f"Fail to find stockNum of HK Stock  {stockNum}  {stockName}"
                )

    def get_daily_data(self, adjust=""):
        """date    open    high     low   close      volume
        0    2021-07-07  168.00  168.50  159.30  165.00  10517381.0
        """
        self.daily_data_pd = ak.stock_hk_daily(self.stockNum)
        return self

    @staticmethod
    def AK_to_BT(data: pd.DataFrame):
        """
        对应stock_hk_daily接口
        """
        columnNames = [
            "date",
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]
        data = data.iloc[:, :6]  # 只取前六列,获取倒数365天数据
        data.columns = columnNames
        data["date"] = pd.to_datetime(data["date"])
        data.set_index("date", inplace=True)
        return data


class emptyBT:
    """
    测试用BT，除了必要设置不设置其余组件。
    """

    def __init__(self) -> None:
        self.cerebro = bt.Cerebro()
        self.cerebro.broker.setcash(100000.0)
        self.broker = self.cerebro.broker
        self.indivalues = list()

    def run(self) -> None:
        self.cerebro.run()
        logger.info("stop running cerebro" + f"value is {self.broker.getvalue()}")

    def add_data(self, data) -> None:
        datafeed = bt.feeds.PandasData(dataname=data)  # type: ignore
        self.cerebro.adddata(datafeed)

    def get_indi(self):  # -> list[Any]:
        strats = self.cerebro.runstrats
        strat = strats[0][0]
        indi = strat.indi.array.tolist()  # 固定将要观察的indicator命名为indi
        indi = indi[-5:]  # take last 5 elements
        self.indivalues.append(indi)
        # self.indivalues = self.cerebro.runstrats[0][0].sma1.array  # TODO 做一般化
        """
        在run的时候，cerebro会分别测试strat，存储在runstrats[0],runstrats[1]中
        """
        return self.indivalues


class tutorialStrategy(bt.Strategy):
    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.sma = bt.indicators.MovingAverageSimple()

    def log(self, txt, dt=None):
        """Logging function for this strategy"""
        dt = dt or self.datas[0].datetime.date(0)
        logger.debug("%s, %s" % (dt.isoformat(), txt))

    def notify_order(self, order: bt.Order):
        """
        Called when the order is changed
        The order may have the following status:

        - Submitted: sent to the broker and awaiting confirmation
        - Accepted: accepted by the broker
        - Partial: partially executed
        - Completed: fully exexcuted
        - Canceled/Cancelled: canceled by the user
        - Expired: expired
        - Margin: not enough cash to execute the order.
        - Rejected: Rejected by the broker
        """
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f"Buy Executed {order.executed.price:.2f},Cost: {order.executed.value:.2f}, Comm:{order.executed.comm:.2f}"
                )
                self.buyprice = order.executed.price
                self.comm = order.executed.comm
            elif order.issell():
                self.log(f"Sell Executed {order.executed.price:.2f}")

            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order canceled/Margined/Rejected")
        # 处理完毕
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log("OPERATION PROFIT, GROSS %.2f, NET %.2f" % (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log("Close, %.2f" % self.dataclose[0])
        if self.order:
            return

        if not self.position:  # not in market
            if self.dataclose[0] < self.dataclose[-1]:
                if self.dataclose[-1] < self.dataclose[-2]:
                    self.log(f"Buy Created, {self.dataclose[0]}")
                    self.order = self.buy()
        else:
            if len(self) >= self.bar_executed + 5:
                # len(self) = len(self.lines)
                self.log(f"Sell Created, {self.dataclose[0]}")
                self.order = self.sell()


class TestStrategy(bt.Strategy):
    params = (("maperiod", 5),)

    def log(self, txt, dt=None):
        """Logging function fot this strategy"""
        dt = dt or self.datas[0].datetime.date(0)
        print("%s, %s" % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.sma1 = bt.indicators.MovingAverageSimple()
        ema1 = bt.indicators.ExponentialMovingAverage()

        close_over_sma = self.data.close > self.sma1
        close_over_ema = self.data.close > ema1

        bt.LinePlotterIndicator(close_over_sma, name="Close_over_Sma")
        self.buy_sig = bt.And(close_over_ema, close_over_sma)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    "BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f"
                    % (order.executed.price, order.executed.value, order.executed.comm)
                )

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log(
                    "SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f"
                    % (order.executed.price, order.executed.value, order.executed.comm)
                )

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log("OPERATION PROFIT, GROSS %.2f, NET %.2f" % (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log("Close, %.2f" % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # Not yet ... we MIGHT BUY if ...
            if self.buy_sig:
                self.order = self.buy()

        else:
            if self.dataclose[0] < self.sma1[0]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log("SELL CREATE, %.2f" % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()


if __name__ == "__main__":
    logger.info("running test on " + __file__)
    # a = HKStock(stockName="小鹏")
    a = HKStock(stockNum="09866")
    a.get_daily_data()
    # logger.info(a.daily_data_pd)
    # logger.info(AK_to_BT(a.daily_data_pd))
    cb = emptyBT()
    cb.cerebro.addstrategy(TestStrategy)
    cb.cerebro.addstrategy(tutorialStrategy)

    cb.add_data(HKStock.AK_to_BT(a.daily_data_pd))
    cb.run()
    print(cb.get_indi())
    cb.cerebro.plot()
