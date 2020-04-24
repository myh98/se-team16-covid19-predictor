""" RNN model and dataloader """

import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence
import seaborn as sns

sns.set()
import matplotlib.pyplot as plt

pd.set_option("mode.chained_assignment", None)


def get_splits(path):
    """ Returns train, val and test splits. """
    with open(os.path.join(path, "train.txt"), "r") as train_file, open(
        os.path.join(path, "val.txt"), "r"
    ) as val_file, open(os.path.join(path, "test.txt"), "r") as test_file:
        train = list(map(lambda x: int(x.strip()), train_file))
        val = list(map(lambda x: int(x.strip()), val_file))
        test = list(map(lambda x: int(x.strip()), test_file))
    return train, val, test


class Dataset:
    """ Dataset Class """

    def __init__(self, geoids, census_file=None, covid_file=None):
        census_data = pd.read_csv(census_file, header=0)
        covid_data = pd.read_csv(covid_file, header=0)
        self.census_data = census_data.set_index("geoid")
        self.covid_data = covid_data.set_index("geoid")
        self.geoids = geoids

        # Convert to float
        self.covid_data = self.covid_data.astype("float")
        self.census_data = self.census_data.astype("float")

        # Normalize census data
        columns = self.census_data.columns
        census_scaler = StandardScaler()
        self.census_data[columns] = census_scaler.fit_transform(
            self.census_data[columns]
        )

        # Get day-wise data (Not cumulative)
        # df_list = []
        # for _, df in self.covid_data.groupby("geoid"):
        # df["cases"] = df["cases"] - df["cases"].shift(1)
        # df["deaths"] = df["deaths"] - df["deaths"].shift(1)
        # df_list.append(df)
        # self.covid_data = pd.concat(df_list)
        # self.covid_data = self.covid_data.dropna()

        # Only consider the first 30 days
        # self.covid_data = self.covid_data.query("day < 30")

        # Reorder columns
        self.covid_data = self.covid_data[["cases", "deaths", "day"]]

        # Drop number of deaths
        self.covid_data = self.covid_data.drop(columns=["cases"])

    def __getitem__(self, idx):
        geoid = self.geoids[idx]
        census_data = self.census_data.loc[geoid].to_numpy()
        covid_data = self.covid_data.loc[geoid].to_numpy()

        # Normalize covid data
        temp = covid_data[:, 0]
        mean = temp.mean()
        std = temp.std()
        covid_data[:, 0] = (temp - mean) / (std + 10 ** -6)

        covid_data = self.add_future(covid_data)

        seq_length = covid_data.shape[0]
        census_data = np.tile(census_data, (seq_length, 1))
        data = np.concatenate([covid_data, census_data], axis=1)
        data = torch.Tensor(data)
        features = data[:-1, :]
        cases = data[seq_length - 7 :, 0]
        # deaths = data[seq_length - 7 :, 1]
        geoid = torch.tensor(geoid)
        mean = torch.tensor(mean)
        std = torch.tensor(std)
        return geoid, features, cases, mean, std

    def add_future(self, data):
        last_day = data[-1, -1]
        future_days = np.arange(1, 8) + last_day
        future_cases = np.zeros(7)
        future = np.stack([future_cases, future_days], axis=1)
        data = np.concatenate([data, future], axis=0)
        return data

    def __len__(self):
        return len(self.geoids)


class LSTM(nn.Module):
    """ LSTM Class """

    def __init__(self, embedding_dim, hidden_dim, output_size=1):
        super(LSTM, self).__init__()
        self.hidden_dim = hidden_dim

        self.input_layer = nn.Linear(embedding_dim, embedding_dim)
        self.layer_norm_1 = nn.LayerNorm(embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.layer_norm_2 = nn.LayerNorm(hidden_dim)
        self.output_layer = nn.Linear(hidden_dim, output_size)

    def forward(self, features, predict=False):
        """ Forward Pass """
        if not predict:
            output = self.forward_step(features)
        else:
            predictions = []
            seq_length = features.shape[1]
            current_features = features[:, : seq_length - 7, :]
            future_features = features[:, seq_length - 7 :, :]
            for i in range(7):
                current_outputs = self.forward_step(current_features)[:, -1, :]
                next_features = future_features[:, i, 1:]
                next_features = torch.cat([current_outputs, next_features], dim=1)
                current_features = torch.cat(
                    [current_features, next_features.unsqueeze(dim=1)], dim=1
                )
                predictions.append(current_outputs)
            output = torch.cat(predictions, dim=1)
        return output

    def forward_step(self, features):
        """ A single forward step """
        embedding = self.input_layer(features)
        embedding = self.layer_norm_1(embedding)
        lstm_out, _ = self.lstm(embedding)
        lstm_out = self.layer_norm_2(lstm_out)
        output = self.output_layer(lstm_out)
        return output


def plot():
    """ Plot outputs """
    y_test = pd.read_csv("deaths.csv", header=0).drop(columns=["geoid"]).to_numpy()
    y_pred = pd.read_csv("deaths_predictions.csv", header=0)
    geoids = y_pred.iloc[:, 0].to_numpy()
    y_pred = y_pred.drop(columns=["geoid"]).to_numpy()

    n = 3
    m = 3
    fig, axes = plt.subplots(n, m, figsize=(60, 60))
    for i in range(n):
        for j in range(m):
            k = i * n + j
            data = pd.DataFrame({"real": y_test[k], "predicted": y_pred[k]})
            sns.lineplot(data=data, ax=axes[i][j]).set_title(geoids[k])
    plt.show()

    mae = np.absolute(y_test - y_pred).mean()
    print("Mean Absolute Error: {}".format(mae))


def main():
    """ Main function (sanity check) """
    dataset = Dataset([1003, 56039, 1015, 1051, 1073, 1081])
    dataloader = DataLoader(dataset, batch_size=1, shuffle=True, num_workers=1)
    model = LSTM(78, 60)
    for i in dataloader:
        print("Geoid: {}".format(i[0].shape))
        print("Features: {}".format(i[1].shape))
        print("Cases: {}".format(i[2].shape))
        print("Mean: {}".format(i[3].shape))
        print("Std: {}".format(i[4].shape))
        print("Model Output: {}".format(model(i[1]).shape))
        break


if __name__ == "__main__":
    main()
