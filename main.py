import networkx as nx
import os
from models import root, link, node, category
from models import json_util
import random


class Router:
    def __init__(self, category_cnt=9):
        # 图数据结构
        self.graph = nx.Graph()
        # 自定义类型，供导出json使用
        self.root = root.Root(nodes=[], links=[], categories=[])
        # 默认定义九种类型,索引下标从0开始
        self.category_cnt = category_cnt
        self.root.categories = [category.Category(name=str(i + 1)) for i in range(category_cnt)]

    # 内置添加点、边系列的函数
    def _add_node_to_root_conditional(self, src_node):
        if self.root.get_id_str_by_name(src_node) == str(-1):
            self.root.nodes.append(node.Node(name=src_node,
                                             id=str(len(self.root.nodes)),
                                             symbolSize=random.uniform(10,15),
                                             x=random.uniform(-500.0, 500.0),
                                             y=random.uniform(-500.0, 500.0),
                                             value=10,
                                             category=random.randint(0, self.category_cnt - 1)))

    def _add_edge_to_root(self, source, target):
        self.root.links.append(link.Link(source=source, target=target))

    def _add_edge_to_graph_and_root_conditional(self, source, target):
        if self.graph.has_edge(source, target) == False:
            self.graph.add_edge(source, target)
            source_id = self.root.get_id_str_by_name(source)
            target_id = self.root.get_id_str_by_name(target)
            self.root.links.append(link.Link(source=source_id, target=target_id))
            self.root.links.append(link.Link(source=target_id, target=source_id))

    # 根据合并文件来恢复结点,默认路由行中不同ip用-隔开
    '''
    合并文件的格式:
    tracert网站1
    ipx1-ipx2-...-ipxn
    tracert网站2
    ipy1-ipy2-...-ipyn
    \n(这里以\n结束)
    '''

    def get_all_edges_from_combine_txt(self, txt_path: str, txt_encoding: str = 'utf-8', sep: str = '-'):
        with open(txt_path, 'r') as f:
            data = f.readlines()

            for i, item in enumerate(data):
                # 以\n结束
                if item == '\n':
                    break
                # 为tracert网站行
                if i % 2 == 0:
                    continue
                # 为ip路径行
                ip_list = item.split(sep)
                for j in range(len(ip_list) - 1):
                    u = ip_list[j].replace('\n', '')
                    v = ip_list[j + 1].replace('\n', '')
                    self._add_node_to_root_conditional(src_node=u)
                    self._add_node_to_root_conditional(src_node=v)

                    self._add_edge_to_graph_and_root_conditional(source=u, target=v)

    def export_to_json(self, export_path: str, json_txt_encoding='utf-8'):
        json_util.model_to_json_file(export_path=export_path,
                                     json_txt_encoding=json_txt_encoding,
                                     src_object=self.root)


'''
将收集到的数据存入数据结构中，计算网络属性并导出可视化的json文件
'''
if __name__ == '__main__':
    my_router = Router()
    my_router.get_all_edges_from_combine_txt(txt_path=os.path.join('file_op', 'out.txt'),
                                             txt_encoding='gbk')
    my_router.export_to_json(export_path=os.path.join('export', 'out.json'),
                             json_txt_encoding='utf-8')
