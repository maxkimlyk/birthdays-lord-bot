import datetime

import bot.db
import pytest


def test_store_periodic_task_last_executed(db, db_path):
    db = bot.db.Db(db_path)

    dt = datetime.datetime(2020, 1, 1, 12, 20)
    db.set_periodic_task_last_executed('task1', dt)
    assert db.get_periodic_task_last_executed('task1') == dt

    assert (
        db.get_periodic_task_last_executed('unknown task')
        == datetime.datetime.min
    )
