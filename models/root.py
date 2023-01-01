from dataclasses import dataclass
from typing import Any
from typing import List
from models import node, link, category, custom_encoder
import json


@dataclass
class Root:
    nodes: List[node.Node]
    links: List[link.Link]
    categories: List[category.Category]

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _nodes = [node.Node.from_dict(y) for y in obj.get("nodes")]
        _links = [link.Link.from_dict(y) for y in obj.get("links")]
        _categories = [category.Category.from_dict(y) for y in obj.get("categories")]
        return Root(_nodes, _links, _categories)

    # 默认结点的id就是在列表中的下标
    def get_id_str_by_name(self, name: str) -> str:
        for id, item in enumerate(self.nodes):
            if name == item.name:
                return str(id)
        return str(-1)
