from dataclasses import dataclass
from typing import Dict, List, Optional, ClassVar


@dataclass(frozen=True)
class Tag:
    identifier: str

    UNSET_VALUE: ClassVar[object] = object()
    value: Optional[object] = UNSET_VALUE
