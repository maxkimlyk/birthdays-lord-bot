import pytest

from bot import birthdays_table, types


@pytest.mark.parametrize(
    'row,expected',
    [
        ([], None),
        (['    '], None),
        (['', '\t', '\n'], None),
        (
            ['   John Balls ', '29.02.1992'],
            types.Birthday(types.AnnualDate(29, 2, 1992), 'John Balls'),
        ),
        (
            ['John Balls  ', '15.11'],
            types.Birthday(types.AnnualDate(15, 11), 'John Balls'),
        ),
        (
            ['John', '1.01.1990'],
            types.Birthday(types.AnnualDate(1, 1, 1990), 'John'),
        ),
    ],
)
def test_parse_row(row, expected):
    assert birthdays_table.parse_row(row) == expected


_Reason = types.TableParseError.Reason

@pytest.mark.parametrize(
    'row,expected_error',
    [
        (['John', '1/01/1990'], birthdays_table.ParseError(_Reason.BAD_DATE_FORMAT)),
        (['John', '01.01.01.1990'], birthdays_table.ParseError(_Reason.BAD_DATE_FORMAT)),
        (['John', '000 1.01.1990'], birthdays_table.ParseError(_Reason.EXPECTED_INTEGER_VALUE)),
        (['John', '-1.01.1990'], birthdays_table.ParseError(_Reason.BAD_DAY_NUMBER)),
        (['John', '30.02.1990'], birthdays_table.ParseError(_Reason.BAD_DAY_NUMBER)),
        (['John', '55.12.1990'], birthdays_table.ParseError(_Reason.BAD_DAY_NUMBER)),
        (['John', '01.13.1990'], birthdays_table.ParseError(_Reason.BAD_MONTH_NUMBER)),
        (['John', '01.05.0000'], birthdays_table.ParseError(_Reason.BAD_YEAR_NUMBER)),
        (['  ', '01.05.1990'], birthdays_table.ParseError(_Reason.BAD_PERSON_NAME)),
    ],
)
def test_parse_row_error(row, expected_error):
    try:
        birthdays_table.parse_row(row)
    except birthdays_table.ParseError as e:
        assert e == expected_error
        return

    assert False, "Expected error"
