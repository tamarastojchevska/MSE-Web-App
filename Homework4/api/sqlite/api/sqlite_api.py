import sqlite3
from Homework4.api.sqlite import sqlite_bp
from Homework4.api.sqlite.model import sqlite_database


@sqlite_bp.route('/tickers/sqlite/<string:ticker>', methods=['GET'])
def get_sqlite_ticker_data(ticker):
    try:
        return sqlite_database.get_ticker_data(ticker)
    except sqlite3.Error as e:
        print('Error while getting ticker data from database: ', e)


@sqlite_bp.route('/tickers/sqlite/<string:ticker> <string:from_date> <string:to_date>', methods=['GET']) # date format YYYY-MM-DD
def get_sqlite_ticker_data_dates(ticker, from_date, to_date):
    try:
        return sqlite_database.get_ticker_data(ticker, from_date, to_date)
    except sqlite3.Error as e:
        print('Error while getting ticker data from database with date parameters: ', e)

@sqlite_bp.route('/tickers/sqlite/upload/<string:ticker>', methods=['POST'])
def upload_sqlite_ticker_data(ticker):
    try:
        sqlite_database.upload_ticker_data_to_database(ticker)
    except sqlite3.Error as e:
        print('Error while uploading ticker data to database: ', e)

