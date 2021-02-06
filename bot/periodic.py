import asyncio
import logging
from typing import List

from . import context
from . import types

_PERIODIC_TASK_SLEEP_SECONDS = 60


async def periodic_main(ctx: context.Context):
    while True:
        try:
            await asyncio.sleep(_PERIODIC_TASK_SLEEP_SECONDS)
            await do_work(ctx)
        except BaseException:
            logging.exception("Periodic task failed")


async def do_work(ctx: context.Context):
    logging.info("do_work")
