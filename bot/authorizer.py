from typing import Any, Dict


class Authorizer:
    def __init__(self, config: Dict[str, Any]):
        self._user_ids = {int(uid) for uid in config['telegram_user_ids']}

    def is_authorized(self, user_id: int):
        return user_id in self._user_ids
