from typing import Any
from dataclasses import dataclass
import json


@dataclass
class Node:
    id: str
    name: str
    symbolSize: float
    x: float
    y: float
    value: float
    category: int

    @staticmethod
    def from_dict(obj: Any) -> 'Node':
        _id = str(obj.get("id"))
        _name = str(obj.get("name"))
        _symbolSize = float(obj.get("symbolSize"))
        _x = float(obj.get("x"))
        _y = float(obj.get("y"))
        _value = float(obj.get("value"))
        _category = int(obj.get("category"))
        return Node(_id, _name, _symbolSize, _x, _y, _value, _category)
