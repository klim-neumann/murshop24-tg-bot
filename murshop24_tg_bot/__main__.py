import aiogram
import murshop24_models as models  # type: ignore
from aiogram import enums as aiogram_enums
from aiogram.fsm.storage import redis as aiogram_redis
from aiogram.webhook import aiohttp_server
from aiohttp import web
from redis import asyncio as redis
from sqlalchemy.ext import asyncio as sqla_asyncio

from murshop24_tg_bot import _db, _handlers, _settings, _webhook
from murshop24_tg_bot._middlewares import tg_customer as customer_middlewares

_WEBHOOK_PATH = "/webhook/{bot_token}"


async def startup(async_engine: sqla_asyncio.AsyncEngine) -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


def _setup_middlewares(dp: aiogram.Dispatcher) -> None:
    tg_customer_middleware = customer_middlewares.TgCustomerMiddleware()
    dp.message.outer_middleware(middleware=tg_customer_middleware)
    dp.callback_query.outer_middleware(middleware=tg_customer_middleware)


def _main() -> None:
    redis_settings = _settings.RedisSettings()  # type: ignore
    tg_bot_settings = _settings.TgBotSettings()  # type: ignore
    async_engine = _db.create_async_engine()
    async_session = sqla_asyncio.async_sessionmaker(
        async_engine, expire_on_commit=False
    )
    redis_client = redis.Redis(
        host=redis_settings.host, port=redis_settings.port, decode_responses=True
    )
    storage = aiogram_redis.RedisStorage(redis_client)
    dp = aiogram.Dispatcher(
        storage=storage, async_engine=async_engine, async_session=async_session
    )
    dp.startup.register(startup)
    _setup_middlewares(dp)
    dp.include_router(_handlers.router)
    bot_settings = {"parse_mode": aiogram_enums.ParseMode.HTML}
    app = web.Application()
    _webhook.TokenBasedRequestHandler(
        dp, tg_bot_settings.secret_token, bot_settings=bot_settings
    ).register(app, path=_WEBHOOK_PATH)
    aiohttp_server.setup_application(app, dp)
    web.run_app(app)


if __name__ == "__main__":
    _main()
