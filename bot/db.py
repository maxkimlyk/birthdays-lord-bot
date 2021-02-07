import datetime
import sqlite3
import logging

from . import exceptions

_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'


def _format_datetime(time: datetime.datetime) -> str:
    return time.strftime(_DATETIME_FORMAT)


def _parse_datetime(strtime: str) -> datetime.datetime:
    return datetime.datetime.strptime(strtime, _DATETIME_FORMAT)


class Db:
    def __init__(self, path_to_dbfile: str):
        self._connection = sqlite3.connect(path_to_dbfile)
        self._connection.row_factory = sqlite3.Row

    def set_last_notified(
            self, notification_id: str, last_notified: datetime.datetime,
    ):
        self._connection.execute(
            'INSERT OR REPLACE INTO notifications(id, last_notified) '
            'VALUES (?, ?)',
            (notification_id, _format_datetime(last_notified)),
        )
        self._connection.commit()

    def get_last_notified(self, notification_id: str) -> datetime.datetime:
        fetched = self._connection.execute(
            'SELECT last_notified FROM notifications WHERE id = ?',
            (notification_id,),
        ).fetchone()

        if fetched is not None:
            try:
                return _parse_datetime(fetched[0])
            except ValueError:
                logging.error('Failed to parse datetime from db: %s', fetched)

        return datetime.datetime.min

    def add_cache_value(self, key: str, value: str):
        self._connection.execute(
            'INSERT OR REPLACE INTO cache(key, value) ' 'VALUES (?, ?)',
            (key, value),
        )
        self._connection.commit()

    def get_cache_value(self, key: str):
        fetched = self._connection.execute(
            'SELECT value FROM cache WHERE key = ?', (key,),
        ).fetchone()

        if fetched is None:
            raise exceptions.NoSuchData('No value with key {}'.format(key))

        return fetched[0]
