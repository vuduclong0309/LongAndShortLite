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
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime

import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds


class StochRSI(bt.Strategy):

    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=14)

    # outputting information
    def log(self, txt):
        dt=self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

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

    def next(self):
        self.logdata()
        #if self.data_live == False:
        #    return

        #if not self.position: # check if you already have a position in the market
        if (self.rsi < 30 and self.position.size < 100):
            self.log('Buy Create, %.2f' % self.datas[1].close[0])
            self.buy(data="d1", size=1) # buy when closing price today crosses above MA.
        else:
            # This means you are in a position, and hence you need to define exit strategy here.
            if (self.rsi > 70 and self.position.size > -100):
                self.log('Position Closed, %.2f' % self.datas[1].close[0])
                self.sell(data="d1", size=1)

    def notify_data(self, data, status, *args, **kwargs):
        print('*' * 5, 'DATA NOTIF:', data._getstatusname(status), *args)
        if status == data.LIVE:
            self.data_live = True

    def notify_order(self, order):
        if order.status == order.Completed:
            if order.isbuy():
                self.log(
                "Executed BUY (Price: %.2f, Value: %.2f, Commission %.2f)" %
                (order.executed.price, order.executed.value, order.executed.comm))
            else:
                self.log(
                "Executed SELL (Price: %.2f, Value: %.2f, Commission %.2f)" %
                (order.executed.price, order.executed.value, order.executed.comm))
                self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order was canceled/margin/rejected")
            self.order = None

def run(args=None):

    cerebro = bt.Cerebro()
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
    data0 = store.getdata(dataname="SPY-STK-SMART-USD", **stockkwargs)
    data1 = store.getdata(dataname="SPY-20221014-SMART-USD-366-PUT", **stockkwargs)
    cerebro.adddata(data0, name='d0')
    cerebro.adddata(data1, name='d1')
    #cerebro.resampledata(data0, timeframe=bt.TimeFrame.Minutes, compression=3)
    stval = cerebro.broker.getvalue()

    #cerebro.broker = store.getbroker()
    stval = cerebro.broker.getvalue()

    cerebro.addstrategy(StochRSI)
    cerebro.run()

    endval = cerebro.broker.getvalue()

    print(stval)
    print(endval)
    cerebro.plot()


if __name__ == '__main__':
    run()
