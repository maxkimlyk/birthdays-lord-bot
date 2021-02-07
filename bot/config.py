from typing import Dict
import yaml


_ENV_MAPPING_TO_CONFIG_KEYS = {
    'TELEGRAM_API_TOKEN': 'telegram_api_token',
    'TELEGRAM_USER_ID': 'telegram_user_id',
    'GOOGLE_SHEETS_CREDENTIALS_FILE': 'google_sheets_credentials_file',
    'GOOGLE_SHEETS_SPREADSHEET_ID': 'google_sheets_spreadsheet_id',
    'GOOGLE_SHEETS_SHEET_NAME': 'google_sheets_sheet_name',
    'DEVMODE': 'devmode',
}

_DEFAULT_VALUES = {
  'db_path': '/var/cache/birthdays-lord-bot/db.db',
  'cache_dir': '/var/cache/birthdays-lord-bot/'
}


def _load_config_file(file: str):
    with open(file) as f:
        content = f.read()
        return yaml.load(content, Loader=yaml.CLoader)


def load_config(config_path: str, environment: Dict[str, str]):
    config = _load_config_file(config_path)

    for env_key, conf_key in _ENV_MAPPING_TO_CONFIG_KEYS.items():
        if env_key in environment and environment[env_key]:
            config[conf_key] = environment[env_key]

    for key, value in _DEFAULT_VALUES.items():
        if key not in config:
            config[key] = value

    return config
