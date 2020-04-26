# Predicting spread of Covid-19 

## Datasets
us-counties.csv: Contains data about cumulative confirmed cases and deaths in each US county related to the covid-19 pandemic.
                 Data from https://www.kaggle.com/fireballbyedimyrnmom/us-counties-covid-19-dataset#us-counties.csv
                 
census_total: Data collected from the US government census website using the following tool- https://github.com/datadesk/census-data-downloader

## Baseline Model
basic_model.py - A basic MLP (Multi-layer perceptron) model to predict cases and deahts. (Does not work well as it does not take into account the sequential nature of the data.)

## Preprocessing
preprocess.py: preprocesses the two datasets and also divides the counties into train, validation and test sets.
int_to_str.json: Mapping from US county codes (fips codes) to Hyderabad regions.
str_to_int.json: Mapping from Hyderabad regions to US county codes (fips codes).
preprocessed_data: Folder in which preprocessed data is stored

## New cases predictor
cases_covid.py: Contains pytorch-lightning module for the case prediction model
cases_modeling.py: Contains dataloader and LSTM model for predicting cases
cases_trainer.py: Contains code to train and test the case model 

## New deaths predictor
deaths_covid.py: Contains pytorch-lightning module for the deaths prediction model
deaths_modeling.py: Contains dataloader and LSTM model for predicting deaths
deaths_trainer.py: Contains code to train and test the deaths model

## Models
models: Folder containing saved (trained) models which are used for testing (predicting new cases and deaths)

## Final Script
get_predictions.py: The script that is to be run to get the predictions for the next 7 days
