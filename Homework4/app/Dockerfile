FROM python:3.10.11-alpine3.17

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

# default flask app port
EXPOSE 5000

CMD ["python", "app.py"]