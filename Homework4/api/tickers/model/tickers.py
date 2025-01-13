import requests
from bs4 import BeautifulSoup

DEF_URL = 'https://www.mse.mk/en/stats/symbolhistory/ADIN'

def check_number_in_string(s):  # for a given string it checks if it contains a number
    return any(i.isdigit() for i in s)


class TickerScraper:
    @staticmethod
    def scrape_tickers():
        # get http request
        response = requests.get(DEF_URL)
        raw_html = response.text

        # parse html from request
        soup = BeautifulSoup(raw_html, "html.parser")

        # get all the codes from the <select> element and it's <option> elements
        raw_codes = soup.select_one('#Code').find_all('option')
        tickers = []
        for code in raw_codes:
            if check_number_in_string(code.text) is not True:
                tickers.append(code.text)
        return tickers

