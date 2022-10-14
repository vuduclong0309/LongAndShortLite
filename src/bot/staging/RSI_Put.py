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

import yfinance as yf

backtest_glob = False
symbol_glob = "SPY"

def getTradingRange(symbol):
    stock = yf.Ticker(symbol)
    latest_price = stock.history(period='0d')['Open'][0]
    basetime = stock.options[2].replace('-', '') # get 3-5dte date

    # Completely optional but I recommend having some sort of round(er?).
    # Dealing with 148.60000610351562 is a pain.
    return basetime, int(latest_price)

expdate, strike_glob = getTradingRange(symbol_glob)

class StochRSI(bt.Strategy):
    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=14)
        self.order = None

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
        self.strike = str(strike_glob)

        if backtest_glob == False: 
            if self.data_live == False:
                return
        if self.order:
            return        

        print("rsi %s last close %s price %s" % (str(self.rsi + 0.01), self.datas[1].close[0], self.getpositionbyname(self.strike).price))

        if self.getpositionbyname(self.strike).size <= 0:
            if self.rsi > 70:
                self.order = self.buy(data=self.strike, size=1, trailpercent = 20) # buy when closing price today crosses above MA.
        else:
            if self.rsi < 30 \
                or self.getpositionbyname(self.strike).price / 100 * 0.9 > self.datas[1].close[0] \
                or self.getpositionbyname(self.strike).price / 100 * 1.2 < self.datas[1].close[0]:
                self.order = self.close(data=self.strike)

    def notify_data(self, data, status, *args, **kwargs):
        print('*' * 5, 'DATA NOTIF:', data._getstatusname(status), *args)
        if status == data.LIVE:
            self.data_live = True

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

def run(args=None):
    cerebro = bt.Cerebro()
    store = bt.stores.IBStore(port=7497)
    stockkwargs = dict(
        timeframe=bt.TimeFrame.Minutes,
        rtbar=not backtest_glob,  # use RealTime 5 seconds bars
        historical=backtest_glob,  # only historical download
        qcheck=0.5,  # timeout in seconds (float) to check for events
        #fromdate=datetime.datetime(2021, 9, 24),  # get data from..
        #todate=datetime.datetime(2022, 9, 25),  # get data from..
        latethrough=False,  # let late samples through
        tradename=None,  # use a different asset as order target
        compression=3
    )
    

    data0 = store.getdata(dataname="%s-STK-SMART-USD" % symbol_glob, **stockkwargs)
    cerebro.adddata(data0, name='stock')

    data = store.getdata(dataname="%s-%s-SMART-USD-%s-PUT" % (symbol_glob, expdate, str(strike_glob)), **stockkwargs)
    cerebro.adddata(data, name='%s' % str(strike_glob))
    
    cerebro.broker.setcash(100)
    stval = cerebro.broker.getvalue()

    if backtest_glob == False:
        cerebro.broker = store.getbroker()

    cerebro.addstrategy(StochRSI)
    cerebro.run()

    endval = cerebro.broker.getvalue()

    cerebro.plot()
    print(stval)
    print(endval)


if __name__ == '__main__':
    run()