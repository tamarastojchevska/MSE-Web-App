from flask import Flask
from Homework4.app.frontend.routes import templates_bp

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'
app.register_blueprint(templates_bp)
