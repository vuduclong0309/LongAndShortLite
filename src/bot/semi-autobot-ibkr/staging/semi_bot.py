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


class RSICall(StrategyWithLogging):
    def next(self):
        self.logdata()
        self.order = self.buy(data=buy_sec, size=ct_size) # buy when closing price today crosses above MA.
        self.cerebro.runstop()

def run(cmd):
    cerebro = bt.Cerebro()
    store = bt.stores.IBStore(port=port_conf)
    #store = bt.stores.IBStore(port=7497)
    stockkwargs = dict(
        timeframe=trade_timeframe_type,
        compression=1,
        rtbar=use_rt_bar,  # use RealTime 5 seconds bars
        historical=backtest_glob,  # only historical download
        qcheck=0.5,  # timeout in seconds (float) to check for events
        #fromdate=datetime.datetime(2021, 9, 24),  # get data from..
        #todate=datetime.datetime(2022, 9, 25),  # get data from..
        latethrough=False,  # let late samples through
        tradename=None,  # use a different asset as order target
        backfill=False
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


    if backtest_glob == False:
        cerebro.broker = store.getbroker()

    cerebro.addstrategy(RSICall)
    cerebro.run()


if __name__ == '__main__':
    while eod == False:
        txt = """
        Enter command:
        0. Recalibrate
        1. Buy Call 
        2. Sell Call
        3. Buy Put
        4. Sell Put
        """
        print(txt)
        cmd = input()
        if cmd == '0':
            print("ok")
            updateGlobalVar(symbol_glob)
        else:
            if cmd == '1':
                buy_sec='call'
                ct_size=1
                run(cmd)
            elif cmd == '2':
                buy_sec='call'
                ct_size=-1
                run(cmd)
            elif cmd == '3':
                buy_sec='put'
                ct_size=1
                run(cmd)
            elif cmd == '4':
                buy_sec='put'
                ct_size=-1
                run(cmd)
            
