from datetime import datetime

import pytest
from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.enums import ChatType
from aiogram.methods import AnswerCallbackQuery, SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import CallbackQuery, Chat, Message, Update, User
from aiogram.utils.markdown import hide_link


from utils.text_messages import MSG_DISPLAY_GRAPH
from tests.mocked_aiogram import MockedBot

user_id = 123456

CAT_LINK = "https://cataas.com/cat"


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


@pytest.mark.asyncio
async def test_about_service_callback(dp: Dispatcher, bot: MockedBot) -> None:
    bot.add_result_for(method=AnswerCallbackQuery, ok=True)
    bot.add_result_for(method=SendMessage, ok=True)
    update = await dp.feed_update(
        bot,
        Update(
            callback_query=make_incoming_callback(
                "display_graph", MSG_DISPLAY_GRAPH.format(link=hide_link(CAT_LINK)),
            ),
            update_id=1,
        ),
    )
    assert update is not UNHANDLED
    outgoing_callback: TelegramType = bot.get_request()
    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_callback, AnswerCallbackQuery)
    assert outgoing_message.text == MSG_DISPLAY_GRAPH.format(link=hide_link(CAT_LINK))