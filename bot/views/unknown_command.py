import aiogram  # type: ignore

from bot import types


def build_response(message: aiogram.types.Message) -> types.Response:
    return types.Response(
        'Неизвестная команда: {}'.format(message.text.strip()),
    )
