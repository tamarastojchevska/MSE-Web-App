import glob
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date, timedelta, datetime
import os
import time

start = time.time()

TODAY = date.today()
CONTENT_TYPE = 'application/x-www-form-urlencoded'
DEF_URL = 'https://www.mse.mk/en/stats/symbolhistory/ADIN'
YEARS_BACK = 10


#-----------------------PARSE DATA------------------------------

def get_last_year(input_date):
    return input_date - timedelta(days=364)

def price_format(price): # from 1,000.00 to 1.000,00
    if price == '0':
        return price

    number = price.replace(',', '.')[:-3]
    decimal = price[-2:]
    return number + ',' + decimal

# parsed data for a given time frame
def get_parsed_data(code, from_date, to_date):
    code_data = []
    from_date = from_date.strftime("%m/%d/%Y")
    to_date = to_date.strftime("%m/%d/%Y")

    response = get_post_request(code, from_date, to_date)
    raw_html = response.text

    soup = BeautifulSoup(raw_html, "html.parser")
    table = soup.select_one('#resultsTable')
    if table is None:
        return None
    table = table.find_all('tbody')[0].find_all('tr')

    for row in table:
        row = row.find_all('td')
        cells = []
        for cell in row:
            cells.append(cell.text)
        data = {
            "Date": datetime.strptime(cells[0], '%m/%d/%Y').date(),
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

    return code_data


#------------------------POST REQUEST-------------------------

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


#------------------------CODES---------------------------

def check_number_in_string(s):
    return any(i.isdigit() for i in s)

def get_codes():
    response = requests.get(DEF_URL)
    raw_html = response.text
    soup = BeautifulSoup(raw_html, "html.parser")

    codes = []
    raw_codes = soup.select_one('#Code').find_all('option')
    for code in raw_codes:
        if check_number_in_string(code.text) is not True:
            codes.append(code.text)
    return codes


#-----------------------DIRECTORY--------------------------

def check_directory_empty(directory, codes):
    if not os.listdir(directory):
       # Directory is empty -> create csv for every code
       for code in codes:
           filename = code + '.csv'
           path = os.path.join(directory, filename)

           with open(path, "w") as csvFile:
               pass
    else:
        # Directory is not empty -> check if code is missing and create csv
        files = glob.glob(directory + "/*.csv")
        for code in codes:
            filename = code + '.csv'
            path = os.path.join(directory, filename)
            if path not in files:
                path = os.path.join(directory, code+'.csv')
                with open(path, "w") as csvFile:
                    pass


#--------------------------------MAIN-------------------------------------
codes = get_codes()
print("Number of codes:", len(codes))

dir_name = 'database'
if os.path.isdir(dir_name):
    # Given directory exists
    check_directory_empty(dir_name, codes)
else:
    # Given directory doesn't exist -> create dir
    os.mkdir(dir_name)
    check_directory_empty(dir_name, codes)

# get data for every code
for code in codes:
    filename = code + '.csv'
    if os.stat(os.path.join(dir_name, filename)).st_size==0: # True if empty
        # data for the past 10 years
        i = 0
        to_date = TODAY
        while i<YEARS_BACK:
            from_date = get_last_year(to_date)
            data = get_parsed_data(code, from_date, to_date)

            # append data to csv
            filename = code + '.csv'
            df = pd.DataFrame(data)

            if i==0:
                df.to_csv(os.path.join(dir_name, filename), mode='a', index=False)
            else:
                df.to_csv(os.path.join(dir_name, filename), mode='a', header=False, index=False)

            to_date = from_date - timedelta(days=1)
            i += 1
    else: # if csv is not empty get last date + add data from last date until today
        df = pd.read_csv(os.path.join(dir_name, filename))
        from_date_file = datetime.strptime(df.iloc[0].tolist()[0], '%Y-%m-%d').date() # last date from csv file

        if from_date_file == TODAY:
            break

        from_date_file = from_date_file + timedelta(days=1)
        days_between = from_date_file - TODAY
        to_date = TODAY
        days = abs(days_between.days)
        while True:
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
            else:
                data = get_parsed_data(code, from_date_file, to_date)

                # append data to csv
                filename = code + '.csv'
                df = pd.DataFrame(data)
                df.to_csv(os.path.join(dir_name, filename), mode='a', header=False, index=False)

                # sort data
                df2 = pd.read_csv(os.path.join(dir_name, filename))
                df2.drop_duplicates()
                df2.sort_values(by=['Date'], ascending=False, inplace=True)
                df2.to_csv(os.path.join(dir_name, filename), index=False)
                break

end = time.time()
length = end - start

print("Runtime in seconds:", length)
print("Runtime in minutes:", length/60)

