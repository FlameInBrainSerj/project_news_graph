from datetime import datetime

import pytest
from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.enums import ChatType
from aiogram.methods import AnswerCallbackQuery, SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import CallbackQuery, Chat, Message, Update, User
from tests.mocked_aiogram import MockedBot
from utils.text_messages import ABOUT_SERVICE, DISCLAIMER

user_id = 123456


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
    # Создание ответного сообщения от Telegram при ответе на колбэк
    bot.add_result_for(method=AnswerCallbackQuery, ok=True)

    bot.add_result_for(method=SendMessage, ok=True)

    # Отправка коллбэка с data = about_service
    update = await dp.feed_update(
        bot,
        Update(
            callback_query=make_incoming_callback("about_service", ABOUT_SERVICE),
            update_id=1,
        ),
    )

    # Проверка, что коллбэк обработан
    assert update is not UNHANDLED

    # Получение отправленного ботом коллбэка
    outgoing_callback: TelegramType = bot.get_request()
    # Получение сообщения от колбэка
    outgoing_message: TelegramType = bot.get_request()
    # Проверка содержимого: тип, текст, вид алерта
    assert isinstance(outgoing_callback, AnswerCallbackQuery)
    assert outgoing_message.text == ABOUT_SERVICE


@pytest.mark.asyncio
async def test_disclaimer_callback(dp: Dispatcher, bot: MockedBot) -> None:
    # Создание ответного сообщения от Telegram при ответе на колбэк
    bot.add_result_for(method=AnswerCallbackQuery, ok=True)

    bot.add_result_for(method=SendMessage, ok=True)

    # Отправка коллбэка с data = disclaimer
    update = await dp.feed_update(
        bot,
        Update(
            callback_query=make_incoming_callback("disclaimer", DISCLAIMER),
            update_id=1,
        ),
    )

    # Проверка, что коллбэк обработан
    assert update is not UNHANDLED

    # Получение отправленного ботом коллбэка
    outgoing_callback: TelegramType = bot.get_request()
    # Получение сообщения от колбэка
    outgoing_message: TelegramType = bot.get_request()

    # Проверка содержимого: тип, текст, вид алерта
    assert isinstance(outgoing_callback, AnswerCallbackQuery)
    assert outgoing_message.text == DISCLAIMER
