import re
from typing import Optional

from bot import types

_URL_REGEXP = re.compile(
    r'https:\/\/docs\.google\.com\/spreadsheets\/d\/([\w\-]+)\/edit.*',
)

_SPREADSHEET_ID = re.compile(r'[\w\-]+$')

_EXPECTED_SPREADSHEET_ID_LENGTH = 44


def build_response_set_spreadsheet_id_step1() -> types.Response:
    return types.Response(
        'Пришлите мне ссылку на новую таблицу или spreadsheet id.',
    )


def _extract_spreadsheet_id(text: str) -> Optional[str]:
    text = text.strip()

    match = re.match(_URL_REGEXP, text)
    if match:
        return match.group(1)

    match = re.match(_SPREADSHEET_ID, text)
    if match:
        return text

    return None


def parse_set_spreadsheet_step2_request(text: str) -> Optional[str]:
    spreadsheet_id = _extract_spreadsheet_id(text)
    if spreadsheet_id is None:
        return None

    if len(spreadsheet_id) != _EXPECTED_SPREADSHEET_ID_LENGTH:
        return None

    return spreadsheet_id


def build_response_bad_spreadsheet_id() -> types.Response:
    return types.Response(
        'Извините, но этот идентификатор неправильный. Проверьте и попробуйте еще раз.',
    )


def build_response_no_access_to_spreadsheet() -> types.Response:
    return types.Response(
        'Нет доступа к вашей таблице. Забыли открыть доступ?',
    )


def build_response_spreadsheet_not_found() -> types.Response:
    return types.Response(
        'Данная таблица не существует. '
        'Пожалуйста, проверьте правильность ссылки или идентификатора.',
    )


def build_response_spreadsheet_id_was_set_successfully() -> types.Response:
    return types.Response('Новая таблица установлена успешно!')
