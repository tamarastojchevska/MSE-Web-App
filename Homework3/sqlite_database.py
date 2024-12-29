import csv
import sqlite3
from datetime import datetime
import pandas as pd
import Homework3.scraper as scraper


def main_db(dir_name):
    scraper.main(dir_name)
    issuers = scraper.get_issuers()
    file = 'database.db'
    connection = sqlite3.connect(file)

    for code in issuers:
        path = dir_name+'/'+code+'.csv'
        is_empty = False
        with open(path, 'r') as csvfile:
            csv_dict = [row for row in csv.DictReader(csvfile)]
            if len(csv_dict) == 0:
                print('csv file is empty')
                is_empty = True
        if is_empty is False:
            df = pd.read_csv(path)
            df['DateFormated'] = df.Date.apply(parse_date)
            df.to_sql(code, connection, if_exists='replace', index=False)

    connection.close()

def parse_date(date):
    newdate = datetime.strptime(date, '%d.%m.%Y')
    return newdate.strftime('%Y-%m-%d')


if __name__ == '__main__':
    main_db('database')

