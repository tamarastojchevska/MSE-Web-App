# Architectural designs

### Conceptual architecture

Through our web application, users interact with the GUI to select specific companies and the date range for which they require stock market data. These filters are then sent to the backend, where they are processed to query the database. The database, which stores pre-processed stock data, retrieves the appropriate records. The stock data is initially collected from the Macedonian Stock Exchange website through a web scraper. This raw data is formatted and structured using the Pipe and Filter architecture.

### Execution architecture

In the execution architecture, the user triggers a user-initiated request by interacting with the GUI. It sends an HTTP request to the Flask framework, which acts as a controller. The request is processed by Flask querying the database for the specific stock market data matching the selected filters, and then the database retrieves the needed data to the Flask backend. Then, Flask sends the data to the frontend (GUI) for display, which can be categorized as a service-oriented execution.

### Implementation architecture

The website uses Bootstrap as a front-end framework, to ensure that the user interface is both visually appealing and functional.

We implemented a web scraper using python and beautiful soup. It extracts historical data from the HTML of the MSE website, formats it into CSV files, and stores it for further analysis.

Further, we use SQLite as the database solution to efficiently store and manage the stock market data collected through our scraping process. For reliability, the raw data is initially stored in CSV files before being transferred into the SQLite database. This acts as a backup mechanism, preventing data loss. 

The framework we have chosen to parse the stock market data tables is Flask. It handles all user input, such as the from and to dates, as well as the company the user wants to analyze, and queries the SQLite database to retrieve the data. 

