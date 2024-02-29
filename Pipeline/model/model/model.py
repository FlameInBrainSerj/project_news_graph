from pathlib import Path
from typing import Any, Dict

import pytorch_lightning as pl
import torch
from omegaconf import DictConfig
from sklearn.metrics import f1_score
from torch import Tensor


class LSTMNewsClassificationModel(pl.LightningModule):
    """
    LSTM model for the News data.
    """

    def __init__(self, cfg: DictConfig):
        super().__init__()
        self.learning_rate = cfg.learning_rate

        self.emb_dim = cfg.emb_dim
        self.hid_dim = cfg.hid_dim
        self.n_layers = cfg.n_layers

        self.vocab = torch.load(Path(cfg.vocab_path) / cfg.vocab_file)
        self.loss_fn = torch.nn.CrossEntropyLoss()

        self.embedding_layer = torch.nn.Embedding(
            num_embeddings=len(self.vocab),
            embedding_dim=self.emb_dim,
        )

        self.lstm = torch.nn.LSTM(
            input_size=self.emb_dim,
            hidden_size=self.hid_dim,
            num_layers=self.n_layers,
            batch_first=True,
        )

        self.linear = torch.nn.Linear(self.hid_dim, 3)

    def forward(
        self,
        x_batch: Tensor,
        labels: Tensor = None,
    ) -> Any | tuple[Any, Any, Any]:
        """
        Forward pass of the model.
        """

        embeddings = self.embedding_layer(x_batch)
        hidden = torch.zeros(self.n_layers, len(x_batch), self.hid_dim)
        carry = torch.zeros(self.n_layers, len(x_batch), self.hid_dim)
        output, (hidden, carry) = self.lstm(embeddings, (hidden, carry))

        logits = self.linear(output[:, -1])

        if labels is not None:
            loss = self.loss_fn(logits, labels)

            preds = logits.argmax(dim=-1)
            f1_metric = f1_score(labels, preds, average="macro")

            return logits, loss, f1_metric

        return logits

    def training_step(
        self,
        batch: Any,
        batch_idx: int,
        dataloader_idx: int = 0,
    ) -> Dict[str, Tensor]:
        """
        Training step implementation.
        """

        texts, labels = batch
        _, loss, f1_metric = self(texts, labels)

        return {
            "loss": loss,
            "train_f1": f1_metric,
        }

    def validation_step(
        self,
        batch: Any,
        batch_idx: int,
        dataloader_idx: int = 0,
    ) -> Dict[str, Tensor]:
        """
        Validation step implementation.
        """

        texts, labels = batch
        _, loss, f1_metric = self(texts, labels)

        return {
            "loss": loss,
            "val_f1": f1_metric,
        }

    def test_step(
        self,
        batch: Any,
        batch_idx: int,
        dataloader_idx: int = 0,
    ) -> Dict[str, Tensor]:
        """
        Test step implementation.
        """

        texts, labels = batch
        _, loss, f1_metric = self(texts, labels)

        return {
            "loss": loss,
            "test_f1": f1_metric,
        }

    def predict_step(
        self,
        batch: Any,
        batch_idx: int,
        dataloader_idx: int = 0,
    ) -> Dict[str, Tensor]:
        """
        Prediction step implementation.
        """

        texts, _ = batch
        logits = self(texts)

        probs = torch.softmax(logits, dim=1)

        return {"probs": probs}

    def configure_optimizers(self) -> torch.optim.Adam:
        return torch.optim.Adam(self.parameters(), lr=self.learning_rate)
