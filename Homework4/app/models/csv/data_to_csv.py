import glob
import os
from Homework4.app.models.sqlite.sqlite_database import *



def data_to_csv(directory, db_path, ticker):
    filename = ticker + '.csv'
    path = directory + '/' + filename
    data = get_sqlite_ticker_data(db_path, ticker)
    df = pd.DataFrame(data, columns=['Date', 'Price', 'Max', 'Min', 'AvgPrice', 'chg', 'Volume', 'TurnoverBEST', 'TurnoverTotal'])
    df.to_csv(path, index=False)


def check_directory_exist(directory, db_path, tickers):
    if os.path.isdir(directory):
        # given directory exists -> check if it's empty
        check_directory_empty(directory, db_path, tickers)
    else:
        # given directory doesn't exist -> create directory and check if it's empty
        os.mkdir(directory)
        check_directory_empty(directory, db_path, tickers)


def check_directory_empty(directory, db_path, tickers):
    if not os.listdir(directory):
        # directory is empty -> create csv for every code
        for ticker in tickers:
            data_to_csv(directory, db_path, ticker)
    else:
        # directory is not empty -> check if code is missing and fill csv with data
        files = glob.glob(directory + "/*" + '.csv')
        for ticker in tickers:
            filename = ticker + '.csv'
            path = os.path.join(directory, filename)
            if path not in files:
                data_to_csv(directory, db_path, ticker)
            else:
                os.remove(path)
                data_to_csv(directory, db_path, ticker)

