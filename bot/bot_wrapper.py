import aiogram # type: ignore

from . import types


class BotWrapper:
    def __init__(self, bot: aiogram.Bot):
        self._bot = bot

    async def reply(self, message: aiogram.types.Message, resp: types.Response):
        await self._bot.send_message(message.chat.id, resp.text, resp.parse_mode)
