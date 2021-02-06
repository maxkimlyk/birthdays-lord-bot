import dataclasses
from typing import List, Optional, Iterable

from . import common
from bot import types


@dataclasses.dataclass
class BirthdayShowParams:
    birthday: types.Birthday
    age: Optional[int]


def _build_age_text_postfix(age: int):
    rest100 = age % 100
    if 10 <= age and age < 19:
        return "лет"

    rest10 = age % 10
    if rest10 == 1:
        return "год"
    elif 2 <= rest10 and rest10 <= 4:
        return "года"
    return "лет"


def _build_birthday_text(params: BirthdayShowParams):
    age = ""
    if params.age:
        age = "({} {})".format(params.age, _build_age_text_postfix(params.age))
    return "<b>{}</b> {}".format(params.birthday.person_name, age)


def build_birthdays_today_notification(birthdays: List[BirthdayShowParams]) -> types.Response:
    if birthdays == []:
        return types.Response("Сегодня нет дней рождения")

    if len(birthdays) == 1:
        text = (
            "Сегодня день рождения у\n" +
            _build_birthday_text(birthdays[0])
        )
    else:
        text = (
          "Сегодня дни рождения у\n" +
          "\n".join((_build_birthday_text(bd) for bd in birthdays))
        )

    return types.Response(text, common.PARSE_MODE_HTML)


def build_errors_notification(errors: Iterable[types.TableParseError]) -> types.Response:
    if errors == []:
        return types.Response("Нет ошибок")

    text = (
        "Обнаружены ошибки в таблице:\n" +
        "\n".join((e.description for e in errors))
    )

    return types.Response(text)
