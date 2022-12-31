import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from file_op import ip_utils


class Router:
    def __init__(self):
        self.graph = nx.Graph()

    # 每个文件操作
    def _tracert_per_file(slef, base_dir: str, encoding: str):
        # 用键值对维护最终的每个路径
        result = dict()

        for item in glob.glob(os.path.join(base_dir, '*.txt')):
            cur_routes = []
            # print(item)
            with open(item, mode='r', encoding=encoding) as f:
                data = f.readlines()
                # print(data)
                s, e = slef._find_start_and_end_in_tracert(data)
                print(f'{s}  {e}')
                data = data[s:e + 1]
                # 每行判断
                for sentence in data:
                    # 每行中以空格隔断，提取其中的ipv4地址
                    small_patterns = sentence.split(' ')
                    for ip_candidate in small_patterns:
                        # 因为tracert的时候规定了只有ipv4地址，因此这里只需要判断ipv4
                        if ip_utils.is_ipv4(ip_candidate) and cur_routes.count(ip_candidate) == 0:
                            cur_routes.append(ip_candidate)
                            break

                result[os.path.basename(item)] = cur_routes

        # print(result)
        return result

    # 找到开始记录的第一个路由下标
    def _find_start_and_end_in_tracert(self, data: list):
        sr = '通过最多 30 个跃点跟踪\n'
        er = '跟踪完成。\n'

        s, e = data.index(sr) + 3, data.index(er) - 2
        return s, e

    # 从固定文件夹下的所有保存有tracert结果的txt中抽取出路径
    def get_all_routes_from_txts(self, base_dir: str, txt_encoding: str):
        results = self._tracert_per_file(base_dir=base_dir, encoding=txt_encoding)
        print(results)
        for key in results:
            values = results[key]
            for i in range(len(values) - 1):
                self.graph.add_edge(values[i], values[i + 1])


if __name__ == '__main__':
    my_router = Router()
    my_router.get_all_routes_from_txts(
        base_dir=os.path.join('tracert', 'tracert_out_txts'),
        txt_encoding='gbk')
