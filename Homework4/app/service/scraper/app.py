from flask import Flask
from Homework4.app.service.scraper.api.data_scraper_api import data_bp

app = Flask(__name__)
app.register_blueprint(data_bp)

app.run(debug=True, port=5002)