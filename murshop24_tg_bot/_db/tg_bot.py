from collections.abc import Sequence

import aiogram
import murshop24_models as models  # type: ignore
import sqlalchemy as sqla
from sqlalchemy.ext import asyncio as sqla_asyncio


async def tg_bot_exists(session: sqla_asyncio.AsyncSession, bot: aiogram.Bot) -> bool:
    stmt = sqla.exists().where(models.TgBot.tg_id == bot.id).select()
    return await session.scalar(stmt)


async def select_tg_operators(
    session: sqla_asyncio.AsyncSession,
) -> Sequence[models.TgOperator]:
    stmt = sqla.select(models.TgOperator)
    return (await session.scalars(stmt)).all()
