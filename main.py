import networkx as nx
import os
from models import root, link, node, category, graph_attribute
from models import json_util
import random
import glob
from attribute import attribute_caculate as ac


class Router:
    def __init__(self, category_cnt=9):
        # 图数据结构
        self.graph = nx.Graph()
        # 自定义类型，供导出json使用
        self.root = root.Root(nodes=[], links=[], categories=[])
        # 默认定义九种类型,索引下标从0开始
        self.category_cnt = category_cnt
        # self.root.categories = [category.Category(name=str(i + 1)) for i in range(category_cnt)]
        self.root.categories = []
        self.lower_bound, self.upper_bound = float('inf'), float('-inf')
        self.grades = []

    # 内置添加点、边系列的函数
    def _add_node_to_root_conditional(self, src_node):
        src_idx = self.root.get_id_str_by_name(src_node)
        if src_idx == str(-1):
            self.root.nodes.append(node.Node(name=src_node,
                                             id=str(len(self.root.nodes)),
                                             symbolSize=random.uniform(10, 15),
                                             x=random.uniform(-500.0, 500.0),
                                             y=random.uniform(-500.0, 500.0),
                                             # value=1,
                                             value=0,
                                             category=random.randint(0, self.category_cnt - 1)))
        # else:
        #     self.root.nodes[int(src_idx)].value += 1

    def _add_edge_to_root(self, source, target):
        self.root.links.append(link.Link(source=source, target=target))

    def _add_edge_to_graph_and_root_conditional(self, source, target):
        if self.graph.has_edge(source, target) == False:
            self.graph.add_edge(source, target)
            source_id = self.root.get_id_str_by_name(source)
            target_id = self.root.get_id_str_by_name(target)
            # 加边
            self.root.links.append(link.Link(source=source_id, target=target_id))
            # self.root.links.append(link.Link(source=target_id, target=source_id))
            # 同时做度调整
            self.root.nodes[int(source_id)].value += 1
            self.root.nodes[int(target_id)].value += 1

    # 对指定文件下的所有txt文件进行结点的计算和合并
    def get_all_edges_from_combine_txts(self, base_dir: str, txt_encoding: str = 'utf-8', sep: str = '-'):
        for item in glob.glob(os.path.join(base_dir, '*.txt')):
            self._get_all_edges_from_single_combine_txt(txt_path=item, txt_encoding=txt_encoding, sep=sep)

    # 根据合并文件来恢复结点,默认路由行中不同ip用-隔开
    '''
    合并文件的格式:
    tracert网站1
    ipx1-ipx2-...-ipxn
    tracert网站2
    ipy1-ipy2-...-ipyn
    \n(这里以\n结束)
    '''

    def _get_all_edges_from_single_combine_txt(self, txt_path: str, txt_encoding: str = 'utf-8', sep: str = '-'):
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

                # 去多余的\n
                for i, item in enumerate(ip_list):
                    ip_list[i] = item.replace('\n', '')

                # 加点
                for item in ip_list:
                    self._add_node_to_root_conditional(item)

                # 加边
                for j in range(len(ip_list) - 1):
                    u = ip_list[j]
                    v = ip_list[j + 1]

                    self._add_edge_to_graph_and_root_conditional(source=u, target=v)

        self._update_grade_by_category_cnt()

    # 根据种类类型划分为不同的等级
    def _update_grade_by_category_cnt(self):
        # 先清空原来的等级划分
        self.grades.clear()
        self.root.categories.clear()
        # 等级划分内置函数
        def get_index_in_grades(need_judge_value: int) -> int:
            # 特殊情况：恰好等于最后一个元素
            if need_judge_value == self.grades[-1]:
                return self.category_cnt - 1

            for i in range(len(self.grades) - 1):
                lower_bound = self.grades[i]
                upper_bound = self.grades[i + 1]

                if need_judge_value >= lower_bound and need_judge_value < upper_bound:
                    # print(i)
                    return i

        # 确定上界和下界
        for i, item in enumerate(self.root.nodes):
            self.lower_bound = min(item.value, self.lower_bound)
            self.upper_bound = max(item.value, self.upper_bound)
        # 划分等级
        step = (self.upper_bound - self.lower_bound + 1) / self.category_cnt
        self.grades.append(self.lower_bound)
        for i in range(self.category_cnt - 1):
            self.grades.append(self.grades[-1] + step)
        self.grades.append(self.upper_bound)

        # print(len(self.grades))
        # for item in self.grades:
        #     print(item)

        # 更新标签
        for i in range(len(self.grades) - 1):
            lower_bound = self.grades[i]
            upper_bound = self.grades[i + 1]
            self.root.categories.append(category.Category(name=f'{int(lower_bound)}~'
            f'{int(upper_bound - 1) if i != len(self.grades) - 2 else self.upper_bound}'))

        # 更新每个节点的对应等级
        for item in self.root.nodes:
            item.category = self.root.categories[get_index_in_grades(item.value)].name

    # 导出为ECharts支持的json格式
    def export_to_json(self, export_path: str, json_txt_encoding='utf-8'):
        json_util.model_to_json_file(export_path=export_path,
                                     json_txt_encoding=json_txt_encoding,
                                     src_object=self.root)

    # 计算网络的属性
    # 可选择是否打印网络属性或导出json格式的直方图
    def get_network_attributes(self,
                               diameter: bool = True,
                               degree_distribution: bool = True,
                               clustering: bool = True,
                               assortativity: bool = True,
                               need_print: bool = False,
                               need_export: bool = False,
                               export_patah: str = '') -> graph_attribute.GraphAttribute:
        res = graph_attribute.GraphAttribute(diameter=None, degree_distribution=None, clustering=None,
                                             is_assortative=None, assortativity_cofficient=None)
        if diameter:
            dia = ac.diameter(self.graph)
            res.diameter = dia
            if need_print:
                print(f'网络直径:{dia}')

        if degree_distribution:
            de_dis = ac.degree_distribution(self.graph)
            res.degree_distribution = de_dis
            if need_print:
                print(f'度分布的结果为:')
                for degree, cnt in enumerate(de_dis):
                    if cnt == 0:
                        continue
                    print(f'度为  {degree}    的结点数量有  {cnt}   个')

        if clustering:
            clu = ac.clustering(self.graph)
            res.clustering = clu
            if need_print:
                print('群聚系数为:')
                for key in clu:
                    print(f'{key}   <-->    {clu[key]}')

        if assortativity:
            assor = ac.is_assortativity(self.graph)
            res.is_assortative, res.assortativity_cofficient = assor[0], assor[1]
            if need_print:
                print('是否为同配网络:', '是' if assor[0] else '不是')
                print(f'其中同配系数为: {assor[1]}')

        if need_export:
            json_util.model_to_json_file(export_path=export_patah, src_object=res)

        return res


'''
运行main.py，将合并化后的结构导出为ECharts支持的json格式，存放在./export/out.json中
'''
if __name__ == '__main__':
    my_router = Router(category_cnt=5)
    # my_router._get_all_edges_from_single_combine_txt(txt_path=os.path.join('combine', 'out.txt'),
    #                                                  txt_encoding='gbk')
    # 自己的
    my_router.get_all_edges_from_combine_txts(base_dir=os.path.join('combine'),
                                              txt_encoding='gbk')
    # 其他人的
    my_router.get_all_edges_from_combine_txts(base_dir=os.path.join('combine', 'others', 'export'),
                                              txt_encoding='gbk')
    my_router.export_to_json(export_path=os.path.join('export', 'topology.json'),
                             json_txt_encoding='utf-8')

    my_router.get_network_attributes(need_print=True, need_export=True,
                                     export_patah=os.path.join('export', 'network_struct.json'))
