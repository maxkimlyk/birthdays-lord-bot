from bot import types
from . import common


def build_response(user_id: int) -> types.Response:
    text = (
        'You aren\'t authorized. Did you forget to add your ID (<b>{}</b>) to config?'
    ).format(user_id)
    return types.Response(text, common.PARSE_MODE_HTML)
