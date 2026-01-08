# Florida Roofs Data Mining Project

## Summary:
This repository holds a data mining project that intends to answer the question, how can one know which roofs are in need of changing? 
To tackle the problem, I used ArcGis data and webscraping to compile public parcels data from Florida as well as a sample of roof
permits from various cities in Broward County. After processing the data I used various machine learning and classification methods
to create a highly accurate model. This work demonstrates an understanding of pipelines, data cleaning and normalization, and data
analysis for prediction.

## Datasets:
Florida Statewide Parcels Database -> https://www.floridagio.gov/datasets/FGIO::florida-statewide-parcels/about

City of Tamarac Building Permits & Inspections Portal -> https://e-gov.tamarac.org/Click2GovBP/selectpermit.html

Pompano Beach Building Department -> https://c2g.pompanobeachfl.gov/Click2GovBP/selectpermit.html

City of Hallandale Beach Self Service Portal -> https://hallandalefl-energovpub.tylerhost.net/apps/SelfService#/search?m=1&fm=1&ps=100&pn=1&em=false&st=roofing

City of Pembroke Pines Development Portal -> https://pembrokepinesfl-energovweb.tylerhost.net/apps/selfservice#/search?m=2&ps=10&pn=1&em=false&st=roof

Wikipedia Hurricanes Dataset -> https://en.wikipedia.org/wiki/List_of_Florida_hurricanes

## Methodology:

The following techniques were explored:
* Exploratory Data Analysis (EDA)
* Feature selection
* Supervised learning models:
    - K-Nearest Neighbors
    - Logistic Regression
    - Decision Trees
    - Random Forest
* Cross-validation and hyperparameter tuning
* Model evaluation:
    - Accuracy 
    - Precision
    - Recall
    - F1-score

## Results:
The best performing model was KNN, with a cross-validation accuracy of 98.9% 
In general, the ArcGis API keeps a very consistent data structure, nonetheless, the following tradeoffs were observed:
    * The model requires information about the material, which may not be specified in every roof-construction permit.
    * Roof permit downloads can vary from city to city, or from county to county, requiring more complex data downloads.

## Repository Structure:

├── parcels/                # Unprocessed parcels data as well as its extraction code

├── permits/                # Unprocessed permits data

├── puppeteer_scraping/     # The node js code for the data extraction of Tamarac county

├── hurricanes_fl.csv       # Data regarding significant hurricanes for the state of Florida

├── main.ipynb              # Processing and Results

## Author:

Fernando Cortés Rentería

Data Analytics and Business Intelligence

B.A in Finance

Student of Software Engineering

[Github](https://github.com/Fernando-Cortes-Renteria) [LinkedIn](https://www.linkedin.com/in/fernando-cortes-renteria/)
