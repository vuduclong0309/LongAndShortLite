# LongAndShort(Lite)

--- 
## Overview
This repo were the coding aspect of my first few months auto-trading bot project LongNShort, 
repurposed into a starter kit into algotrading for engineering colleagues with similar interest,
by adding suggestion on extra reading and brief guide on each steps. 

My aim for this repo is to be a (not-so)short step-by-step guide to get the absolute basic technical trading concept, and to build
a medium frequency automated option trading bot (5 second timeframe+) from scratch with Backtrader 
and InteractiveBroker. I trust this is much better than reading full API documentation and trading books
(I also included my first trading bot in this repo :D).

While technically everyone can use this bot (you can literally run a command line to fire the bot), 
I believe:
* The skill to read API documentation will help much along the way
* You should create or modify my bot before you do real time trading.

You can head towards doc folder and read 0_Before_You_Begin.md to begin the journey. 

The rest of documenation provides:
* A glimpse of my full LongNShort project
* A high-level overview of this repo structure
* Credits to predecessor that enabled me to walk on this project.

## Higher Overview (LongNShortFull)
Even though my main job since I have graduated from NTU Singapore in 2019 was a data engineer, 
I always have a special interest in finance and trading, which influenced my decision a parttime master 
course in financial engineering in Oct 2020.

Nonetheless, there was always a rift between theoretical and practical. 
Having dissatisfied with my investment result over the last 3 years,
In July 2022, I made a brave jump out of my comfort zone to fully focus on my wet dream,
which were to become a trader for living, an experiment and a huge gamble to see if
I really have a knack for it.

Having learnt from two different group of people who have different characteristic:
- In Shopee, most of engineering colleague have superb coding standard, but usually have limited financial knowledge beyond investing.
- In WorldQuant University, most of my teammate so far come from analytical background with profound knowledge in trading and hedging experience, 
but face obstacle when it come to coding.

LongNShort is my attempt at combining these experience to create a trading project that can utilize both advanced trading concept
and decent code standard, while making it as user-friendly to an engineer as much as a analytical trader.

At the moment, my full LongNShort consists of (but not limited to) these components
- Atlassian JIRA ticket tracker system, which adopt a much simplified version of AGILE SDLC
  - I stripped the idea down to the core, which only consist of:
    - A Kanban Board
    - Epic, Task and Bug ticket type
    - Sprint shortened to a week as opposed to 2 week
- Atlassian Confluence trader knowledge archive, where I store
  - Day by day live trading journal
  - Bugfix record and experience
  - AGILE SPIKE research documentation
Both of these two components I wish to maintain as my private property at the moment, 
but I would happy to demo it should it is appropriate at the later time, but I can recommend Atlassian
should you ever need to track your progress

- The coding repo, which include the coding aspects of the project (which should be closely similar to this)
  - I mostly use Python to run this project, with only some minor bash script to run it in Azure server
    - The two major framework I use would be IBKR TWS API and Backtrader
  - I will include any critical documentation describing the project in Confluence into the doc folder of this public repo :)
    
## This Repo Folder Structure

```
├───doc                     ## General guide & how to navigate through src folder
├───src  
│   ├───bot                 ## Bot / Tools that I at least ran on paper trading account
│   │   ├───ibapi-tws
│   │   └───ibbacktrader
│   │       ├───1-RSICallPut
│   │       └───2-DMIOscCustom
│   └───proto               ## Prototype / Useful example that I found during creating trading bot
│       ├───backtrader-research-spike
│       ├───ibapi-tws
│       ├───ibbacktrader
│       └───jupytersandbox
```

## Credit
During my learning my project, I was forturnated to meet these amazing predecessor on craving a path for me to follow:
- [Jacob Amaral](https://www.youtube.com/@jacobamaral), for his introduction to IBKR bot trading series
- [TradersAcademy](https://tradersacademy.online/) by InteractiveBroker
- [mementum](https://github.com/mementum), for creating a commercial grade strategy backtest framework and released it for free 
  - Unfortunately it's not supported anymore. However, I am still maintaining a fork with IBKR focused bugfix until I find another alternative
- [u/DaddyDersch](https://www.reddit.com/user/DaddyDersch/), for his series of helpful post regarding general trading advice. You may click the link to refer to his public profile 
