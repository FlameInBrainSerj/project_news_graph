from pathlib import Path

import hydra
import pytorch_lightning as pl
import torch
from __init__ import PROJECT_ROOT
from dataset.dataset import DataModuleNews
from model.model import LSTMNewsClassificationModel
from omegaconf import DictConfig


class Trainer:
    """
    Trainer class for training a PyTorch Lightning model.

    Args:
        cfg (DictConfig): Configuration object containing settings.

    Attributes:
        cfg (DictConfig): Configuration object containing settings.

    Methods:
        train(): Main method for training the PyTorch Lightning model.
    """

    def __init__(self, cfg: DictConfig):
        self.cfg = cfg

    def train(self) -> None:
        """
        Main method for training the PyTorch Lightning model.
        """
        # Initialize the DataModule
        datamodule = DataModuleNews(self.cfg, infer=False)
        datamodule.setup()

        # Initialize the model
        model = LSTMNewsClassificationModel(self.cfg)

        trainer = pl.Trainer(
            # Main params
            max_epochs=self.cfg.max_epochs,
            gradient_clip_val=self.cfg.gradient_clip_val,
            # Technical params
            val_check_interval=self.cfg.val_check_interval,
            devices=self.cfg.devices,
            accelerator=self.cfg.accelerator,
            deterministic=self.cfg.full_deterministic_mode,
            # Debug params
            overfit_batches=self.cfg.overfit_batches,
            num_sanity_val_steps=self.cfg.num_sanity_val_steps,
            # Logging
            log_every_n_steps=self.cfg.log_every_n_steps,
        )

        # Train the model
        trainer.fit(model, datamodule=datamodule)

        # Save the resulting model
        torch.save(
            model,
            Path(self.cfg.model_path) / self.cfg.model_file,
        )


@hydra.main(
    config_path=str(PROJECT_ROOT / "configs" / "model"),
    config_name="basic_model_config.yaml",
    version_base="1.3",
)
def train(cfg: DictConfig) -> None:
    """Train a model"""
    Trainer(cfg).train()


if __name__ == "__main__":
    train()
