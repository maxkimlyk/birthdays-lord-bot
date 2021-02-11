import aiogram  # type: ignore

from bot import context, views
from . import user_state


async def handle_set_spreadsheet_id(
        ctx: context.Context, message: aiogram.types.Message,
):
    response = views.settings.build_response_set_spreadsheet_id_step1()
    await user_state.UserState.on_set_spreadsheet_id.set()
    await ctx.bot_wrapper.reply(message, response)


async def handle_set_spreadsheet_id_step2(
        ctx: context.Context,
        message: aiogram.types.Message,
        state: aiogram.dispatcher.FSMContext,
):
    await state.finish()

    spreadsheet_id = views.settings.parse_set_spreadsheet_step2_request(
        message.text,
    )
    if spreadsheet_id is None:
        await ctx.bot_wrapper.reply(
            message, views.settings.build_response_bad_spreadsheet_id(),
        )
        return

    # try spreadsheet

    user_settings = ctx.settings.get_for_user(message.from_user.id)
    user_settings['spreadsheet_id'] = spreadsheet_id

    await ctx.bot_wrapper.reply(
        message,
        views.settings.build_response_spreadsheet_id_was_set_successfully(),
    )
