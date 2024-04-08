from datetime import datetime

import pytest
from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.enums import ChatType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.methods import AnswerCallbackQuery, SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import (
    CallbackQuery,
    Chat,
    Message,
    ReplyKeyboardRemove,
    Update,
    User,
)

from tests.mocked_aiogram import MockedBot
from utils.display_ticker_vars import TICKERS
from utils.text_messages import MSG_CHOOSE_TICKER, MSG_DISPLAY_TICKER

user_id = 123456


class Tick(StatesGroup):
    """
    Class for the state of operation.
    """

    choosing_ticker = State()


def make_incoming_callback(callback_data: str, text: str) -> CallbackQuery:
    """
    Генерирует объект CallbackQuery,
    имитирующий результат нажатия юзером кнопки
    с callback_data "myid"
    :return: объект CallbackQuery
    """
    return CallbackQuery(
        id="1111111111111",
        chat_instance="22222222222222",
        from_user=User(id=user_id, is_bot=False, first_name="User"),
        data=callback_data,
        message=Message(
            message_id=1,
            chat=Chat(id=user_id, type=ChatType.PRIVATE),
            from_user=User(id=user_id, is_bot=False, first_name="User"),
            date=datetime.now(),
            text=text,
        ),
    )


def make_incoming_message(text: str) -> Message:
    """
    Generates text message with a given text from user to bot
    :return: объект Message с текстовой командой /id
    """
    return Message(
        message_id=1,
        chat=Chat(id=user_id, type=ChatType.PRIVATE),
        from_user=User(id=user_id, is_bot=False, first_name="User"),
        date=datetime.now(),
        text=text,
    )


@pytest.mark.asyncio
async def test_get_ticket(dp: Dispatcher, bot: MockedBot) -> None:
    fsm_context: FSMContext = dp.fsm.get_context(
        bot=bot,
        user_id=user_id,
        chat_id=user_id,
    )
    await fsm_context.set_state(None)

    bot.add_result_for(method=AnswerCallbackQuery, ok=True)
    bot.add_result_for(method=SendMessage, ok=True)

    update = await dp.feed_update(
        bot,
        Update(
            callback_query=make_incoming_callback("display_ticker", MSG_DISPLAY_TICKER),
            update_id=1,
        ),
    )
    assert update is not UNHANDLED
    # Получение отправленного ботом коллбэка
    outgoing_callback: TelegramType = bot.get_request()
    # Получение сообщения от колбэка
    outgoing_message: TelegramType = bot.get_request()

    # Проверка содержимого: тип, текст, вид алерта
    assert isinstance(outgoing_callback, AnswerCallbackQuery)
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == MSG_DISPLAY_TICKER
    assert outgoing_message.reply_markup is not None
    markup = outgoing_message.reply_markup
    assert isinstance(markup, ReplyKeyboardRemove)
    current_state = await fsm_context.get_state()
    assert current_state == Tick.choosing_ticker


@pytest.mark.asyncio
@pytest.mark.parametrize("ticket", ["SBER"])
async def test_feed_score(dp: Dispatcher, bot: MockedBot, ticket: str) -> None:
    fsm_context: FSMContext = dp.fsm.get_context(
        bot=bot,
        user_id=user_id,
        chat_id=user_id,
    )
    await fsm_context.set_state(Tick.choosing_ticker)
    bot.add_result_for(method=SendMessage, ok=True)

    update = await dp.feed_update(
        bot,
        Update(message=make_incoming_message(ticket.upper()), update_id=1),
    )
    assert update is not UNHANDLED
    await fsm_context.update_data(chosen_ticket=ticket)
    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    current_state = await fsm_context.get_state()
    assert current_state is None


@pytest.mark.asyncio
@pytest.mark.parametrize("ticket", ["BBBB", "AAAA", "abab"])
async def test_wrong_ticker(dp: Dispatcher, bot: MockedBot, ticket: str) -> None:
    fsm_context: FSMContext = dp.fsm.get_context(
        bot=bot,
        user_id=user_id,
        chat_id=user_id,
    )
    await fsm_context.set_state(Tick.choosing_ticker)

    bot.add_result_for(method=SendMessage, ok=True)

    update = await dp.feed_update(
        bot,
        Update(message=make_incoming_message(ticket.upper()), update_id=1),
    )
    assert update is not UNHANDLED
    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == MSG_CHOOSE_TICKER
