import json
from models import node, link, category, root, graph_attribute


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if type(obj) in (node.Node, link.Link, category.Category, root.Root):
            return obj.__dict__
        if isinstance(obj, graph_attribute.GraphAttribute):
            return obj.custom_dict()
        return json.JSONEncoder.default(self, obj)
