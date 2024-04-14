import pytest
from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.methods import AnswerCallbackQuery, SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import Update

from tests.mocked_aiogram import MockedBot
from utils.tests_help_functions import make_incoming_callback
from utils.text_messages import ABOUT_SERVICE, DISCLAIMER

user_id = 123456


@pytest.mark.asyncio
async def test_about_service_callback(dp: Dispatcher, bot: MockedBot) -> None:
    bot.add_result_for(method=AnswerCallbackQuery, ok=True)
    bot.add_result_for(method=SendMessage, ok=True)

    update = await dp.feed_update(
        bot,
        Update(
            callback_query=make_incoming_callback(
                user_id=user_id,
                callback_data="about_service",
                text=ABOUT_SERVICE,
            ),
            update_id=1,
        ),
    )

    assert update is not UNHANDLED

    outgoing_callback: TelegramType = bot.get_request()
    assert isinstance(outgoing_callback, AnswerCallbackQuery)

    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == ABOUT_SERVICE


@pytest.mark.asyncio
async def test_disclaimer_callback(dp: Dispatcher, bot: MockedBot) -> None:
    bot.add_result_for(method=AnswerCallbackQuery, ok=True)
    bot.add_result_for(method=SendMessage, ok=True)

    update = await dp.feed_update(
        bot,
        Update(
            callback_query=make_incoming_callback(
                user_id=user_id,
                callback_data="disclaimer",
                text=DISCLAIMER,
            ),
            update_id=1,
        ),
    )

    assert update is not UNHANDLED

    outgoing_callback: TelegramType = bot.get_request()
    assert isinstance(outgoing_callback, AnswerCallbackQuery)

    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == DISCLAIMER
