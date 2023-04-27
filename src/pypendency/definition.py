from dataclasses import dataclass, field
from typing import List, Dict, Set

from pypendency.argument import Argument
from pypendency.tag import Tag


@dataclass(frozen=True)
class Definition:
    identifier: str
    fully_qualified_name: str
    arguments: List[Argument] = field(default_factory=list)
    tags: Set[Tag] = field(default_factory=set)
