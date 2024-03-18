import datetime

import pytz
import requests
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from utils.display_ticker_vars import COMPANIES_API_STRING, TICKERS
from utils.text_messages import (
    MSG_CHOOSE_TICKER,
    MSG_DISPLAY_TICKER,
    TICKER_DESCRIPTION,
)

router = Router()


class Tick(StatesGroup):
    """
    Class for the state of operation.
    """

    choosing_ticker = State()


async def get_ticket_data(ticker: str) -> str:
    """
    Requests last available hour candle of selected ticker.

    :param ticker: textual input for ticker to match tickers from one of the companies,
    present in Moscow Exchange Broad Market Index
    :type ticker: str

    :rtype (str), str
    :return text: formatted candlestick of last trade hour of selected ticker
    """
    date = (datetime.datetime.now(pytz.timezone("Europe/Moscow"))).date()
    text = (
        "Open: {}\nClose: {}\nHigh: {}\nLow: {}\nValue: {}"
        "\nVolume: {}\nBegin: {} (GMT+3)\nEnd: {} (GMT+3)"
    )
    while True:
        n = requests.get(COMPANIES_API_STRING.format(ticker, date)).json()
        try:
            data = n["candles"]["data"][-1]
            break
        except IndexError:
            date -= datetime.timedelta(days=1)
            continue
    return text.format(*data)


@router.callback_query(F.data == "display_ticker")
async def msg_get_ticket(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Asks user to select ticker. Changes status to ticker selection.

    :param callback: asks to select ticker
    :type callback: CallbackQuery
    :param state: state of operation, changes to choosing ticker
    :type state: FSMContext
    """
    if callback.message:
        await callback.answer(cache_time=1)
        await callback.message.answer(
            MSG_DISPLAY_TICKER,
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.set_state(Tick.choosing_ticker)


@router.message(Tick.choosing_ticker, F.text.upper().in_(TICKERS))
async def feed_score(msg: Message, state: FSMContext) -> None:
    """
    Messages request result. Clears status.

    :param msg: result of request
    :type msg: Message
    :param state: state of operation, container for data, clears in the end
    :type state: FSMContext
    """
    if msg.text:
        await state.update_data(chosen_ticker=msg.text.upper())
    ticker = await state.get_data()
    ticker = ticker["chosen_ticker"]

    data = await get_ticket_data(ticker)
    text = TICKER_DESCRIPTION + f"Ticker: {ticker}\n\n" + data

    await msg.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(Tick.choosing_ticker)
async def wrong_ticker(msg: Message) -> None:
    """
    Warns user of incorrect ticker.

    :param msg: warning
    :type msg: Message
    """
    await msg.answer(
        text=MSG_CHOOSE_TICKER,
    )
