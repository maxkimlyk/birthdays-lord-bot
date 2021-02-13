import aiogram  # type: ignore

from bot import context, views, db, exceptions
from . import settings, user_state


def _is_guide_passed(ctx: context.Context, user_id: int) -> bool:
    try:
        ctx.db.get_cache_value(db.CACHE_GUIDE_PASSED, user_id)
        return True
    except exceptions.NoSuchData:
        return False


async def start(ctx: context.Context, message: aiogram.types.Message):
    await ctx.bot_wrapper.reply(message, views.start.build_response())

    if not _is_guide_passed(ctx, message.from_user.id):
        await handle_guide_step1(ctx, message)
    else:
        await ctx.bot_wrapper.reply(
            message, views.command_list.build_command_list(),
        )


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

    ctx.db.add_cache_value(db.CACHE_GUIDE_PASSED, message.from_user.id, 'true')

    await state.finish()
    await ctx.bot_wrapper.reply(message, views.guide.build_guide_step2())
    await ctx.bot_wrapper.reply(
        message, views.command_list.build_command_list(),
    )
