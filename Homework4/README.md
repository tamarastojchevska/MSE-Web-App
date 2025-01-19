# Macedonian Stock Exchange
## Microservice

This project offers a microservice that is responsible for scraping the issuers and their historical data from the [Macedonian Stock Exchange Website](https://www.mse.mk/en/stats/symbolhistory/ADIN). This microservice is an independent app separate from the main app and can run on its own. 

## Design Patterns

- **Singleton** Pattern: Modules in python are essentially Singleton instances of an internal module class and all their global parameters and/or functions are attributes on the module instance. For example the [scraper urls](app/models/sqlite/scraper_urls.py). Wherever this module is imported it acts like a Singleton.
- **MVC** Pattern: This application has a similar structure to the Model-View-Controller Design Pattern; it has the [Models](app/models), the View in this case are the [templates](app/templates), and the Controller are the [routes](app/frontend/routes.py) that access the templates and the models. The microservice also follows this pattern. It has a [Model](scraper_app/model), a ["Controller"](scraper_app/api), but it lacks the View because it does not need it since it is a microservice and not an app.


## Docker Containerization
This project has multiple Dockerfiles that are then composed in a [Docker Compose](docker-compose.yml) file.

### How to build the images and run the app locally
```console
[path/to/scraper_app/Dockerfile]> docker build -t scraper-app:final .
[path/to/app/Dockerfile]> docker build -t app:final .
[path/to/update/Dockerfile]> docker build -t update:final .

[path/to/docker-compose]> docker-compose up
```
After the images have been started, the application can be accessed through http://localhost:5000/

The microservice can be accessed through http://localhost:5001/scraper/tickers to get the issuer codes,

`http://localhost:5001/scraper/{issuer-code}` to access all the data for the specified issuer, 

or `http://localhost:5001/scraper/{issuer-code} {yyyy-mm-dd} {yyyy-mm-dd}` to access the data within a specific time frame (from date, to date) for the given issuer.

## Hosting
The application and microservice are hosted on Azure.

## Links
- Application: https://mkse.azurewebsites.net/
- Microservice:
  - List of issuers in JSON:<br />
      https://mkse-scraper.azurewebsites.net/scraper/tickers
  - Histroical data for issuer in JSON: <br />
      `https://mkse-scraper.azurewebsites.net/scraper/{issuer-code}`
  - Historical data for issuer for a given time frame (from - to) dates: <br />
      `https://mkse-scraper.azurewebsites.net/scraper/{issuer-code} {yyyy-mm-dd} {yyyy-mm-dd}`

<sub>Note: replace the parameters in the curly brackets {} with valid values in the links<sub>
