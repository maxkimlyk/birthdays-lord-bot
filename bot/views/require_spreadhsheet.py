from bot import types


def build_response() -> types.Response:
    return types.Response(
        'Сначала необходимо привязать таблицу Google Sheets.\n'
        'Привязать: /set_spreadsheet',
    )
