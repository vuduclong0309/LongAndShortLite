# -*- coding: utf-8 -*-

###############################################################################
#
# Copyright (C) 2022 Duc Long Vu
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
        @Author: vuduclong0309
        @Date: 2022-Nov-30

TODO: refactor those horrendous variable name choices (Yep, I'm aware of that, please pardon me, I tried my best)

DISCLAIMER: THIS BOT IS ONLY FOR DEMONSTRATION, DON'T RUN IT IN PROD FOLDER (REAL TIME TRADING) IF YOU ARE NOT SURE

This RSI bot strategy is the first bot that I have ever run in real market during Oct 2022.

I included this bot only for demonstration purpose that we can develop sophisticated strategy using this framework.
Due to this reason, I will not include comment for the bot, unless this is critical (at least not in this lite version), but you are free to study this bot

I would only warn that RSI strategy is not as reliable in trending market.

You can move this file to any other folder (dev / staging / prod) to run in different environment:
    dev: backtesting strategy on historical data in test client
    staging: test run strategy real time in test client
    prod: real time trading (again, please read the disclaimer)

I'm more aware that I can use other approach on setting up config (e.g set up --conf flag). However, I find it user-friendly and most practical, 
having able to access and edit 3 environment at the same time, at the cost of somewhat duplicated code.

I will definitely use alternative approach in corporation enviroment.

To run this file, please simply run the associated bash script in the folder

It's a sophisticated variation of RSI indicator, with the following additional rules:

1. Instead of buying / selling underlying, we leverage by buying 4-5 dte at the money CALL / PUT option
    1.5 When the price of underlying stock move too far away, recalibrate STRIKE price
2. Doesn't trade within 30 minute of opening and closing (refer to start_time & close_time) as I assume this period to be volatile
3. Stop loss & take profit level as determined in config
4. If stop loss is hit, we wait until there is a trend reversal (oversold -> overbuy, and vice versa) before continuing
5. Instead of buying order when there is a cross signal, wait until there is a reversion.
"""


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
    basetime = stock.options[4].replace('-', '') # get 3-5dte date

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

    def next(self):
        global stop_loss_wait_reversal
        print(self.cerebro.broker.getvalue())

        self.logdata()
        self.rsi_arr.append(self.rsi + 0.0)

        sec_price = self.getpositionbyname('put').price / p_factor
        last_close = self.getdatabyname('put').close[0]

        print("rsi %s %s put %s price %s" % (str(self.rsi_arr[-1]), str(self.rsi_arr[-2]), self.getdatabyname('put').close[0], sec_price))
        print(stop_loss_wait_reversal)

        if backtest_glob == False:
            if self.data_live == False:
                return

            bar_time = self.data.datetime.datetime(0)

            if(bar_time < self.start_time):
                print("Not in trading time yet")
                return

            if(bar_time > self.close_time):
                print("Closing Position EOD")
                global eod
                eod = True
                self.eod_flush_position()
                return

        if (last_close > price_ceiling or last_close < price_floor) and not self.have_position() and backtest_glob == False:
            print("Price trade deviated, exiting and recalibrate")
            self.cerebro.runstop()

        if(stop_loss_wait_reversal == -1):
            print("Waiting for neutral")

        if self.rsi_arr[-1] <= rsi_low:
            if(stop_loss_wait_reversal == -1):
                print("Neutral Waiting Finished")
                stop_loss_wait_reversal = 0

        if self.order:
            print("pending order, returning")
            return

        if self.getpositionbyname('put').size <= 0:
            if (last_close > price_ceiling or last_close < price_floor):
                return
            if self.rsi_arr[-2]> rsi_high and self.rsi_arr[-1]< self.rsi_arr[-2]:
                print("Buy Put")
                if stop_loss_wait_reversal == -1:
                    print("Hostile Condition, waiting until neutral")
                else:
                    self.order = self.buy(data='put', size=ct_size) 
        else:
            if ((self.rsi_arr[-1]< rsi_low + safe_padding or self.rsi_arr[-2] < rsi_low + safe_padding) and self.rsi_arr[-1]> self.rsi_arr[-2]):
                print("Close Put on RSI")
                self.order = self.close(data='put')
            elif sec_price * sl_limit > self.getdatabyname('put').close[0]:
                print("Close Put on Stop Loss")
                stop_loss_wait_reversal = -1
                self.order = self.close(data='put')
            elif sec_price * tp_floor < self.getdatabyname('put').close[0] and self.rsi_arr[-1]> self.rsi_arr[-2]:
                print("Close Put on Target")
                self.order = self.close(data='put')


class RSICall(StrategyWithLogging):
    def __init__(self):
        self.rsi = bt.talib.RSI(self.data.close, period=14)
        self.order = None
        self.rsi_arr = []
        self.rsi_arr.append(self.rsi + 0.0)

    def next(self):
        global stop_loss_wait_reversal
        self.rsi_arr.append(self.rsi + 0.0)

        sec_price = self.getpositionbyname('call').price / p_factor
        last_close = self.getdatabyname('call').close[0]
        
        print("rsi %s %s call %s price %s" % (str(self.rsi_arr[-1]), str(self.rsi_arr[-2]), self.getdatabyname('call').close[0], sec_price))
        print(stop_loss_wait_reversal)

        if backtest_glob == False:
            if self.data_live == False:
                return
            bar_time = self.data.datetime.datetime(0)

            if(bar_time < self.start_time):
                print("Not in trading time yet")
                return

            if(bar_time > self.close_time):
                print("Closing Position EOD")
                global eod
                eod = True
                self.eod_flush_position()
                return
        
        if self.order:
            print("call order pending, returning")
            return

        if (last_close > price_ceiling or last_close < price_floor) and not self.have_position() and backtest_glob == False:
            print("Price trade deviated, exiting and recalibrate")
            self.cerebro.runstop()

        if(stop_loss_wait_reversal == 1):
            print("Waiting for neutral")

        if self.rsi_arr[-1] >= rsi_high:
            if(stop_loss_wait_reversal == 1):
                print("Neutral Waiting Finished")
                stop_loss_wait_reversal = 0

        if self.getpositionbyname('call').size <= 0:
            if (last_close > price_ceiling or last_close < price_floor):
                return 

            if self.rsi_arr[-2]< rsi_low and self.rsi_arr[-1]> self.rsi_arr[-2]:
                print("Buy Call")
                if stop_loss_wait_reversal == 1:
                    print("Hostile Condition, waiting until neutral")
                else:
                    self.order = self.buy(data='call', size=ct_size) 
        else:

            if ((self.rsi_arr[-1]> rsi_high - safe_padding or self.rsi_arr[-2] > rsi_high - safe_padding) and self.rsi_arr[-1]< self.rsi_arr[-2]):
                print("Close Call on RSI")
                self.order = self.close(data='call')
            elif sec_price * sl_limit > self.getdatabyname('call').close[0]:
                print("Close Call on Stop Loss")
                stop_loss_wait_reversal = 1
                self.order = self.close(data='call')
            elif sec_price * tp_floor < self.getdatabyname('call').close[0] and self.rsi_arr[-1]< self.rsi_arr[-2]:
                print("Close Call on Big Profit")
                self.order = self.close(data='call')

def run(args=None):
    updateGlobalVar(symbol_glob)
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
    while eod == False:
        print(eod)
        run()
