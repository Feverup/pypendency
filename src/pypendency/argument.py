from typing import Any, Optional

from dataclasses import dataclass


@dataclass(frozen=True)
class Argument:
    key: Optional[str]
    value: Any

    @classmethod
    def no_kw_argument(cls, value: Any) -> "Argument":
        return cls(None, value)
