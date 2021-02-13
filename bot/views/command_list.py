from bot import types
from . import common


def build_command_list() -> types.Response:
    text = (
        'Мои команды:\n'
        '/start, /help - показать приветственное сообщение и список команд\n'
        '/today - дни рождения сегодня\n'
        '/next_week - дни рождения на следующей неделе\n'
        '\n'
        '/set_spreadsheet - использовать новую таблицу\n'
    )

    return types.Response(text, common.PARSE_MODE_HTML)
