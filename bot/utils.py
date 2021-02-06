import dataclasses
import typing
import datetime
from typing import Optional

import dateutil.tz


@dataclasses.dataclass
class _MockTime:
    utc: Optional[datetime.datetime] = None
    local: Optional[datetime.datetime] = None


_MOCK_TIME = _MockTime()


def set_mock_time(local: datetime.datetime, utc: datetime.datetime):
    _MOCK_TIME.local = local
    _MOCK_TIME.utc = utc


def reset_mock_time():
    _MOCK_TIME.local = None
    _MOCK_TIME.utc = None


def now_utc() -> datetime.datetime:
    if _MOCK_TIME.utc is not None:
        return _MOCK_TIME.utc

    return datetime.datetime.now()


def now_local() -> datetime.datetime:
    if _MOCK_TIME.local is not None:
        return _MOCK_TIME.local

    from_zone = dateutil.tz.tzutc()
    to_zone = dateutil.tz.tzlocal()
    utc = now_utc()
    utc = utc.replace(tzinfo=from_zone)
    return utc.astimezone(to_zone)


def parse_daytime(timestr: str) -> datetime.time:
    dt = datetime.datetime.strptime(timestr, '%H:%M')
    return datetime.time(hour=dt.hour, minute=dt.minute)
