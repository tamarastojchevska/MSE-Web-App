from csv_data.data_to_csv import *
from sqlite.sqlite_database import *
from sqlite.scraper_urls import TICKER_URL
import schedule
import time


tickers = requests.get(TICKER_URL).json()
directory = '../../csv_database'
db_path = '../database.db'

def update_sqlite_database():
    for ticker in tickers:
        upload_ticker_data_to_database(db_path, ticker)

def update_csv_database():
    check_directory_exist(directory, db_path, tickers)

schedule.every().day.at("00:00").do(update_sqlite_database).do(update_csv_database)

while True:
    schedule.run_pending()
    time.sleep(1)
