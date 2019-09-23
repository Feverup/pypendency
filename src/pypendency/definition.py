from typing import List

from dataclasses import dataclass, field

from pypendency.argument import Argument


@dataclass(frozen=True)
class Definition:
    identifier: str
    fully_qualified_name: str
    arguments: List[Argument] = field(default_factory=list)
