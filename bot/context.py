import asyncio
from typing import Dict

import aiogram  # type: ignore
import aiogram.contrib.fsm_storage.memory  # type: ignore

from . import authorizer
from . import db
from . import config


def _create_dispatcher(bot: aiogram.Bot):
    storage = aiogram.contrib.fsm_storage.memory.MemoryStorage()
    return aiogram.Dispatcher(bot, storage=storage)


class Context:
    def __init__(self, config_path: str, environ: Dict[str, str]):
        self.config = config.load_config(config_path, environ)
        self.authorizer = authorizer.Authorizer(self.config)
        self.db = db.Db(self.config['db_path'])
        self.aio_loop = asyncio.get_event_loop()
        self.bot = aiogram.Bot(
            token=self.config['telegram_api_token'], loop=self.aio_loop)
        self.dp = _create_dispatcher(self.bot)
