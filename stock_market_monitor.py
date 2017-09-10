import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import sqlalchemy

def GetHistoricalData(ticker, source):
    '''
    ticker (str): Stock ticker symbol.
    source (str): The database to pull the data from as outlined in pandas datareader.

    Returns a dataframe.
    '''
    # Start date is Jan 1, 1970 because Yahoo uses Unix timestamps in their requests URL.
    # Any date before that causes problems with request from Yahoo.
    start = dt.datetime(1970, 1, 1)

    # End date is yesterday.
    # Can we make this pull today's data if the stock market has closed during execution time?
    end = dt.date.today() - dt.timedelta(days=1)

    # Yahoo dataframe index: Date.
    # Yahoo dataframe columns: Open, High, Low, Close, Adj Close, and Volume.
    return web.DataReader(ticker, source, start, end)

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


output = GetHistoricalData("^GSPC", "yahoo")