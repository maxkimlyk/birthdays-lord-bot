from typing import List

from bot import types
from . import common

_CREATE_NEW_TABLE_LINK = (
    'https://docs.google.com/spreadsheets/u/0/create?usp=sheets_home&ths=true'
)


def build_guide_step1() -> List[types.Response]:
    return [
        types.Response(
            'Для начала создайте таблицу на Google Sheets, '
            'в которой будут храниться дни рождения ваших друзей.\n'
            'Для этого перейдите по '
            + '<a href="{}">ссылке</a>.'.format(_CREATE_NEW_TABLE_LINK),
            common.PARSE_MODE_HTML,
        ),
        types.Response(
            'Чтобы я мог читать данные из этой таблицы, вам необходимо открыть к ней доступ. '
            'Для этого в меню <b>Файл</b> выберите <b>Открыть доступ</b>',
            common.PARSE_MODE_HTML,
            photo_path='guide/allow_access1.png',
        ),
        types.Response(
            'Нажмите <b>Разрешить доступ всем, у кого есть ссылка</b>, '
            'скопируйте ссылку и просто пришлите её мне.',
            common.PARSE_MODE_HTML,
            photo_path='guide/allow_access2.png',
        ),
    ]


def build_guide_step2() -> List[types.Response]:
    return [
        types.Response(
            'Отлично! Теперь остается только заполнить таблицу.'
        ),
        types.Response(
            'Указывайте имя в первом столбце, а дату рождения во втором. '
            'Остальные столбцы можно использовать как угодно, например, для заметок. '
            'Кстати, вы можете использовать любые цвета, шрифты и визуальное оформление таблицы. ',
            parse_mode=common.PARSE_MODE_HTML,
            photo_path='guide/table_example.png'
        ),
        types.Response(
            'Если в таблице будет допушена ошибка, или я не смогу понять содержания, '
            'то я незамедлительно об этом сообщу.'
        )
    ]
