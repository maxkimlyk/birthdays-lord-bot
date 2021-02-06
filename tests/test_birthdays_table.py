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


@pytest.mark.parametrize(
    'row,expected_error',
    [
        (['John Balls'], 'Unexpected row length. At least 2 cells expected'),
        (['John', '1/01/1990'], 'Unexpected date format'),
        (['John', '01.01.01.1990'], 'Unexpected date format'),
        (['John', '000 1.01.1990'], 'Expected integer value'),
        (['John', '-1.01.1990'], 'Bad day number'),
        (['John', '30.02.1990'], 'Bad day number'),
        (['John', '55.12.1990'], 'Bad day number'),
        (['John', '01.13.1990'], 'Bad month number'),
        (['John', '01.05.0000'], 'Bad year number'),
        (['  ', '01.05.1990'], 'Bad person name'),
    ],
)
def test_parse_row_error(row, expected_error):
    try:
        birthdays_table.parse_row(row)
    except birthdays_table.ParseError as e:
        assert str(e) == expected_error
        return

    assert False, "Expected error"
