from job.Indicators import emptyIndicator, emptyStrategy
from job.Stock import HKStock, emptyBT

from datetime import datetime


class job_autorun:  # 港股
    def __init__(self, stockNum="09866"):
        self.autorunning = True
        self.runcount = 0
        self.result = list()
        self.stockNum = stockNum

        # cb initiation
        self.data = HKStock(stockNum=stockNum).get_daily_data().daily_data_pd
        self.cb = emptyBT()
        self.cb.cerebro.addstrategy(emptyStrategy)
        self.data = HKStock.AK_to_BT(self.data)
        self.cb.add_data(self.data)

    def run(self):
        print(f"running job {self.runcount} times, time is {datetime.now()}")
        self.cb.run()

        self.result.append(self.cb.get_indi()[0])
        self.runcount += 1
        print(self.result)
        self.cleanup()

        return self.result

    def test_run(self):
        print(f"running job {self.runcount} times, time is {datetime.now()}")
        self.cb.run()

        self.result.append(self.cb.get_indi()[0])
        self.runcount += 1
        print(self.result)
        self.cleanup()
        # self.stockNum = str(int(self.stockNum) + 1)# 股票代号不连续 出错

        return self.result

    def get_result(self):  # -> list[Any]:
        return self.result

    def cleanup(self):
        self.data = HKStock(stockNum=self.stockNum).get_daily_data().daily_data_pd
        self.cb = emptyBT()
        self.cb.cerebro.addstrategy(emptyStrategy)
        self.data = HKStock.AK_to_BT(self.data)
        self.cb.add_data(self.data)
        self.result = list()


if __name__ == "__main__":
    a = job_autorun()  # 每次run玩要记得clear
    a.run()
    print(a.get_result())
