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

A quick demonstration with a custom built indicator in action (paper account trading)
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

def updateGlobalVar(symbol, dtestep):
    global expdate_glob
    global strike_glob
    strike_glob = 0
    stock = yf.Ticker(symToYF(symbol))
    latest_price = stock.history(period='2d', interval='1m')['Close'][-1]
    basetime = stock.options[dtestep].replace('-', '') # get 3-5dte date

    expdate_glob = basetime

    for strike in stock.option_chain().calls['strike']:
        if(abs(strike - latest_price) < abs(strike_glob - latest_price)):
            strike_glob = strike

    print("global var update: "  + symbol + " " + expdate_glob + " " + str(strike_glob))
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

        self.l.dmiStoch = bt.DivByZero(bt.ind.SumN(dmiOsc - oscLowest, period = self.p.stochPeriod) , bt.ind.SumN(oscHighest - oscLowest, period = self.p.stochPeriod) , 1) * 100

class dmiStochPut(StrategyWithLogging):
    def __init__(self):
        self.dmi = dmiStoch()
        self.order = None
        self.dmi_arr = []
        self.dmi_arr.append(self.dmi + 0.0)

    def next(self):
        global stop_loss_wait_reversal
        print(self.cerebro.broker.getvalue())

        self.logdata()
        self.dmi_arr.append(self.dmi + 0.0)

        sec_price = self.getpositionbyname('put').price / p_factor
        last_close = self.getdatabyname('put').close[0]

        print("dmi %s %s put %s price %s" % (str(self.dmi_arr[-1]), str(self.dmi_arr[-2]), self.getdatabyname('put').close[0], sec_price))
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

        if self.dmi_arr[-1] <= dmi_low:
            if(stop_loss_wait_reversal == -1):
                print("Neutral Waiting Finished")
                stop_loss_wait_reversal = 0

        if self.order:
            print("pending order, returning")
            return

        print (self.getpositionbyname('put'))
        if self.getpositionbyname('put').size <= 0:
            if (last_close > price_ceiling or last_close < price_floor):
                return
            if self.dmi_arr[-2]> dmi_high and self.dmi_arr[-1]< self.dmi_arr[-2]:
                print("Buy Put")
                if stop_loss_wait_reversal == -1:
                    print("Hostile Condition, waiting until neutral")
                else:
                    self.order = self.buy(data='put', size=ct_size) # buy when closing price today crosses above MA.
        else:
            if ((self.dmi_arr[-1]< dmi_low + safe_padding or self.dmi_arr[-2] < dmi_low + safe_padding) and self.dmi_arr[-1]> self.dmi_arr[-2]):
                print("Close Put on dmi")
                self.order = self.close(data='put')
            elif sec_price * sl_limit > self.getdatabyname('put').close[0]:
                print("Close Put on Stop Loss")
                stop_loss_wait_reversal = -1
                self.order = self.close(data='put')
            elif sec_price * tp_floor < self.getdatabyname('put').close[0] and self.dmi_arr[-1]> self.dmi_arr[-2]:
                print("Close Put on Target")
                self.order = self.close(data='put')

class dmiStochCall(StrategyWithLogging):
    def __init__(self):
        self.dmi = dmiStoch()
        self.order = None
        self.dmi_arr = []
        self.dmi_arr.append(self.dmi + 0.0)

    def next(self):
        global stop_loss_wait_reversal
        self.logdata()
        print(self.broker.getvalue())
        self.dmi_arr.append(self.dmi + 0.0)

        sec_price = self.getpositionbyname('call').price / p_factor
        last_close = self.getdatabyname('call').close[0]
        
        print("dmi %s %s call %s price %s" % (str(self.dmi_arr[-1]), str(self.dmi_arr[-2]), self.getdatabyname('call').close[0], sec_price))
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

        if self.dmi_arr[-1] >= dmi_high:
            if(stop_loss_wait_reversal == 1):
                print("Neutral Waiting Finished")
                stop_loss_wait_reversal = 0

        print(self.getpositionbyname('call'))
        if self.getpositionbyname('call').size <= 0:
            if (last_close > price_ceiling or last_close < price_floor):
                return 
            try:
                print((self.dmi_arr[-2]< dmi_low) and (self.dmi_arr[-1]> self.dmi_arr[-2]))
            except Exception as e:
                print (e)

            if self.dmi_arr[-2]< dmi_low and self.dmi_arr[-1]> self.dmi_arr[-2]:
                print("Buy Call")
                if stop_loss_wait_reversal == 1:
                    print("Hostile Condition, waiting until neutral")
                else:
                    self.order = self.buy(data='call', size=ct_size) # buy when closing price today crosses above MA.
        else:
            if ((self.dmi_arr[-1]> dmi_high - safe_padding or self.dmi_arr[-2] > dmi_high - safe_padding) and self.dmi_arr[-1]< self.dmi_arr[-2]):
                print("Close Call on dmi")
                self.order = self.close(data='call')
            elif sec_price * sl_limit > self.getdatabyname('call').close[0]:
                print("Close Call on Stop Loss")
                stop_loss_wait_reversal = 1
                self.order = self.close(data='call')
            elif sec_price * tp_floor < self.getdatabyname('call').close[0] and self.dmi_arr[-1]< self.dmi_arr[-2]:
                print("Close Call on Big Profit")
                self.order = self.close(data='call')

def run(args=None):
    updateGlobalVar(symbol_glob, dtestep_glob)
    cerebro = bt.Cerebro()
    store = bt.stores.IBStore(port=port_conf)
    #store = bt.stores.IBStore(port=7497)
    stockkwargs = dict(
        timeframe=trade_timeframe_type,
        compression=trade_timeframe_compress,
        rtbar=True,  # use RealTime 5 seconds bars
        historical=False,  # only historical download
        qcheck=0.5,  # timeout in seconds (float) to check for events
        preload=False,
        live=False,
        latethrough=False,  # let late samples through
    )

    datafeeds = [
        ('stock'    , "%s-STK-SMART-USD"            % symbol_glob                                       ),
        ('call'     , "%s-%s-SMART-USD-%s-CALL"      % (symbol_glob, expdate_glob, str(strike_glob))    ),
        ('put'      , "%s-%s-SMART-USD-%s-PUT"      % (symbol_glob, expdate_glob, str(strike_glob))     ),

    ]


    for alias, full_sec_name in datafeeds:
        data = store.getdata(dataname = full_sec_name, **stockkwargs)
        cerebro.resampledata(data, timeframe = trade_timeframe_type, compression=trade_timeframe_compress)
        cerebro.adddata(data, name=alias)

    cerebro.broker.setcash(1000)
    stval = cerebro.broker.getvalue()

    if backtest_glob == False:
        cerebro.broker = store.getbroker()

    cerebro.addstrategy(dmiStochCall)
    cerebro.addstrategy(dmiStochPut)
    cerebro.run()

    endval = cerebro.broker.getvalue()

    print(stval)
    print(endval)


if __name__ == '__main__':
    while eod == False:
        print(eod)
        run()
