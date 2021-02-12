import re
from typing import Optional

from bot import types

_URL_REGEXP = re.compile(
    r'https:\/\/docs\.google\.com\/spreadsheets\/d\/([\w\-]+)\/edit.*',
)

_SPREADSHEET_ID = re.compile(r'[\w\-]+$')

_EXPECTED_SPREADSHEET_ID_LENGTH = 44


def build_response_set_spreadsheet_id_step1() -> types.Response:
    text = 'Send me spreadsheet id or link to your table with birthdays.'

    return types.Response(text)


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
    text = 'Sorry but your spreadsheet id seems to be invalid. Check it and try again.'
    return types.Response(text)


def build_response_no_access_to_spreadsheet() -> types.Response:
    text = 'No access to your spreadsheet. Did you allow access?'
    return types.Response(text)


def build_response_spreadsheet_not_found() -> types.Response:
    text = 'Given spreadsheet does not exist. Please, check whether you wrote it correctly.'
    return types.Response(text)


def build_response_spreadsheet_id_was_set_successfully() -> types.Response:
    text = 'Spreadsheet id set successfully!'
    return types.Response(text)
