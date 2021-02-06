import datetime

import pytest

from bot import utils

@pytest.mark.parametrize(
  'input,expected',
  (
    ("12:00", datetime.time(12, 0)),
    ("01:01", datetime.time(1, 1)),
  )
)
def test_parse_daytime(input, expected):
    assert utils.parse_daytime(input) == expected
