import aiogram  # type: ignore

from bot import context, views


async def start(ctx: context.Context, message: aiogram.types.Message):
    response = views.start.build_response()
    await ctx.bot_wrapper.reply(message, response)

    await handle_guide_step1(ctx, message)


async def handle_guide_step1(ctx: context.Context, message: aiogram.types.Message):
    response = views.guide.build_guide_step1()
    await ctx.bot_wrapper.reply(message, response)
