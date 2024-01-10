from aiogram import Router, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
)

from utils.database import add_feedback_to_db
from utils.verification_dict import available_scores

router = Router()


class Feedback(StatesGroup):
    """
    Class for state changes and also container for data.
    """

    scoring = State()
    giving_feedback = State()


def get_review_score() -> ReplyKeyboardMarkup:
    """Creates keyboard with digits for user review.

    :rtype: ReplyKeyboardMarkup
    :return: kb.as_markup: keyboard
    """
    kb = ReplyKeyboardBuilder()
    for i in range(1, 6):
        kb.add(KeyboardButton(text=str(i)))
    kb.adjust(5)
    return kb.as_markup(resize_keyboard=True)


@router.callback_query(F.data == "leave_feedback")
async def write_review(callback: CallbackQuery, state: FSMContext):
    """Offers user to select digital score.

    :param callback: offer to select digit
    :type callback: CallbackQuery
    :param state: current state of operation, changes to scoring
    :type state: FSMContext"""

    await callback.answer(cache_time=1)
    await callback.message.answer(
        "Please select one of the digits from the list below:",
        reply_markup=get_review_score(),
    )
    await state.set_state(Feedback.scoring)


@router.message(Feedback.scoring, F.text.in_(available_scores))
async def feed_score(message: Message, state: FSMContext):
    """Recieves score. Thanks for score. Changes status to giving feedback.

    :param messsage: thanks for score
    :type message: Message
    :param state: current state of operation, changes to giving feedback
    :type state: FSMContext"""
    await state.update_data(chosen_score=message.text.lower())
    await message.answer(
        text="Thank you for your assessment. Please also leave a review.",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(Feedback.giving_feedback)


@router.message(Feedback.scoring)
async def incorrect_score(message: Message):
    """Warnes user of incorrect score.

    :param message: warning
    :type message: Message
    """
    await message.answer(
        text="Incorrect rating.\n\n"
        "Please select one of the digits from the list below:",
        reply_markup=get_review_score(),
    )


@router.message(Feedback.giving_feedback, F.text.lower().len() <= 1000)
async def recieve_feedback(message: Message, state: FSMContext):
    """Takes feedback and thanks for it. Clears state of operation.

    :param message: thanks for feedback
    :type message: Message
    :param state: state of giving feedback, clears after sending data to database
    :type state: FSMContext
    """
    await state.update_data(given_feedback=message.text.lower())
    await message.answer(
        text="Thank you for your feedback, it is very valuable to us!\n\n"
        "P.S. If you have already given us a feedback earlier, only first feedback will be saved"
    )
    data = await state.get_data()
    await add_feedback_to_db(
        message.from_user.id, int(data["chosen_score"]), data["given_feedback"]
    )
    await state.clear()


@router.message(Feedback.giving_feedback)
async def incorrect_feedback(message: Message):
    """Gives user warning of too big input.

    :param message: message of warning
    :type message: Message
    """
    await message.answer(
        text="Your message is too big. Please try to limit yourself to 1000 characters."
    )
