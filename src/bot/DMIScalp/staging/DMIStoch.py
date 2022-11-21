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
import pytz

import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds

import yfinance as yf

from config import *
from utils import *

expdate_glob = ""
strike_glob = ""

stop_loss_wait_reversal = 0

eod = False

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

class dmiOsc(bt.Indicator):
    lines = ('dmiOsc',)

    def __init__(self):
        dmi = bt.ind.DirectionalMovementIndex()
        self.l.dmiOsc = dmi.DIplus - dmi.DIminus

class dmiStoch(bt.Indicator):
    lines = ('dmiStoch',)
    params = (('dmiPeriod', 3), ('stochPeriod', 2),)

    def __init__(self):
        dmi = bt.ind.DirectionalMovementIndex()
        dmiOsc = dmi.DIplus - dmi.DIminus

        oscHighest = bt.ind.Highest(dmiOsc, period=self.p.dmiPeriod)
        oscLowest = bt.ind.Lowest(dmiOsc, period=self.p.dmiPeriod)

        self.l.dmiStoch = bt.ind.SumN(dmiOsc - oscLowest, period = self.p.stochPeriod) / bt.ind.SumN(oscHighest - oscLowest, period = self.p.stochPeriod)

class RSIPut(StrategyWithLogging):
    lines = ('dmiStoch',)
    def __init__(self):
        global dmiPeriod
        global stochPeriod

        self.dmiOsc = dmiOsc()
        self.dmiStoch = dmiStoch(dmiPeriod = dmiPeriod, stochPeriod = stochPeriod)
        
        self.order = None

    def next(self):
        self.logdata()
        print(self.cerebro.broker.getvalue())
        print(self.dmiOsc + 0.0)
        print(self.dmiStoch + 0.0)
        if(len(self) == 480):
            self.cerebro.runstop()
        print("ok")



def run(args=None):
    updateGlobalVar(symbol_glob)
    cerebro = bt.Cerebro()
    store = bt.stores.IBStore(port=port_conf)
    #store = bt.stores.IBStore(port=7497)
    stockkwargs = dict(
        timeframe=trade_timeframe_type,
        compression=trade_timeframe_compress,
        rtbar=use_rt_bar,  # use RealTime 5 seconds bars
        historical=True,  # only historical download
        qcheck=0.5,  # timeout in seconds (float) to check for events
        preload=False,
        live=False,
        #fromdate=datetime.datetime(2021, 9, 24),  # get data from..
        #todate=datetime.datetime(2022, 9, 25),  # get data from..
        latethrough=False,  # let late samples through
        tradename=None,  # use a different asset as order target
    )

    datafeeds = [
        ('stock'    , "%s-STK-SMART-USD"            % symbol_glob                                       ),
        #('put'      , "%s-%s-SMART-USD-%s-PUT"      % (symbol_glob, expdate_glob, str(strike_glob))     ),
    ]

    for alias, full_sec_name in datafeeds:
        data = store.getdata(dataname = full_sec_name, **stockkwargs)
        #cerebro.resampledata(data, timeframe = trade_timeframe_type, compression=trade_timeframe_compress)
        cerebro.adddata(data, name=alias)

    cerebro.broker.setcash(1000)
    stval = cerebro.broker.getvalue()

    if backtest_glob == False:
        cerebro.broker = store.getbroker()

    cerebro.addstrategy(RSIPut)
    cerebro.run()

    endval = cerebro.broker.getvalue()

    cerebro.plot()
    print(stval)
    print(endval)


if __name__ == '__main__':
    while eod == False:
        print(eod)
        run()
