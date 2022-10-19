from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
import pytz

import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds

class StrategyWithLogging(bt.Strategy):
    start_time = None
    close_time = None 

    # outputting information
    def log(self, txt):
        dt=self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def logdata(self):
        txt = []
        txt.append('{}'.format(len(self)))
        txt.append('{}'.format(self.data.datetime.datetime(0).isoformat()))
        txt.append('{:.2f}'.format(self.data.open[0]))
        txt.append('{:.2f}'.format(self.data.high[0]))
        txt.append('{:.2f}'.format(self.data.low[0]))
        txt.append('{:.2f}'.format(self.data.close[0]))
        txt.append('{:.2f}'.format(self.data.volume[0]))
        print(','.join(txt))

    data_live = False

    def notify_data(self, data, status, *args, **kwargs):
        print('*' * 5, 'DATA NOTIF:', data._getstatusname(status), *args)
        if status == data.LIVE:
            self.data_live = True
            #sgtz = pytz.timezone("Asia/Singapore")
            #nytz = pytz.timezone("America/New_York")

            nytime_now = datetime.datetime.now()
            self.start_time = nytime_now.replace(hour = 9, minute = 45, second = 0)
            self.close_time = nytime_now.replace(hour = 15, minute = 55, second = 0)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def eod_flush_position(self):
        self.close(data='put')
        self.close(data='call')
        self.cerebro.runstop()