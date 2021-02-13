import re
from typing import Optional, Any

from bot import types, settings
from . import common

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


def build_response_set_notification_time_step1() -> types.Response:
    return types.Response(
        'Задайте новое время для ежедневных оповещений. Например, 07:30.',
        common.PARSE_MODE_HTML,
    )


def build_response_bad_setting_value() -> types.Response:
    return types.Response('Извините, но это значение не подходит.')


def _localize_setting_value(setting: Any) -> str:
    if setting is None:
        return 'не установлено'
    if isinstance(setting, bool):
        return 'вкл' if setting else 'выкл'
    return str(setting)


def _format_setting_value(setting: Any) -> str:
    return '<code>{}</code>'.format(_localize_setting_value(setting))


def _format_spreadsheet_id_with_link(spreadsheet_id: str) -> str:
    return '<a href="{}">{}</a>'.format(
        common.make_google_sheets_edit_link(spreadsheet_id), spreadsheet_id,
    )


def build_response_current_settings(
        user_settings: settings.UserSettings,
) -> types.Response:
    setting_descrs = [
        (
            'Идентификатор таблицы Google Sheets',
            'spreadsheet_id',
            _format_spreadsheet_id_with_link,
            '/set_spreadsheet',
        ),
        (
            'Оповещения на неделю вперед (по понедельникам)',
            'enable_weekly_notifications',
            _format_setting_value,
            '/toggle_weekly_notifications',
        ),
        (
            'Время оповещений',
            'notification_time',
            _format_setting_value,
            '/set_notification_time',
        ),
    ]

    lines = []
    for loc, key, format_func, handler in setting_descrs:
        lines.append(
            '<b>{}</b>: {}\n'.format(
                loc, format_func(user_settings[key]),
            )
            + 'Изменить: {}'.format(handler),
        )

    text = 'Текущие настройки:\n\n' + '\n\n'.join(lines)
    return types.Response(text, common.PARSE_MODE_HTML)
