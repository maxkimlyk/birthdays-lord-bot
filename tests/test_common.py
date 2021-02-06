import datetime
import functools

from bot import bot_wrapper, utils

MOCK_CHAT_ID = 1488300
MOCK_MESSAGE_ID = 19
MOCK_QUERY_ID = 12
MOCK_USER_ID = 228

MOCK_CONFIG = {'telegram_user_id': MOCK_USER_ID, 'google_sheets_sheet_name': 'sheet_name'}


class Chat:
    def __init__(self, chat_id):
        self.id = chat_id


class MockMessage:
    def __init__(
            self,
            text,
            chat_id=MOCK_CHAT_ID,
            parse_mode=None,
            reply_markup=None,
    ):
        self.message_id = MOCK_MESSAGE_ID
        self.chat = Chat(chat_id)
        self.text = text
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup

    def get_buttons(self):
        if self.reply_markup is None:
            return None

        result = []
        rows = self.reply_markup.inline_keyboard
        for row in rows:
            for btn in row:
                payload = buttons.parse_payload(btn.callback_data)
                result.append((btn.text, payload))
        return result


class MockState:
    def __init__(self):
        self.finished = False

    async def finish(self):
        self.finished = True


class MockButtonQuery:
    def __init__(self, payload):
        self.id = MOCK_QUERY_ID
        self.data = buttons.make_payload(payload)
        self.message = MockMessage('')


class MockBot:
    def __init__(self):
        self.messages = []

    @property
    def last_message(self):
        return self.messages[-1]

    async def send_message(
            self, chat_id, response, parse_mode=None, reply_markup=None,
    ):
        msg = MockMessage(response, chat_id, parse_mode, reply_markup)
        self.messages.append(msg)

    async def answer_callback_query(self, query_id):
        pass

    async def edit_message_reply_markup(
            self, chat_id, message_id, reply_markup=None,
    ):
        # expect only deleting keyboard
        assert reply_markup == ''


class MockGoogleSheetsClient:
    def __init__(self):
        self.used_ranges = None
        self.data = []

    def get_data(self, ranges):
        self.used_ranges = ranges
        return self.data


class MockContext:
    def __init__(self, db):
        self.config = MOCK_CONFIG
        self.authorizer = None
        self.db = db
        self.bot = MockBot()
        self.google_sheets_client = MockGoogleSheetsClient()
        self.bot_wrapper = bot_wrapper.BotWrapper(self.bot, self.config)


class TimeMocker:
    def __init__(self):
        utils.reset_mock_time()

    def set_local(self, local):
        utc = local - datetime.timedelta(hours=3)
        utils.set_mock_time(local, utc)

    def set_utc(self, utc):
        local = utc + datetime.timedelta(hours=3)
        utils.set_mock_time(local, utc)

    def __del__(self):
        utils.reset_mock_time()
