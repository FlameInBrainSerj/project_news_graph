from datetime import datetime
from typing import Optional

from aiogram.enums import ChatType
from aiogram.types import CallbackQuery, Chat, Message, User


def make_incoming_message(user_id: int, text: str) -> Message:
    """
    Generates text message with specified text from user to bot
    :param user_id: id of the user
    :type user_id: int
    :param text: text to send to bot
    :type text: str

    :rtype: aiogram.types.Message
    :return: text message
    """
    return Message(
        message_id=1,
        chat=Chat(id=user_id, type=ChatType.PRIVATE),
        from_user=User(id=user_id, is_bot=False, first_name="User", last_name="User"),
        date=datetime.now(),
        text=text,
    )


def make_incoming_callback(
    user_id: int,
    callback_data: str,
    text: Optional[str],
) -> CallbackQuery:
    """
    Generates CallbackQuery which imitates pressing button
    And sending callback message to user
    :param user_id: id of the user
    :type user_id: int
    :param callback_data: text of callback button
    :type callback_data: str
    :param text: text to send to user
    :type text: Optional[str]

    :rtype: aiogram.types.CallbackQuery
    :return: callback imitating pressing button
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
