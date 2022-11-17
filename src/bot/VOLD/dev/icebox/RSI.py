from datetime import datetime
import backtrader as bt
import yfinance as yf
import time

# Create a subclass of Strategy to define the indicators and logic

class StochRSI(bt.Strategy):

    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=14)
        
    # outputting information
    def log(self, txt):
        dt=self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def next(self):
        #if not self.position: # check if you already have a position in the market
        if (self.rsi < 30 and self.position.size < 10):
            self.log('Buy Create, %.2f' % self.data.close[0])
            self.buy(size=1) # buy when closing price today crosses above MA.
        else:
            # This means you are in a position, and hence you need to define exit strategy here.
            if (self.rsi > 70 and self.position.size > -10):
                self.log('Position Closed, %.2f' % self.data.close[0])
                self.sell(size=1)

    def notify_order(self, order):
        if order.status == order.Completed:
            if order.isbuy():
                self.log(
                "Executed BUY (Price: %.2f, Value: %.2f, Commission %.2f)" %
                (order.executed.price, order.executed.value, order.executed.comm))
            else:
                self.log(
                "Executed SELL (Price: %.2f, Value: %.2f, Commission %.2f)" %
                (order.executed.price, order.executed.value, order.executed.comm))
                self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order was canceled/margin/rejected")
            self.order = None



if __name__ == '__main__':
    # Create a cerebro instance, add our strategy, some starting cash at broker and a 0.1% broker commission
    cerebro = bt.Cerebro()
    cerebro.addstrategy(StochRSI)
    cerebro.broker.setcash(10000)
    cerebro.broker.setcommission(commission=0.001)
    data = bt.feeds.PandasData(dataname=yf.download("SPY", start="2021-01-01", end="2022-10-25", interval = "1h"))
    cerebro.adddata(data)

    print('<START> Brokerage account: $%.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('<FINISH> Brokerage account: $%.2f' % cerebro.broker.getvalue())
    cerebro.plot()
