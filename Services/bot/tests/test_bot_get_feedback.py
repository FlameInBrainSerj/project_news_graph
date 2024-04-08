import asyncio
import sys
from asyncio import WindowsSelectorEventLoopPolicy
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
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    Update,
    User,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Reviews
from tests.mocked_aiogram import MockedBot

user_id = 123456

# for Windows only
if "win" in sys.platform:
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())


class Feedback(StatesGroup):
    """
    Class for state changes and also container for data.
    """

    scoring = State()
    giving_feedback = State()


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
async def test_write_review(dp: Dispatcher, bot: MockedBot) -> None:

    # Получение контекста FSM для текущего юзера
    fsm_context: FSMContext = dp.fsm.get_context(
        bot=bot,
        user_id=user_id,
        chat_id=user_id,
    )
    await fsm_context.set_state(None)

    bot.add_result_for(method=AnswerCallbackQuery, ok=True)

    bot.add_result_for(method=SendMessage, ok=True)

    # Отправка коллбэка с data = about_service
    update = await dp.feed_update(
        bot,
        Update(
            callback_query=make_incoming_callback(
                "leave_feedback",
                "Please select one of the digits from the list below:",
            ),
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
    assert isinstance(outgoing_message, SendMessage)
    assert (
        outgoing_message.text == "Please select one of the digits from the list below:"
    )

    assert outgoing_message.reply_markup is not None
    markup = outgoing_message.reply_markup
    assert isinstance(markup, ReplyKeyboardMarkup)
    button: KeyboardButton
    for i in range(1, 6):
        button = markup.keyboard[0][i - 1]
        assert button.text == str(i)

    current_state = await fsm_context.get_state()
    assert current_state == Feedback.scoring


@pytest.mark.asyncio
@pytest.mark.parametrize("text_message", ["7", "0", "семь", "a", "-", "\\"])
async def test_incorrect_score(
    dp: Dispatcher, bot: MockedBot, text_message: str,
) -> None:
    fsm_context: FSMContext = dp.fsm.get_context(
        bot=bot,
        user_id=user_id,
        chat_id=user_id,
    )
    await fsm_context.set_state(Feedback.scoring)

    bot.add_result_for(method=SendMessage, ok=True)
    update = await dp.feed_update(
        bot,
        Update(message=make_incoming_message(text_message), update_id=1),
    )

    assert update is not UNHANDLED

    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    assert (
        outgoing_message.text
        == "Incorrect rating.\n\nPlease select one of the digits from the list below:"
    )

    assert outgoing_message.reply_markup is not None
    markup = outgoing_message.reply_markup
    assert isinstance(markup, ReplyKeyboardMarkup)
    button: KeyboardButton
    for i in range(1, 6):
        button = markup.keyboard[0][i - 1]
        assert button.text == str(i)
    current_state = await fsm_context.get_state()
    assert current_state == Feedback.scoring


@pytest.mark.asyncio
@pytest.mark.parametrize("text_message", ["1", "2", "3", "4", "5"])
async def test_feed_score(dp: Dispatcher, bot: MockedBot, text_message: str) -> None:
    fsm_context: FSMContext = dp.fsm.get_context(
        bot=bot,
        user_id=user_id,
        chat_id=user_id,
    )
    await fsm_context.set_state(Feedback.scoring)

    bot.add_result_for(method=SendMessage, ok=True)

    update = await dp.feed_update(
        bot,
        Update(message=make_incoming_message(text_message), update_id=1),
    )

    assert update is not UNHANDLED

    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    assert (
        outgoing_message.text
        == "Thank you for your assessment. Please also leave a review."
    )

    current_state = await fsm_context.get_state()
    assert current_state == Feedback.giving_feedback


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "text_message, score",
    [["А" * 1001, "5"]],
)
async def test_incorrect_feedback(
    dp: Dispatcher, bot: MockedBot, score: str, text_message: str,
) -> None:
    fsm_context: FSMContext = dp.fsm.get_context(
        bot=bot,
        user_id=user_id,
        chat_id=user_id,
    )
    await fsm_context.update_data(chosen_score=score)
    await fsm_context.set_state(Feedback.giving_feedback)
    bot.add_result_for(method=SendMessage, ok=True)
    update = await dp.feed_update(
        bot, Update(message=make_incoming_message(text_message), update_id=1),
    )
    assert update is not UNHANDLED
    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    text = (
        "Your message is too big. " "Please try to limit yourself to 1000 characters."
    )
    assert outgoing_message.text == text
    current_state = await fsm_context.get_state()
    assert current_state == Feedback.giving_feedback


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "text_message, score",
    [["Супер", "5"], [" ", "1"], ["03-285-159-5371", "2"], ["\\)(=+-_=+-_=+-_=", "5"]],
)
async def test_receive_feedback(
    dp: Dispatcher,
    bot: MockedBot,
    session: AsyncSession,
    score: str,
    text_message: str,
) -> None:
    fsm_context: FSMContext = dp.fsm.get_context(
        bot=bot,
        user_id=user_id,
        chat_id=user_id,
    )
    await fsm_context.update_data(chosen_score=score)
    await fsm_context.set_state(Feedback.giving_feedback)

    bot.add_result_for(method=SendMessage, ok=True)

    update = await dp.feed_update(
        bot,
        Update(message=make_incoming_message(text_message), update_id=1),
    )

    assert update is not UNHANDLED
    stmt = select(Reviews).where(Reviews.user_id == str(user_id))
    user_response = await session.scalar(stmt)
    assert user_response is not None
    assert user_response.user_id == str(user_id)
    assert user_response.score == int(score)
    assert user_response.feedback == text_message.lower()

    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    text = (
        "Thank you for your feedback, it is very valuable to us!"
        "P.S. If you have already given us a feedback "
        "earlier, only first feedback will be saved"
    )
    assert outgoing_message.text == text

    current_state = await fsm_context.get_state()
    assert current_state is None
