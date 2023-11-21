from typing import Any

import aiogram
from aiogram import filters, types
from sqlalchemy.ext import asyncio as sqla_asyncio

from murshop24_tg_bot._db import tg_bot as db


class TgBotFilter(filters.Filter):
    async def __call__(
        self,
        event: types.Message | types.CallbackQuery,
        bot: aiogram.Bot,
        async_session: sqla_asyncio.async_sessionmaker[sqla_asyncio.AsyncSession],
    ) -> Any:
        del event
        async with async_session() as session:
            return await db.tg_bot_exists(session, bot)
