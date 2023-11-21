import aiogram
import murshop24_models as models  # type: ignore
import sqlalchemy as sqla
from sqlalchemy import orm
from sqlalchemy.ext import asyncio as sqla_asyncio


async def select_tg_bot(
    session: sqla_asyncio.AsyncSession, bot: aiogram.Bot
) -> models.TgBot:
    stmt = (
        sqla.select(models.TgBot)
        .where(models.TgBot.tg_id == bot.id)
        .options(
            orm.selectinload(models.TgBot.tg_operator),
            orm.selectinload(models.TgBot.tg_reviews_channel)
        )
    )
    return await session.scalar(stmt)
