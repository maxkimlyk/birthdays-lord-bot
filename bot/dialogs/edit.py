import aiogram  # type: ignore

from bot import context, views
from . import decorators


@decorators.require_spreadsheet
async def handle_edit(ctx: context.Context, message: aiogram.types.Message):
    user_settings = ctx.settings.get_for_user(message.from_user.id)
    await ctx.bot_wrapper.reply(
        message, views.edit.build_response(user_settings['spreadsheet_id']),
    )
