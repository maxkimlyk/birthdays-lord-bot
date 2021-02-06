import datetime
import logging
from typing import Iterable, Set, List, Tuple

import aiogram  # type: ignore

from bot import context, views, types, birthdays_table, utils

MonthDay = Tuple[int, int]

_DAILY_BIRTHDAY_NOTIFICATION = 'daily_birthday_notification'


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


def _build_birthday_show_parameters(
        birthdays: List[types.Birthday], year_now: int,
) -> List[views.notify.BirthdayShowParams]:
    def transform(birthday):
        age: Optional[int] = None
        if birthday.date.first_year:
            age = year_now - birthday.date.first_year
        return views.notify.BirthdayShowParams(birthday, age)

    return [transform(bd) for bd in birthdays]


async def _notify_about_birthdays_today(
        ctx: context.Context,
        now: datetime.datetime,
        birthdays: Iterable[types.Birthday],
):
    birthdays_to_notify = select_birthdays_today(now, birthdays)

    logging.info('Birthdays to notify: %s', birthdays_to_notify)

    message = views.notify.build_birthdays_today_notification(
        _build_birthday_show_parameters(birthdays_to_notify, now.year),
    )
    await ctx.bot_wrapper.notify(message)


def _get_data_from_google_table(
        ctx: context.Context,
) -> Tuple[List[types.Birthday], List[birthdays_table.ParseError]]:
    try:
        raw_data = ctx.google_sheets_client.get_data(
            ranges=[ctx.config['google_sheets_sheet_name']],
        )
    except BaseException as e:
        logging.exception('Got exception during checking google table')
        raise
    return birthdays_table.parse(raw_data)


async def handle_birthdays_today(
        ctx: context.Context, message: aiogram.types.Message,
):
    birthdays, errors = _get_data_from_google_table(ctx)
    now = utils.now_local()
    await _notify_about_birthdays_today(ctx, now, birthdays)


def _should_notify(
        ctx: context.Context,
        now: datetime.datetime,
        notification_time: datetime.time,
        notification_id: str,
) -> bool:
    last_notified = ctx.db.get_last_notified(notification_id)

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


async def do_periodic_stuff(ctx: context.Context):
    now = utils.now_local()
    birthdays, errors = _get_data_from_google_table(ctx)

    if errors != []:
        # TODO: notify about errors
        pass

    notification_time = utils.parse_daytime(ctx.config['notification_time'])
    if _should_notify(
            ctx,
            now,
            notification_time,
            _DAILY_BIRTHDAY_NOTIFICATION,
    ):
        await _notify_about_birthdays_today(ctx, now, birthdays)
        ctx.db.set_last_notified(_DAILY_BIRTHDAY_NOTIFICATION, now)
