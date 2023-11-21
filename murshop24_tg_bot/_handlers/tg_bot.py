import aiogram
from aiogram import types
from sqlalchemy.ext import asyncio as sqla_asyncio

from murshop24_tg_bot._filters import tg_bot as tg_bot_filters
from murshop24_tg_bot._markups import tg_bot as markups
from murshop24_tg_bot._db import tg_bot as db

router = aiogram.Router(name=__name__)


async def tg_bot_not_exists(
    async_session: sqla_asyncio.async_sessionmaker[sqla_asyncio.AsyncSession],
) -> tuple[str, types.InlineKeyboardMarkup]:
    async with async_session() as session:
        tg_operators = await db.select_tg_operators(session)
    use_tg_username = True
    text = (
        "🤖 Увы, в данный момент бот отключен.\n\n"
        "🌟 Но не расстраивайтесь, скоро он снова будет готов вам помочь!"
    )
    if len(tg_operators) == 1:
        use_tg_username = False
    elif len(tg_operators) > 1:
        text = f"{text}\n\n📞 Наши операторы:"
    markup = markups.tg_bot_not_exists(tg_operators, use_tg_username)
    return text, markup


@router.message(~tg_bot_filters.TgBotFilter())
async def msg_tg_bot_not_exists(
    message: types.Message,
    async_session: sqla_asyncio.async_sessionmaker[sqla_asyncio.AsyncSession],
) -> None:
    text, markup = await tg_bot_not_exists(async_session)
    await message.answer(text, reply_markup=markup)


@router.callback_query(~tg_bot_filters.TgBotFilter(), aiogram.F.message.is_not(None))
async def cq_tg_bot_not_exists(
    callback_query: types.CallbackQuery,
    async_session: sqla_asyncio.async_sessionmaker[sqla_asyncio.AsyncSession],
) -> None:
    text, markup = await tg_bot_not_exists(async_session)
    await callback_query.answer()
    assert callback_query.message is not None
    await callback_query.message.answer(text, reply_markup=markup)
