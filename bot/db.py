import datetime
import sqlite3
import logging

from . import exceptions

_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'


# Cache keys
CACHE_TABLE_DATA_HASH = 'table_data_hash'
CACHE_GUIDE_PASSED = 'guide_passed'
CACHE_SETTINGS = 'settings'


def _format_datetime(time: datetime.datetime) -> str:
    return time.strftime(_DATETIME_FORMAT)


def _parse_datetime(strtime: str) -> datetime.datetime:
    return datetime.datetime.strptime(strtime, _DATETIME_FORMAT)


class Db:
    def __init__(self, path_to_dbfile: str):
        self._connection = sqlite3.connect(path_to_dbfile)
        self._connection.row_factory = sqlite3.Row

    def set_last_notified(
            self, notification_id: str, user_id: int, last_notified: datetime.datetime,
    ):
        self._connection.execute(
            'INSERT OR REPLACE INTO notifications(id, user_id, last_notified) '
            'VALUES (?, ?, ?)',
            (notification_id, user_id, _format_datetime(last_notified)),
        )
        self._connection.commit()

    def get_last_notified(self, notification_id: str, user_id: int) -> datetime.datetime:
        fetched = self._connection.execute(
            'SELECT last_notified FROM notifications WHERE id = ? AND user_id = ?',
            (notification_id, user_id),
        ).fetchone()

        if fetched is not None:
            try:
                return _parse_datetime(fetched[0])
            except ValueError:
                logging.error('Failed to parse datetime from db: %s', fetched)

        return datetime.datetime.min

    def add_cache_value(self, key: str, user_id: int, value: str):
        self._connection.execute(
            'INSERT OR REPLACE INTO cache(key, user_id, value) VALUES (?, ?, ?)',
            (key, user_id, value),
        )
        self._connection.commit()

    def get_cache_value(self, key: str, user_id: int):
        fetched = self._connection.execute(
            'SELECT value FROM cache WHERE key = ? AND user_id = ?',
            (key, user_id),
        ).fetchone()

        if fetched is None:
            raise exceptions.NoSuchData('No value with key {}'.format(key))

        return fetched[0]
