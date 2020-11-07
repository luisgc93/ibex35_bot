# Ibex35 Bot 🤖
https://twitter.com/BotIbex

A twitter bot that posts financial news articles about [Spain's stock market index](https://en.wikipedia.org/wiki/IBEX_35). You can also ask the bot for the current price of a stock by mentioning it and adding a dollar sign followed by the [stock's ticker symbol](https://en.wikipedia.org/wiki/Ticker_symbol). 

<p align="center">
    <img width="447" alt="happy_path_response" src="https://user-images.githubusercontent.com/32971373/98453334-41389d00-2158-11eb-8e61-f41b0f2d62eb.png">
</p>

## Implementation 🛠️
The bot uses [RomelTorres' python wrapper](https://github.com/RomelTorres/alpha_vantage) for the [Alpha Vantage API](https://www.alphavantage.co/documentation/). It's deployed on Heroku with Docker 🐳 and uses two separate [clock processes](https://devcenter.heroku.com/articles/clock-processes-python) for posting articles and listening to twitter mentions.
