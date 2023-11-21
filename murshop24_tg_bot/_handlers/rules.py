import aiogram
from aiogram import types

from murshop24_tg_bot import _consts
from murshop24_tg_bot._markups import rules as markups

router = aiogram.Router(name=__name__)


@router.callback_query(
    aiogram.F.data == _consts.CallbackData.RULES, aiogram.F.message.is_not(None)
)
async def cq_rules(callback_query: types.CallbackQuery) -> None:
    text = (
        "Cовершая покупку в нашем магазине "
        "Вы автоматически соглашаетесь "
        "со всеми перечисленными условиями указанными ниже:\n\n"
        "1. Вежливо общаться с сотрудниками нашего магазина.\n\n"
        "2. В случае ненахода обратиться к оператору в течении 24ч, "
        "иначе проблема рассматриваться не будет.\n\n"
        "3. При оплате заказа, оплачивать строго точную сумму, "
        "которая указана в описании заказа.\n\n"
        "<strong>В случае несоболюдения условий, "
        "магазин в праве отказать от предоставления дальнейших услуг.</strong>"
    )
    markup = markups.rules()
    await callback_query.answer()
    assert callback_query.message is not None
    await callback_query.message.edit_text(text, reply_markup=markup)
