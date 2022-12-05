# Installation Guide

--- 
## Overview
This documents is a brief guide on how to install all prerequisite to run this project:
* Git
* Python 3
* Backtrader (Disclaimer: please use my forked repo, for IBKR related bug fix)
* IBKR TradeWorkerStation

## Git
Just in case if you are using Github Desktop or similar case, 
setting up a Git client should help tremendously.
Here's a quick start guide for setting up git.

https://docs.github.com/en/get-started/quickstart/set-up-git

When things are done, you can test this by cloning this repo to your computer:

```git clone https://github.com/vuduclong0309/LongAndShort.git ```

## Python
And here's a guide for installing Python:
```https://realpython.com/installing-python/```

## Backtrader
```A feature-rich Python framework for backtesting and trading```

Short version: Copy and Paste this command line
```
pip install git+https://github.com/vuduclong0309/backtrader && pip install git+https://github.com/blampe/IbPy.git
```

There's an official guide here: https://github.com/mementum/backtrader, 
but you need to swap the pip installion line to my own repo

However, as this repo is not longer supported, and there was a nasty datetime format issue change
there would be an issue here https://community.backtrader.com/topic/6522/ib-market-data-subscriptions-end-date-time-the-date-time-or-time-zone-entered-is-invalid

I managed to fix it on my own fork: https://github.com/vuduclong0309/backtrader/tree/master/backtrader

Once you're done, you can check by running the code at /src/proto/AAPL_yfinance_feed.py to test the program
(doesn't need TradeWorkerStation)
If you encounter problem related to yfinance module not found, run this:
```pip install yfinance```

## IBKR TraderWorkStation
For real trading you would need a broker. IBKR is one broker that Backtrader support both backtesting and live trading.
This is also one of the best broker available online 

You can sign up for a free trial paper trade account here https://ibkr.com/referral/duclong842
Should you want to do real trade, you can convert to real account. 

If you do so, you can use a referral code https://ibkr.com/referral/duclong842,
so you get up to 1000$USD and I also have some extra coffee (blush)

*Notes:* When you are using free trial you may want to test your program only in real trading hour, 
or your need to subscribe into IBKR market data pack

```US Securities Snapshot and Futures Value Bundle: real-time top of book quotes for CBOT, CME, COMEX, and NYMEXUS.```

After you have a trial account, you'd want to install TWS here 
```https://www.interactivebrokers.com.sg/en/trading/tws.php```

After TWS installed, you would need to config TWS to send data to the bot:

Here's a video guide by Jacob Amaral https://youtu.be/XKbk8SY9LD0?t=576

If you are interested, you could actually follow his guide (4 videos total) to build a bot using vanilla AWS API
The final program following his guide is available in this repo, under /src/proto/ibapi-tws/vanilla_triangle_bot_with_jacob.py
