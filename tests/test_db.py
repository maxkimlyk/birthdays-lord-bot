import datetime

import bot.db


def test_last_notified(db, db_path):
    db = bot.db.Db(db_path)

    dt = datetime.datetime(2020, 1, 1, 12, 20)
    db.set_last_notified('notification1', 228, dt)
    assert db.get_last_notified('notification1', 228) == dt

    assert db.get_last_notified('new notification', 228) == datetime.datetime.min
    assert db.get_last_notified('notification1', 118) == datetime.datetime.min



def test_cache(db_path):
    db = bot.db.Db(db_path)

    db.add_cache_value("key1", 228, "value1")
    assert db.get_cache_value("key1", 228) == "value1"
