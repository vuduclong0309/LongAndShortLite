import datetime
import backtrader as bt

#Instantiate Cerebro engine
cerebro = bt.Cerebro(stdstats=False)

#Set data parameters and add to Cerebro
data1 = bt.feeds.YahooFinanceCSVData(
    dataname='TSLA.csv',
    fromdate=datetime.datetime(2018, 1, 1),
    todate=datetime.datetime(2020, 1, 1))
cerebro.adddata(data1)

data2 = bt.feeds.YahooFinanceCSVData(
    dataname='AAPL.csv',
    fromdate=datetime.datetime(2018, 1, 1),
    todate=datetime.datetime(2020, 1, 1))

data2.compensate(data1)  # let the system know ops on data1 affect data0
data2.plotinfo.plotmaster = data1
data2.plotinfo.sameaxis = True
cerebro.adddata(data2)

#Run Cerebro Engine
cerebro.run()
cerebro.plot()