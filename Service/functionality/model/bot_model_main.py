from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode

from functionality.model.bot_model_buttons import model_btns

router = Router()

MODEL_INFO = f"""
This model was created with NLP methods and aimed to make predictions of news' influence on financial instruments in accordance with certain levels

_*Levels:*_
\- *Global*: MOEX index, RVI index, RUBUSD course
\- *Indsutry*: industrial indicies \(i\.e\. MOEXOG, MOEXEU, MOEXTL, etc\.\)
\- *Company*: companies' share price according to ticket \(i\.e\. VKCO, SBER, YNDX, etc\.\)

_*Model's output:*_ label of influence on financial instrument \(Negative, Neytral, Positive\)

_*Model's constraints:*_
\- Model was trained on Russian financial news and is only applicable to these kind of news
\- Model is sensetive only to companies from top\-100 of Russian market basing on MOEX index
\- It is highly recommended to pass news with no more than 1\-2 companies, otherwise results could be inadequate
"""


@router.callback_query(F.data == "make_prediction")
async def msg_model(callback: CallbackQuery):
    await callback.answer(cache_time=1)
    await callback.message.answer(
        f"What would you like to do with the model?", reply_markup=model_btns()
    )


def prediction_raw_text(text):
    pass


@router.callback_query(F.data == "model_info")
async def msg_model_info(callback: CallbackQuery):
    await callback.answer(cache_time=1)
    await callback.message.answer(MODEL_INFO, parse_mode=ParseMode.MARKDOWN_V2)


@router.callback_query(F.data == "insert_link")
async def msg_insert_link(callback: CallbackQuery):
    pass


@router.message(F.text.contains("https"))
async def make_prediction_link(msg: Message):
    pass


@router.callback_query(F.data == "insert_text")
async def msg_insert_text(callback: CallbackQuery):
    pass


@router.message(F.text.contains("/text"))
async def make_prediction_text(msg: Message):
    pass
