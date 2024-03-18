import requests
from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from config_reader import config
from handlers.model.bot_model_buttons import model_btns
from utils.text_messages import (
    ERROR_MSG_PAGE_NOT_LOADED,
    INSERT_LINK_MSG,
    INSERT_TEXT_MSG,
    MODEL_INFO,
    PREDICTION_LEVEL_1,
    PREDICTION_LEVEL_3,
)
from utils.verification_dict import WEBSITES_XPATHS

router = Router()

# Host and port of API (model)
api_host = config.api_host.get_secret_value()
api_port = config.api_port.get_secret_value()


class ModelInference(StatesGroup):
    """
    Class for the state of model inference.
    """

    pass_link = State()
    pass_text = State()


@router.callback_query(F.data == "make_prediction")
async def msg_model(callback: CallbackQuery) -> None:
    """
    Send message for the user about the model prediction and display model's buttons.

    :param callback: warning
    :type callback: CallbackQuery
    """
    if callback.message:
        await callback.answer(cache_time=1)
        await callback.message.answer(
            "What would you like to do with the model?",
            reply_markup=model_btns(),
        )


@router.callback_query(F.data == "model_info")
async def msg_model_info(callback: CallbackQuery) -> None:
    """
    Display information about the model.

    :param callback: display model info
    :type callback: CallbackQuery
    """
    if callback.message:
        await callback.answer(cache_time=1)
        await callback.message.answer(MODEL_INFO, parse_mode=ParseMode.MARKDOWN_V2)


@router.callback_query(F.data == "insert_link")
async def msg_insert_link(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Ask to insert the link. Changes state to pass_link.

    :param callback: asks to insert the link
    :type callback: CallbackQuery
    :param state: state of operation, changes to pass_link
    :type state: FSMContext
    """
    if callback.message:
        await callback.answer(cache_time=1)
        await callback.message.answer(
            INSERT_LINK_MSG.format(websites=[*WEBSITES_XPATHS.keys()]),
            parse_mode=ParseMode.HTML,
        )
        await state.set_state(ModelInference.pass_link)


@router.message(ModelInference.pass_link)
async def make_prediction_link(msg: Message, state: FSMContext) -> None:
    """
    Parse news' webpage. Return the model prediction.

    :param msg: result of model's prediction
    :type msg: Message
    :param state: state of operation, clears in the end
    :type state: FSMContext
    """
    if msg.text:
        # Get prediction by text
        endpoint = f"http://{api_host}:{api_port}/model/predict_by_link?url={msg.text}"
        prediction = requests.post(endpoint).json()["0"]

        if len(prediction) == 5:
            result = PREDICTION_LEVEL_3.format(
                comp_share_price_label=prediction["Company"],
                ind_index_label=prediction["Industry"],
                moex_index_label=prediction["Global_moex"],
                rvi_index_label=prediction["Global_rvi"],
                rubusd_index_label=prediction["Global_rubusd"],
            )
        elif len(prediction) == 3:
            result = PREDICTION_LEVEL_1.format(
                moex_index_label=prediction["Global_moex"],
                rvi_index_label=prediction["Global_rvi"],
                rubusd_index_label=prediction["Global_rubusd"],
            )
        else:
            result = ERROR_MSG_PAGE_NOT_LOADED

        await msg.answer(
            result,
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await state.clear()


@router.callback_query(F.data == "insert_text")
async def msg_insert_text(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Ask to insert the text. Changes state to pass_text.

    :param callback: asks to insert the text
    :type callback: CallbackQuery
    :param state: state of operation, changes to pass_text
    :type state: FSMContext
    """
    if callback.message:
        await callback.answer(cache_time=1)
        await callback.message.answer(
            INSERT_TEXT_MSG,
            parse_mode=ParseMode.HTML,
        )
        await state.set_state(ModelInference.pass_text)


@router.message(ModelInference.pass_text)
async def make_prediction_text(msg: Message, state: FSMContext) -> None:
    """
    Return the model prediction.

    :param msg: result of model's prediction
    :type msg: Message
    :param state: state of operation, clears in the end
    :type state: FSMContext
    """
    if msg.text:
        # Get prediction by text
        endpoint = (
            f"http://{api_host}:{api_port}/model/"
            f"predict_by_text?text={msg.text.lower()}"
        )
        prediction = requests.post(endpoint).json()["0"]

        if len(prediction) == 5:
            result = PREDICTION_LEVEL_3.format(
                comp_share_price_label=prediction["Company"],
                ind_index_label=prediction["Industry"],
                moex_index_label=prediction["Global_moex"],
                rvi_index_label=prediction["Global_rvi"],
                rubusd_index_label=prediction["Global_rubusd"],
            )
        else:
            result = PREDICTION_LEVEL_1.format(
                moex_index_label=prediction["Global_moex"],
                rvi_index_label=prediction["Global_rvi"],
                rubusd_index_label=prediction["Global_rubusd"],
            )

        await msg.answer(
            result,
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await state.clear()
