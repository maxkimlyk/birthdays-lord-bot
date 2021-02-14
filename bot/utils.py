import dataclasses
import datetime
from typing import Optional

import dateutil.tz


@dataclasses.dataclass
class _MockTime:
    utc: Optional[datetime.datetime] = None
    local: Optional[datetime.datetime] = None


_MOCK_TIME = _MockTime()


def set_mock_time(local: datetime.datetime):
    _MOCK_TIME.local = local


def reset_mock_time():
    _MOCK_TIME.local = None


def now_local() -> datetime.datetime:
    if _MOCK_TIME.local is not None:
        return _MOCK_TIME.local

    return datetime.datetime.now()


def get_local_timezone():
    return dateutil.tz.tzlocal()


def parse_daytime(timestr: str) -> datetime.time:
    dt = datetime.datetime.strptime(timestr, '%H:%M')
    return datetime.time(hour=dt.hour, minute=dt.minute)


def format_daytime(time: datetime.time) -> str:
    return '{:02d}:{:02d}'.format(time.hour, time.minute)
