import requests
from Homework4.api.csv.model import data_to_csv
from Homework4.api.sqlite.model import sqlite_database
from Homework4.api import api_urls


tickers = requests.get(api_urls.tickers_url).json()
directory = './csv_database'

def update_sqlite_database():
    for ticker in tickers:
        sqlite_database.upload_ticker_data_to_database(ticker)

def update_csv_database():
    data_to_csv.check_directory_exist(directory, tickers)


update_sqlite_database()
update_csv_database()
