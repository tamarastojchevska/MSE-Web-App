from Homework4.TickersService import tickers_bp
from Homework4.TickersService.model.tickers import TickerScraper

@tickers_bp.route('/tickers', methods=['GET'])
def get_tickers():
    return TickerScraper.scrape_tickers()

