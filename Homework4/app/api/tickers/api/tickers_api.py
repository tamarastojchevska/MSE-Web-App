from Homework4.app.api.tickers import tickers_bp
from Homework4.app.api.tickers.model import tickers


@tickers_bp.route('/tickers', methods=['GET'])
def get_tickers():
    return tickers.scrape_tickers()

