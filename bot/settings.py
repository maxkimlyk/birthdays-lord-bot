import copy
import json
import logging
from typing import Any, Dict, Optional

from . import db, exceptions, utils


class TypeDescr:
    def cast_value(self, value: Any) -> Any:
        raise NotImplementedError

    def get_default(self) -> Any:
        raise NotImplementedError


class TypeBool(TypeDescr):
    def __init__(self, default=None):
        self._default = default

    def cast_value(self, value: Any) -> bool:
        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            return bool(str)

        raise exceptions.CannotCast('value of unexpected type')

    def get_default(self) -> bool:
        if self._default is not None:
            return self._default
        return False


class TypeOptionalStr(TypeDescr):
    def __init__(self, default=None):
        self._default = default

    def cast_value(self, value: Any) -> Optional[str]:
        if value is None:
            return value
        return str(value)

    def get_default(self) -> Optional[str]:
        return self._default


class TypeDaytime(TypeDescr):
    def __init__(self, default: str):
        self.default = self.cast_value(default)

    def cast_value(self, value: Any) -> str:
        text = str(value).strip()
        try:
            time = utils.parse_daytime(text)
            return utils.format_daytime(time)
        except ValueError as e:
            raise exceptions.CannotCast('Bad value: {}'.format(text)) from e

    def get_default(self) -> str:
        return self.default


SchemaType = Dict[str, TypeDescr]

_USER_SETTINGS_SCHEMA: SchemaType = {
    'spreadsheet_id': TypeOptionalStr(default=None),
    'enable_weekly_notifications': TypeBool(default=True),
    'notification_time': TypeDaytime(default='07:00'),
}


class UserSettings:
    def __init__(
            self,
            db_: db.Db,
            user_id: int,
            schema: Optional[SchemaType] = None,
    ):
        self._db = db_
        self._user_id = user_id
        self._schema = schema if schema is not None else _USER_SETTINGS_SCHEMA
        self._settings = self._try_load_settings_from_db(
            db_, user_id, self._schema,
        )

    @staticmethod
    def _try_load_settings_from_db(
            db_: db.Db, user_id: int, schema: SchemaType,
    ) -> Dict[str, Any]:
        doc = {}
        try:
            doc = json.loads(db_.get_cache_value(db.CACHE_SETTINGS, user_id))
        except exceptions.NoSuchData:
            logging.warning('Settings is missing in db (user_id=%s)', user_id)
        except BaseException:
            logging.exception(
                'Failed to load settings from df (user=%s)', user_id,
            )

        settings = {}

        for key, type_descr in schema.items():
            if key not in doc:
                default = type_descr.get_default()
                logging.debug(
                    'setting "%s" is missing in db, using default: %s',
                    key,
                    default,
                )
                settings[key] = default
            else:
                try:
                    settings[key] = type_descr.cast_value(doc[key])
                except BaseException:
                    logging.exception(
                        'could not read setting "%s" with value "%s" '
                        'from db, using default',
                        key,
                        doc[key],
                    )
                    settings[key] = type_descr.get_default()

        return settings

    def _dump_settings(self, settings: Dict[str, Any]):
        value = json.dumps(settings)
        self._db.add_cache_value(db.CACHE_SETTINGS, self._user_id, value)

    def __getitem__(self, key: str) -> Any:
        return self._settings[key]

    def __setitem__(self, key: str, value: Any):
        if key not in self._schema:
            raise KeyError('unknown setting "{}"'.format(key))

        type_descr = self._schema[key]
        new_value = type_descr.cast_value(value)

        # do we really need copy here?
        new_settings = copy.deepcopy(self._settings)
        new_settings[key] = new_value
        self._dump_settings(new_settings)
        self._settings = new_settings


class Settings:
    def __init__(self, db_: db.Db):
        self._db = db_

    def get_for_user(self, user_id: int) -> UserSettings:
        return UserSettings(self._db, user_id)
