import datetime

import bot.db
import pytest


def test_last_notified(db, db_path):
    db = bot.db.Db(db_path)

    dt = datetime.datetime(2020, 1, 1, 12, 20)
    db.set_last_notified('notification1', dt)
    assert db.get_last_notified('notification1') == dt

    assert db.get_last_notified('new notification') == datetime.datetime.min
