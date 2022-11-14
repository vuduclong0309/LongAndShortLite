from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
from ibapi.order import *

from threading import Timer

import yfinance as yf

symbol = "SPY"
expdate_glob = ""
strike_glob = ""
ct_size = 1

dte = {
    "SPX": 0,
    "SPY": 2
    }


def symToYF(symbol):
    if symbol == "SPX":
        return "^SPX"
    return symbol

def trimPrice(symbol, latest_price):
    tprice = int(latest_price)
    
    if(symbol == "SPX"):
        tprice = tprice - tprice % 5
    
    return tprice

def updateGlobalVar(symbol, dtestep):
    global expdate_glob
    global strike_glob
    stock = yf.Ticker(symToYF(symbol))
    latest_price = stock.history(period='2d', interval='1m')['Close'][-1]
    basetime = stock.options[dtestep].replace('-', '') # get 3-5dte date

    expdate_glob = basetime
    strike_glob = trimPrice(symbol, latest_price)

    print("global var update: "  + symbol + " " + expdate_glob + " " + str(strike_glob))
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

        self.placeOrder(self.nextOrderId, contract, order)

    def stop(self):
        self.done = True
        self.disconnect()


def run(optRight, ct_size, action):
    app = OrderApp(optRight, ct_size, action)
    app.nextOrderId = 0

    app.connect("127.0.0.1", 7496, 0)


    #app.reqContractDetails(1, contract)
    #app.reqMarketDataType(4)
    #app.reqMktData(1, contract, "", False, False, [])
    #app.reqHistoricalData(1, contract, "", "1 D", "1 min", "MIDPOINT", 0, 1, False, [])

    Timer(3, app.stop).start()
    app.run()

if __name__ == "__main__":
    while(True):
        txt = """
            Enter command:
            dte. Update Stock DTE
            0. Set Size
            1. Buy Call
            2. Buy Put
            3. Sell Call
            4. Sell Put
            """
        print(txt)
        cmd = input()
        if cmd in ['0', '1', '2']:
            updateGlobalVar(symbol, dte[symbol])
        if cmd == '1':
            run("C", ct_size, "BUY")
        elif cmd == '2':
            run("P", ct_size, "BUY")
        elif cmd == '3':
            run("C", ct_size, "SELL")
        elif cmd == '4':
            run("P", ct_size, "SELL")
        elif cmd in dte.keys():
            symbol = cmd
        elif cmd == "dte":
            nsym = input("select ticker: ")
            ndte = int(input("select dte step: "))
            dte[nsym] = ndte
        elif cmd == '0':
            ct_size = int(input("select size:"))
