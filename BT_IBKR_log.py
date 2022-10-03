#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-e

from __future__ import absolute_import, division, print_function, unicode_literals
import backtrader as bt
import datetime

class St(bt.Strategy):

    def logdata(self):
            txt = []
            txt.append("{}".format(self.data._name))
            txt.append("{}".format(len(self)))
            txt.append("{}".format(self.data.datetime.date(0)))
            txt.append("{:.2f}".format(self.data.open[0]))
            txt.append("{:.2f}".format(self.data.high[0]))
            txt.append("{:.2f}".format(self.data.low[0]))
            txt.append("{:.2f}".format(self.data.close[0]))
            txt.append("{:.2f}".format(self.data.volume[0]))
            print(", ".join(txt))


    def next(self):
        print("ok")
        self.logdata()

    def notify_store(self, msg, *args, **kwargs):
        print('STORE NOTIF:{}', msg)


def run():

    cerebro = bt.Cerebro(stdstats=False)

    store = bt.stores.IBStore(host="127.0.0.1", port=7496)
    cerebro.broker = store.getbroker()

    stockkwargs = dict(
        timeframe=bt.TimeFrame.Minutes,
        rtbar=False,  # use RealTime 5 seconds bars
        historical=True,  # only historical download
        qcheck=0.5,  # timeout in seconds (float) to check for events
        #fromdate=datetime.datetime(2021, 9, 24),  # get data from..
        #todate=datetime.datetime(2022, 9, 25),  # get data from..
        latethrough=False,  # let late samples through
        tradename=None  # use a different asset as order target
    )
    data0 = store.getdata(dataname="AAPL-STK-SMART-USD", **stockkwargs)
    cerebro.resampledata(data0, timeframe=bt.TimeFrame.Minutes, compression=5)

    #data = store.getdata(dataname='TWTR', timeframe=bt.TimeFrame.Ticks)
    #cerebro.resampledata(data, timeframe=bt.TimeFrame.Seconds, compression=10)
    cerebro.addstrategy(St)
    cerebro.run()




if __name__ == "__main__":

    run()
