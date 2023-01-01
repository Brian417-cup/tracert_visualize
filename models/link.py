from dataclasses import dataclass
from typing import Any


@dataclass
class Link:
    source: str
    target: str

    @staticmethod
    def from_dict(obj: Any) -> 'Link':
        _source = str(obj.get("source"))
        _target = str(obj.get("target"))
        return Link(_source, _target)
