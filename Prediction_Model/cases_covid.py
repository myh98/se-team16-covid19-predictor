""" Lightining Module for projection. """

import os
from collections import OrderedDict
from argparse import ArgumentParser

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from torch import optim
from torch.utils.data import DataLoader

from pytorch_lightning import _logger as log
from pytorch_lightning.core import LightningModule

from cases_modeling import LSTM, Dataset, get_splits


class CovidProjection(LightningModule):
    """ The lightning class for covid projection. """

    def __init__(self, hparams):
        # init superclass
        super().__init__()
        self.hparams = hparams
        self.covid_file = "preprocessed_data/covid_data.csv"
        self.batch_size = hparams.batch_size
        self.train_ids, self.val_ids, self.test_ids = get_splits(hparams.data_root)
        self.model = LSTM(hparams.in_features, hparams.hidden_dim)

    def forward(self):
        pass

    def loss(self, predictions, cases):
        mse = F.mse_loss(predictions, cases)
        return mse

    def training_step(self, batch, batch_idx):
        """ Training Step """
        # forward pass
        _, features, cases, _, _ = batch
        output = self.model(features)
        predictions = output.squeeze()[:, -7:]

        # calculate loss
        loss_val = self.loss(predictions, cases)

        tqdm_dict = {"train_loss": loss_val}
        output = OrderedDict(
            {"loss": loss_val, "progress_bar": tqdm_dict, "log": tqdm_dict}
        )

        # can also return just a scalar instead of a dict (return loss_val)
        return output

    def validation_step(self, batch, batch_idx):
        """ Validation Step """
        # forward pass
        _, features, cases, _, _ = batch
        output = self.model(features, predict=True)
        predictions = output.squeeze()[:, -7:]

        # calculate loss
        loss_val = self.loss(predictions, cases)

        output = OrderedDict({"val_loss": loss_val})
        return output

    def validation_epoch_end(self, outputs):
        """
        Called at the end of validation to aggregate outputs.
        :param outputs: list of individual outputs of each validation step.
        """
        # if returned a scalar from validation_step, outputs is a list of tensor scalars
        # we return just the average in this case (if we want)
        # return torch.stack(outputs).mean()

        val_loss_mean = 0
        for output in outputs:
            val_loss = output["val_loss"]

            # reduce manually when using dp
            if self.trainer.use_dp or self.trainer.use_ddp2:
                val_loss = torch.mean(val_loss)
            val_loss_mean += val_loss

        val_loss_mean /= len(outputs)
        tqdm_dict = {"val_loss": val_loss_mean}
        result = {
            "progress_bar": tqdm_dict,
            "log": tqdm_dict,
            "val_loss": val_loss_mean,
        }
        return result

    def test_step(self, batch, batch_idx):
        """ Testing Step """
        # forward pass
        geoids, features, cases, mean, std = batch
        output = self.model(features, predict=True)
        predictions = output.squeeze()[:, -7:]

        # create output dict
        output = {}
        output["predictions"] = predictions
        output["cases"] = cases
        output["geoids"] = geoids
        output["mean"] = mean
        output["std"] = std
        return output

    def test_epoch_end(self, outputs):
        """
        Called at the end of test to aggregate outputs, similar to `validation_epoch_end`.
        :param outputs: list of individual outputs of each test step
        """

        predictions = []
        cases = []
        geoids = []
        mean = []
        std = []
        for output in outputs:
            predictions.append(output["predictions"])
            cases.append(output["cases"])
            geoids.append(output["geoids"])
            mean.append(output["mean"])
            std.append(output["std"])
        predictions = torch.cat(predictions, dim=0)
        cases = torch.cat(cases, dim=0)
        geoids = torch.cat(geoids, dim=0).squeeze()
        mean = torch.cat(mean, dim=0).squeeze()
        std = torch.cat(std, dim=0).squeeze()

        # Un-normalize the data
        predictions = (predictions * std.unsqueeze(1)) + mean.unsqueeze(1)
        cases = (cases * std.unsqueeze(1)) + mean.unsqueeze(1)

        predictions[predictions < 0] = 0

        # compute mean absolute error
        mae = F.l1_loss(predictions, cases)

        # Write outputs to disk
        columns = list(range(1, 8))
        predictions = pd.DataFrame(data=predictions.numpy(), columns=columns)
        cases = pd.DataFrame(data=cases.numpy(), columns=columns)
        geoids = geoids.numpy().squeeze().tolist()
        predictions.insert(0, "geoid", geoids)
        cases.insert(0, "geoid", geoids)
        predictions.to_csv("cases_predictions.csv", header=True, index=False)
        cases.to_csv("cases.csv", header=True, index=False)

        # create output dict
        tqdm_dict = {"mae": mae}
        results = {}
        results["progress_bar"] = tqdm_dict
        results["log"] = tqdm_dict
        results["mae"] = mae

        return results

    def configure_optimizers(self):
        """
        Return whatever optimizers and learning rate schedulers you want here.
        At least one optimizer is required.
        """
        optimizer = optim.Adam(self.model.parameters(), lr=self.hparams.learning_rate)
        scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=10)
        return [optimizer], [scheduler]

    def __dataloader(self, geoids):
        census_file = "preprocessed_data/census.csv"
        covid_file = self.covid_file
        dataset = Dataset(geoids, census_file=census_file, covid_file=covid_file)
        # when using multi-node (ddp) we need to add the  datasampler
        batch_size = self.hparams.batch_size
        loader = DataLoader(dataset=dataset, batch_size=batch_size, num_workers=4)
        return loader

    def train_dataloader(self):
        log.info("Training data loader called.")
        return self.__dataloader(geoids=self.train_ids)

    def val_dataloader(self):
        log.info("Validation data loader called.")
        return self.__dataloader(geoids=self.val_ids)

    def test_dataloader(self):
        log.info("Test data loader called.")
        return self.__dataloader(geoids=self.test_ids)

    @staticmethod
    def add_model_specific_args(parent_parser, root_dir):  # pragma: no-cover
        """
        Parameters you define here will be available to your model through `self.hparams`.
        """
        parser = ArgumentParser(parents=[parent_parser])

        # network params
        parser.add_argument("--in_features", default=78, type=int)
        parser.add_argument("--hidden_dim", default=120, type=int)
        parser.add_argument("--drop_prob", default=0.2, type=float)
        parser.add_argument("--learning_rate", default=0.001, type=float)

        # data
        parser.add_argument(
            "--data_root", default="preprocessed_data", type=str
        )

        parser.add_argument(
            "--covid_file", default="preprocessed_data/covid.csv", type=str
        )

        # training params (opt)
        parser.add_argument("--epochs", default=200, type=int)
        parser.add_argument("--batch_size", default=64, type=int)
        return parser
