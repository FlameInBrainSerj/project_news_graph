from pathlib import Path

import torch

ARTIFACTS_PATH = Path(__file__).parent.parent.parent / "artifacts"

MODELS_PATH = ARTIFACTS_PATH / "models"
VOCABS_PATH = ARTIFACTS_PATH / "tokenizers"

# Device for PyTorch
DEVICE = torch.device("cpu")
