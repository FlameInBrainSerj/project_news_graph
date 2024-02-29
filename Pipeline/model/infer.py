from pathlib import Path

import hydra
import pytorch_lightning as pl
import torch
from __init__ import PROJECT_ROOT
from dataset.dataset import DataModuleNews
from omegaconf import DictConfig


class Inference:
    """
    Inference class for making predictions with a pre-trained PyTorch Lightning model.

    Args:
        cfg (DictConfig): Configuration object containing settings.

    Attributes:
        cfg (DictConfig): Configuration object containing settings.

    Methods:
        infer(): Main method for making predictions using the specified model.
    """

    def __init__(self, cfg: DictConfig):
        self.cfg = cfg

    def infer(self) -> None:
        """
        Main method for making predictions using the specified PyTorch Lightning model.
        """
        # Load the trained model
        model = torch.load(Path(self.cfg.model_path) / self.cfg.model_file)

        # Initialize the datamodule
        datamodule = DataModuleNews(self.cfg, infer=True)
        datamodule.setup()

        # Make sure that datamodule is using the vocab as model
        datamodule.vocab = model.vocab

        infer_model = pl.Trainer(
            # Inference
            inference_mode=self.cfg.inference_mode,
            # Technical params
            devices=self.cfg.devices,
            accelerator=self.cfg.accelerator,
            # Logging
            log_every_n_steps=self.cfg.log_every_n_steps,
        )

        # Get inference from the model
        infer_model.predict(model=model, datamodule=datamodule)


@hydra.main(
    config_path=str(PROJECT_ROOT / "configs" / "model"),
    config_name="basic_model_config.yaml",
    version_base="1.3",
)
def infer(cfg: DictConfig) -> None:
    """Infer best train experiment"""
    Inference(cfg).infer()


if __name__ == "__main__":
    infer()
