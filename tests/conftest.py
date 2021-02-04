import os

import sqlite3

import pytest


_DB_INIT_SCRIPT_PATH = 'createdb.sql'


def _init_db(connection):
    with open(_DB_INIT_SCRIPT_PATH, 'r') as f:
        sql = f.read()
    connection.executescript(sql)


def _get_db_path(tmpdir):
    file = os.path.join(tmpdir.strpath, 'test.db')
    return file


@pytest.fixture(name='db')
def _db(tmpdir):
    file = _get_db_path(tmpdir)
    connection = sqlite3.connect(file)
    _init_db(connection)
    yield connection
    connection.close()


@pytest.fixture(name='db_path')
def _db_path(tmpdir):
    return _get_db_path(tmpdir)

