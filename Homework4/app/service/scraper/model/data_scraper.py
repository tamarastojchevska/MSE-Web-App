import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
from datetime import datetime
from Homework4.app.service import api_urls

CONTENT_TYPE = 'application/x-www-form-urlencoded'
TODAY = date.today()
TO_DATE = TODAY.strftime("%Y-%m-%d")
FROM_DATE = (TODAY - timedelta(days=3650)).strftime("%Y-%m-%d")


# convert a string from 1,000.00 to float number
def convert_price_float(price):
    if price == '0':
        return float(price)
    number = price.replace(',', '')
    if number == '':
        return 0
    return float(number)

# send a http request with given parameters
def get_post_request(code, from_date, to_date):
    url = api_urls.DEF_URL[:-4] + code
    header = {
        'content-type': CONTENT_TYPE
    }
    data = {
        "FromDate": from_date,
        "ToDate": to_date
    }
    response = requests.post(url, headers=header, data=data)
    return response

def last_year_date(date, years=1):
    return date - timedelta(days=364*years)


# scrape ticker data and format it for further use
def scrape_data(ticker, from_date, to_date):
    data = {}
    # get http request with the given parameters
    response = get_post_request(ticker, from_date, to_date)
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
        data[datetime.strptime(cells[0], '%m/%d/%Y').date().strftime("%Y-%m-%d")] = {
            "Price": convert_price_float(cells[1]),
            "Max": convert_price_float(cells[2]),
            "Min": convert_price_float(cells[3]),
            "AvgPrice": convert_price_float(cells[4]),
            "chg": cells[5],
            "Volume": cells[6],
            "TurnoverBEST": cells[7],
            "TurnoverTotal": cells[8]
        }
    return data


# update ticker data with new scraped data
def get_ticker_data(ticker, from_date=FROM_DATE, to_date=TO_DATE):
    data = {}

    from_date = datetime.strptime(from_date, '%Y-%m-%d')
    to_date = datetime.strptime(to_date, '%Y-%m-%d')

    days_between = from_date - to_date
    days = abs(days_between.days)

    if days_between == 0:
        return
    while True:
        if days > 364:
            from_date = last_year_date(to_date)
            year_data = scrape_data(ticker, from_date.strftime("%m/%d/%Y"), to_date.strftime("%m/%d/%Y"))
            if year_data is not None:
                data.update(year_data)
            to_date = from_date - timedelta(days=1)
            days -= 364
        else:
            year_data = scrape_data(ticker, from_date, to_date)
            if year_data is not None:
                data.update(year_data)
            break
    return data

