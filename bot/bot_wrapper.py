import collections.abc
import logging
from typing import Iterable, Union

import aiogram  # type: ignore

from . import types, share, exceptions

ResponseType = Union[types.Response, Iterable[types.Response]]


class BotWrapper:
    def __init__(self, bot: aiogram.Bot, share_: share.Share):
        self._bot = bot
        self._share = share_

    async def _send_one(self, chat_id: int, resp: types.Response):
        photo_bytes = None
        if resp.photo_path:
            try:
                photo_bytes = self._share.get_file(resp.photo_path)
            except exceptions.ResourceNotFound:
                logging.error(
                    'Resource not found: %s, falling back to plain text',
                    resp.photo_path,
                )

        if photo_bytes:
            await self._bot.send_photo(
                chat_id, photo_bytes, resp.text, resp.parse_mode,
            )
        else:
            await self._bot.send_message(chat_id, resp.text, resp.parse_mode)

    async def send(self, chat_id: int, response: ResponseType):
        if isinstance(response, collections.abc.Iterable):
            for msg in response:
                await self._send_one(chat_id, msg)
        else:
            await self._send_one(chat_id, response)

    async def reply(self, message: aiogram.types.Message, resp: ResponseType):
        await self.send(message.chat.id, resp)
