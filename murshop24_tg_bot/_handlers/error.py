import aiogram
from aiogram import filters, types
from aiogram.types import error_event

from murshop24_tg_bot import _errors
from murshop24_tg_bot._markups import error as markups

router = aiogram.Router(name=__name__)


@router.error(
    filters.ExceptionTypeFilter(_errors.TgBotError),
    aiogram.F.update.callback_query.as_("callback_query"),
    aiogram.F.update.callback_query.is_not(None),
)
async def cq_tg_bot_error(
    event: error_event.ErrorEvent, callback_query: types.CallbackQuery
) -> None:
    del event
    text = (
        "Ой, кажется, что-то пошло не так. 😕\n\n"
        "Попробуйте вернуться на главную! 🌟"
    )
    markup = markups.tg_bot_error()
    await callback_query.answer()
    assert callback_query.message is not None
    await callback_query.message.edit_text(text, reply_markup=markup)
