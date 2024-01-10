from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keras.models import load_model
from keras.preprocessing.text import tokenizer_from_json, Tokenizer
from keras.preprocessing.sequence import pad_sequences
import json
from pathlib import Path

from functionality.model.bot_model_buttons import model_btns
from functionality.model.scrapers import websites_xpath, parse_page

from utils.ner_and_clean import ner_and_clear_text
from utils.custom_exceptions import ParseError
from utils.models_vars import MAXLEN, MODEL_OUTPUT
from utils.text_messages import (
    MODEL_INFO,
    INSERT_LINK_MSG,
    INSERT_TEXT_MSG,
    PREDICTION_LEVEL_1,
    PREDICTION_LEVEL_3,
)

router = Router()


class ModelInference(StatesGroup):
    """
    Class for state changes and also container for data.
    """

    pass_link = State()
    pass_text = State()


@router.callback_query(F.data == "make_prediction")
async def msg_model(callback: CallbackQuery):
    await callback.answer(cache_time=1)
    await callback.message.answer(
        f"What would you like to do with the model?", reply_markup=model_btns()
    )


def read_json_tokenizer(path: Path):
    with open(path, "r") as f:
        data = json.load(f)
        return tokenizer_from_json(data)


def initialize_models_and_tokenizers():
    global comp_model, ind_model, glob_moex_model, glob_rvi_model, glob_rubusd_model
    global comp_tokenizer, ind_tokenizer, glob_moex_tokenizer, glob_rvi_tokenizer, glob_rubusd_tokenizer

    model_path_unif = Path().cwd() / "utils" / "models"
    tokenizer_path_unif = Path().cwd() / "utils" / "tokenizers"

    comp_model = load_model(model_path_unif / "comp_model.keras")
    ind_model = load_model(model_path_unif / "ind_model.keras")
    glob_moex_model = load_model(model_path_unif / "glob_moex_model.keras")
    glob_rvi_model = load_model(model_path_unif / "glob_rvi_model.keras")
    glob_rubusd_model = load_model(model_path_unif / "glob_rubusd_model.keras")

    comp_tokenizer = read_json_tokenizer(tokenizer_path_unif / "comp_tokenizer.json")
    ind_tokenizer = read_json_tokenizer(tokenizer_path_unif / "ind_tokenizer.json")
    glob_moex_tokenizer = read_json_tokenizer(
        tokenizer_path_unif / "glob_moex_tokenizer.json"
    )
    glob_rvi_tokenizer = read_json_tokenizer(
        tokenizer_path_unif / "glob_rvi_tokenizer.json"
    )
    glob_rubusd_tokenizer = read_json_tokenizer(
        tokenizer_path_unif / "glob_rubusd_tokenizer.json"
    )


def tokenize_and_pad_seq_text(text: str, tokenizer: Tokenizer):
    seq_text = tokenizer.texts_to_sequences([text])
    seq_text = pad_sequences(seq_text, maxlen=MAXLEN)

    return seq_text


def prediction_raw_text(text: str):
    level, text = ner_and_clear_text(text)

    # Global_MOEX
    seq_text_glob_moex = tokenize_and_pad_seq_text(text, glob_moex_tokenizer)
    pred_glob_moex = glob_moex_model.predict(seq_text_glob_moex)
    pred_glob_moex_label = MODEL_OUTPUT[pred_glob_moex[0].argmax()]
    # Global_RVI
    seq_text_glob_rvi = tokenize_and_pad_seq_text(text, glob_rvi_tokenizer)
    pred_glob_rvi = glob_rvi_model.predict(seq_text_glob_rvi)
    pred_glob_rvi_label = MODEL_OUTPUT[pred_glob_rvi[0].argmax()]
    # Global_RUBUSD
    seq_text_glob_rubusd = tokenize_and_pad_seq_text(text, glob_rubusd_tokenizer)
    pred_glob_rubusd = glob_rubusd_model.predict(seq_text_glob_rubusd)
    pred_glob_rubusd_label = MODEL_OUTPUT[pred_glob_rubusd[0].argmax()]

    if level == 3:
        # Company
        seq_text_comp = tokenize_and_pad_seq_text(text, comp_tokenizer)
        pred_comp = comp_model.predict(seq_text_comp)
        pred_comp_label = MODEL_OUTPUT[pred_comp[0].argmax()]
        # Industry
        seq_text_ind = tokenize_and_pad_seq_text(text, ind_tokenizer)
        pred_ind = ind_model.predict(seq_text_ind)
        pred_ind_label = MODEL_OUTPUT[pred_ind[0].argmax()]
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
async def msg_model_info(callback: CallbackQuery):
    await callback.answer(cache_time=1)
    await callback.message.answer(MODEL_INFO, parse_mode=ParseMode.MARKDOWN_V2)


@router.callback_query(F.data == "insert_link")
async def msg_insert_link(callback: CallbackQuery, state: FSMContext):
    await callback.answer(cache_time=1)
    await callback.message.answer(
        INSERT_LINK_MSG.format(websites=[*websites_xpath.keys()]),
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(ModelInference.pass_link)


@router.message(ModelInference.pass_link)
async def make_prediction_link(msg: Message, state: FSMContext):
    url = msg.text.lower()
    text = False

    try:
        if "smart-lab" in url:
            text = parse_page(url, "smartlab")
        elif "kommersant" in url:
            text = parse_page(url, "kommersant")
        elif "interfax" in url:
            text = parse_page(url, "interfax")
        elif "ria" in url:
            text = parse_page(url, "ria")
        else:
            await msg.answer("Sorry, the link you passed is invalid")

        if text:
            await msg.answer(
                prediction_raw_text(text),
                parse_mode=ParseMode.MARKDOWN_V2,
            )

    except ParseError as e:
        await msg.answer(e)
    finally:
        await state.clear()


@router.callback_query(F.data == "insert_text")
async def msg_insert_text(callback: CallbackQuery, state: FSMContext):
    await callback.answer(cache_time=1)
    await callback.message.answer(
        INSERT_TEXT_MSG,
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(ModelInference.pass_text)


@router.message(ModelInference.pass_text)
async def make_prediction_text(msg: Message, state: FSMContext):
    text = msg.text[5:]
    await msg.answer(
        prediction_raw_text(text),
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    await state.clear()
