import datetime
import requests

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from utils.display_ticker_vars import COMPANIES_API_STRING, TICKERS
from utils.text_messages import TICKER_DESCRIPTION

router = Router()


class Tick(StatesGroup):
    """
    Class for state of operation.
    """

    choosing_ticker = State()


async def get_ticket_data(ticker: str) -> str:
    """Requests last available hour candle of selected ticker.

    :param ticker: textual input for ticker to match tickers from one of the companies, present in Moscow Exchange Broad Market Index
    :type ticker: str

    :rtype (str), str
    :return text: formated candlestick of last trade hour of selected ticker
    """
    date = datetime.datetime.today() - datetime.timedelta(days=1)

    n = requests.get(COMPANIES_API_STRING.format(ticker, date)).json()
    data = n["candles"]["data"][-1]
    text = "Open: {}\nClose: {}\nHigh: {}\nLow: {}\nValue: {}\nVolume: {}\nBegin: {}\nEnd: {}"
    return text.format(*data)


@router.callback_query(F.data == "display_ticker")
async def msg_get_ticket(callback: CallbackQuery, state: FSMContext):
    """Asks user to select ticker. Changes status to ticker selection.

    :param callback: asks to select ticker
    :type callback: CallbackQuery
    :param state: state of operation, changes to choosing ticker
    :type state: FSMContext
    """
    await callback.answer(cache_time=1)
    await callback.message.answer(
        "Please select the ticker of the company represented in the broad market index of the Moscow Stock Exchange",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(Tick.choosing_ticker)


@router.message(Tick.choosing_ticker, F.text.upper().in_(TICKERS))
async def feed_score(message: Message, state: FSMContext):
    """Messages request result. Clears status.

    :param message: result of request
    :type message: Message
    :param state: state of operation, container for data, clears in the end
    :type state: FSMContext
    """
    await state.update_data(chosen_ticker=message.text.upper())
    ticker = await state.get_data()
    ticker = ticker["chosen_ticker"]

    data = await get_ticket_data(ticker)
    text = TICKER_DESCRIPTION + f"Ticker: {ticker}\n\n" + data

    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(Tick.choosing_ticker)
async def wrong_ticker(message: Message):
    """Warns user of incorrect ticker.

    :param message: warning
    :type message: Message"""
    await message.answer(
        text="Wrong ticker!\n"
        "Please select the ticker of the company represented in the broad market index of the Moscow Stock Exchange"
    )
