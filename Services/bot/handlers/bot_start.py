import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

logger = logging.getLogger(__name__)
router = Router()


def main_btns() -> InlineKeyboardMarkup:
    """
    Inline buttons for the bot start.

    :rtype: InlineKeyboardMarkup
    :return kb: keyboard markup
    """
    kb = InlineKeyboardBuilder()

    kb.row(
        InlineKeyboardButton(text="About the service", callback_data="about_service"),
    )
    kb.row(InlineKeyboardButton(text="Disclaimer", callback_data="disclaimer"))
    kb.row(
        InlineKeyboardButton(
            text="Make prediction of news' influence on financial instrument",
            callback_data="make_prediction",
        ),
    )
    kb.row(
        InlineKeyboardButton(
            text="Rate our app and leave the comment",
            callback_data="leave_feedback",
        ),
    )
    kb.row(
        InlineKeyboardButton(
            text="Show app ratings and comments",
            callback_data="show_feedback",
        ),
    )
    kb.row(
        InlineKeyboardButton(
            text="Display info about the ticker",
            callback_data="display_ticker",
        ),
    )
    kb.row(
        InlineKeyboardButton(
            text="Display graph of connections between financial entities",
            callback_data="display_graph",
        ),
    )

    return kb.as_markup()


@router.message(Command("start"))
async def cmd_start(msg: Message) -> None:
    """
    Greetings and display main buttons.

    :param msg: message of the greetings
    :type msg: Message
    """
    logger.info("The /start was triggered")

    if msg.from_user:
        await msg.answer(
            f"Hello, {msg.from_user.full_name}, let's start!",
            reply_markup=main_btns(),
        )
