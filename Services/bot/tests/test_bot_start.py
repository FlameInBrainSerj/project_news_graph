from datetime import datetime
import pytest
from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.enums import ChatType
from aiogram.methods import SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import (
    Chat,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    Update,
    User,
)
from tests.mocked_aiogram import MockedBot

user_id = 123456
callback_data = "about_service"


def make_incoming_message() -> Message:
    """
    Генерирует текстовое сообщение с командой /id от юзера к боту
    :return: объект Message с текстовой командой /id
    """
    return Message(
        message_id=1,
        chat=Chat(id=user_id, type=ChatType.PRIVATE),
        from_user=User(id=user_id, is_bot=False, first_name="User", last_name="User"),
        date=datetime.now(),
        text="/start",
    )


@pytest.mark.asyncio
async def test_start_command(dp: Dispatcher, bot: MockedBot) -> None:
    # Создание ответного сообщения от Telegram в ответ на команду /start
    bot.add_result_for(method=SendMessage, ok=True)

    # "Отправка" сообщения с командой /start
    message = make_incoming_message()
    update = await dp.feed_update(bot, Update(message=message, update_id=1))

    # Проверка, что сообщение обработано
    assert update is not UNHANDLED

    # Получение отправленного ботом сообщения
    outgoing_message: TelegramType = bot.get_request()
    # Проверка содержамого: тип, текст, наличие клавиатуры, что внутри клавиатуры
    assert isinstance(outgoing_message, SendMessage)
    assert isinstance(message.from_user, User)
    assert (
        outgoing_message.text == f"Hello, {message.from_user.full_name}, let's start!"
    )
    assert outgoing_message.reply_markup is not None
    markup = outgoing_message.reply_markup
    assert isinstance(markup, InlineKeyboardMarkup)
    button: InlineKeyboardButton
    button = markup.inline_keyboard[0][0]
    assert button.text == "About the service"
    assert button.callback_data == "about_service"
    button = markup.inline_keyboard[1][0]
    assert button.text == "Disclaimer"
    assert button.callback_data == "disclaimer"
    button = markup.inline_keyboard[2][0]
    assert button.text == "Make prediction of news' influence on financial instrument"
    assert button.callback_data == "make_prediction"
    button = markup.inline_keyboard[3][0]
    assert button.text == "Rate our app and leave the comment"
    assert button.callback_data == "leave_feedback"
    button = markup.inline_keyboard[4][0]
    assert button.text == "Show app ratings and comments"
    assert button.callback_data == "show_feedback"
    button = markup.inline_keyboard[5][0]
    assert button.text == "Display info about the ticker"
    assert button.callback_data == "display_ticker"
    button = markup.inline_keyboard[6][0]
    assert button.text == "Display graph of connections between financial entities"
    assert button.callback_data == "display_graph"
