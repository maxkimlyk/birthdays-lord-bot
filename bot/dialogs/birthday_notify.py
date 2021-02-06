import datetime
import logging
from typing import Iterable, Set, List, Tuple

import aiogram  # type: ignore

from bot import context, views, types, birthdays_table, utils

MonthDay = Tuple[int, int]


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

    if birthdays_to_notify != []:
        logging.info('Birthdays to notify: %s', birthdays_to_notify)

        message = views.notify.build_birthdays_today_notification(
            _build_birthday_show_parameters(birthdays_to_notify, now.year),
        )
        await ctx.bot_wrapper.notify(message)


async def handle_birthdays_today(ctx: context.Context, message: aiogram.types.Message):
    try:
        raw_data = ctx.google_sheets_client.get_data(
            ranges=[ctx.config['google_sheets_sheet_name']],
        )
    except BaseException as e:
        logging.exception('Got exception during checking google table')
        return

    birthdays, errors = birthdays_table.parse(raw_data)
    now = utils.now_local()
    await _notify_about_birthdays_today(ctx, now, birthdays)


async def main_periodic(ctx: context.Context):
    pass
