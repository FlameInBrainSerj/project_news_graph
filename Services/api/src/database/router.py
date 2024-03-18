import json

from database.db import get_async_session
from fastapi import APIRouter, Depends, Response
from fastapi_cache.decorator import cache
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

router = APIRouter(prefix="/db", tags=["Database"])


@router.get("/get_feedback", description="Get users' reviews as a JSON file")
@cache(expire=60)
async def get_users_feedback(
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    """
    Get users feedback collected in the Telegram Bot.

    :param session: async session to the database with users' reviews
    :type session: AsyncSession

    :rtype: Response
    :return json: .json file with users' reviews
    """
    try:
        result = await session.execute(text("SELECT * FROM reviews;"))
        reviews_json = json.dumps(
            [
                {"id": user_id, "rating": rating, "comment": comment}
                for user_id, rating, comment in result.fetchall()
            ],
        )
        return Response(content=reviews_json, media_type="application/json")

    except ProgrammingError:
        reviews_json = json.dumps([{0: "No reviews :("}])
        return Response(content=reviews_json, media_type="application/json")
