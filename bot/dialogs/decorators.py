import functools

import aiogram  # type: ignore

from bot import context, views


def require_spreadsheet(handler):
    @functools.wraps(handler)
    async def new_handler(
            ctx: context.Context,
            message: aiogram.types.Message,
            *args,
            **kwargs,
    ):
        user_settings = ctx.settings.get_for_user(message.from_user.id)
        if user_settings['spreadsheet_id'] is None:
            await ctx.bot_wrapper.reply(
                message, views.require_spreadhsheet.build_response(),
            )
            return
        return await handler(ctx, message, *args, **kwargs)

    return new_handler
