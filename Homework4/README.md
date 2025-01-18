# Macedonian Stock Exchange
## Microservice

This project offers a microservice that is responsible for scraping the issuers and their historical data from the [Macedonian Stock Exchange Website](https://www.mse.mk/en/stats/symbolhistory/ADIN). This microservice is an independent app separate from the main app and can run on its own. 

## Design Patterns

- **Singleton** Pattern: Modules in python are essentially Singleton instances of an internal module class and all their global parameters and/or functions are attributes on the module instance. For example the [scraper urls](Homework4/app/models/sqlite/scraper_urls.py). Wherever this module is imported it acts like a Singleton.
- **MVC** Pattern: This application has a similar structure to the Model-View-Controller Design Pattern; it has the [Models](Homework4/app/models), the View in this case are the [templates](Homework4/app/templates), and the Controller are the [routes](Homework4/app/frontend/routes.py) that access the templates and the models.


## Docker Containerization
This project has multiple Dockerfiles that are then composed in a [Docker Compose](Homework4/docker-compose.yml) file.

### How to build the images and run the app locally
```console
[path/to/scraper_app/Dockerfile]> docker build -t scraper-app:final .
[path/to/app/Dockerfile]> docker build -t app:final .
[path/to/update/Dockerfile]> docker build -t update:final .

[path/to/docker-compose]> docker-compose up
```
After the images have been started, the application can be accessed through http://localhost:5000/, and the microservice can be accessed through http://localhost:5001/scraper/tickers to get the issuer codes, or http://localhost:5001/scraper/[issuer-code] 
to access the data for the specified issuer.