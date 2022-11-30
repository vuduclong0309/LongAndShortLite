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
        @Credit: Backtrader
        @Links: https://www.backtrader.com/docu

This module is an example the most basic example of a Backtrader Bot based on the introduction page, 
using InteractiveBroker as the data source to print close price of selected security (SPY)
and then plot the historical price.
"""

import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds


class PrintClose(bt.Strategy):
    def logdata(self):
        txt = []
        txt.append('{}'.format(len(self)))
        txt.append('{}'.format(
            self.data.datetime.datetime(0).isoformat()))
        txt.append('{:.2f}'.format(self.data.open[0]))
        txt.append('{:.2f}'.format(self.data.high[0]))
        txt.append('{:.2f}'.format(self.data.low[0]))
        txt.append('{:.2f}'.format(self.data.close[0]))
        txt.append('{:.2f}'.format(self.data.volume[0]))
        print(','.join(txt))

    def next(self):
        self.logdata()


def run(args=None):
    cerebro = bt.Cerebro()
    ibstore = bt.stores.IBStore(host='127.0.0.1', port=7497)
    data = ibstore.getdata(dataname='SPY-STK-SMART-USD',
                       timeframe=bt.TimeFrame.Seconds, compression=5, historical="True")

    # Compress real time 5 second bar to 1 minute bar
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=1)

    cerebro.addstrategy(PrintClose)


    cerebro.run()
    cerebro.plot()

if __name__ == '__main__':
    run()
