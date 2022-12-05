# Why I Setup All Environment In One Folder

--- 
## Overview
If I was myself a year ago I would have hated myself with passion when I look at this repo...

This article discuss about good Git branch practices and explain my reasoning on why I stopped hating it

## Example of a good Git branch practice
This is a good git article about this topic https://www.gitkraken.com/learn/git/best-practices/git-branch-strategy

Key learning:
```
The main idea behind the Git flow branching strategy is to isolate your work into different types of branches. There are five different branch types in total:
    Main
    Develop
    Feature
    Release
    Hotfix

The two primary branches in Git flow are main and develop. There are three types of supporting branches with different intended purposes: feature, release, and hotfix.

The Benefits of Git Flow:
    1. The various types of branches make it easy and intuitive to organize your work.
    2. The systematic development process allows for efficient testing.
    3. The use of release branches allows you to easily and continuously support multiple versions of production code.

The Challenges of Git Flow:
    1. Depending on the complexity of the product, the Git flow model could overcomplicate and slow the development process and release cycle.
    2. Because of the long development cycle, Git flow is historically not able to support Continuous Delivery or Continuous Integration.
```

Back in my Shopee day we also used variant of Git flow with the same idea. (master / feature / hotfix / dev / staging)
Moreover, normally I would advise to practice this, however, due to "personal reason" I reduced to this:

- Put all dev / staging / prod in sub folder
- Only maintain main & feature branch. 
  - Simply: main -> branch out a feature branch -> test all the stuff -> merge back to main one you are done


## Why I have been adopting this all-environment in one approach
Now look at this article https://www.bbc.com/news/magazine-19214294

In short there is a trading firm that lost 440M due to some software mistake.

During the last few months I learnt that:
* Bug fix speed is king.
* Even a small mistake left for small duration can cost it dearly

This aspects is personal, but one of my worst nightmare is Git conflict.

While if we maintain the code this wouldn't happens, when this happens it is one 
of the common root cause for code inconsistency that can go worse exponentially. So utmost careful attitude is important.

However, that utmost careful mental attitude is not easy to maintain when one are in time-pressure, 
not even mentioning the fear of losing money second by second.

Perhaps I'm not that good yet, but after a day of losing more than 1k because of this,
I decided not to let this happen at all, prevention is better than cure.

While that explanation is kinda subjective, let's take an more objective comparison between this approach and Git Flow.

```
Pros:
- Can run multiple environment without changing branches
- Only feature(development) branch and main branch -> less chance for conflict, 
virtually no with frequent rebase and decent handling. (also friendly with user who are new to Git)
- Quickest hotfix deploy speed so far (after confirmed fixing just copy and paste)

Cons:
- Might run files in wrong environment (fixable with good folder arrangement and printing environment to stop when wrong)
- Might need to manually change enviroment specific variable after copy paste (actually nullifiable with proper config file, check RSI_Combine.py_)
- Duplicated code (actually bad but I'm not complaining as long as I'm not losing money)
```

In this particular context, I would largely favor the approach to put all environment in the same branches
until I get a better solution. 

You can find an actual example of me fixing a bug with my semibot (src/bot/ibapi-tws/placeAtmOption[__stg].py)
![Incident](https://raw.githubusercontent.com/vuduclong0309/LongAndShort/main/img/4_Staging_And_Prod_hotfix.png)

So in short, there is a problem with putting my PUT order (but not CALL order). 

In response, I freeze execution of PUT order in prod (right side) but still do CALL order,
while hotfixing the problem in staging at the same time (left side)

(objectively the safest possible way is to halt PROD completely, but that also mean an 
opportunity I lost (e.g that juicy CALL scalp). I believe this is more or less subjective issue.)

So ... that some up my explanation for this choice