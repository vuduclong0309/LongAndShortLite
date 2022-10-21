import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds

#IBKR Client parameters
port_conf=7497
p_factor = 1  # IBKR simul broker has option price *100, thus need to divide by 100 to make price back to normal
use_rt_bar = True

# Trade parameters
backtest_glob = True
symbol_glob = "SPY"
trade_timeframe_type = bt.TimeFrame.Minutes
trade_timeframe_compress = 3

price_ceiling = 7.5
safe_padding = 2


  