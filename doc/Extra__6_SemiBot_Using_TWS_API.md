# Logging Trade History

--- 
## Overview
Beside using full auto bot, I'm also researching on receiving trade signal of successful trader for mimic their behavior.
This guide will demo a tools that I oftenly use: a semibot to rapid fire at the money option order for scalp play.

Hope this might help you understand the basic of TWS API and how to utilise it.

## Getting Started:
The full course access can be found here https://tradersacademy.online/trading-courses/python-tws-api
* Key facts
- IBKR TWS API can be understand as a Client, but also a Wrapper (more details in lesson 4)
- We then override some function of this Client/Wrapper to extract data and place order through it
- Backtrader also use TWS API for it IBKR trader, but I utilize TWS for faster speed
    - Semibot version that use backtrader can be found in my icebox (yes I tried)

## Code example
While I recommend you to take the full lessons (takes around 1 full day to complete), for more compact example you can access
src/proto/ibapi-tws folder:

- historicalData.py & marketData (Lesson 5)
- placeOrder.py (Lesson 6)
- optionData.py (Lesson 7)

And of course, for a full demonstration of a bot using API with Jacob Amaral:
- vanilla_triangle_bot_with_jacob.py (https://www.youtube.com/watch?v=XKbk8SY9LD0)

## To the real stuff
Now, for the actual stuff that I use in real time trading, you can navigate to 
bot/ibapi-tws/placeAtmOption[_stg].py

- This is the bot that I'm trading with at the time of writing (Dec 2022)

(Pardon me if there is some unfamiliar term regarding option / derivative security.
I will try to provide some quick tutorial on how to trade option in the future, if time permit)

In short description, I listen to some reliable trade signal with high winrate, 
then leverage it with 0-5 day to expire at the money option, which have comfortable risk & size for me.

This tool automatically find closest strike price and play corresponding option, which enable me to place correct option only seconds after receiving the signal.
 