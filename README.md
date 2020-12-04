# Ibex35 Bot 🤖 
[![Build Status](https://travis-ci.org/luisgc93/ibex35_bot.svg?branch=master)](https://travis-ci.org/luisgc93/ibex35_bot) [![codecov](https://codecov.io/gh/luisgc93/ibex35_bot/branch/master/graph/badge.svg?token=QM9L6HQ3YQ)](https://codecov.io/gh/luisgc93/ibex35_bot)

A [twitter bot](https://twitter.com/BotIbex) that posts financial news articles about [Spain's stock market index](https://en.wikipedia.org/wiki/IBEX_35). You can also ask the bot for the current price of a stock by mentioning it and adding a dollar sign followed by the stock's ticker symbol. 

<img width="447" alt="happy_path_response" src="https://user-images.githubusercontent.com/32971373/98453334-41389d00-2158-11eb-8e61-f41b0f2d62eb.png">

## Implementation 🛠️
The bot uses [RomelTorres' python wrapper](https://github.com/RomelTorres/alpha_vantage) for the [Alpha Vantage API](https://www.alphavantage.co/documentation/). It's deployed on [Heroku with Docker](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml) 🐳 and uses two separate [clock processes](https://devcenter.heroku.com/articles/clock-processes-python) for posting articles and listening to twitter mentions. To avoid duplicate replies, the bot saves the mention's id into a postgres database table which is queried through [peewee](http://docs.peewee-orm.com/en/latest/)'s ORM.

## Usage
Register an account on [Twitter's Developer Platform](https://developer.twitter.com/en) and store your credentials in `docker/envfiles/local.env`.
To run the bot locally, start the project containers with `make env-start` and then try out the bot's features with:

`make tweet-article`

`make reply-mentions`
 
To run all the tests use:
 
`make test`
