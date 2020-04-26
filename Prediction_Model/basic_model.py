""" Script to train a simple MLP using only the static features. """

import os
from tqdm import tqdm
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
import seaborn as sns

sns.set()
import matplotlib.pyplot as plt


def get_splits(path):
    """ Returns train, val and test splits. """
    with open(os.path.join(path, "train.txt"), "r") as train_file, open(
        os.path.join(path, "val.txt"), "r"
    ) as val_file, open(os.path.join(path, "test.txt"), "r") as test_file:
        train = list(map(lambda x: int(x.strip()), train_file))
        val = list(map(lambda x: int(x.strip()), val_file))
        test = list(map(lambda x: int(x.strip()), test_file))
    return train, val, test


def combine_data(census_data, covid_data):
    """ Returns feature, label pairs """
    covid_data = covid_data.query("day < 30")
    data_dict = {"geoid": []}
    for i in range(60):
        data_dict[str(i)] = []
    for geoid, df in tqdm(covid_data.groupby("geoid")):
        data_dict["geoid"].append(geoid)
        df = df.drop(columns=["geoid"])
        df = df.set_index("day")
        for i in range(30):
            data_dict[str(i)].append(df.loc[i]["cases"])
            data_dict[str(i + 30)].append(df.loc[i]["deaths"])
    covid_data = pd.DataFrame(data_dict)
    data = census_data.merge(covid_data, how="inner", on="geoid")
    x = data.iloc[:, : 77 + 24]
    y = data.iloc[:, 77 + 24 : 77 + 30]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)
    return x_train, x_test, y_train, y_test


def plot(y_test, y_pred):
    """ Plot outputs """
    n = 3
    m = 3
    fig, axes = plt.subplots(n, m, figsize=(60, 60))
    for i in range(n):
        for j in range(m):
            k = i * n + j
            data = pd.DataFrame({"real": y_test[k], "predicted": y_pred[k]})
            sns.lineplot(data=data, ax=axes[i][j])
    plt.show()


def main():
    """ Main Function """
    # Load Data
    census_data = pd.read_csv("preprocessed_data/census.csv", header=0)
    covid_data = pd.read_csv("preprocessed_data/covid.csv", header=0)

    # train, val, test = get_splits("preprocessed_data")
    x_train, x_test, y_train, y_test = combine_data(census_data, covid_data)

    # Scale the data
    feature_scaler = StandardScaler()
    label_scaler = StandardScaler()

    x_train = feature_scaler.fit_transform(x_train)
    y_train = label_scaler.fit_transform(y_train)

    # Define and train MLP
    mlp = MLPRegressor(
        hidden_layer_sizes=(77 + 24, 100, 100, 7),
        learning_rate_init=0.0001,
        verbose=True,
        batch_size=64,
        max_iter=5000,
        alpha=0.005,
    )
    mlp.fit(x_train, y_train)

    # Test MLP
    x_test = feature_scaler.transform(x_test)
    y_pred = mlp.predict(x_test)
    y_pred = label_scaler.inverse_transform(y_pred)

    # Compute MAE
    mae = mean_absolute_error(y_test, y_pred)
    print("MAE: {}".format(mae))

    # Plot
    y_test = y_test.to_numpy()
    plot(y_test, y_pred)


if __name__ == "__main__":
    main()
