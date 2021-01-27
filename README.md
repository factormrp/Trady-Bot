# Trady Bot
This mini-project showcases my web programming skills. In particular, I leveraged *[Flask](https://flask.palletsprojects.com/en/1.1.x/)* to connect my algorithmic trading bot with custom written templates. I created a minimalistic UI to allow visitors to simulate a chosen trading strategy on a selected stock security from a list of options.

## Inspiration
Surfing through YouTube, I stumbled on some clickbait video about trading bots and algorithmic trading. This led me to find [this](https://youtu.be/SEQbb8w7VTw) video, which walks through a simple implementation of a MAC indicator using data from [Yahoo! Finance](https://finance.yahoo.com). Wanting to make this a more general project, I decided to make a webpage using *Flask* that would allow users to interact with my bot. I ended up diving off the deep end and learning WAYYY more about HTTP request methods and routing than I wanted to before getting it up and running.

## How to Use
To mess around with the bot yourself, I suggest downloading the code here. **To make sure it works**, be sure to have the following dependencies in your build environment:
- matplotlib
- yfinance
- pandas
- numpy

From there simply open a command shell in your folder containing tradebot.py and use: `flask run`

### USAGE NOTE
Currently the routing is not yet robust enough to handle "un-nice" behavior. In particular, this means that you must make a selection for each option before pressing Run. Otherwise, the web app gets angry.