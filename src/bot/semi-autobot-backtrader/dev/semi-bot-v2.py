#Imports
import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
import ta
import numpy as np
import pandas as pd
import pytz
import math
from datetime import datetime, timedelta
import threading
import time

import yfinance as yf

from config import *

#Vars
orderId = 2221121221
reqId = 1

#Class for Interactive Brokers Connection
class IBApi(EWrapper,EClient):
    def __init__(self):
        EClient.__init__(self, self)

    # Historical Backtest Data
    def historicalData(self, reqId, bar):
        print("HistoricalData. ReqId:", reqId, "BarData.", bar)

    # On Realtime Bar after historical data finishes
    def historicalDataUpdate(self, reqId, bar):
        print("HistoricalDataUpdate. ReqId:", reqId, "BarData.", bar)
    # On Historical Data End
    def historicalDataEnd(self, reqId, start, end):
        super().historicalDataEnd(reqId, start, end)
        print("HistoricalDataEnd. ReqId:", reqId, "from", start, "to", end)
    
    # Get next order id we can use
    def nextValidId(self, nextorderId):
        super().nextValidId(orderId)

        print("setting nextValidOrderId: %d" % orderId)
        self.nextValidOrderId = orderId
        print("NextValidId:", orderId)


ib = IBApi()
ib.connect("127.0.0.1", 7497,1)

ib.reqIds(-1)

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

    print("global var update: "  + symbol + " " + expdate_glob + " " + str(strike_glob))
    return

#Bar Object
class Bar:
    open = 0
    low = 0
    high = 0
    close = 0
    volume = 0
    date = datetime.now()
    def __init__(self):
        self.open = 0
        self.low = 0
        self.high = 0
        self.close = 0
        self.volume = 0
        self.date = datetime.now()

#Bracet Order Setup
def bracketOrder(parentOrderId, action, quantity, opt_right):
    #Initial Entry
    #Create our IB Contract Object
    contract = Contract()
    contract.symbol = symbol.upper()
    contract.secType = "OPT"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.lastTradeDateOrContractMonth = expdate_glob
    contract.strike = strike_glob
    contract.right = opt_right
    contract.multiplier = "100"
    print("kk")
    ib.reqContractDetails(1,contract)
    print("kk")
    ##ib.run()
   
    # Create Parent Order / Initial Entry
    parent = Order()
    parent.orderId = parentOrderId
    parent.orderType = "MKT"
    parent.action = action
    parent.totalQuantity = quantity
    parent.transmit = False
    
    # Stop Loss
    stopLossOrder = Order()
    stopLossOrder.orderId = parent.orderId+1
    stopLossOrder.orderType = "TRAIL"
    stopLossOrder.action = "SELL"
    stopLossOrder.totalQuantity = quantity
    stopLossOrder.parentId = parentOrderId
    stopLossOrder.trailingPercent = 0.2
    stopLossOrder.transmit = True

    bracketOrders = [parent, stopLossOrder]
    return bracketOrders

def run(opt_right, ct_size):
    global orderId
    updateGlobalVar(symbol)
        
    #Create our IB Contract Object
    contract = Contract()
    contract.symbol = symbol.upper()
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
  
    quantity = ct_size
    bracket = bracketOrder(orderId,"BUY",quantity,opt_right)

    #Place Bracket Order

    for o in bracket:
        o.ocaGroup = "OCA_"+str(orderId)
        print(o)
        ib.placeOrder(o.orderId,contract,o)
    orderId += 3

while(True):
    txt = """
        Enter command:
        0. Recalibrate
        1. Buy Call 
        2. Buy Put
        """
    print(txt)
    cmd = input()
    if cmd == '0':
        print("ok")
        updateGlobalVar(symbol)
    else:
        if cmd == '1':
            run("C", ct_size)
        elif cmd == '2':
            run("P", ct_size)



      
