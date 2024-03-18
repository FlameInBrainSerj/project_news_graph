import torch
from models_functionality import DEVICE
from torch import nn
from torchtext.vocab import Vocab


class LSTMClassifier(nn.Module):
    """
    LSTMClassifier class for news' influence on financial assets predictions.
    """

    def __init__(self, emb_dim: int, hid_dim: int, n_layers: int, vocab: Vocab):
        super(LSTMClassifier, self).__init__()

        self.vocab = vocab
        self.emb_dim = emb_dim
        self.hid_dim = hid_dim
        self.n_layers = n_layers

        self.embedding_layer = nn.Embedding(
            num_embeddings=len(self.vocab),
            embedding_dim=self.emb_dim,
        )

        self.lstm = nn.LSTM(
            input_size=self.emb_dim,
            hidden_size=self.hid_dim,
            num_layers=self.n_layers,
            batch_first=True,
        )

        self.linear = nn.Linear(self.hid_dim, 3)

    def forward(self, x_batch: torch.Tensor) -> torch.Tensor:
        embeddings = self.embedding_layer(x_batch)
        hidden, carry = torch.zeros(
            self.n_layers,
            len(x_batch),
            self.hid_dim,
            device=DEVICE,
        ), torch.zeros(self.n_layers, len(x_batch), self.hid_dim, device=DEVICE)
        output, (hidden, carry) = self.lstm(embeddings, (hidden, carry))
        return self.linear(output[:, -1])
