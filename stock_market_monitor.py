import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import sqlalchemy

def CalculateSMA(df, column, periods=[5, 10, 20, 50, 200]):
    '''
    df (dataframe): Dataframe to append moving averages to.
    column (str): Column to calculate moving averages on.
    period (list): Periods to calculate moving averages for.

    Appends moving averages to dataframe.
    '''
    for period in periods:
        df["SMA(" + str(period) + ")"] = df[column].rolling(period).mean()

def GetHistoricalData(ticker, source):
    '''
    ticker (str): Stock ticker symbol.
    source (str): The source to pull the data from as outlined in pandas datareader documentation.

    Returns a dataframe with stock price data from January 1, 1970 to present.
    '''
    # Start date is Jan 1, 1970 because Yahoo uses Unix timestamps in their requests URL.
    # Any date before that causes problems with request from Yahoo.
    start = dt.datetime(1970, 1, 1)

    # End date is yesterday.
    # Can we make this pull today's data if the stock market has closed during execution time?
    end = dt.date.today() - dt.timedelta(days=1)

    # Yahoo dataframe index: Date.
    # Yahoo dataframe columns: Open, High, Low, Close, Adj Close, and Volume.
    df = web.DataReader(ticker, source, start, end)

    # Rename Adj Close to match database column label.
    df.rename(columns={"Adj Close": "AdjClose"}, inplace=True)

    return df

def GetRecentData(database, table, ticker, source):
    '''
    database (str): Name of the database to read from.
    table (str): Name of the table to read from.
    ticker (str): Stock ticker symbol.
    source (str): The database to pull the data from as outlined in pandas datareader.

    Checks the database for the last stock price record.
    If more recent data exists, pull the data from the specified source.
    Returns a dataframe if there are new records. Otherwise, returns None.
    '''
    # Get the StockID for the specified stock ticker.
    stockIDQuery = "SELECT [StockID] FROM [Stock] WHERE [StockTicker] = " + "'" + ticker + "'"
    stockID = ReadDBToDF(database, stockIDQuery)["StockID"][0]

    # Set up the SQL query to get the latest record date from the database for that stock.
    selectArg = "SELECT TOP (1) [Date]"
    fromArg = "FROM [" + table + "]"
    whereArg = "WHERE [StockID] = " + str(stockID)
    orderByArg = "ORDER BY [Date] DESC"

    dateQuery = "\n".join([selectArg, fromArg, whereArg, orderByArg])

    # Execute query.
    latestDate = ReadDBToDF(database, dateQuery, ["Date"])["Date"][0]
    latestDate = latestDate.date()  # Pandas returns a timestamp. This converts it to a date.

    # TODO: Can we make this more efficient?
    # TODO: Need to account for errors when the source returns something unexpected.
    # TODO: Should this write to the database if there is new data?
    # Returns a dataframe with new records if there is new data between the last database record date and yesterday's date.
    if latestDate < dt.date.today() - dt.timedelta(days=1):
        start = latestDate + dt.timedelta(days=1)
        end = dt.date.today() - dt.timedelta(days=1)
        df = web.DataReader(ticker, source, start, end)
        df.rename(columns={"Adj Close": "AdjClose"}, inplace=True)  # Rename Adj Close to match database column label.

        if latestDate == df.index[0].date():
            print("Database is up to date for " + ticker + ".")
            return None
        else:
            return df
    else:
        print("Database is up to date for " + ticker + ".")
        return None

def ReadDBToDF(database, sql, parse_dates=None, index_col=None):
    '''
    database (str): Name of the database to read from.
    sql (str): Name of the table to read from or the query to run.
    parse_dates (list): List of column names to parse as dates, per the pandas documentation.
    index_col (str): Name of column to set as dataframe index.

    Returns a dataframe with the table/query results.
    '''
    engine = sqlalchemy.create_engine("mssql+pyodbc://.\MSSQLSERVER2016/" + database + "?driver=SQL+Server")
    return pd.read_sql(sql, engine, parse_dates=parse_dates, index_col=index_col)

def WriteDFToDB(df, database, table):
    '''
    df (dataframe): Pandas dataframe object.
    database (str): Name of the database to write to.
    table (str): Name of the table to write to.

    Writes the dataframe to the referenced database and table.
    If the table exists, it appends records.
    If the table doesn't exist, it creates a new table.
    '''
    engine = sqlalchemy.create_engine("mssql+pyodbc://.\MSSQLSERVER2016/" + database + "?driver=SQL+Server")
    df.to_sql(table, engine, if_exists="append")


#output = GetHistoricalData("^GSPC", "yahoo")
#output["StockID"] = 1
#output.rename(columns={"Adj Close": "AdjClose"}, inplace=True)
#WriteDFToDB(output, "StockMarketMonitor", "StockDailyData")