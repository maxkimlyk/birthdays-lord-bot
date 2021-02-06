import argparse
import logging
import os

import aiogram  # type: ignore

from . import context
from . import dialogs
from . import periodic


def _parse_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('-c', '--config', type=str,
                       default='config.yaml', help='Path to config file')
    parse.add_argument('-l', '--logfile', type=str,
                       default=None, help='Path to log file')
    args = parse.parse_args()
    return args


def main():
    args = _parse_args()

    logging.basicConfig(
        filename=args.logfile,
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    ctx = context.Context(args.config, os.environ)
    dialogs.register_handlers(ctx)

    ctx.aio_loop.create_task(periodic.periodic_main(ctx))
    aiogram.executor.start_polling(ctx.dp, skip_updates=True)
