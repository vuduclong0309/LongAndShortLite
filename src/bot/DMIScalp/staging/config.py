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
trade_timeframe_compress = 1

price_ceiling = 6.5
price_floor = 3.5

dmi_low = 10
dmi_high = 90
safe_padding = 0

sl_limit = 0.8
tp_floor = 1.2
ct_size = 1

dmiPeriod = 3
stochPeriod = 2
  