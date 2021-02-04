from bot import context
from bot import types

import aiogram  # type: ignore


async def dev_get_data(ctx: context.Context, message: aiogram.types.Message):
    rows = ctx.google_sheets_client.get_data(ranges='birthdays')

    lines = [','.join(r) for r in rows]
    text = '\n'.join(lines)

    await ctx.bot_wrapper.reply(message, types.Response(text))
