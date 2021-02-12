import aiogram  # type: ignore

from . import types


class BotWrapper:
    def __init__(self, bot: aiogram.Bot):
        self._bot = bot

    async def send(self, chat_id: int, resp: types.Response):
        if resp.photo_bytes:
            await self._bot.send_photo(
                chat_id, resp.photo_bytes, resp.text, resp.parse_mode,
            )
        else:
            await self._bot.send_message(chat_id, resp.text, resp.parse_mode)

    async def reply(
            self, message: aiogram.types.Message, resp: types.Response,
    ):
        await self.send(message.chat.id, resp)
