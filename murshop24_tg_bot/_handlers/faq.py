import aiogram
from aiogram import types

from murshop24_tg_bot import _consts
from murshop24_tg_bot._markups import faq as markups

router = aiogram.Router(name=__name__)


@router.callback_query(
    aiogram.F.data == _consts.CallbackData.FAQ, aiogram.F.message.is_not(None)
)
async def cq_rules(callback_query: types.CallbackQuery) -> None:
    text = (
        "<strong>Часто задаваемые вопросы:</strong>\n\n"
        "<strong>Как правильно оформить заказ?</strong>\n"
        "Настоятельно рекомендуем "
        "следовать следующей инструкции при оформлении заказа:\n\n"
        "1. Cохранить контакты оператора.\n"
        "2. Убедиться, что с вами можно связаться.\n"
        "3. Выбрать товар из каталога.\n"
        "4. Оплатить точную сумму по реквизитам.\n"
        "5. Дождаться уведомления от бота с полной информацией по кладу "
        "(оператор продублирует информацию в личные сообщения).\n\n"
        "<strong>Что делать в случае ненахода?</strong>\n"
        "В случае ненахода необходимо обратиться к оператору, "
        "предоставив фотографии с места ненахода "
        "в хорошем качестве с нескольких ракурсов.\n\n"
        "<strong>Возможен ли перезаклад?</strong>\n"
        "Да, перезаклад возможен при соблюдении всех правил "
        "на усмотрение администрации."
    )
    markup = markups.faq()
    await callback_query.answer()
    assert callback_query.message is not None
    await callback_query.message.edit_text(text, reply_markup=markup)
