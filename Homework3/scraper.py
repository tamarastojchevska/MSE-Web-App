import glob
from itertools import repeat

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date, timedelta, datetime
import os
import time
from multiprocessing.pool import ThreadPool

# start timer for runtime execution
start = time.time()

# constants
TODAY = date.today()
CONTENT_TYPE = 'application/x-www-form-urlencoded'
DEF_URL = 'https://www.mse.mk/en/stats/symbolhistory/ADIN'
YEARS_BACK = 10


#------------------------CODES---------------------------

def check_number_in_string(s): # for a given string it checks if it contains a number
    return any(i.isdigit() for i in s)

def get_codes():
    # get http request
    response = requests.get(DEF_URL)
    raw_html = response.text
    # parse html from request
    soup = BeautifulSoup(raw_html, "html.parser")

    codes = []
    # get all the codes from the <select> element and it's <option> elements
    raw_codes = soup.select_one('#Code').find_all('option')
    # filter the codes and add them to a list
    for code in raw_codes:
        if check_number_in_string(code.text) is not True:
            codes.append(code.text)
    return codes

def save_codes(codes):
    with open('issuers.txt', 'w') as f:
        for code in codes:
            f.write(f"{code}\n")

def get_issuers():
    with open('issuers.txt') as f:
        lines = [line.rstrip('\n') for line in f]
    return lines

#-----------------------PARSE DATA------------------------------

# for a given date subtract 364 days
def get_last_year(input_date): 
    return input_date - timedelta(days=364)

# transform a string from 1,000.00 to 1.000,00 format
def price_format(price): 
    if price == '0':
        return price
    number = price.replace(',', '.')[:-3]
    decimal = price[-2:]
    return number + ',' + decimal

# parsed data for a given code and time frame
def get_parsed_data(code, from_date, to_date):
    code_data = []
    # parse data in the right format
    from_date = from_date.strftime("%m/%d/%Y") 
    to_date = to_date.strftime("%m/%d/%Y")

    # get http request with the given parameters
    response = get_post_request(code, from_date, to_date)
    raw_html = response.text

    # parse the html from the request
    soup = BeautifulSoup(raw_html, "html.parser")
    # get the table element
    table = soup.select_one('#resultsTable')
    if table is None:
        return None
    # get all rows <tr> from the table element
    table = table.find_all('tbody')[0].find_all('tr')

    for row in table:
        # for every row get the individual <td> element
        row = row.find_all('td')
        cells = []
        # get the text of the <td> elements from the current row
        for cell in row:
            cells.append(cell.text)
        # input the data in the correct format for the current row
        data = {
            "Date": datetime.strptime(cells[0], '%m/%d/%Y').date().strftime("%d.%m.%Y"),
            "Last trade price": price_format(cells[1]),
            "Max": price_format(cells[2]),
            "Min": price_format(cells[3]),
            "Avg. Price": price_format(cells[4]),
            "%chg.": cells[5],
            "Volume": cells[6],
            "Turnover in BEST in denars": cells[7],
            "Total turnover in denars": cells[8]
        }
        code_data.append(data)
    # returns all the rows in the table for the given code and time frame
    return code_data


#------------------------POST REQUEST-------------------------

# send a http request with given parameters
def get_post_request(code, from_date, to_date):
    url = DEF_URL[:-4] + code

    header = {
      'content-type': CONTENT_TYPE
    }
    data = {
      "FromDate": from_date,
      "ToDate": to_date
    }

    response = requests.post(url, headers=header, data=data)
    return response
    

#-----------------------DIRECTORY--------------------------

# check if the database is empty or not
def check_directory_empty(directory, codes, ext):
    if not os.listdir(directory):
       # directory is empty -> create csv for every code
       for code in codes:
           filename = code + ext
           path = os.path.join(directory, filename)
           with open(path, "w") as File:
               pass
    else:
        # directory is not empty -> check if code is missing and create csv
        files = glob.glob(directory + "/*"+ext)
        for code in codes:
            filename = code + ext
            path = os.path.join(directory, filename)
            if path not in files:
                path = os.path.join(directory, code+ext)
                with open(path, "w") as File:
                    pass

def check_directory_exist(directory, codes, ext):
    if os.path.isdir(directory):
        # given directory exists -> check if it's empty
        check_directory_empty(directory, codes, ext)
    else:
        # given directory doesn't exist -> create directory and check if it's empty
        os.mkdir(directory)
        check_directory_empty(directory, codes, ext)

#---------------------------------DATA------------------------------
def get_data_for_code(dir_name, code):
    filename = code + '.csv'
    # check if the file for the given code is empty
    if os.stat(os.path.join(dir_name, filename)).st_size==0: # True if empty
        # get data for the past 10 years
        i = 0
        to_date = TODAY
        while i<YEARS_BACK:
            # get from date with a difference of 364 days from the current date
            from_date = get_last_year(to_date)
            data = get_parsed_data(code, from_date, to_date)

            # append data to csv
            filename = code + '.csv'
            df = pd.DataFrame(data)

            if i==0:
                # put a header in the csv
                df.to_csv(os.path.join(dir_name, filename), mode='a', index=False)
            else:
                # just append the data
                df.to_csv(os.path.join(dir_name, filename), mode='a', header=False, index=False)

            # get the next set of dates
            to_date = from_date - timedelta(days=1)
            i += 1
    else: # if csv is not empty -> get last recorded date and append the data from the last recorded date until today
        df = pd.read_csv(os.path.join(dir_name, filename))
        # last recorded date from csv file
        from_date_file = datetime.strptime(df.iloc[0].tolist()[0], '%d.%m.%Y').date()

        # no new data to fetch
        if from_date_file != TODAY:
            # start from the next day in order not to have duplicates
            from_date_file = from_date_file + timedelta(days=1)
            days_between = from_date_file - TODAY
            to_date = TODAY
            days = abs(days_between.days)
            if days_between == 0:
                return
            while True:
                # fetch data on a "yearly" bases (difference between the dates is more than 364 days)
                if days > 364:
                    from_date = get_last_year(to_date)
                    data = get_parsed_data(code, from_date, to_date)

                    # append data to csv
                    filename = code + '.csv'
                    df = pd.DataFrame(data)
                    # df = df.sort_values(by='Date', ascending=True)
                    df.to_csv(os.path.join(dir_name, filename), mode='a', header=False, index=False)

                    to_date = from_date - timedelta(days=1)
                    days -= 364
                else: # if the difference is less than a "year" (364 days) no need to itterate, just fetch the data for the given dates
                    data = get_parsed_data(code, from_date_file, to_date)

                    # append data to csv
                    filename = code + '.csv'
                    # missing data (the one fetched earlier)
                    df1 = pd.DataFrame(data)
                    # current data in file
                    df2 = pd.read_csv(os.path.join(dir_name, filename))
                    # join missing and current data in right order
                    frames = [df1, df2]
                    final_df = pd.concat(frames, ignore_index=True)
                    # replace with new data
                    final_df.to_csv(os.path.join(dir_name, filename), index=False)
                    break

#--------------------------------MAIN-------------------------------------

def main(dir_name):
    codes = get_codes()
    ext = '.csv'
    save_codes(codes)

    # check if directory exists
    check_directory_exist(dir_name, codes, ext)

    # get data for every code with multithreading
    with ThreadPool() as pool:
        pool.starmap(get_data_for_code, zip(repeat(dir_name), codes))


if __name__ == '__main__':
    main('database')

