import functools
import logging
from typing import Union

import aiogram  # type: ignore

from bot import context, views
from . import start, devmode, birthdays, settings, user_state


async def _not_authorized(
        ctx: context.Context,
        arg: Union[aiogram.types.Message, aiogram.types.CallbackQuery],
):
    logging.info(
        'Not authorized. id: %s, name: "%s"',
        arg.from_user.id,
        arg.from_user.full_name,
    )

    await ctx.bot_wrapper.send(
        arg.chat.id, views.not_authorized.build_response(arg.from_user.id),
    )


def _extract_chat_id(
        param: Union[aiogram.types.Message, aiogram.types.CallbackQuery],
) -> int:
    if hasattr(param, 'chat'):
        return param.chat.id
    return param.message.chat.id


def _extract_loggable_data(
        param: Union[aiogram.types.Message, aiogram.types.CallbackQuery],
) -> str:
    if hasattr(param, 'text'):
        return param.text
    if hasattr(param, 'data'):
        return 'CallbackQuery(\'{}\')'.format(param.data)
    return '(no data)'


def _verbose_handler(bot: aiogram.Bot):
    def decorator(func):
        async def _reply(arg, message):
            chat_id = _extract_chat_id(arg)
            await bot.send_message(chat_id, message)

        @functools.wraps(func)
        async def handle(
                arg: Union[aiogram.types.Message, aiogram.types.CallbackQuery],
                *args,
                **kwargs,
        ):
            logging.info('Handling %s', _extract_loggable_data(arg))
            try:
                return await func(arg, *args, **kwargs)
            except BaseException as e:
                msg = 'Something went wrong: {} {}'.format(repr(e), str(e))
                await _reply(arg, msg)
                raise

        return handle

    return decorator


def _only_for_authorized(ctx: context.Context):
    def decorator(func):
        @functools.wraps(func)
        async def handle(
                arg: Union[aiogram.types.Message, aiogram.types.CallbackQuery],
                *args,
                **kwargs,
        ):
            if not ctx.authorizer.is_authorized(arg.from_user.id):
                await _not_authorized(ctx, arg)
                return

            return await func(arg, *args, **kwargs)

        return handle

    return decorator


def register_handlers(ctx: context.Context):
    def wrap_f(handler):
        f = functools.partial(handler, ctx)
        f = _only_for_authorized(ctx)(f)
        return _verbose_handler(ctx.bot)(f)

    def register_handler(handler, *args, **kwargs):
        ctx.dp.register_message_handler(wrap_f(handler), *args, **kwargs)

    # def register_kb_callback(handler, *args, **kwargs):
    #     ctx.dp.register_callback_query_handler(
    #         wrap_f(handler), *args, **kwargs,
    #     )

    register_handler(start.start, commands=['start', 'help'])
    register_handler(birthdays.handle_birthdays_today, commands=['today'])
    register_handler(
        birthdays.handle_birthdays_next_week, commands=['next_week'],
    )

    register_handler(
        settings.handle_set_spreadsheet_id, commands=['set_spreadsheet'],
    )
    register_handler(
        settings.handle_set_spreadsheet_id_step2,
        state=user_state.UserState.on_set_spreadsheet_id,
    )

    register_handler(
        start.handle_guide_step2, state=user_state.UserState.on_guide_step2,
    )

    if 'devmode' in ctx.config and bool(ctx.config['devmode']):
        logging.info('DEVMODE enabled')
        register_handler(start.handle_guide_step1, commands=['guide'])
        register_handler(devmode.get_data, commands=['get_data'])
        register_handler(devmode.get_datetime, commands=['get_datetime'])
