import logging

import aiogram  # type: ignore

from bot import context, views, google_sheets_client, exceptions
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
    await try_set_spreadsheet(ctx, message)


async def try_set_spreadsheet(
        ctx: context.Context, message: aiogram.types.Message,
) -> bool:
    spreadsheet_id = views.settings.parse_set_spreadsheet_step2_request(
        message.text,
    )
    if spreadsheet_id is None:
        await ctx.bot_wrapper.reply(
            message, views.settings.build_response_bad_spreadsheet_id(),
        )
        return False

    check_result = ctx.google_sheets_client.check_spreadsheet(spreadsheet_id)
    if check_result == google_sheets_client.SpreadsheetCheckResult.NO_ACCESS:
        await ctx.bot_wrapper.reply(
            message, views.settings.build_response_no_access_to_spreadsheet(),
        )
        return False
    if check_result == google_sheets_client.SpreadsheetCheckResult.NOT_FOUND:
        await ctx.bot_wrapper.reply(
            message, views.settings.build_response_spreadsheet_not_found(),
        )
        return False

    user_settings = ctx.settings.get_for_user(message.from_user.id)
    user_settings['spreadsheet_id'] = spreadsheet_id

    await ctx.bot_wrapper.reply(
        message,
        views.settings.build_response_spreadsheet_id_was_set_successfully(),
    )

    logging.info('Set spreadsheet: success')

    return True


async def handle_settings(
        ctx: context.Context, message: aiogram.types.Message,
):
    user_settings = ctx.settings.get_for_user(message.from_user.id)
    await ctx.bot_wrapper.reply(
        message, views.settings.build_response_current_settings(user_settings),
    )


async def handle_toggle_weekly_notifications(
        ctx: context.Context, message: aiogram.types.Message,
):
    user_settings = ctx.settings.get_for_user(message.from_user.id)
    user_settings['enable_weekly_notifications'] = not user_settings[
        'enable_weekly_notifications'
    ]
    await ctx.bot_wrapper.reply(
        message, views.settings.build_response_current_settings(user_settings),
    )


async def handle_set_notification_time(
        ctx: context.Context, message: aiogram.types.Message,
):
    await user_state.UserState.on_set_notification_time.set()
    await ctx.bot_wrapper.reply(
        message, views.settings.build_response_set_notification_time_step1(),
    )


async def handle_set_notification_time_step2(
        ctx: context.Context,
        message: aiogram.types.Message,
        state: aiogram.dispatcher.FSMContext,
):
    await state.finish()
    user_settings = ctx.settings.get_for_user(message.from_user.id)
    try:
        user_settings['notification_time'] = message.text
        await ctx.bot_wrapper.reply(
            message,
            views.settings.build_response_current_settings(user_settings),
        )
    except exceptions.CannotCast:
        logging.exception('Cannot cast')
        await ctx.bot_wrapper.reply(
            message, views.settings.build_response_bad_setting_value(),
        )
