import sqlite3
from datetime import datetime

import pandas as pd

import Homework1.scraper
from Homework1.scraper import get_codes, main

def main_db(dir_name):
    Homework1.scraper.main(dir_name)
    codes = get_codes()
    file = 'database.db'
    connection = sqlite3.connect(file)

    for code in codes:
        path = dir_name+'/'+code+'.csv'

        df = pd.read_csv(path)
        df['DateFormated'] = df.Date.apply(parse_date)
        df.to_sql(code, connection, if_exists='replace', index=False)

    connection.close()

def parse_date(date):
    newdate = datetime.strptime(date, '%d.%m.%Y')
    return newdate.strftime('%Y-%m-%d')


if __name__ == '__main__':
    main_db('../../Homework1/database')

