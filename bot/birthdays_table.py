import base64
import hashlib

from typing import Optional, List, Tuple

from . import types


class ParseError(BaseException):
    def __init__(self, reason):
        super().__init__()
        self.reason = reason

    def __repr__(self):
        return 'ParseError({})'.format(self.reason)

    def __eq__(self, other):
        return self.reason == other.reason


_Reason = types.TableParseError.Reason


_DAYS_IN_MONTH = {
    1: 31,
    2: 29,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}


def _is_empty_row(row: List[str]) -> bool:
    return all((v.strip() == '' for v in row))


def _parse_int(raw: str) -> int:
    try:
        return int(raw)
    except ValueError as e:
        raise ParseError(_Reason.EXPECTED_INTEGER_VALUE) from e


def _parse_day(day_raw: str, max_day_in_month: int) -> int:
    day = _parse_int(day_raw)
    if day < 1 or day > max_day_in_month:
        raise ParseError(_Reason.BAD_DAY_NUMBER)
    return day


def _parse_month(month_raw: str) -> int:
    month = _parse_int(month_raw)
    if month < 1 or month > 12:
        raise ParseError(_Reason.BAD_MONTH_NUMBER)
    return month


def _parse_year(year_raw: str) -> int:
    year = _parse_int(year_raw)
    if year < 1:
        raise ParseError(_Reason.BAD_YEAR_NUMBER)
    return year


def _parse_date(raw: str) -> types.AnnualDate:
    components = raw.split('.')

    if len(components) not in {2, 3}:
        raise ParseError(_Reason.BAD_DATE_FORMAT)

    month = _parse_month(components[1])
    day = _parse_day(components[0], _DAYS_IN_MONTH[month])
    year = _parse_year(components[2]) if len(components) > 2 else None

    return types.AnnualDate(day, month, year)


def parse_row(row: List[str]) -> Optional[types.Birthday]:
    if _is_empty_row(row):
        return None

    if len(row) < 2:
        return None

    person_name = row[0].strip()
    if person_name == '':
        raise ParseError(_Reason.BAD_PERSON_NAME)

    date_raw = row[1].strip()
    date = _parse_date(date_raw)

    return types.Birthday(date, person_name)


def _get_hash(rows: List[List[str]]) -> str:
    h = hashlib.sha256()
    for row in rows:
        for value in row:
            h.update(value.encode('utf-8'))
    hash_bytes = h.digest()
    return base64.b64encode(hash_bytes).decode('utf-8')


def parse(
        rows: List[List[str]],
) -> Tuple[List[types.Birthday], List[types.TableParseError], str]:
    result = []
    errors = []

    for i, row in enumerate(rows):
        try:
            birthday = parse_row(row)
            if birthday is not None:
                result.append(birthday)
        except ParseError as e:
            errors.append(types.TableParseError(e.reason, i + 1))

    return result, errors, _get_hash(rows)
