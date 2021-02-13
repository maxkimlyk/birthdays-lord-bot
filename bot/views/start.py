from bot import types
from . import common


def build_response() -> types.Response:
    text = (
        'Привет!\n\n'
        'Я - ваш скромный Birthdays Lord (Повелитель Дней Рождения). '
        'Я буду ежедневно напоминать вам, у кого день рождения в этот день.'
    )

    return types.Response(text, common.PARSE_MODE_HTML)
