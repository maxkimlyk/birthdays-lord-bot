import dataclasses
import enum
from typing import Optional

@dataclasses.dataclass
class Response:
    text: str
    parse_mode: Optional[str] = None
    photo_path: Optional[str] = None


@dataclasses.dataclass
class AnnualDate:
    day: int
    month: int
    first_year: Optional[int] = None


@dataclasses.dataclass
class Birthday:
    date: AnnualDate
    person_name: str


@dataclasses.dataclass
class TableParseError:
    class Reason(enum.Enum):
        EXPECTED_INTEGER_VALUE = 0
        BAD_DAY_NUMBER = 1
        BAD_MONTH_NUMBER = 2
        BAD_YEAR_NUMBER = 3
        BAD_DATE_FORMAT = 4
        BAD_PERSON_NAME = 5

    reason: Reason
    row: int
