import pytest
from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.fsm.context import FSMContext
from aiogram.methods import AnswerCallbackQuery, SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import ReplyKeyboardRemove, Update

from handlers.bot_display_ticker import Tick
from tests.mocked_aiogram import MockedBot
from utils.tests_help_functions import make_incoming_callback, make_incoming_message
from utils.text_messages import MSG_CHOOSE_TICKER, MSG_DISPLAY_TICKER

user_id = 123456


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
            callback_query=make_incoming_callback(
                user_id=user_id,
                callback_data="display_ticker",
                text=MSG_DISPLAY_TICKER,
            ),
            update_id=1,
        ),
    )

    assert update is not UNHANDLED

    outgoing_callback: TelegramType = bot.get_request()
    assert isinstance(outgoing_callback, AnswerCallbackQuery)

    outgoing_message: TelegramType = bot.get_request()
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
        Update(
            message=make_incoming_message(user_id=user_id, text=ticket.upper()),
            update_id=1,
        ),
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
        Update(
            message=make_incoming_message(user_id=user_id, text=ticket.upper()),
            update_id=1,
        ),
    )

    assert update is not UNHANDLED

    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == MSG_CHOOSE_TICKER
