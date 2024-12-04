import sqlite3
import pandas as pd

import Homework1.scraper
from Homework1.scraper import get_codes, main

def main_db(dir_name):
    Homework1.scraper.main(dir_name)
    codes = get_codes()
    file = 'database.db'

    for code in codes:
        path = dir_name+'/'+code+'.csv'

        df = pd.read_csv(path)

        df.columns = df.columns.str.strip()

        connection = sqlite3.connect(file)

        df.to_sql(code, connection, if_exists='replace')

        connection.close()

if __name__ == '__main__':
    main_db('../../Homework1/database')

