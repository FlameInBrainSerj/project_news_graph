import asyncio
from asyncio import WindowsSelectorEventLoopPolicy
from datetime import datetime
from typing import Optional, Sequence

import pytest
from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.enums import ChatType
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
from db.models import Reviews
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from tests.mocked_aiogram import MockedBot

asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())


def make_message(user_id: int, text: str) -> Message:
    user = User(id=user_id, first_name="User", is_bot=False)
    chat = Chat(id=user_id, type=ChatType.PRIVATE)
    return Message(
        message_id=1,
        from_user=user,
        chat=chat,
        date=datetime.now(),
        text=text,
    )


def make_incoming_callback(
    user_id: int,
    callback_data: str,
    text: Optional[str],
) -> CallbackQuery:
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


@pytest.mark.asyncio
async def test_show_feedback(dp: Dispatcher, bot: MockedBot) -> None:
    user_id = 123456

    bot.add_result_for(method=AnswerCallbackQuery, ok=True)
    bot.add_result_for(method=SendMessage, ok=True)
    update = await dp.feed_update(
        bot,
        Update(
            callback_query=make_incoming_callback(user_id, "show_feedback", text=None),
            update_id=1,
        ),
    )
    assert update is not UNHANDLED
    outgoing_callback: TelegramType = bot.get_request()
    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_callback, AnswerCallbackQuery)
    assert isinstance(outgoing_message, SendMessage)
    markup = outgoing_message.reply_markup
    assert isinstance(markup, ReplyKeyboardRemove)
    assert outgoing_message.text.startswith("Average score: ")
    assert outgoing_message.text.endswith("\n")
