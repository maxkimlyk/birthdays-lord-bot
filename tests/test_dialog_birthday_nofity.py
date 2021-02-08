import datetime

import pytest
from bot.dialogs import birthdays as dialogs_birthdays
from bot import types

from .test_common import *


@pytest.mark.parametrize(
    'now,birthdays,expected',
    [
        (
            datetime.datetime(2020, 2, 1),
            [
                types.Birthday(types.AnnualDate(1, 3), 'John'),
                types.Birthday(types.AnnualDate(1, 2), 'Kate'),
                types.Birthday(types.AnnualDate(1, 2, 1990), 'Amy'),
            ],
            [
                types.Birthday(types.AnnualDate(1, 2), 'Kate'),
                types.Birthday(types.AnnualDate(1, 2, 1990), 'Amy'),
            ],
        ),
        (
            datetime.datetime(2020, 2, 28),
            [types.Birthday(types.AnnualDate(29, 2), 'Leapman')],
            [],
        ),
        (
            datetime.datetime(2021, 2, 28),
            [types.Birthday(types.AnnualDate(29, 2), 'Leapman')],
            [types.Birthday(types.AnnualDate(29, 2), 'Leapman')],
        ),
    ],
)
def test_select_birthdays_today(now, birthdays, expected):
    assert dialogs_birthdays.select_birthdays_today(now, birthdays) == expected


@pytest.mark.parametrize(
    'birthdays',
    [
        [
            types.Birthday(types.AnnualDate(8, 2), 'John'),
            types.Birthday(types.AnnualDate(10, 2, 1990), 'Amy'),
            types.Birthday(types.AnnualDate(10, 2), 'Kate'),
            types.Birthday(types.AnnualDate(14, 2), 'John'),
            types.Birthday(types.AnnualDate(16, 2, 2000), 'Dick'),
            types.Birthday(types.AnnualDate(17, 2), 'Peter'),
            types.Birthday(types.AnnualDate(15, 3), 'Jane'),
        ],
    ],
)
@pytest.mark.parametrize(
    'now,expected',
    [
        (
            datetime.datetime(2020, 2, 3),  # monday
            [
                types.Birthday(types.AnnualDate(10, 2, 1990), 'Amy'),
                types.Birthday(types.AnnualDate(10, 2), 'Kate'),
                types.Birthday(types.AnnualDate(14, 2), 'John'),
                types.Birthday(types.AnnualDate(16, 2, 2000), 'Dick'),
            ],
        ),
        (
            datetime.datetime(2020, 2, 10),  # monday
            [types.Birthday(types.AnnualDate(17, 2), 'Peter')],
        ),
        (
            datetime.datetime(2020, 2, 16),  # monday
            [types.Birthday(types.AnnualDate(17, 2), 'Peter')],
        ),
        (datetime.datetime(2020, 2, 17), []),

    ],
)
def test_select_birthdays_next_week(now, birthdays, expected):
    assert dialogs_birthdays.select_birthdays_next_week(now, birthdays) == expected


@pytest.mark.parametrize(
    'now,birthdays_data,expected',
    [
        (
            datetime.datetime(2020, 2, 1),
            [['John', '1.03'], ['Kate', '01.2'], ['Amy', '01.02.1990']],
            (
                'Сегодня дни рождения у\n'
                '<b>Kate</b>\n'
                '<b>Amy</b> - 30 лет'
            ),
        ),
    ],
)
@pytest.mark.asyncio
async def test_handle_birthdays_today(
        mock_context, mock_time, now, birthdays_data, expected,
):
    mock_time.set_local(now)
    mock_context.google_sheets_client.data = birthdays_data
    await dialogs_birthdays.handle_birthdays_today(mock_context, '/today')
    assert mock_context.bot.last_message.text == expected


@pytest.mark.parametrize(
    'now,birthdays_data,expected',
    [
        (
            datetime.datetime(2020, 2, 5),
            [['John', '1.03'], ['Kate', '10.2'], ['Amy', '12.02.1990']],
            (
                'На следующей неделе дни рождения будут праздновать:\n'
                '<b>Kate</b> (пн, 10 февраля)\n'
                '<b>Amy</b> - 30 лет (ср, 12 февраля)'
            ),
        ),
    ],
)
@pytest.mark.asyncio
async def test_handle_birthdays_next_week(
        mock_context, mock_time, now, birthdays_data, expected,
):
    mock_time.set_local(now)
    mock_context.google_sheets_client.data = birthdays_data
    await dialogs_birthdays.handle_birthdays_next_week(mock_context, '/today')
    assert mock_context.bot.last_message.text == expected


@pytest.mark.parametrize(
    'birthdays_data',
    [[['John', '1.03'], ['Kate', '01.2'], ['Amy', '01.02.1990']]],
)
@pytest.mark.parametrize(
    'now,last_notification,notification_time,should_notify',
    [
        (
            datetime.datetime(2020, 2, 1, 6, 58),
            datetime.datetime(2020, 1, 31, 7, 1),
            '07:00',
            False,
        ),
        (
            datetime.datetime(2020, 2, 1, 7, 0),
            datetime.datetime(2020, 1, 31, 7, 1),
            '07:00',
            True,
        ),
        (
            datetime.datetime(2020, 2, 1, 12, 11),
            datetime.datetime(2020, 1, 1, 7, 0),
            '12:00',
            True,
        ),
    ],
)
@pytest.mark.asyncio
async def test_periodic_birthday_today_notification(
        mock_context,
        mock_time,
        now,
        birthdays_data,
        last_notification,
        notification_time,
        should_notify,
):
    mock_time.set_local(now)
    mock_context.google_sheets_client.data = birthdays_data
    mock_context.db.set_last_notified(
        dialogs_birthdays._TABLE_DATA_HASH_KEY, last_notification,
    )
    mock_context.config['notification_time'] = notification_time
    await dialogs_birthdays.do_periodic_stuff(mock_context)
    assert len(mock_context.bot.messages) == int(should_notify)


@pytest.mark.parametrize('birthdays_data', ([['John', '01 feb 202020']]))
@pytest.mark.asyncio
async def test_periodic_errors_notification(
        mock_context, mock_time, birthdays_data,
):
    mock_context.google_sheets_client.data = birthdays_data
    await dialogs_birthdays.do_periodic_stuff(mock_context)
    assert mock_context.bot.messages[0].text.startswith(
        'Обнаружены ошибки в таблице',
    )

