import dataclasses
from typing import List, Optional, Iterable

from bot import types
from . import common


@dataclasses.dataclass
class BirthdayShowParams:
    birthday: types.Birthday
    age: Optional[int]
    weekday: Optional[int]


def _build_age_text_postfix(age: int) -> str:
    rest100 = age % 100
    if 10 <= rest100 < 19:
        return 'лет'

    rest10 = age % 10
    if rest10 == 1:
        return 'год'
    if 2 <= rest10 <= 4:
        return 'года'
    return 'лет'


def _localize_weekday(weekday: int) -> str:
    switch = {0: 'пн', 1: 'вт', 2: 'ср', 3: 'чт', 4: 'пт', 5: 'сб', 6: 'вс'}
    return switch[weekday]


def _localize_date(date: types.AnnualDate) -> str:
    month_switch = {
        1: 'января',
        2: 'февраля',
        3: 'марта',
        4: 'апреля',
        5: 'мая',
        6: 'июня',
        7: 'июля',
        8: 'августа',
        9: 'сентября',
        10: 'октября',
        11: 'ноября',
        12: 'декабря',
    }

    return '{} {}'.format(date.day, month_switch[date.month])


def _build_birthday_text_short(params: BirthdayShowParams):
    result = '<b>{}</b>'.format(params.birthday.person_name)
    if params.age:
        result += ' - {} {}'.format(
            params.age, _build_age_text_postfix(params.age),
        )
    return result


def _build_birthday_text_full(params: BirthdayShowParams):
    short = _build_birthday_text_short(params)
    details = []
    if params.weekday is not None:
        details.append(_localize_weekday(params.weekday))
    details.append(_localize_date(params.birthday.date))
    return '{} ({})'.format(short, ', '.join(details))


def build_birthdays_today_notification(
        birthdays: List[BirthdayShowParams],
) -> types.Response:
    if birthdays == []:
        return types.Response('Сегодня нет дней рождения')

    if len(birthdays) == 1:
        text = 'Сегодня день рождения у\n' + _build_birthday_text_short(
            birthdays[0],
        )
    else:
        text = 'Сегодня дни рождения у\n' + '\n'.join(
            (_build_birthday_text_short(bd) for bd in birthdays),
        )

    return types.Response(text, common.PARSE_MODE_HTML)


def build_birthdays_weekly_notification(
        birthdays: List[BirthdayShowParams],
) -> types.Response:
    if birthdays == []:
        return types.Response('На следующей неделе не будет дней рождения')

    text = 'На следующей неделе дни рождения будут праздновать:\n' + '\n'.join(
        (_build_birthday_text_full(bd) for bd in birthdays),
    )

    return types.Response(text, common.PARSE_MODE_HTML)


def _localize_error(error: types.TableParseError) -> str:
    Reason = types.TableParseError.Reason
    switch = {
        Reason.EXPECTED_INTEGER_VALUE: 'Ожидалось целое число',
        Reason.BAD_DAY_NUMBER: 'Несуществующий день',
        Reason.BAD_MONTH_NUMBER: 'Несуществующий месяц',
        Reason.BAD_YEAR_NUMBER: 'Несуществующий год',
        Reason.BAD_DATE_FORMAT: 'Неправильный формат даты',
        Reason.BAD_PERSON_NAME: 'Отсутствует имя',
    }
    reason_text = switch.get(error.reason, 'Неизвестная ошибка')
    return 'Строка {}: {}'.format(error.row, reason_text)


def build_errors_notification(
        errors: Iterable[types.TableParseError],
) -> types.Response:
    if errors == []:
        return types.Response('Нет ошибок')

    text = 'Обнаружены ошибки в таблице:\n' + '\n'.join(
        (_localize_error(e) for e in errors),
    )

    return types.Response(text)
