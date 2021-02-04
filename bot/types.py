import dataclasses
from typing import Optional

@dataclasses.dataclass
class Response:
    text: str
    parse_mode: Optional[str] = None
