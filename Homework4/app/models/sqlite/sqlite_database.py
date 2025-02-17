from datetime import date, datetime, timedelta
import pandas as pd
import sqlite3
import requests
from . import scraper_urls

TODAY = date.today().strftime('%Y-%m-%d')


def db_connection(db_path):
    conn = None
    try:
        conn = sqlite3.connect(db_path, isolation_level=None)
    except sqlite3.Error as e:
        print("Error while connecting to SQLite database: ", e)
    return conn


def upload_ticker_data_to_database(db_path, ticker):
    connection = db_connection(db_path)
    cursor = connection.cursor()
    table_exists = cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?", [ticker]).fetchone()[0]
    if table_exists == 1:
        update_ticker_data(db_path, ticker)
    else:
        add_ticker_data(db_path, ticker)
    connection.close()

# return ticker data with or without given dates from the database
def get_sqlite_ticker_data(db_path, ticker, from_date=None, to_date=None):
    connection = db_connection(db_path)
    cursor = connection.cursor()
    if from_date is None and to_date is None:
        cursor.execute("SELECT * FROM %s ORDER BY [Date] DESC" % ticker )
    else:
        cursor.execute("SELECT * FROM %s WHERE [Date] > ? AND [Date] < ? ORDER BY [Date] DESC" % ticker, [from_date, to_date])
    data = cursor.fetchall()
    connection.close()
    return data

# update the database for the new scraped ticker data
def update_ticker_data(db_path, ticker):
    connection = db_connection(db_path)
    cursor = connection.cursor()
    last_date = datetime.strptime(
        cursor.execute("SELECT [Date] FROM %s order by [Date] desc limit 1" % ticker).fetchone()[0],
        "%Y-%m-%d") - timedelta(days=1)
    last_date = last_date.strftime('%Y-%m-%d')
    if last_date != TODAY:
        data = requests.get(scraper_urls.SCRAPER_URL + '/' + ticker + ' ' + last_date + '' + TODAY).json()
        df = pd.DataFrame.from_dict(data, orient='index')
        for index, row in df.iterrows():
            try:
                cursor.execute("INSERT OR IGNORE INTO %s "
                               "VALUES (?,?,?,?,?,?,?,?,?)" % ticker,
                               (str(index), row['Price'], row['Max'], row['Min'], row['AvgPrice'], row['chg'],
                                row['Volume'], row['TurnoverBEST'], row['TurnoverTotal']), )
            except sqlite3.Error as e:
                print('Error while inserting new data into table: ', e)
    connection.commit()
    connection.close()

# add scraped ticker data to database
def add_ticker_data(db_path, ticker):
    connection = db_connection(db_path)
    cursor = connection.cursor()
    try:
        cursor.execute('CREATE TABLE %s ('
                        '[Date] TEXT UNIQUE PRIMARY KEY,'
                        'Price TEXT,'
                        'Max  TEXT,'
                        'Min  TEXT,'
                        'AvgPrice  TEXT,'
                        'chg  TEXT,'
                        'Volume  TEXT,'
                        'TurnoverBEST TEXT,'
                        'TurnoverTotal TEXT'
                        ')' % ticker)
    except sqlite3.OperationalError as e:
        print('Error while creating SQLite Table: ', e)

    data = requests.get(scraper_urls.SCRAPER_URL + '/' + ticker).json()
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.rename_axis('Date').reset_index()
    df.to_sql(ticker, connection, if_exists='append', index=False)
    connection.commit()
    connection.close()

