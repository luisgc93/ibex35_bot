# Ibex35 Bot 🤖
https://twitter.com/BotIbex

A twitter bot that posts financial news articles about [Spain's stock market index](https://en.wikipedia.org/wiki/IBEX_35). You can also ask the bot for the current price of a stock by mentioning it and adding a dollar sign followed by the [stock's ticker symbol](https://en.wikipedia.org/wiki/Ticker_symbol). 

![Alt text](/happy_path_response.png)

## Implementation 🛠️
The bot uses [RomelTorres' python wrapper](https://github.com/RomelTorres/alpha_vantage) for [Alpha Vantage's API](https://www.alphavantage.co/documentation/). It's deployed on Heroku with Docker 🐳 and uses two separate [clock processes](https://devcenter.heroku.com/articles/clock-processes-python) for posting articles and listening to twitter mentions.
