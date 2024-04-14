import pytest
from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.fsm.context import FSMContext
from aiogram.methods import AnswerCallbackQuery, SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Update

from handlers.model.bot_model_main import ModelInference
from tests.mocked_aiogram import MockedBot
from utils.tests_help_functions import make_incoming_callback
from utils.text_messages import INSERT_LINK_MSG, INSERT_TEXT_MSG, MODEL_INFO
from utils.verification_dict import WEBSITES_XPATHS

user_id = 123456


@pytest.mark.asyncio
async def test_msg_model(dp: Dispatcher, bot: MockedBot) -> None:
    bot.add_result_for(method=AnswerCallbackQuery, ok=True)
    bot.add_result_for(method=SendMessage, ok=True)

    update = await dp.feed_update(
        bot,
        Update(
            callback_query=make_incoming_callback(
                user_id=user_id,
                callback_data="make_prediction",
                text="What would you like to do with the model?",
            ),
            update_id=1,
        ),
    )

    assert update is not UNHANDLED

    outgoing_callback: TelegramType = bot.get_request()
    assert isinstance(outgoing_callback, AnswerCallbackQuery)

    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == "What would you like to do with the model?"
    assert outgoing_message.reply_markup is not None

    markup = outgoing_message.reply_markup
    assert isinstance(markup, InlineKeyboardMarkup)
    button: InlineKeyboardButton
    button = markup.inline_keyboard[0][0]
    assert button.text == "More information about the model"
    assert button.callback_data == "model_info"
    button = markup.inline_keyboard[1][0]
    assert button.text == "Insert link of the news to make prediction"
    assert button.callback_data == "insert_link"
    button = markup.inline_keyboard[2][0]
    assert button.text == "Insert text of the news to make prediction"
    assert button.callback_data == "insert_text"


@pytest.mark.asyncio
async def test_msg_model_info(dp: Dispatcher, bot: MockedBot) -> None:
    bot.add_result_for(method=AnswerCallbackQuery, ok=True)
    bot.add_result_for(method=SendMessage, ok=True)

    update = await dp.feed_update(
        bot,
        Update(
            callback_query=make_incoming_callback(
                user_id=user_id,
                callback_data="model_info",
                text=MODEL_INFO,
            ),
            update_id=1,
        ),
    )

    assert update is not UNHANDLED

    outgoing_callback: TelegramType = bot.get_request()
    assert isinstance(outgoing_callback, AnswerCallbackQuery)

    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == MODEL_INFO


@pytest.mark.asyncio
async def test_msg_insert_link(dp: Dispatcher, bot: MockedBot) -> None:
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
            callback_query=make_incoming_callback(
                user_id=user_id,
                callback_data="insert_link",
                text=INSERT_LINK_MSG.format(websites=[*WEBSITES_XPATHS.keys()]),
            ),
            update_id=1,
        ),
    )

    assert update is not UNHANDLED

    outgoing_callback: TelegramType = bot.get_request()
    assert isinstance(outgoing_callback, AnswerCallbackQuery)

    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == INSERT_LINK_MSG.format(
        websites=[*WEBSITES_XPATHS.keys()],
    )

    current_state = await fsm_context.get_state()
    assert current_state == ModelInference.pass_link


@pytest.mark.asyncio
async def test_msg_insert_text(dp: Dispatcher, bot: MockedBot) -> None:
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
            callback_query=make_incoming_callback(
                user_id=user_id,
                callback_data="insert_text",
                text=INSERT_TEXT_MSG,
            ),
            update_id=1,
        ),
    )

    assert update is not UNHANDLED

    outgoing_callback: TelegramType = bot.get_request()
    assert isinstance(outgoing_callback, AnswerCallbackQuery)

    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == INSERT_TEXT_MSG

    current_state = await fsm_context.get_state()
    assert current_state == ModelInference.pass_text
