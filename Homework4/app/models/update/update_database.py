from Homework4.app.models.csv import data_to_csv
from Homework4.scraper_app.model.tickers import scrape_tickers
from Homework4.app.models.sqlite import sqlite_database
import schedule
import time

tickers = scrape_tickers()
directory = '../../csv_database'
db_path = '../../database.db'

def update_sqlite_database():
    for ticker in tickers:
        sqlite_database.upload_ticker_data_to_database(db_path, ticker)

def update_csv_database():
    data_to_csv.check_directory_exist(directory, db_path, tickers)

update_sqlite_database()
update_csv_database()
