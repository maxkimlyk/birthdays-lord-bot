import os
import sqlite3

import pytest

from . import test_common


_DB_INIT_SCRIPT_PATH = 'createdb.sql'


def _init_db(connection):
    with open(_DB_INIT_SCRIPT_PATH, 'r') as f:
        sql = f.read()
    connection.executescript(sql)


def _get_db_path(tmpdir):
    file = os.path.join(tmpdir.strpath, 'test.db')
    return file


@pytest.fixture(name='db', autouse=True)
def _db(tmpdir):
    file = _get_db_path(tmpdir)
    connection = sqlite3.connect(file)
    _init_db(connection)
    yield connection
    connection.close()


@pytest.fixture(name='db_path')
def _db_path(tmpdir):
    return _get_db_path(tmpdir)


@pytest.fixture(name='mock_context')
def _mock_context(db_path):
    return test_common.MockContext(db_path)


@pytest.fixture(name='mock_time', autouse=True)
def _mock_time():
    return test_common.TimeMocker()
