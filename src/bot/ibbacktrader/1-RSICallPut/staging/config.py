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
trade_timeframe_type = bt.TimeFrame.Seconds
trade_timeframe_compress = 15

# If option price go out of (price_floor, price_ceiling) range, recalibrate strike price as we assume price action has deviated from at the money
price_ceiling = 10
price_floor = 1

rsi_low = 30
rsi_high = 70
safe_padding = 0

# Hard stop loss / take profit & amount of contract for each trade
sl_limit = 0.8
tp_floor = 1.2
ct_size = 1

  