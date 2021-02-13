import pytest

from bot import db, settings, exceptions
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


def test_daytime(db_path):
    db_ = db.Db(db_path)
    key = 'daytime'
    schema = {
        'daytime': settings.TypeDaytime(default='12:00'),
    }

    user_settings = settings.UserSettings(db_, MOCK_USER_ID, schema)

    with pytest.raises(exceptions.CannotCast):
        user_settings[key] = '24:32'

    with pytest.raises(exceptions.CannotCast):
        user_settings[key] = '12h 5m'

    user_settings[key] = '00:00'
    assert user_settings[key] == '00:00'

    user_settings[key] = '8:1'
    assert user_settings[key] == '08:01'
