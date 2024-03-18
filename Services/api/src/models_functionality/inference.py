from typing import Any

import __main__
import pandas as pd
import torch
from celery import Celery
from config import REDIS_HOST, REDIS_PORT
from models_functionality import DEVICE, MODELS_PATH, VOCABS_PATH
from models_functionality.main_model import LSTMClassifier
from models_functionality.ner_and_preprocess import ner_and_clear_text
from models_functionality.utils import MAXLEN, MODEL_OUTPUT
from torchtext.vocab import Vocab

# Celery for queuing model inference calls
celery = Celery(
    "inference",
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}",
)
celery.conf.broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

# Some kostyl
setattr(__main__, "LSTMClassifier", LSTMClassifier)

# Initialize models
comp_model = torch.load(MODELS_PATH / "comp_model.h5", map_location=DEVICE)
ind_model = torch.load(MODELS_PATH / "ind_model.h5", map_location=DEVICE)
glob_moex_model = torch.load(
    MODELS_PATH / "glob_moex_model.h5",
    map_location=DEVICE,
)
glob_rvi_model = torch.load(
    MODELS_PATH / "glob_rvi_model.h5",
    map_location=DEVICE,
)
glob_rubusd_model = torch.load(
    MODELS_PATH / "glob_rubusd_model.h5",
    map_location=DEVICE,
)

# Initialize vocabs
comp_vocab = torch.load(VOCABS_PATH / "comp_vocab.pt")
ind_vocab = torch.load(VOCABS_PATH / "ind_vocab.pt")
glob_moex_vocab = torch.load(VOCABS_PATH / "glob_moex_vocab.pt")
glob_rvi_vocab = torch.load(VOCABS_PATH / "glob_rvi_vocab.pt")
glob_rubusd_vocab = torch.load(VOCABS_PATH / "glob_rubusd_vocab.pt")


def tokenize_and_pad_seq_text(text: str, vocab: Vocab) -> torch.Tensor:
    """
    Tokenize text and pad tokenized text according to MAXLEN.

    :param text: text for tokenization
    :type text: str
    :param vocab: vocab for the model
    :type vocab: Vocab

    :rtype: torch.Tensor
    :return torch.Tensor(text): tokenized and padded text
    """
    # Change words to indexes according to vocab
    text = vocab(text.split(" "))
    # Pad or truncate the sequence
    text = [
        text + ([0] * (MAXLEN - len(text))) if len(text) < MAXLEN else text[:MAXLEN],
    ][0]

    return torch.tensor(text, dtype=torch.int32).reshape(1, -1)


@celery.task
def predict_raw_text(text: str) -> dict[str, Any]:
    """
    Make predictions of news' influence on financial instruments
    in accordance with certain levels with beautiful message.

    :param text: text of the news
    :type text: str

    :rtype: dict[str, Any]
    :return dict: dict with predictions to certain assets
    """
    level, text = ner_and_clear_text(text)

    # Global_MOEX
    seq_text_glob_moex = tokenize_and_pad_seq_text(text, glob_moex_vocab)
    pred_glob_moex = glob_moex_model(seq_text_glob_moex)
    pred_glob_moex_label = MODEL_OUTPUT[pred_glob_moex.detach().numpy()[0].argmax()]
    # Global_RVI
    seq_text_glob_rvi = tokenize_and_pad_seq_text(text, glob_rvi_vocab)
    pred_glob_rvi = glob_rvi_model(seq_text_glob_rvi)
    pred_glob_rvi_label = MODEL_OUTPUT[pred_glob_rvi.detach().numpy()[0].argmax()]
    # Global_RUBUSD
    seq_text_glob_rubusd = tokenize_and_pad_seq_text(text, glob_rubusd_vocab)
    pred_glob_rubusd = glob_rubusd_model(seq_text_glob_rubusd)
    pred_glob_rubusd_label = MODEL_OUTPUT[pred_glob_rubusd.detach().numpy()[0].argmax()]

    if level == 3:
        # Company
        seq_text_comp = tokenize_and_pad_seq_text(text, comp_vocab)
        pred_comp = comp_model(seq_text_comp)
        pred_comp_label = MODEL_OUTPUT[pred_comp.detach().numpy()[0].argmax()]
        # Industry
        seq_text_ind = tokenize_and_pad_seq_text(text, ind_vocab)
        pred_ind = ind_model(seq_text_ind)
        pred_ind_label = MODEL_OUTPUT[pred_ind.detach().numpy()[0].argmax()]

        return {
            "Company": pred_comp_label,
            "Industry": pred_ind_label,
            "Global_moex": pred_glob_moex_label,
            "Global_rvi": pred_glob_rvi_label,
            "Global_rubusd": pred_glob_rubusd_label,
        }

    return {
        "Global_moex": pred_glob_moex_label,
        "Global_rvi": pred_glob_rvi_label,
        "Global_rubusd": pred_glob_rubusd_label,
    }


def predict_texts_and_return_dict(texts: pd.DataFrame) -> dict:
    """
    Get predictions by the texts.

    :param texts: dataframe with texts
    :type texts: pd.DataFrame

    :rtype: dict
    :return response: dict with predictions to corresponding texts
    """
    response = {}

    for i in range(texts.shape[0]):
        text = texts.iloc[i, 0].lower()
        pred = predict_raw_text.delay(text)

        response[i] = pred.get()

    return response
