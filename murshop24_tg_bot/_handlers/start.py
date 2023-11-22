import aiogram
from aiogram import filters, types
from sqlalchemy.ext import asyncio as sqla_asyncio

from murshop24_tg_bot import _consts
from murshop24_tg_bot._markups import start as markups
from murshop24_tg_bot._db import start as db

router = aiogram.Router(name=__name__)


async def start(
    bot: aiogram.Bot,
    async_session: sqla_asyncio.async_sessionmaker[sqla_asyncio.AsyncSession],
) -> tuple[str, types.InlineKeyboardMarkup]:
    async with async_session() as session:
        tg_bot = await db.select_tg_bot(session, bot)
    text = "<strong>Murshop24</strong> - быстрые клады."
    markup = markups.start(
        tg_bot.tg_operator,
        tg_reviews_channel=tg_bot.tg_reviews_channel,
        tg_customer_group=tg_bot.tg_customer_group,
    )
    return text, markup


@router.message(filters.CommandStart())
async def cmd_start(
    message: types.Message,
    bot: aiogram.Bot,
    async_session: sqla_asyncio.async_sessionmaker[sqla_asyncio.AsyncSession],
) -> None:
    text, markup = await start(bot, async_session)
    await message.answer(text, reply_markup=markup)


@router.callback_query(
    aiogram.F.data == _consts.CallbackData.START, aiogram.F.message.is_not(None)
)
async def cq_start(
    callback_query: types.CallbackQuery,
    bot: aiogram.Bot,
    async_session: sqla_asyncio.async_sessionmaker[sqla_asyncio.AsyncSession],
) -> None:
    text, markup = await start(bot, async_session)
    await callback_query.answer()
    assert callback_query.message is not None
    await callback_query.message.edit_text(text, reply_markup=markup)
