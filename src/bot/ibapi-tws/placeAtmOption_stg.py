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

This is a helper tool to place at the money option order rapidly
Especially helpful for manually play based on trade signal

There are two files (one file with _stg postfix for staging). The only different is ENV variable

I find this set up is the most efficient at hotfixing and patching real time bug at the cost of duplicated file (Please refer to EnvironmentSetup.md explanation)
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
from ibapi.order import *

from threading import Timer

import yfinance as yf

ENV = "prod"

port = {
    "staging": 7497,
    "prod": 7496
    }

symbol = "SPY"
expdate_glob = ""
strike_glob = 0
ct_size = 1

dte = {
    "SPX": 0,
    "SPY": 2,
    "TSLA": 1,
    "AAPL": 0
    }


def symToYF(symbol):
    if symbol == "SPX":
        return "^SPX"
    return symbol

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

    print("Option Info: "  + symbol + " " + expdate_glob + " " + str(strike_glob))
    return

def printLastOptionInfo():
    print("Last Option Info: "  + symbol + " " + expdate_glob + " " + str(strike_glob))
    stock = yf.Ticker(symToYF(symbol))

    for i in range(6):
        print("dtestep = " + str(i) + "expdate: " + stock.options[i].replace('-', ''))
    return



class OrderApp(EWrapper, EClient):
    optRight = "C"
    quantity = 1
    action = "BUY"

    def __init__(self):
        EClient.__init__(self, self)

    def __init__(self, optRight, quantity, action):
        EClient.__init__(self, self)
        self.optRight = optRight
        self.quantity = quantity
        self.action = action

    def tickPrice(self, reqId, tickType, price, attrib):
        print("Tick Price. Ticker Id:", reqId, "tickType:", TickTypeEnum.to_str(tickType))

    def tickSize(self, reqId, tickType, size):
        print("Tick Size. Ticker Id:", reqId, "tickType", TickTypeEnum.to_str(tickType), "Size:", size)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def contractDetails(self, reqId, contractDetails):
        print("contractDetails: ", reqId, " ", contractDetails)

    def historicalData(self, reqId, bar):
        print("HistoricalData. ", reqId, "Date:", bar.date, "Open:", bar.open, "High:", bar.high, "Low:", bar.low, "Close:", bar.close, "Volume:", bar.volume)

    def nextValidId(self, orderId):
        self.nextOrderId = orderId
        self.start()

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPriceA):
        print("OrderStatus. Id: ", orderId, ", Status: ", status, ", Filled: ", filled, ",Remaining: ", remaining, ", LastFillPrice: ", lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        print("OpenOrder. ID:", orderId, contract.symbol, contract.secType, "@", contract.exchange, ":", order.action, order.orderType, order.totalQuantity, orderState.status)

    def execDetails(self, reqId, contract, execution):
        print("ExecDetails. ", reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)


    def start(self):
        global expdate_glob, strike_glob, symbol
        contract = Contract()
        contract.symbol = symbol
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = expdate_glob
        contract.strike = strike_glob
        contract.right = self.optRight
        contract.multiplier = "100"

        order = Order()
        order.action = self.action
        order.totalQuantity = self.quantity
        order.orderType = "MKT"
        order.eTradeOnly = ''
        order.firmQuoteOnly = ''


        self.placeOrder(self.nextOrderId, contract, order)

    def stop(self):
        self.done = True
        self.disconnect()


def run(optRight, ct_size, action):
    app = OrderApp(optRight, ct_size, action)
    app.nextOrderId = 0

    app.connect("127.0.0.1", port[ENV], 0)


    #app.reqContractDetails(1, contract)
    #app.reqMarketDataType(4)
    #app.reqMktData(1, contract, "", False, False, [])
    #app.reqHistoricalData(1, contract, "", "1 D", "1 min", "MIDPOINT", 0, 1, False, [])

    Timer(3, app.stop).start()
    app.run()

if __name__ == "__main__":
    updateGlobalVar(symbol, dte[symbol])
    while(True):
        print("ENV: " + ENV)
        printLastOptionInfo()
        txt = """
            Enter command: [TickerName | dte | [0-4] ]
            TickerName. (e.g SPX) Change Underlying Security 
            dte. Update Stock DTE
            0. Set Size
            1. Buy Call
            2. Buy Put
            3. Sell Call
            4. Sell Put
            """
        print(txt)
        try:
            cmd = input()
                
            if cmd == '1':
                updateGlobalVar(symbol, dte[symbol])
                run("C", ct_size, "BUY")
            elif cmd == '2':
                updateGlobalVar(symbol, dte[symbol])
                run("P", ct_size, "BUY")
            elif cmd == '3':
                run("C", ct_size, "SELL")
            elif cmd == '4':
                run("P", ct_size, "SELL")
            elif cmd in dte.keys():
                symbol = cmd
                updateGlobalVar(symbol, dte[symbol])
            elif cmd == "dte":
                print(dte)
                ndte = int(input("select dte step: "))
                dte[symbol] = ndte
            elif cmd == '0':
                ct_size = int(input("select size:"))
        except Exception as e:
            print(e)
