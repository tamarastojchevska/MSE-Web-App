import requests
from Homework4.api.csv.model import data_to_csv
from Homework4.api.sqlite.model import sqlite_database


tickers_url = 'http://127.0.0.1:5000/tickers'
tickers = requests.get(tickers_url).json()

def update_sqlite_database():
    for ticker in tickers:
        sqlite_database.upload_ticker_data_to_database(ticker)

def update_csv_database(directory):
    data_to_csv.check_directory_exist(directory, tickers)
