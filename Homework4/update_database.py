import requests
from Homework4.api.csv.model.data_to_csv import CSVdata
from Homework4.api.sqlite.model.sqlite_database import SqliteDatabase


tickers_url = 'http://127.0.0.1:5000/tickers'
tickers = requests.get(tickers_url).json()

def update_sqlite_database():
    for ticker in tickers:
        SqliteDatabase.upload_ticker_data_to_database(ticker)

def update_csv_database(directory):
    CSVdata.check_directory_exist(directory, tickers)
