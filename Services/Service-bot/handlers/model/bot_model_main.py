from pathlib import Path

import torch
from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from handlers.model.bot_model_buttons import model_btns
from handlers.model.scrapers import parse_page, websites_xpath
from torch import nn
from torchtext.vocab import Vocab
from utils.custom_exceptions import ParseError
from utils.models_vars import MAXLEN, MODEL_OUTPUT
from utils.ner_and_clean import ner_and_clear_text
from utils.text_messages import (
    INSERT_LINK_MSG,
    INSERT_TEXT_MSG,
    MODEL_INFO,
    PREDICTION_LEVEL_1,
    PREDICTION_LEVEL_3,
)

device = torch.device("cpu")
router = Router()


class LSTMClassifier(nn.Module):
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
            device=device,
        ), torch.zeros(self.n_layers, len(x_batch), self.hid_dim, device=device)
        output, (hidden, carry) = self.lstm(embeddings, (hidden, carry))
        return self.linear(output[:, -1])


class ModelInference(StatesGroup):
    """
    Class for the state of model inference.
    """

    pass_link = State()
    pass_text = State()


@router.callback_query(F.data == "make_prediction")
async def msg_model(callback: CallbackQuery) -> None:
    """
    Send message for the user about the model prediction and display model's buttons.

    :param callback: warning
    :type callback: CallbackQuery
    """
    if callback.message:
        await callback.answer(cache_time=1)
        await callback.message.answer(
            "What would you like to do with the model?",
            reply_markup=model_btns(),
        )


def initialize_models_and_vocabs() -> None:
    """
    Initialize models and tokenizers for them.
    """
    global comp_model, ind_model, glob_moex_model, glob_rvi_model, glob_rubusd_model
    global comp_vocab, ind_vocab, glob_moex_vocab, glob_rvi_vocab, glob_rubusd_vocab

    model_path_unif = Path().cwd() / "utils" / "models"
    vocab_path_unif = Path().cwd() / "utils" / "tokenizers"

    comp_model = torch.load(model_path_unif / "comp_model.h5", map_location=device)
    ind_model = torch.load(model_path_unif / "ind_model.h5", map_location=device)
    glob_moex_model = torch.load(
        model_path_unif / "glob_moex_model.h5",
        map_location=device,
    )
    glob_rvi_model = torch.load(
        model_path_unif / "glob_rvi_model.h5",
        map_location=device,
    )
    glob_rubusd_model = torch.load(
        model_path_unif / "glob_rubusd_model.h5",
        map_location=device,
    )

    comp_vocab = torch.load(vocab_path_unif / "comp_vocab.pt")
    ind_vocab = torch.load(vocab_path_unif / "ind_vocab.pt")
    glob_moex_vocab = torch.load(vocab_path_unif / "glob_moex_vocab.pt")
    glob_rvi_vocab = torch.load(vocab_path_unif / "glob_rvi_vocab.pt")
    glob_rubusd_vocab = torch.load(vocab_path_unif / "glob_rubusd_vocab.pt")


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


def prediction_raw_text(text: str) -> str:
    """
    Make predictions of news' influence on financial instruments
    in accordance with certain levels with beautiful message.

    :param text: text of the news
    :type text: str

    :rtype: str
    :return message: message of the prediciton result
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

        return PREDICTION_LEVEL_3.format(
            comp_share_price_label=pred_comp_label,
            ind_index_label=pred_ind_label,
            moex_index_label=pred_glob_moex_label,
            rvi_index_label=pred_glob_rvi_label,
            rubusd_index_label=pred_glob_rubusd_label,
        )

    return PREDICTION_LEVEL_1.format(
        moex_index_label=pred_glob_moex_label,
        rvi_index_label=pred_glob_rvi_label,
        rubusd_index_label=pred_glob_rubusd_label,
    )


@router.callback_query(F.data == "model_info")
async def msg_model_info(callback: CallbackQuery) -> None:
    """
    Display information about the model.

    :param callback: display model info
    :type callback: CallbackQuery
    """
    if callback.message:
        await callback.answer(cache_time=1)
        await callback.message.answer(MODEL_INFO, parse_mode=ParseMode.MARKDOWN_V2)


@router.callback_query(F.data == "insert_link")
async def msg_insert_link(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Ask to insert the link. Changes state to pass_link.

    :param callback: asks to insert the link
    :type callback: CallbackQuery
    :param state: state of operation, changes to pass_link
    :type state: FSMContext
    """
    if callback.message:
        await callback.answer(cache_time=1)
        await callback.message.answer(
            INSERT_LINK_MSG.format(websites=[*websites_xpath.keys()]),
            parse_mode=ParseMode.HTML,
        )
        await state.set_state(ModelInference.pass_link)


@router.message(ModelInference.pass_link)
async def make_prediction_link(msg: Message, state: FSMContext) -> None:
    """
    Parse news' webpage. Return the model prediction.

    :param msg: result of model's prediction
    :type msg: Message
    :param state: state of operation, clears in the end
    :type state: FSMContext
    """
    if msg.text:
        url = msg.text.lower()
    text = ""

    try:
        for site in websites_xpath.keys():
            if site in url:
                text = parse_page(url, site)

        if len(text):
            await msg.answer(
                prediction_raw_text(text),
                parse_mode=ParseMode.MARKDOWN_V2,
            )
        else:
            await msg.answer("Sorry, the link you passed is invalid")

    except ParseError as e:
        await msg.answer(e.message)

    finally:
        await state.clear()


@router.callback_query(F.data == "insert_text")
async def msg_insert_text(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Ask to insert the text. Changes state to pass_text.

    :param callback: asks to insert the text
    :type callback: CallbackQuery
    :param state: state of operation, changes to pass_text
    :type state: FSMContext
    """
    if callback.message:
        await callback.answer(cache_time=1)
        await callback.message.answer(
            INSERT_TEXT_MSG,
            parse_mode=ParseMode.HTML,
        )
        await state.set_state(ModelInference.pass_text)


@router.message(ModelInference.pass_text)
async def make_prediction_text(msg: Message, state: FSMContext) -> None:
    """
    Return the model prediction.

    :param msg: result of model's prediction
    :type msg: Message
    :param state: state of operation, clears in the end
    :type state: FSMContext
    """
    if msg.text:
        await msg.answer(
            prediction_raw_text(msg.text.lower()),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await state.clear()
