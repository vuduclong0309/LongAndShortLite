# LongAndShort(Lite)

--- 
## Overview
This repo were the coding aspect of my first few months into the auto-trading bot project LongNShort, 
repurposed into an introduction to technical algotrading, targeted engineering colleagues with similar interest.

In other word, I want to serve this as a (not-so)short step-by-step guide build
a medium frequency automated option trading bot (5 second timeframe+) from scratch with Backtrader 
and InteractiveBroker. A partial archive of what I have found and learn from August 2022 until Dec 2022
(I also included my first trading bot in this repo :D).

If you want a quick start, you can head towards doc folder and read 0_Before_You_Begin.md to begin the journey. 

The rest of documenation provides:
* A glimpse of my full LongNShort project
* A high-level overview of this repo structure
* Credits to predecessor that enabled me to walk on this project.

## LongNShortFull

### Why I did this?
Beside an obvious interest in computer science and data analytics, I have always had a keen interest in trading.
I grew up selling (secretly) Yu-gi-oh magic card in my middle schoole and then Dota 2 ingame item in my university.
Even though I have graduated in NTU as a computer science student in 2019, with the emergence of algotrading, I happily took 
a parttime master in Financial Engineering in Oct 2020.

While I'm still grateful for an opportunity to work as a data engineer in Shopee, in middle of 2022,
feeling the time is right, I took a brave crazy leap. My last day in Shopee was also the day I commemorate
working for 3 full years (and 1 day :>), the only job I have after graduation.

One of my main motivation is that I was unhappy with my self-investment result in 2020-2021. Thus, 
I want to commit full-time into trading without even knowing if I can make it or not, only with a little 
fortune I have saved over last 3 years.

It's still funny to this day that I did the stuff in the most crazy market period. This is like jumping off a cliff.
However, I know that I wouldn't do such reckless move if I'm in my 30s. I want to take a chance while I still can
afford to do it while I'm still 25, young and dumb, but wise enough to know about damage control.

On the bright side, may the grow explode exponentially in the hardest time. I know that if 
I'm stalling for perfect day then I would never do it. 

So now I'm writing this guide (actually I consider this guide as a method of self-emotion control)
to have a recap of the path that I have walked, and maybe to help anyone who will need a guide later.

### How I'm doing this?
When I look from different perspectives: as a data engineer and as a financial engineering student, I see different
problems to each group of people:
- In Shopee, most of my colleague have strong technical background, but usually have limited financial knowledge beyond investing.
- In WorldQuant University, my teammate often have profound knowledge in trading and hedging experience, 
but face obstacle when it come to coding.

LongNShort is my attempt at combining these experience to create a trading project that can utilize both advanced trading concept
and decent code standard, while making it as user-friendly to an engineer as much as a analytical trader.

At the moment, my full LongNShort consists of (but not limited to) these components
- Atlassian JIRA ticket tracker system, which adopt a much simplified version of AGILE SDLC
  - I stripped the idea down to the core, which only consist of:
    - A Kanban Board
    - Epic, Task and Bug ticket type
![JiraPreview](https://github.com/vuduclong0309/LongAndShortLite/blob/main/img/RM_2_JIRA_preview.png?raw=true)

- Atlassian Confluence trader knowledge archive, where I store
  - Day by day live trading journal
  - Bugfix record and experience
  - SPIKE Research documentation
![JiraPreview](https://raw.githubusercontent.com/vuduclong0309/LongAndShortLite/main/img/RM_1_Confluence_Review.png)

Both of these two components I wish to maintain as my private property at the moment, 
but I would happy to demo it should it is appropriate at the later time. I only mention this as a suggestion
if you need a team managed software. I worked with this in Shopee for 3 years so I'm comfortable with that.

- The coding repo, which include the coding aspects of the project
  - I mostly use Python to run this project, with only some minor bash script to run it in Azure server
    - The two major framework I use would be IBKR TWS API and Backtrader
  - I will try include any critical documentation from the other repo into this Lite version as much as possible
    
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

