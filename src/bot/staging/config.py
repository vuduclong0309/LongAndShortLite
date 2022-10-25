import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds

#IBKR Client parameters
port_conf=7497
p_factor = 100  # IBKR simul broker has option price *100, thus need to divide by 100 to make price back to normal
use_rt_bar = True

# Trade parameters
backtest_glob = False
symbol_glob = "SPY"
trade_timeframe_type = bt.TimeFrame.Seconds
trade_timeframe_compress = 15

price_ceiling = 10.0

rsi_low = 30
rsi_high = 70
safe_padding = 2

sl_limit = 0.9
tp_floor = 1.1
ct_size = 1


  