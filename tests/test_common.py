import datetime
import functools

from bot import bot_wrapper, utils, db, settings, google_sheets_client

MOCK_CHAT_ID = 1488300
MOCK_MESSAGE_ID = 19
MOCK_QUERY_ID = 12
MOCK_USER_ID = 228

MOCK_CONFIG = {
    'telegram_user_ids': [MOCK_USER_ID],
    'google_sheets_sheet_name': 'sheet_name',
    'notification_time': '07:00',
}


class MockChat:
    def __init__(self, chat_id):
        self.id = chat_id


class MockUser:
    def __init__(self, user_id):
        self.id = user_id


class MockMessage:
    def __init__(
            self,
            text,
            chat_id=MOCK_CHAT_ID,
            user_id=MOCK_USER_ID,
            parse_mode=None,
            reply_markup=None,
    ):
        self.message_id = MOCK_MESSAGE_ID
        self.chat = MockChat(chat_id)
        self.from_user = MockUser(user_id)
        self.text = text
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup


class MockState:
    def __init__(self):
        self.finished = False

    async def finish(self):
        self.finished = True


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
        self.data = []

    def get_data(self, spreadsheet_id):
        return self.data

    def check_spreadsheet(self, spreadsheet_id):
        return google_sheets_client.SpreadsheetCheckResult.OK


class MockContext:
    def __init__(self, db_path):
        self.config = MOCK_CONFIG
        self.authorizer = None
        self.db = db.Db(db_path)
        self.bot = MockBot()
        self.settings = settings.Settings(self.db)
        self.google_sheets_client = MockGoogleSheetsClient()
        self.bot_wrapper = bot_wrapper.BotWrapper(self.bot)


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
