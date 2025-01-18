import os
from api.routes import data_scraper_app

if __name__ == '__main__':
    port = os.environ.get("PORT", 5001)
    data_scraper_app.run(debug=False, host='0.0.0.0', port=port)