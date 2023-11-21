import aiogram

from murshop24_tg_bot._handlers import faq, rules, start, tg_bot, catalog, order, error

router = aiogram.Router(name=__name__)
router.include_routers(
    error.router,
    tg_bot.router,
    start.router,
    catalog.router,
    order.router,
    rules.router,
    faq.router,
)
