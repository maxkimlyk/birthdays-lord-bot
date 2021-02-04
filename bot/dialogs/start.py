from bot import context
from bot import views

import aiogram  # type: ignore


async def start(ctx: context.Context, message: aiogram.types.Message):
    response = views.start.build_response()
    await ctx.bot_wrapper.reply(message, response)
