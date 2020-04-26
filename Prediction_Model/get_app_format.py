import pandas as pd


def get_app_format(file, geoids):
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
        df["day"] = df["date"] - df["date"].iloc[0]
        df_list.append(df)
    covid_data = pd.concat(df_list)
    covid_data = covid_data.reset_index(drop=True)
    covid_data["day"] = covid_data["day"].dt.days
    covid_data = covid_data.query("fips in @geoids")
    covid_data = covid_data.query("day < 23")
    covid_data = covid_data.drop(columns=["day"])
    covid_data = covid_data.rename(columns={"date": "day", "fips": "geoid"})

    # Get day-wise data (Not cumulative)
    df_list = []
    for _, df in covid_data.groupby("geoid"):
        df["cases"] = df["cases"] - df["cases"].shift(1)
        df["deaths"] = df["deaths"] - df["deaths"].shift(1)
        df_list.append(df)
    covid_data = pd.concat(df_list)
    covid_data = covid_data.dropna()

    return covid_data
