import datetime
import json
import sqlite3
import logging
from typing import Any, Dict, Iterable, List, Optional, Tuple

_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'


def _format_datetime(time: datetime.datetime) -> str:
    return time.strftime(_DATETIME_FORMAT)


def _parse_datetime(strtime: str) -> datetime.datetime:
    return datetime.datetime.strptime(strtime, _DATETIME_FORMAT)


class Db:
    def __init__(self, path_to_dbfile: str):
        self._connection = sqlite3.connect(path_to_dbfile)
        self._connection.row_factory = sqlite3.Row

    def set_periodic_task_last_executed(
            self, periodic_task: str, last_executed: datetime.datetime,
    ):
        self._connection.execute(
            'INSERT OR REPLACE INTO periodic_task(id, last_executed) '
            'VALUES (?, ?)',
            (periodic_task, _format_datetime(last_executed)),
        )
        self._connection.commit()

    def get_periodic_task_last_executed(
            self, periodic_task: str,
    ) -> datetime.datetime:
        fetched = self._connection.execute(
            'SELECT last_executed FROM periodic_task WHERE id = ?',
            (periodic_task,),
        ).fetchone()

        if fetched is not None:
            try:
                return _parse_datetime(fetched[0])
            except ValueError:
                logging.error('Failed to parse datetime from db: %s', fetched)

        return datetime.datetime.min
