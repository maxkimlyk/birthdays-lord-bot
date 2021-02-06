import datetime

import pytest
from bot.dialogs import birthday_notify
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
            [
                types.Birthday(types.AnnualDate(29, 2), 'Leapman'),
            ],
            [],
        ),
        (
            datetime.datetime(2021, 2, 28),
            [
                types.Birthday(types.AnnualDate(29, 2), 'Leapman'),
            ],
            [
                types.Birthday(types.AnnualDate(29, 2), 'Leapman'),
            ],
        ),
    ],
)
def test_select_birthdays_today(now, birthdays, expected):
    assert birthday_notify.select_birthdays_today(now, birthdays) == expected


@pytest.mark.parametrize(
    'now,birthdays_data,expected',
    [
        (
            datetime.datetime(2020, 2, 1),
            [
                ['John', '1.03'],
                ['Kate', '01.2'],
                ['Amy', '01.02.1990'],
            ],
            (
                'Сегодня дни рождения у\n'
                '<b>Kate</b> \n'
                '<b>Amy</b> (30 лет)'
            )
        ),
    ],
)
@pytest.mark.asyncio
async def test_handle_birthdays_today(mock_context, mock_time, now, birthdays_data, expected):
    mock_time.set_local(now)
    mock_context.google_sheets_client.data = birthdays_data
    await birthday_notify.handle_birthdays_today(mock_context, "/today")
    assert mock_context.bot.last_message.text == expected
