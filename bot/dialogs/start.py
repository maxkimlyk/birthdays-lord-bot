import aiogram  # type: ignore

from bot import context, views
from . import settings, user_state


async def start(ctx: context.Context, message: aiogram.types.Message):
    await ctx.bot_wrapper.reply(message, views.start.build_response())

    # TODO: if guide is not passed
    await handle_guide_step1(ctx, message)


async def handle_guide_step1(
        ctx: context.Context, message: aiogram.types.Message,
):
    await user_state.UserState.on_guide_step2.set()
    await ctx.bot_wrapper.reply(message, views.guide.build_guide_step1())


async def handle_guide_step2(
        ctx: context.Context,
        message: aiogram.types.Message,
        state: aiogram.dispatcher.FSMContext,
):
    status = await settings.try_set_spreadsheet(ctx, message)
    if not status:
        return

    await state.finish()

    await ctx.bot_wrapper.reply(message, views.guide.build_guide_step2())
