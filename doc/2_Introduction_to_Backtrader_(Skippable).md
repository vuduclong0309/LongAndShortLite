# Introduction to Backtrader (Skippable)

--- 
## Overview
This documents summarize the critical point of Backtrader framework, and run through a few examples for you to understand


## Backtrader Document Skimming Guide
First, go here for a warm welcome from original author: https://www.backtrader.com/

Then, go here for an introduction: https://www.backtrader.com/docu/. 

I made a corresponding printClose program, available at src/bot/proto/ibbacktrader/Backtrader_1_SPY_printClose.py

Optionally, read the Quickstart Guide: https://www.backtrader.com/docu/quickstart/quickstart/ (but the example is not using IB data feed)

Next, read the concept guide https://www.backtrader.com/docu/concepts/

## After you (somewhat) know the concept
Here's what I can summarize:
* Basically the main concept is Cerebro bot object. Think it's like a motherboard or a skeleton.
* You plug and play gadget (Like TestSizer, Strategy, DataFeed) into the Cerebro then run it
* In Cerebro object, two main function we should focus now is:
  * start(): in this function we set up the techical indicators (refer to 0.5_why_techinal_bot_for_now.md)
  * next(): the function is called when there is new data send to the Cerebro. We will decide to buy or sell in this function
  
After this, you can go to src/bot/proto/ibbacktrader/Backtrader_2_APPL_sell_T_plus_3.py and maybe run it.

This bot is the most simple full function bot that buy and sell.

Finally, src/bot/proto/ibbacktrader/Backtrader_3_SPY_optionPlay.py and maybe run it. This bot starts to get close to my running bot by trading derivatives

For the one who like to learn more simple examples regarding indicator, please proceed to proto/backtrader-research-spike folder


