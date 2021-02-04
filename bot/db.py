import datetime
import json
import sqlite3
from typing import Any, Dict, Iterable, List, Optional, Tuple


class Db:
    def __init__(self, path_to_dbfile: str):
        self._connection = sqlite3.connect(path_to_dbfile)
        self._connection.row_factory = sqlite3.Row
