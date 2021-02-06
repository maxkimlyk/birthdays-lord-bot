from typing import Mapping, Any

import aiogram  # type: ignore

from . import types


class BotWrapper:
    def __init__(self, bot: aiogram.Bot, config: Mapping[str, Any]):
        self._bot = bot
        self._user_id = config['telegram_user_id']

    async def send(self, user_id: int, resp: types.Response):
        await self._bot.send_message(user_id, resp.text, resp.parse_mode)

    async def reply(
            self, message: aiogram.types.Message, resp: types.Response,
    ):
        await self.send(message.chat.id, resp)

    async def notify(self, resp: types.Response):
        await self.send(self._user_id, resp)
