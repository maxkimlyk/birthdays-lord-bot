import aiogram  # type: ignore

from bot import context, types, utils


async def get_data(ctx: context.Context, message: aiogram.types.Message):
    user_settings = ctx.settings.get_for_user(message.from_user.id)
    rows = ctx.google_sheets_client.get_data(
        user_settings['spreadsheet_id'], ranges=['birthdays'],
    )

    lines = [','.join(r) for r in rows]
    text = '\n'.join(lines)

    await ctx.bot_wrapper.reply(message, types.Response(text))


async def get_datetime(ctx: context.Context, message: aiogram.types.Message):
    text = utils.now_local().strftime('%Y-%m-%d %H:%M:%S')
    await ctx.bot_wrapper.reply(message, types.Response(text))
