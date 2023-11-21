import secrets
from typing import Any

import aiogram
from aiogram.webhook import aiohttp_server


class TokenBasedRequestHandler(aiohttp_server.TokenBasedRequestHandler):
    def __init__(
        self,
        dispatcher: aiogram.Dispatcher,
        secret_token: str,
        handle_in_background: bool = True,
        bot_settings: dict[str, Any] | None = None,
        **data: Any
    ) -> None:
        super().__init__(dispatcher, handle_in_background, bot_settings, **data)
        self._secret_token = secret_token

    def verify_secret(self, telegram_secret_token: str, bot: aiogram.Bot) -> bool:
        del bot
        return secrets.compare_digest(telegram_secret_token, self._secret_token)
