""" Train and Test """

import os
from argparse import ArgumentParser

import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint

from deaths_covid import CovidProjection
from deaths_modeling import plot


def main(hparams):
    """ Main Function """
    model = CovidProjection(hparams)

    checkpoint_callback = ModelCheckpoint(filepath="models/{epoch}-{val_loss:.2f}")
    trainer = pl.Trainer(
        checkpoint_callback=checkpoint_callback,
        max_epochs=hparams.epochs,
        gpus=hparams.gpus,
        distributed_backend=hparams.distributed_backend,
        fast_dev_run=False,
    )
    if not hparams.test:
        trainer.fit(model)
        trainer.test(model)
    else:
        model = CovidProjection.load_from_checkpoint(
            checkpoint_path="models/epoch=145-val_loss=1.27.ckpt"
        )
        trainer.test(model)
    # plot()


if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.realpath(__file__))
    parent_parser = ArgumentParser(add_help=False)

    parent_parser.add_argument(
        "--test", dest="test", action="store_true", help="run testing"
    )

    # gpu args
    parent_parser.add_argument("--gpus", type=int, default=0, help="how many gpus")
    parent_parser.add_argument(
        "--distributed_backend",
        type=str,
        default="dp",
        help="supports three options dp, ddp, ddp2",
    )

    # each LightningModule defines arguments relevant to it
    parser = CovidProjection.add_model_specific_args(parent_parser, root_dir)
    hyperparams = parser.parse_args()

    main(hyperparams)
