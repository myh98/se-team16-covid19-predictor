""" Script for preprocessing data. """

import os
from functools import partial, reduce
import pandas as pd


def get_file_list(folder_path):
    """ Function that returns the list of files containing census data. """
    file_list = []
    folders = os.listdir(folder_path)
    for folder in folders:
        files = os.listdir(os.path.join(folder_path, folder, "processed"))
        test_file = None
        for file in files:
            if "_counties.csv" in file:
                test_file = file
                break
        file_list.append(os.path.join(folder_path, folder, "processed", test_file))
    return file_list


def drop_rows_and_cols(file):
    """ Drops uncessary columns from the dataframe. """
    data = pd.read_csv(file, header=0)
    cols_to_drop = []
    for column in data.columns:
        if "_moe" in column or "_annotation" in column or "total" in column:
            cols_to_drop.append(column)
        elif column in ("name", "state", "county"):
            cols_to_drop.append(column)
        elif "population" not in file and column == "universe":
            cols_to_drop.append(column)
    data = data.drop(columns=cols_to_drop)
    data = data.dropna(subset=["geoid"])
    data = data.drop_duplicates(subset=["geoid"], keep="last")
    return data


def process_covid_data(file):
    """ Returns the processed dataframe containing case counts. """
    covid_data = pd.read_csv(file, header=0)
    covid_data = covid_data.drop(columns=["county", "state"])
    covid_data = covid_data.dropna()
    covid_data = covid_data.astype({"fips": "int"})
    covid_data["date"] = pd.to_datetime(covid_data["date"])
    covid_data = covid_data.groupby("fips").filter(lambda x: len(x) > 30)
    df_list = []
    for _, df in covid_data.groupby("fips"):
        df = df.sort_values(by=["date"])
        df["date"] = df["date"] - df["date"].iloc[0]
        df_list.append(df)
    covid_data = pd.concat(df_list)
    covid_data = covid_data.reset_index(drop=True)
    covid_data["date"] = covid_data["date"].dt.days
    covid_data = covid_data.rename(columns={"date": "day", "fips": "geoid"})
    return covid_data


def main():
    """ Main Function """
    # Processing Covid Data
    covid_data = process_covid_data("us-counties.csv")
    geoids = covid_data["geoid"].unique().to_list()

    # Processing Census Data
    file_list = get_file_list("census_total")
    data_list = []
    for file in file_list:
        data_list.append(drop_rows_and_cols(file))
    merge = merge = partial(pd.merge, on=["geoid"], how="inner")
    census_data = reduce(merge, data_list)
    census_data = census_data.query("geoid in @geoids")

    new_col_names = {
        "universe": "population",
        "median": "median_income",
        "income_past12months_below_poverty_level": "below_poverty_level",
        "income_past12months_at_or_above_poverty_level": "above_poverty_level",
    }
    census_data = census_data.rename(columns=new_col_names)

    # Save to disk
    covid_data.to_csv("covid.csv", index=False)
    census_data.to_csv("census.csv", index=False)


if __name__ == "__main__":
    main()
