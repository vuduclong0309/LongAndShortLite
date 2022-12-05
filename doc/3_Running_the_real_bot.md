# Running The Real Bot

---
## Overview
This documents summarize the standard of procedure of how I develop and run a trade bot, and step on how to run my first two bots that traded in real life

## What is technical trading?
Well ... this is a very big question to ask...

I don't think at my experience level I can't teach much ... I'm kinda in the survival mode at the moment.

But this might be a good starting point for you to explore
https://www.investopedia.com/terms/t/technicalanalysis.asp

## Why only technical analysis for now?
1. I'm still quite a newbie in this, I cannot explain high level strategies in simple manner yet.
It's seriously hard to explain something like Black-Scholes model or Delta Hedging to a majority of people.
(But that's not mean I'm not trying to do it in private)

2. Technical indicator are often easier to calculate it mean faster implementation and bot responding time.

## Let's run the real stuff!
For real reference, you can navigate to src/bot/ibbacktrader/RSICallPut for my RSI bot that I run in Oct - mid Nov 2022

You can find 3 subfolder dev, staging & prod as 3 of my environment.

Just run this baby [RSICombine.py](https://github.com/vuduclong0309/LongAndShortLite/blob/main/src/bot/ibbacktrader/1-RSICallPut/staging/RSI_Combine.py) and yep you ran your (probably) first trading bot!

![RunBaby](https://raw.githubusercontent.com/vuduclong0309/LongAndShortLite/main/img/3_Bot_First_Day.jpg)

I also provide a bash script like ```run_staging.sh``` if you just want to click ... well nvm :D

Note: please don't run in prod folder until you know what it is

Note2 : I'm aware of common Git practice to have main / feature / dev / staging / etc... as separate branch as practiced in my old company.
I will explain this in the subsequent guide [4_Why_I_Setup_Environment_Like_This.md](https://github.com/vuduclong0309/LongAndShortLite/blob/main/doc/Extra__4_Why_I_Included_All_Environment_In_A_Folder.md)

### How I'm writing my bot
My standard operating procedure can be simplified into those steps:
1. Testing idea / indicator in dev folder (a.k.a editing RSI_Combine.py) in dev folder
   * Since IBKR data provide more limited range of data, I option use yfinance datafeed instead (refer to file).
   * Alternatively, I also test strategy in TradingView, but only can test stock trade, not option.
     * I also provided a pine script example here to test my RSI
     ```
		//@version=5
		strategy("RSI Strategy", overlay=true)
		length = input( 14 )
		overSold = input( 30 )
		overBought = input( 70 )
		price = close
		vrsi = ta.rsi(price, length)
		co = ta.crossover(vrsi, overSold)
		cu = ta.crossunder(vrsi, overBought)
		if (not na(vrsi))
			if (co)
				strategy.entry("RsiLE", strategy.long, comment="RsiLE")
			if (cu)
				strategy.entry("RsiSE", strategy.short, comment="RsiSE")
		//plot(strategy.equity, title="equity", color=color.red, linewidth=2, style=plot.style_areabr)
		```
	* TradingView also have a tutorial here https://www.tradingview.com/pine-script-docs/en/v4/Quickstart_guide.html
    * This is an example test, but it's VERY DECEIVING. RSI tends to have high winrate only in certain period, please care for the abysmal drawdown in the image.

![Oops](https://raw.githubusercontent.com/vuduclong0309/LongAndShortLite/main/img/3_TradingView.png)

2. If backtesting is good, run in paper account at least (but not limited) 3 days, record it into paper trading journal.
   * In other words, copy RSI_Combine.py from dev to staging folder
   * If the bot aged like milk, return to step 1
3. If paper trading return good result, start live trading
   * In other words, copy RSI_Combine.py from staging to prod
4. When live trading turn sour, return to step 2

### Last disclaimer
* My first bot is already somewhat a sophisticated example, but it started from a very simple idea (as in [src/proto/ibbacktrader/Backtrader_3_SPY_optionPlay.py](https://github.com/vuduclong0309/LongAndShortLite/blob/main/src/proto/ibbacktrader/Backtrader_3_SPY_optionPlay.py))
  * So, the key fact is to start simple, and then adapt overtime.
* Also, even if a bot may work now, it might not work later
  * I'm not using RSI bot at the moment because we might be entering a trending market, which are not good for RSI based strategy
    * Remember to monitor the bot performance, don't just let it run for a month.

As a bonus, I will share a portion of my new DMIOscCustom that I'm working at the moment. Which show how I create my custom indicator

You can also read official guide for creating custom indicator here: https://www.backtrader.com/docu/inddev/

That's how I built an automated trading bot after 3 months of learning.

For guide / discussion in extra topic, you may find these useful:
* [Extra__4_Why_I_Setup_Environment_Like_This.md](https://github.com/vuduclong0309/LongAndShortLite/blob/main/doc/Extra__4_Why_I_Included_All_Environment_In_A_Folder.md)
* [Extra__5_Logging_Trade_Journal.md](https://github.com/vuduclong0309/LongAndShortLite/blob/main/doc/Extra__5_Logging_Trade_History.md)
* [Extra__6_SemiBot_For_Trading_Signal.md](https://github.com/vuduclong0309/LongAndShortLite/blob/main/doc/Extra__6_SemiBot_Using_TWS_API.md)
