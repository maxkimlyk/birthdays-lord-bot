import asyncio
import logging
from typing import List

from . import context, dialogs

_PERIODIC_TASK_SLEEP_SECONDS = 60


async def periodic_main(ctx: context.Context):
    while True:
        try:
            await asyncio.sleep(_PERIODIC_TASK_SLEEP_SECONDS)
            await do_work(ctx)
        except BaseException:
            logging.exception("Periodic task failed")


async def do_work(ctx: context.Context):
    await dialogs.birthdays.do_periodic_stuff(ctx)
