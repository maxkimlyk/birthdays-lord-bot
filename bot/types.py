import dataclasses
from typing import Optional

@dataclasses.dataclass
class Response:
    text: str
    parse_mode: Optional[str] = None


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
    description: str
