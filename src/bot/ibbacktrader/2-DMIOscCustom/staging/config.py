import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds

backtest_glob = False

#IBKR Client parameters
port_conf=7497
p_factor = 100  # IBKR simul broker has option price *100, thus need to divide by 100 to make price back to normal
use_rt_bar = True

# Trade parameters
symbol_glob = "SPY"
dtestep_glob = 0
trade_timeframe_type = bt.TimeFrame.Seconds
trade_timeframe_compress = 30

price_ceiling = 12.0
price_floor = 2.0

dmi_low = 10
dmi_high = 90
safe_padding = 0

sl_limit = 0.8
tp_floor = 1.2
ct_size = 1

dmiPeriod = 3
stochPeriod = 2
  