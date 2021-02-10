from bot import db, settings
from .test_common import *

_TEST_SCHEMA = {'opt_str': settings.TypeOptionalStr(default=None)}


def test_setget(db_path):
    db_ = db.Db(db_path)

    key = 'opt_str'

    user_settings = settings.UserSettings(db_, MOCK_USER_ID, _TEST_SCHEMA)
    user_settings[key] = None

    assert user_settings[key] is None

    user_settings[key] = 'str'
    assert user_settings[key] == 'str'


def test_use_default(db_path):
    db_ = db.Db(db_path)

    db_.add_cache_value(db.CACHE_SETTINGS, MOCK_USER_ID, '{ }')
    user_settings = settings.UserSettings(db_, MOCK_USER_ID, _TEST_SCHEMA)

    assert user_settings['opt_str'] is None
