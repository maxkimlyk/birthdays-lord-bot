import pytest

from bot import views


@pytest.mark.parametrize(
    'param,expected',
    [
        (
            'https://docs.google.com/spreadsheets/d/111-jdisopasdoiwejfjjeifopsodijjdjjskkdklsld/edit?usp=sharing',
            '111-jdisopasdoiwejfjjeifopsodijjdjjskkdklsld',
        ),
        (
            'https://docs.google.com/spreadsheets/d/281-fpwoefijasd823jfdawoe38jf90e98jfndiopspa/edit#gid=0',
            '281-fpwoefijasd823jfdawoe38jf90e98jfndiopspa',
        ),
        ('https://docs.google.com/', None),
        (
            '111-jdisopasdoiwejfjjeifopsodijjdjjskkdklsld',
            '111-jdisopasdoiwejfjjeifopsodijjdjjskkdklsld',
        ),
        ('abcdefg', None),
    ],
)
def test_parse_set_spreadsheet_step2_request(param, expected):
    assert (
        views.settings.parse_set_spreadsheet_step2_request(param) == expected
    )
