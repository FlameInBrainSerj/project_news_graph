from typing import Sequence

from db.models import Reviews
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_by_id(session: AsyncSession, user_id: str) -> Reviews | None:
    """
    Получает пользователя по его айди.
    :param session: объект AsyncSession
    :param user_id: айди пользователя
    :return: объект RegisteredUser или None
    """
    stmt = select(Reviews).where(Reviews.user_id == user_id)
    return await session.scalar(stmt)


async def ensure_user(session: AsyncSession, user_id: str) -> bool:
    """
    Создаёт пользователя, если его раньше не было
    :param session: объект AsyncSession
    :param user_id: айди пользователя
    """
    existing_user = await get_user_by_id(session, user_id)
    if existing_user is not None:
        return True
    else:
        return False


async def add_feedback_to_db(
    session: AsyncSession,
    user_id: str,
    score: int,
    feedback: str,
) -> None:
    """
    Inserts user review to our database.
    :param session: SQLAlchemy session
    :type session: AsyncSession
    :param user_id: unique telegram user_id
    :type user_id: str
    :param score: user score of our app
    :type score: int
    :param feedback: user textual feedback on our app
    :type feedback: str
    """
    exist = await ensure_user(session, user_id)
    if exist:
        review = select(Reviews).where(Reviews.user_id == user_id)
        review = await session.scalar(review)
        review.score = score
        review.feedback = feedback
    else:
        user_feedback = Reviews(user_id=user_id, score=score, feedback=feedback)
        session.add(user_feedback)
    await session.commit()


async def read_feedback_from_db(session: AsyncSession) -> str:
    """
    Queries obtained feedback from database.
    Also calculates average score.

    :param session: SQLAlchemy session
    :type session: AsyncSession
    :rtype: str
    :return text: average and users' reviews
    """
    average_score = await session.scalar(select(func.avg(Reviews.score)))
    average = "Average score: " + str(average_score) + "\n\n"
    query_results: Sequence[Reviews] = (await session.scalars(select(Reviews))).all()
    text = "\n\n".join(
        [
            "user_id: {}\nscore: {}\nfeedback: {}\n".format(
                x.user_id,
                x.score,
                x.feedback,
            )
            for x in query_results
        ],
    )
    return average + str(text)


# Support function (can be unused)
async def test_connection(session: AsyncSession) -> int:
    """
    Check connection to DB
    :param session: SQLAlchemy session
    :type session: AsyncSession
    """
    stmt = select(1)
    return await session.scalar(stmt)
