import logging

from config import REDIS_HOST, REDIS_PORT
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from logging_setup import LoggerSetup
from models_functionality.router import router as models_router
from redis import asyncio as aioredis
from starlette_exporter import PrometheusMiddleware, handle_metrics

# Setup root logger
logger_setup = LoggerSetup()
main_logger = logging.getLogger(__name__)

app = FastAPI(title="API for DL model: predicting influence of news on asset")

# Prometheus stuff
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

# Router for models' inference
app.include_router(models_router)


@app.get("/ping")
async def ping() -> str:
    """
    Simple handler for health-check.

    :rtype: str
    :return text: HelloWorld-like text
    """
    main_logger.info("--- I was pinged ---")
    return "I am alive!"


@app.on_event("startup")
async def startup_event() -> None:
    """
    Initialize services required for the API on its startup.
    """
    main_logger.info("--- Start up App ---")

    # Initialize redis for caching stuff
    redis = aioredis.from_url(
        f"redis://{REDIS_HOST}:{REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """
    Some logging staff.
    """
    main_logger.info("--- Shut down App ---")
