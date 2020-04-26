""" Final Script """

import os
import subprocess
import pandas as pd
import ujson as json


def int_to_str(integer, mapping):
    """ Helper function """
    return mapping[str(integer)]


def str_to_int(string, mapping):
    """ Helper function """
    return mapping[string]


def process_zonal_file(path):
    """ Process zonal file """
    covid_data = pd.read_csv(path, header=0, usecols=["zone", "date", "new", "death"],)

    with open("str_to_int.json", "r") as json_file:
        mapping = json.load(json_file)
    covid_data["zone"] = covid_data["zone"].apply(lambda x: str_to_int(x, mapping))
    covid_data = covid_data.rename(
        columns={"zone": "geoid", "date": "day", "new": "cases", "death": "deaths"}
    )

    covid_data["day"] = pd.to_datetime(covid_data["day"])
    covid_data = covid_data.sort_values(by=["geoid", "day"])
    covid_data["min_date"] = covid_data.groupby("geoid")["day"].transform("min")
    covid_data["day"] = covid_data["day"] - covid_data["min_date"]
    covid_data["day"] = covid_data["day"].dt.days
    covid_data = covid_data.reset_index(drop=True)
    covid_data = covid_data.drop(columns=["min_date"])
    covid_data.to_csv("preprocessed_data/covid_data.csv", index=False)


def main():
    """ Main Function """
    process_zonal_file("data_files/my_final_sample.csv")

    cases = ["python", "cases_trainer.py", "--test"]
    deaths = ["python", "deaths_trainer.py", "--test"]
    result = subprocess.run(cases)
    result = subprocess.run(deaths)

    cases = pd.read_csv("cases_predictions.csv", header=0)
    deaths = pd.read_csv("deaths_predictions.csv", header=0)
    data = cases.merge(deaths, how="inner", on="geoid")
    data = data.astype("int")

    threshold_1 = 20
    threshold_2 = 80
    max_cases = cases.iloc[:, 1:].max(axis=1)
    data["predicted_risk"] = ["medium"] * data.shape[0]
    data.loc[max_cases < threshold_1, "predicted_risk"] = "low"
    data.loc[max_cases > threshold_2, "predicted_risk"] = "high"

    with open("int_to_str.json", "r") as json_file:
        mapping = json.load(json_file)
    data["location"] = data["geoid"].apply(lambda x: int_to_str(x, mapping))

    data.to_csv("data_files/final_dataset.csv", index=False)


if __name__ == "__main__":
    main()
