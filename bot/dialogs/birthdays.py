import datetime
import logging
from typing import Iterable, Set, List, Tuple, Optional

import aiogram  # type: ignore

from bot import context, views, types, birthdays_table, utils, exceptions

MonthDay = Tuple[int, int]

_DAILY_BIRTHDAY_NOTIFICATION = 'daily_birthday_notification'
_WEEKLY_NOTIFICATION = 'weekly_notification'
_TABLE_DATA_HASH_KEY = 'table_data_hash'


def _as_month_day(annual_date: types.AnnualDate) -> MonthDay:
    return (annual_date.month, annual_date.day)


def _filter_birthdays(
        birthdays: Iterable[types.Birthday], wished_month_days: Set[MonthDay],
):
    result = []
    for bd in birthdays:
        if _as_month_day(bd.date) in wished_month_days:
            result.append(bd)
    return result


def _get_same_time_monday_this_week(now: datetime.datetime):
    weekday_from0 = now.weekday()
    return now - datetime.timedelta(days=weekday_from0)


def select_birthdays_today(
        now: datetime.datetime, birthdays: Iterable[types.Birthday],
):
    day_tommorow = now + datetime.timedelta(days=1)
    today = (now.month, now.day)
    tomorrow = (day_tommorow.month, day_tommorow.day)

    wished_month_days = {today}
    if today == (2, 28) and tomorrow == (3, 1):
        # handle February 29 in not leap year
        wished_month_days.add((2, 29))

    return _filter_birthdays(birthdays, wished_month_days)


def select_birthdays_next_week(
        now: datetime.datetime, birthdays: Iterable[types.Birthday],
):
    monday_same_time = _get_same_time_monday_this_week(now)
    next_week_monday = monday_same_time + datetime.timedelta(days=7)

    wished_month_days = set()
    for i in range(7):
        time_point = next_week_monday + datetime.timedelta(days=i)
        wished_month_days.add((time_point.month, time_point.day))

    return _filter_birthdays(birthdays, wished_month_days)


def _build_birthday_show_parameters(
        birthdays: List[types.Birthday], year_now: int,
) -> List[views.notify.BirthdayShowParams]:
    def transform(birthday):
        age: Optional[int] = None
        if birthday.date.first_year:
            age = year_now - birthday.date.first_year
        weekday = datetime.date(
            year_now, birthday.date.month, birthday.date.day,
        ).weekday()
        return views.notify.BirthdayShowParams(birthday, age, weekday)

    return [transform(bd) for bd in birthdays]


async def _notify_about_birthdays_today(
        ctx: context.Context,
        now: datetime.datetime,
        birthdays_to_notify: List[types.Birthday],
):
    logging.info('Notifying about birthdays: %s', birthdays_to_notify)

    message = views.notify.build_birthdays_today_notification(
        _build_birthday_show_parameters(birthdays_to_notify, now.year),
    )
    await ctx.bot_wrapper.notify(message)


def _get_data_from_google_table(ctx: context.Context):
    try:
        raw_data = ctx.google_sheets_client.get_data(
            ranges=[ctx.config['google_sheets_sheet_name']],
        )
    except BaseException:
        logging.exception('Got exception during checking google table')
        raise
    return birthdays_table.parse(raw_data)


def _should_notify_about_today(
        ctx: context.Context,
        now: datetime.datetime,
        notification_time: datetime.time,
) -> bool:
    last_notified = ctx.db.get_last_notified(_DAILY_BIRTHDAY_NOTIFICATION)

    today_notification_time = datetime.datetime(
        now.year,
        now.month,
        now.day,
        notification_time.hour,
        notification_time.minute,
    )

    if (
            last_notified >= today_notification_time
            or now < today_notification_time
    ):
        return False

    return True


def _should_notify_about_errors(ctx: context.Context, new_hash: int):
    try:
        old_hash = ctx.db.get_cache_value(_TABLE_DATA_HASH_KEY)
    except exceptions.NoSuchData:
        logging.debug(
            'No saved table data hash in db, consider that data is new',
        )
        return True

    logging.debug(
        'Checking table data hash. Old: "%s" , new: "%s"', old_hash, new_hash,
    )
    return old_hash != str(new_hash)


async def notify_about_errors(
        ctx: context.Context,
        data_hash: int,
        errors: Iterable[types.TableParseError],
):
    if not _should_notify_about_errors(ctx, data_hash):
        logging.debug('Shouldn\'t notify about errors')
        return

    logging.info('Notifying about errors')
    await ctx.bot_wrapper.notify(
        views.notify.build_errors_notification(errors),
    )

    ctx.db.add_cache_value(_TABLE_DATA_HASH_KEY, str(data_hash))


def _should_notify_about_next_week(
        ctx: context.Context,
        now: datetime.datetime,
        notification_time: datetime.time,
):
    last_notified = ctx.db.get_last_notified(_WEEKLY_NOTIFICATION)

    monday_same_time = _get_same_time_monday_this_week(now)

    this_week_notification_time = datetime.datetime(
        monday_same_time.year,
        monday_same_time.month,
        monday_same_time.day,
        notification_time.hour,
        notification_time.minute,
    )

    logging.debug(
        'This week notification time: %s', this_week_notification_time,
    )

    if (
            last_notified >= this_week_notification_time
            or now < this_week_notification_time
    ):
        return False

    return True


async def _notify_about_birthdays_next_week(
        ctx: context.Context,
        now: datetime.datetime,
        birthdays_to_notify: List[types.Birthday],
):
    logging.info('Notifying weekly')

    message = views.notify.build_birthdays_weekly_notification(
        _build_birthday_show_parameters(birthdays_to_notify, now.year),
    )
    await ctx.bot_wrapper.notify(message)


async def do_periodic_stuff(ctx: context.Context):
    logging.debug('Start periodic stuff')

    now = utils.now_local()
    birthdays, errors, data_hash = _get_data_from_google_table(ctx)

    logging.debug('Birthdays: %s', birthdays)
    logging.debug('Errors: %s', errors)

    if errors != []:
        await notify_about_errors(ctx, data_hash, errors)

    notification_time = utils.parse_daytime(ctx.config['notification_time'])

    if _should_notify_about_next_week(ctx, now, notification_time):
        birthdays_to_notify = select_birthdays_next_week(now, birthdays)
        if birthdays_to_notify != []:
            await _notify_about_birthdays_next_week(ctx, now, birthdays_to_notify)
        ctx.db.set_last_notified(_WEEKLY_NOTIFICATION, now)

    if _should_notify_about_today(ctx, now, notification_time):
        birthdays_to_notify = select_birthdays_today(now, birthdays)
        if birthdays_to_notify != []:
            await _notify_about_birthdays_today(ctx, now, birthdays_to_notify)
        ctx.db.set_last_notified(_DAILY_BIRTHDAY_NOTIFICATION, now)


async def handle_birthdays_today(
        ctx: context.Context, _: aiogram.types.Message,
):
    birthdays, _, _ = _get_data_from_google_table(ctx)
    now = utils.now_local()
    birthdays_to_notify = select_birthdays_today(now, birthdays)
    await _notify_about_birthdays_today(ctx, now, birthdays_to_notify)


async def handle_birthdays_next_week(
        ctx: context.Context, _: aiogram.types.Message,
):
    birthdays, _, _ = _get_data_from_google_table(ctx)
    now = utils.now_local()
    birthdays_to_notify = select_birthdays_next_week(now, birthdays)
    await _notify_about_birthdays_next_week(ctx, now, birthdays_to_notify)
