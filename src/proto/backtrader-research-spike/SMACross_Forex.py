#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2018 Daniel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

"""
        @Credit: Backtrader
        @Links: https://www.backtrader.com/home/helloalgotrading/
"""


from datetime import datetime
import backtrader as bt
import time

# Create a subclass of Strategy to define the indicators and logic

class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30   # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def logdata(self):
        txt = []
        txt.append('{}'.format(len(self)))
        txt.append('{}'.format(self.data.datetime.datetime(0).isoformat()))
        txt.append('{:.2f}'.format(self.data.open[0]))
        txt.append('{:.2f}'.format(self.data.high[0]))
        txt.append('{:.2f}'.format(self.data.low[0]))
        txt.append('{:.2f}'.format(self.data.close[0]))
        txt.append('{:.2f}'.format(self.data.volume[0]))
        print(','.join(txt))

    data_live = False

    def notify_data(self, data, status, *args, **kwargs):
        print('*' * 5, 'DATA NOTIF:', data._getstatusname(status), *args)
        if status == data.LIVE:
            self.data_live = True
        else:
            self.data_live = False

    def notify_order(self, order):
        if order.status == order.Completed:
            buysell = 'BUY ' if order.isbuy() else 'SELL'
            txt = '{} {}@{}'.format(buysell, order.executed.size,
                                    order.executed.price)
            print(txt)

    def notify_store(self, msg, *args, **kwargs):
        print('STORE NOTIF:{}', msg)

    def next(self):
        self.logdata()

        if self.data_live == False:
            return

        print(self.position)
        self.crossover

        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position

cerebro = bt.Cerebro(stdstats=False)
store = bt.stores.IBStore(port=7497)
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
data0 = store.getdata(dataname="EUR.USD-CASH-IDEALPRO", **stockkwargs)
cerebro.resampledata(data0, timeframe=bt.TimeFrame.Seconds, compression=5)

cerebro.broker = store.getbroker()

cerebro.addstrategy(SmaCross)
print(cerebro.broker.value)
cerebro.run()
print(cerebro.broker.value)
#cerebro.plot(style='candlestick',loc='grey', grid=False) #You can leave inside the paranthesis empty
