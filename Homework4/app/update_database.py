import requests
from Homework4.app.service.csv.model import data_to_csv
from Homework4.app.service.sqlite.model import sqlite_database
from Homework4.app.service import api_urls
import schedule
import time


tickers = requests.get(api_urls.tickers_url).json()
directory = './csv_database'

def update_sqlite_database():
    for ticker in tickers:
        sqlite_database.upload_ticker_data_to_database(ticker)

def update_csv_database():
    data_to_csv.check_directory_exist(directory, tickers)

schedule.every().day.at("00:00").do(update_sqlite_database).do(update_csv_database)

while True:
    schedule.run_pending()
    time.sleep(1)
