import pytest
from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.methods import SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Update, User

from tests.mocked_aiogram import MockedBot
from utils.tests_help_functions import make_incoming_message

user_id = 123456


@pytest.mark.asyncio
async def test_start_command(dp: Dispatcher, bot: MockedBot) -> None:
    bot.add_result_for(method=SendMessage, ok=True)

    message = make_incoming_message(user_id=user_id, text="/start")
    update = await dp.feed_update(bot, Update(message=message, update_id=1))

    assert update is not UNHANDLED

    outgoing_message: TelegramType = bot.get_request()
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
