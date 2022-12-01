#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2022 Duc Long Vu
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
        @Author: vuduclong0309
        @Date: 2022-Nov-30
        @Credit: Backtrader
        @Links: https://github.com/mementum/backtrader/blob/master/samples/macd-settings/macd-settings.py

A complexed version of MACD bot pulled from original backtrader repo.
Author modified datafeed it to work with IBKR data feed 
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime

import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds


class MACDStopLoss(bt.Strategy):
    '''
    This strategy is loosely based on some of the examples from the Van
    K. Tharp book: *Trade Your Way To Financial Freedom*. The logic:
      - Enter the market if:
        - The MACD.macd line crosses the MACD.signal line to the upside
        - The Simple Moving Average has a negative direction in the last x
          periods (actual value below value x periods ago)
     - Set a stop price x times the ATR value away from the close
     - If in the market:
       - Check if the current close has gone below the stop price. If yes,
         exit.
       - If not, update the stop price if the new stop price would be higher
         than the current
    '''
    lines = ('macdmin',)

    params = (
        # Standard MACD Parameters
        ('macd1', 12),
        ('macd2', 26),
        ('macdsig', 9),
        ('atrperiod', 14),  # ATR Period (standard)
        ('atrdist', 3.0),   # ATR distance for stop price
        ('smaperiod', 30),  # SMA Period (pretty standard)
        ('dirperiod', 10),  # Lookback period to consider SMA trend direction
    )

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

    def notify_order(self, order):
        if order.status == order.Completed:
            pass

        if not order.alive():
            self.order = None  # indicate no order is pending

    def __init__(self):
        self.macd = bt.indicators.MACD(self.data,
                                       period_me1=self.p.macd1,
                                       period_me2=self.p.macd2,
                                       period_signal=self.p.macdsig)


        self.l.macdmin = bt.indicators.EMA(period = 12) - bt.indicators.EMA(period = 26)

        # Cross of macd.macd and macd.signal
        self.mcross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

        # To set the stop price
        self.atr = bt.indicators.ATR(self.data, period=self.p.atrperiod)

        # Control market trend
        self.sma = bt.indicators.SMA(self.data, period=self.p.smaperiod)
        self.smadir = self.sma - self.sma(-self.p.dirperiod)

    def start(self):
        self.order = None  # sentinel to avoid operrations on pending order

    lastmacd = -10
    def next(self):
        #print(str(self.macdmin[0]) + " " + str(self.lastmacd))
        if(self.lastmacd == -10):
            self.lastmacd = self.macdmin[0]

        if self.order:
            return  # pending order execution

        if not self.position:  # not in the market
            if self.mcross[0] > 0.0 and self.smadir < 0.0:
                self.order = self.buy(size=10)
                self.log('Buy Create, %.2f' % self.data.close[0])
                pdist = self.atr[0] * self.p.atrdist
                self.pstop = self.data.close[0] - pdist

        else:  # in the market
            pclose = self.data.close[0]
            pstop = self.pstop

            if abs(self.lastmacd) > abs(self.macdmin[0]) or pclose < pstop:
                self.close()  # stop met - get out
                self.log('Position Closed, %.2f' % self.data.close[0])
            else:
                pdist = self.atr[0] * self.p.atrdist
                # Update only if greater than
                self.pstop = max(pstop, pclose - pdist)
        self.lastmacd = self.macdmin[0]




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
    cerebro.resampledata(data0, timeframe=bt.TimeFrame.Minutes, compression=15)
    stval = cerebro.broker.getvalue()


    cerebro.addstrategy(MACDStopLoss)
    cerebro.run()
    cerebro.plot(style='candlestick',loc='grey', grid=False) #You can leave inside the paranthesis empty
    endval = cerebro.broker.getvalue()
    print(stval)
    print(endval)


if __name__ == '__main__':
    run()
