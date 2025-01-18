FROM python:3.10.11-alpine3.17
WORKDIR /scraper-app
COPY . /scraper-app
RUN pip install -r requirements.txt
EXPOSE 5001
CMD ["python", "app.py"]