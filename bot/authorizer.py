from typing import Any, Dict

class Authorizer:
    def __init__(self, config: Dict[str, Any]):
        self._user_id = int(config['telegram_user_id'])

    def is_authorized(self, user_id: int):
        return self._user_id == user_id
