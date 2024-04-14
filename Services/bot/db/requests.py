from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Reviews


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
    stmt = select(Reviews).where(Reviews.user_id == user_id)
    review = await session.scalar(stmt)
    if review is None:
        user_feedback = Reviews(user_id=user_id, score=score, feedback=feedback)
        session.add(user_feedback)
    else:
        review.score = score
        review.feedback = feedback
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
    average = "Average score: " + str(int(average_score)) + "\n\n"
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
async def try_connection(session: AsyncSession) -> int:
    """
    Check connection to DB
    :param session: SQLAlchemy session
    :type session: AsyncSession

    :rtype: int
    :return: returns 1 if session is connected
    """
    stmt = select(1)
    return await session.scalar(stmt)
