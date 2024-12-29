# MSE Web App
This project is a homework assignment for the subject 'Software Design and Architecture' at FCSE. The goal is to display the historical data from the [Macedonian Stock Exchange Website](https://www.mse.mk/en/stats/symbolhistory/ADIN) and the technical analysis performed on it.


## Technologies
- **Beautiful Soup** - With the use of this library, the historical data from the [Macedonian Stock Exchange Website](https://www.mse.mk/en/stats/symbolhistory/ADIN) is scraped and stored in csv files that serve as a temporary database.

- **pandas** - In order to work with the raw data, the pandas library is used. It helps organize the historical data, format it, and store it in a more easily understandable form (dataframe).
- **Flask** - The main application is built on top of this technology. It uses HTTP requests and responses to establish communication between the browser and the application, it renders the HTMLs and handles the user inputs.
- **SQLite** - It is used to establish a communication between the Flask application and the database. It is also used to filter and return data from the given user inputs.
- **Plotly** - For the display of the technical analysis performed on the historical data, the plotting library Plotly is used. It uses charts (plots) to showcase the correlation between the historical data and the different indicators, such as Moving Averages and Oscillators.


## How to run the app
### Homework 1
To run this homework successfully, only the [scraper](Homework1/scraper.py) needs to be executed.
### Homework 2
Because this homework uses parts of the previous homework (Homework 1), it is necessary to download both folders, [Homework1](Homework1) and [Homework2](Homework2). Firstly, to run the application, the [app.py](Homework2/tech_prototype/app.py) script needs to be executed and then the URL http://127.0.0.1:5000 to be entered in the browser.
### Homework 3
This homework can be executed independently from the previous homeworks. To run the application, the [app.py](app.py) script needs to be executed first and then the url http://127.0.0.1:5000 to be entered in the browser.


# Team
Tamara Stojchevska (221551) 

Marija Ilievska (221508)
