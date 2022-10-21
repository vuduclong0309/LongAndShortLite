import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds

#IBKR Client parameters
port_conf=7497
p_factor = 100  # IBKR simul broker has option price *100, thus need to divide by 100 to make price back to normal
use_rt_bar = False

# Trade parameters
backtest_glob = False
symbol_glob = "SPY"
trade_timeframe_type = bt.TimeFrame.Seconds
trade_timeframe_compress = 15

price_ceiling = 6.0
safe_padding = 2

  