import asyncio
import sys
from asyncio import WindowsSelectorEventLoopPolicy
from typing import Sequence

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Reviews
from db.requests import add_feedback_to_db, read_feedback_from_db, try_connection

# for Windows only
if "win" in sys.platform:
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())


@pytest.mark.asyncio
@pytest.mark.parametrize("user_id, score, feedback", [["123456", 5, "cool"]])
async def test_read_feedback_from_db(
    session: AsyncSession,
    user_id: str,
    score: int,
    feedback: str,
) -> None:
    await add_feedback_to_db(session, user_id, score, feedback)
    average_score = await session.scalar(select(func.avg(Reviews.score)))
    assert int(average_score) == score
    average = "Average score: " + str(int(average_score)) + "\n\n"
    assert average == f"Average score: {score}\n\n"
    query_results: Sequence[Reviews] = (await session.scalars(select(Reviews))).all()
    assert isinstance(query_results[0], Reviews)
    ret = await read_feedback_from_db(session)
    exp_text = (
        f"Average score: {score}\n\n"
        f"user_id: {user_id}\nscore: {score}\nfeedback: {feedback}\n"
    )
    assert ret == exp_text


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_id, score, feedback",
    [["123456", 5, "cool"], ["223456", 5, "cool"]],
)
async def test_add_feedback_to_db(
    session: AsyncSession,
    user_id: str,
    score: int,
    feedback: str,
) -> None:
    await add_feedback_to_db(session, "123456", 5, "cool")
    await add_feedback_to_db(session, user_id, score, feedback)
    review = select(Reviews).where(Reviews.user_id == user_id)
    review = await session.scalar(review)
    assert isinstance(review, Reviews)
    assert review.user_id == user_id
    assert review.score == score
    assert review.feedback == feedback


@pytest.mark.asyncio
async def test_try_connection(session: AsyncSession) -> None:
    res = await try_connection(session)
    assert res == 1
