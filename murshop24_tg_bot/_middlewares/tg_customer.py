from typing import Any, Awaitable, Callable, Coroutine

import aiogram
import murshop24_models as models  # type: ignore
import sqlalchemy as sqla
from aiogram import types
from sqlalchemy.ext import asyncio as sqla_asyncio


async def select_tg_customer(
    session: sqla_asyncio.AsyncSession, user: types.User
) -> models.TgCustomer | None:
    stmt = sqla.select(models.TgCustomer).where(
        models.TgCustomer.tg_id == user.id
    )
    return await session.scalar(stmt)


async def insert_tg_customer(
    session: sqla_asyncio.AsyncSession, user: types.User
) -> None:
    stmt = (
        sqla.insert(models.TgCustomer)
        .values(
            {
                "tg_id": user.id,
                "tg_first_name": user.first_name,
                "tg_last_name": user.last_name,
                "tg_username": user.username,
            }
        )
    )
    await session.execute(stmt)


async def update_tg_customer(
    session: sqla_asyncio.AsyncSession, user: types.User
) -> None:
    stmt = (
        sqla.update(models.TgCustomer)
        .where(models.TgCustomer.tg_id == user.id)
        .values(
            {
                "tg_first_name": user.first_name,
                "tg_last_name": user.last_name,
                "tg_username": user.username,
            }
        )
    )
    await session.execute(stmt)


class TgCustomerMiddleware(aiogram.BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: types.Message | types.CallbackQuery,  # type: ignore
        data: dict[str, Any],
    ) -> Coroutine[Any, Any, Any]:
        user = event.from_user
        if user is None:
            return await handler(event, data)
        async_session: sqla_asyncio.async_sessionmaker[
            sqla_asyncio.AsyncSession
        ] = data["async_session"]
        async with async_session() as session:
            tg_customer = await select_tg_customer(session, user)
            if tg_customer is None:
                await insert_tg_customer(session, user)
            else:
                await update_tg_customer(session, user)
            await session.commit()
        return await handler(event, data)
