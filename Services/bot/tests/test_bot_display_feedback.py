import asyncio
from asyncio import WindowsSelectorEventLoopPolicy

import pytest
from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.methods import AnswerCallbackQuery, SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import ReplyKeyboardRemove, Update
from sqlalchemy.ext.asyncio import AsyncSession

from db.requests import add_feedback_to_db
from tests.mocked_aiogram import MockedBot
from utils.tests_help_functions import make_incoming_callback

asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())


@pytest.mark.asyncio
async def test_show_feedback(
    dp: Dispatcher,
    bot: MockedBot,
    session: AsyncSession,
) -> None:
    user_id = 123456

    await add_feedback_to_db(session, str(user_id), 5, "cool")

    bot.add_result_for(method=AnswerCallbackQuery, ok=True)
    bot.add_result_for(method=SendMessage, ok=True)

    update = await dp.feed_update(
        bot,
        Update(
            callback_query=make_incoming_callback(
                user_id=user_id,
                callback_data="show_feedback",
                text=None,
            ),
            update_id=1,
        ),
    )

    assert update is not UNHANDLED

    outgoing_callback: TelegramType = bot.get_request()
    assert isinstance(outgoing_callback, AnswerCallbackQuery)

    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text.startswith("Average score: ")
    assert outgoing_message.text.endswith("\n")

    markup = outgoing_message.reply_markup
    assert isinstance(markup, ReplyKeyboardRemove)
