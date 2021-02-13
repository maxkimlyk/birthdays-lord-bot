from typing import Optional

from bot import types
from . import common


def build_response(spreadsheet_id: Optional[str]) -> types.Response:
    if spreadsheet_id is None:
        return types.Response(
            'Вы еще не установили таблицу с днями рождения. '
            'Используйте /start, чтобы начать.',
        )

    text = (
        'Редактируйте таблицу дней рождений на Google Sheets.\n'
        'Вот '
        + '<a href="{}">ссылка на вашу таблицу</a> '.format(
            common.make_google_sheets_edit_link(spreadsheet_id),
        )
    )
    return types.Response(text, common.PARSE_MODE_HTML)
