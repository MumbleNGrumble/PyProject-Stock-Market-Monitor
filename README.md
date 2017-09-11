# PyProject-Stock-Market-Monitor
## *Overview*
- This is a personal project that monitors the stock market and implements automated trades based on technical analysis.
- The goal is to learn more about data science with Python, databases, machine learning, security analysis, and macroeconomics.
- I'll be starting with a simplified model, monitoring the S&P 500 index and simulating automated trades on the SPDR S&P 500 ETF (SPY) based on moving averages.
- The model will become more complex over time as other economic indicators are added and more complex features are introduced.

## *Goals*
- Learn more about databases and become more familiar with SQL.
- Familiarize myself with the pandas library in Python for data science and data manipulation.
- Write better unit tests for my code and get into the habit of constantly testing.
- Be comfortable with manipulating Excel in Python to generate reports.
- Use machine learning to forecast stock price direction and magnitude of change. Candidates for machine learning libraries include scikit-learn and TensorFlow.
- Get a better understanding of how to use git for version control.

## *Assumptions*
- There are no external costs or price factors to consider other than the price of the security itself. In other words, there are no brokerage fees, no dividends, and no tax.
- Decisions on whether to buy or sell are made at the end of the day after closing and are executed at the start of the next day at opening. There is only one buy or sell order executed per day.

## *Feature Roadmap*
- Pull stock data via Yahoo Finance.
- Set up SQL database to store data.
- Calculate 5 day, 30 day, and 1 year moving averages.
- Track a single stock portfolio and monitor profits and losses.
- Back calculate profit and list history of a trading algorithm.
- Establish a buy and hold benchmark to compare trading algorithms against.
- Output reports to Excel.
- Use machine learning algorithms for forecasting and compare to moving average trades.
- Expand the portfolio to hold more than one stock.
- Implement the ability to short stocks.
- Add other macroeconomic indicators to the model like unemployment rate, housing price index, consumer price index, producer price index, etc.
- Use more complicated technical analysis trading algorithms.

## *To Do List*
- [ ] Research licenses and add one to readme if necessary.
- [x] Write a function that grabs stock price history from Yahoo Finance. It should take a stock ticker as an argument so the function can pull the S&P 500 index as well as individual stocks.
- [x] Set up database tables based on what's returned from Yahoo Finance.
- [x] Set up database tables to track portfolios and buy/sell transactions.
- [ ] Rename "Adj Close" column from Yahoo to "AdjClose" for writing to database.
- [ ] Rread and write data to the database from Python.
- [ ] Calculate moving averages.
- [ ] Predict stock price change direction from moving averages.