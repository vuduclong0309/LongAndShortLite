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
        @Credit: TraderAcademy by InteractiveBroker
        @Links: https://tradersacademy.online/trading-lesson/python-placing-orders

This module is the real code module using in TraderAcademy lesson on TWS API on how to place order through TWS API
I just write this according to the video, since I can't find the code anywhere else
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
from ibapi.order import *

from threading import Timer

class OrderApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

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
        print("ExecDetails. ", reqId, contract.symbol, contract.secType, contract.currecncy, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)

    def start(self):
        contract = Contract()
        contract.symbol = "AAPL"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.primaryExchange = "NASDAQ"

        order = Order()
        order.action = "BUY"
        order.totalQuantity = 10
        order.orderType = "LMT"
        order.lmtPrice = 210
        order.eTradeOnly = ''
        order.firmQuoteOnly = ''

        self.placeOrder(self.nextOrderId, contract, order)

    def stop(self):
        self.done = True
        self.disconnect()


def main():
    app = OrderApp()
    app.nextOrderId = 0

    app.connect("127.0.0.1", 7497, 0)


    #app.reqContractDetails(1, contract)
    #app.reqMarketDataType(4)
    #app.reqMktData(1, contract, "", False, False, [])
    #app.reqHistoricalData(1, contract, "", "1 D", "1 min", "MIDPOINT", 0, 1, False, [])

    Timer(3, app.stop).start()
    app.run()

if __name__ == "__main__":
    main()