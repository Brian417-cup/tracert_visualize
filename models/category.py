from typing import Any
from dataclasses import dataclass
from enum import Enum

@dataclass
class Category:
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'Category':
        _name = str(obj.get("name"))
        return Category(_name)
