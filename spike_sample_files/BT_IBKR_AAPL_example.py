
import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds


class PrintClose(bt.Strategy):

    def start(self):
        print("ok")

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
    def notify_store(self, msg, *args, **kwargs):
        print('STORE NOTIF:{}', msg)

    def next(self):
        self.logdata()


def run(args=None):
    cerebro = bt.Cerebro()
    ibstore = bt.stores.IBStore(host='127.0.0.1', port=7497)
    data = ibstore.getdata(dataname='AAPL-STK-SMART-USD',
                       timeframe=bt.TimeFrame.Seconds, compression=5, historical="True")

    ##cerebro.replaydata(data, timeframe=bt.TimeFrame.Minutes, compression=2)
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=1)

    #cerebro.adddata(data) #not sure if this is needed, but commenting it out does not fix the problem

    cerebro.addstrategy(PrintClose)


    cerebro.run()

if __name__ == '__main__':
    run()
