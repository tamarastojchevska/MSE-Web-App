import glob
import os

import pandas as pd
import requests

sqlite_data_url = 'http://127.0.0.1:5000/tickers/sqlite/'

class CSVdata:
    @staticmethod
    def data_to_csv(directory, ticker):
        filename = ticker + '.csv'
        path = directory + '/' + filename
        data = requests.get(sqlite_data_url + ticker).json()
        df = pd.DataFrame(data, columns=['Date', 'Price', 'Min', 'Max', 'AvgPrice', 'chg', 'Volume', 'TurnoverBEST', 'TurnoverTotal'])
        df.to_csv(path, index=False)

    @staticmethod
    def check_directory_exist(directory, tickers):
        if os.path.isdir(directory):
            # given directory exists -> check if it's empty
            CSVdata.check_directory_empty(directory, tickers)
        else:
            # given directory doesn't exist -> create directory and check if it's empty
            os.mkdir(directory)
            CSVdata.check_directory_empty(directory, tickers)

    @staticmethod
    def check_directory_empty(directory, tickers):
        if not os.listdir(directory):
            # directory is empty -> create csv for every code
            for ticker in tickers:
                CSVdata.data_to_csv(directory, ticker)
        else:
            # directory is not empty -> check if code is missing and fill csv with data
            files = glob.glob(directory + "/*" + '.csv')
            for ticker in tickers:
                filename = ticker + '.csv'
                path = os.path.join(directory, filename)
                if path not in files:
                    CSVdata.data_to_csv(directory, ticker)

