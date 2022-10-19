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

from config import *
from utils import *

expdate_glob = ""
strike_glob = ""

def updateGlobalVar(symbol):
    global expdate_glob
    global strike_glob
    stock = yf.Ticker(symbol)
    latest_price = stock.history(period='0d', interval='1m')['Close'][-1]
    basetime = stock.options[2].replace('-', '') # get 3-5dte date

    expdate_glob = basetime
    strike_glob = int(latest_price)

    print("global var update: "  + symbol_glob + " " + expdate_glob + " " + str(strike_glob))
    return

class RSIPut(StrategyWithLogging):
    def __init__(self):
        self.rsi = bt.talib.RSI(self.data.close, period=14)
        self.order = None
        self.rsi_arr = []
        self.rsi_arr.append(self.rsi + 0.0)
        self.stop_loss_wait_neutral = False

    def next(self):
        print(self.cerebro.broker.getvalue())
        self.logdata()
        self.rsi_arr.append(self.rsi + 0.0)

        if backtest_glob == False:
            if self.data_live == False:
                return

        sec_price = self.getpositionbyname('put').price / p_factor
        last_close = self.getdatabyname('put').close[0]


        print("rsi %s %s put %s price %s" % (str(self.rsi_arr[-1]), str(self.rsi_arr[-2]), self.getdatabyname('put').close[0], sec_price))
        if(self.stop_loss_wait_neutral == True):
            print("Waiting for neutral")

        if self.rsi_arr[-1] < 50:
            if(self.stop_loss_wait_neutral == True):
                print("Neutral Waiting Finished")
            self.stop_loss_wait_neutral = False

        if self.order:
            print("pending order, returning")
            return

        if self.getpositionbyname('put').size <= 0:
            if self.rsi_arr[-2]> 70 and self.rsi_arr[-1]< self.rsi_arr[-2]:
                print("Buy Put")
                if self.stop_loss_wait_neutral == True:
                    print("Hostile Condition, waiting until neutral")

                elif last_close > price_ceiling:
                    print("Price trade deviated, exiting and recalibrate")
                    #   Make sure to close all position before stop, otherwise we will have hanging position
                    #   But this strat ensure this not happen, to do advanced stop later
                    self.cerebro.runstop()
                else:
                    self.order = self.buy(data='put', size=1, trailpercent = 7) # buy when closing price today crosses above MA.
        else:
            if ((self.rsi_arr[-1]< 30 or self.rsi_arr[-2] < 30) and self.rsi_arr[-1]> self.rsi_arr[-2]):
                print("Close Put on RSI")
                self.order = self.close(data='put')
            elif sec_price * 0.93 > self.getdatabyname('put').close[0]:
                print("Close Put on Stop Loss")
                self.stop_loss_wait_neutral = True
                self.order = self.close(data='put')
            elif sec_price * 1.1 < self.getdatabyname('put').close[0] and self.rsi_arr[-1]> self.rsi_arr[-2]:
                print("Close Put on Target")
                self.order = self.close(data='put')


class RSICall(StrategyWithLogging):
    def __init__(self):
        self.rsi = bt.talib.RSI(self.data.close, period=14)
        self.order = None
        self.rsi_arr = []
        self.rsi_arr.append(self.rsi + 0.0)
        self.stop_loss_wait_neutral = False

    def next(self):
        self.rsi_arr.append(self.rsi + 0.0)

        if backtest_glob == False:
            if self.data_live == False:
                return

        if self.order:
            print("call order pending, returning")
            return

        sec_price = self.getpositionbyname('call').price / p_factor
        last_close = self.getdatabyname('call').close[0]

        print("rsi %s %s call %s price %s" % (str(self.rsi_arr[-1]), str(self.rsi_arr[-2]), self.getdatabyname('call').close[0], sec_price))
        if(self.stop_loss_wait_neutral == True):
            print("Waiting for neutral")

        if self.rsi_arr[-1] > 50:
            if(self.stop_loss_wait_neutral == True):
                print("Neutral Waiting Finished")
            self.stop_loss_wait_neutral = False

        if self.getpositionbyname('call').size <= 0:
            if self.rsi_arr[-2]< 30 and self.rsi_arr[-1]> self.rsi_arr[-2]:
                print("Buy Call")
                if self.stop_loss_wait_neutral == True:
                    print("Hostile Condition, waiting until neutral")

                elif last_close > price_ceiling:
                    print("Price trade deviated, exiting and recalibrate")
                    #   Make sure to close all position before stop, otherwise we will have hanging position
                    #   But this strat ensure this not happen, to do advanced stop later
                    self.cerebro.runstop()
                else:
                    self.order = self.buy(data='call', size=1, trailpercent = 7) # buy when closing price today crosses above MA.
        else:

            if ((self.rsi_arr[-1]> 70 or self.rsi_arr[-2] > 70) and self.rsi_arr[-1]< self.rsi_arr[-2]):
                print("Close Call on RSI")
                self.order = self.close(data='call')
            elif sec_price * 0.93 > self.getdatabyname('call').close[0]:
                print("Close Call on Stop Loss")
                self.stop_loss_wait_neutral = True
                self.order = self.close(data='call')
            elif sec_price * 1.1 < self.getdatabyname('call').close[0] and self.rsi_arr[-1]< self.rsi_arr[-2]:
                print("Close Call on Big Profit")
                self.order = self.close(data='call')

def run(args=None):
    updateGlobalVar(symbol_glob)
    cerebro = bt.Cerebro()
    store = bt.stores.IBStore(port=port_conf)
    #store = bt.stores.IBStore(port=7497)
    stockkwargs = dict(
        timeframe=bt.TimeFrame.Minutes,
        compression=1,
        rtbar=True,  # use RealTime 5 seconds bars
        historical=backtest_glob,  # only historical download
        qcheck=0.5,  # timeout in seconds (float) to check for events
        #fromdate=datetime.datetime(2021, 9, 24),  # get data from..
        #todate=datetime.datetime(2022, 9, 25),  # get data from..
        latethrough=False,  # let late samples through
        tradename=None,  # use a different asset as order target
    )

    datafeeds = [
        ('stock'    , "%s-STK-SMART-USD"            % symbol_glob                                       ),
        ('put'      , "%s-%s-SMART-USD-%s-PUT"      % (symbol_glob, expdate_glob, str(strike_glob))     ),
        ('call'     , "%s-%s-SMART-USD-%s-CALL"     % (symbol_glob, expdate_glob, str(strike_glob))     )
    ]

    for alias, full_sec_name in datafeeds:
        data = store.getdata(dataname = full_sec_name, **stockkwargs)
        cerebro.resampledata(data, timeframe = trade_timeframe_type, compression=trade_timeframe_compress)
        cerebro.adddata(data, name=alias)

    cerebro.broker.setcash(1000)
    stval = cerebro.broker.getvalue()

    if backtest_glob == False:
        cerebro.broker = store.getbroker()

    cerebro.addstrategy(RSIPut)
    cerebro.addstrategy(RSICall)
    cerebro.run()

    endval = cerebro.broker.getvalue()

    #cerebro.plot()
    print(stval)
    print(endval)


if __name__ == '__main__':
    while True:
        run()
