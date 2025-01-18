FROM python:3.10.11-alpine3.17

WORKDIR /scraper-app
COPY . /scraper-app

RUN pip install -r requirements.txt

# main flask app already uses the default port
EXPOSE 5001

CMD ["python", "app.py"]