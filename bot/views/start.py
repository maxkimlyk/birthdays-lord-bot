from bot import types
from . import common


def build_response() -> types.Response:
    text = (
        'Hello!\n'
        'I\'m your humble Birthday Lord. I\'ll send your everyday notifications about '
        'who celebrate his birthday today.'
    )

    return types.Response(text, common.PARSE_MODE_HTML)
