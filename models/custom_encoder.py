import json
from models import node, link, category, root


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if type(obj) in (node.Node, link.Link, category.Category, root.Root):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
