import requests
from Homework4.SQLiteService.model.sqlite_database import SqliteDatabase


tickers_url = 'http://127.0.0.1:5000/tickers'

def update_database():
    tickers = requests.get(tickers_url).json()

    for ticker in tickers:
        print(ticker)
        SqliteDatabase.upload_ticker_data_to_database(ticker)

