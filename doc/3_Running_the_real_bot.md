# Running The Real Bot

--- 
## Overview
This documents summarize the standard of procedure of how I develop and run a trade bot, and step on how to run my first two bots that traded in real life

## Why only technical analysis for now?
1. I'm still quite a newbie in this, I cannot explain high level strategies in simple manner yet.
It's seriously hard to explain something like Black-Scholes model or Delta Hedging to a majority of people.
(But that's not mean I'm not trying to do it in private)

2. Technical indicator are often easier to calculate it mean faster implementation and bot responding time.

## How I'm writing my bot.
For real reference, you can navigate to src/bot/ibbacktrader/RSICallPut for my RSI bot that I run in Oct - mid Nov 2022
You can find 3 subfolder dev, staging & prod as 3 of my environment.

(Note: I'm aware of common Git practice to have main / feature / dev / staging as separate branch as practiced in my old company.
I will explain this in the subsequent guide 4_Why_I_Setup_Environment_Like_This.md) 

My standard operating procedure can be simplified into those steps:
1. Testing idea / indicator in dev folder (a.k.a editing RSI_Combine.py) in dev folder
   * Since IBKR data provide more limited range of data, I option use yfinance datafeed instead (refer to file).
   * Alternatively, I also test strategy in TradingView, but only can test stock trade, not option.
     * I also provided a pine script example in dev/tradingview_test.pine.md
2. If backtesting is good, run in paper account at least (but not limited) 3 days, record it into paper trading journal.
   * A.k.a copy RSI_Combine.py from dev to staging folder
   * Else, return to step 1
3. If paper trading return good result, start live trading
   * A.k.a copy RSI_Combine.py from staging to prod
4. When live trading turn sour, return to step 2

## About running my bot
* In my real bot example, it's a sophisticated example, but it started from a very simple idea (as in src/proto/ibbacktrader/Backtrader_3_SPY_optionPlay.py)
  * So, the key fact is to start simple, and then adapt overtime.
* Also, even if a bot may work now, it might not work later
  * I'm not using RSI bot at the moment because we might be entering a trending market, which are not good for RSI based strategy
    * Remember to monitor the bot performance, don't just let it run for a month.

As a bonus, I will share a portion of my new DMIOscCustom that I'm working at the moment. Which show how I create my custom indicator
You can also read official guide for it here: https://www.backtrader.com/docu/inddev/

That's how I built an automated trading bot after 3 months of learning.

For guide / discussion in extra topic, you may find these useful:
* Extra__4_Why_I_Setup_Environment_Like_This.md
* Extra__5_Logging_Trade_Journal.md
* Extra__6_SemiBot_For_Trading_Signal.md

