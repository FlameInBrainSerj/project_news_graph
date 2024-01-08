from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from pathlib import Path

from functionality.model.bot_model_buttons import model_btns
from functionality.model.scrapers import websites_xpath, parse_page

from utils.ner_and_clean import ner_and_clear_text
from utils.text_messages import MODEL_INFO, INSERT_LINK_MSG, INSERT_TEXT_MSG

router = Router()


@router.callback_query(F.data == "make_prediction")
async def msg_model(callback: CallbackQuery):
    await callback.answer(cache_time=1)
    await callback.message.answer(
        f"What would you like to do with the model?", reply_markup=model_btns()
    )


def read_json_tokenizer(path):
    # global <models>
    # global <tokenizers>
    pass


def initialize_models_and_tokenizers():
    pass


def prediction_raw_text(text):
    # clean+ner text
    # tokenize text
    # make prediction (levels 1 and 3)
    # beautify output
    pass


@router.callback_query(F.data == "model_info")
async def msg_model_info(callback: CallbackQuery):
    await callback.answer(cache_time=1)
    await callback.message.answer(MODEL_INFO, parse_mode=ParseMode.MARKDOWN_V2)


@router.callback_query(F.data == "insert_link")
async def msg_insert_link(callback: CallbackQuery):
    await callback.answer(cache_time=1)
    await callback.message.answer(
        INSERT_LINK_MSG.format(websites=[*websites_xpath.keys()]),
        parse_mode=ParseMode.HTML,
    )


@router.message(F.text.contains("https"))
async def make_prediction_link(msg: Message):
    # parse text
    # make prediction
    pass


@router.callback_query(F.data == "insert_text")
async def msg_insert_text(callback: CallbackQuery):
    await callback.answer(cache_time=1)
    await callback.message.answer(
        INSERT_TEXT_MSG,
        parse_mode=ParseMode.HTML,
    )


@router.message(F.text.contains("/text"))
async def make_prediction_text(msg: Message):
    # make prediction
    pass


initialize_models_and_tokenizers()
