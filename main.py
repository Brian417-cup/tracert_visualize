import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from file_op import ip_utils


class Router:
    def __init__(self):
        self.graph = nx.Graph()

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
            data=f.readlines()

            for i,item in enumerate(data):
                # 以\n结束
                if item=='\n':
                    break
                # 为tracert网站行
                if i%2==0:
                    continue
                # 为ip路径行
                ip_list=item.split(sep)
                for j in range(len(ip_list)-1):
                    self.graph.add_edge(ip_list[j],ip_list[j+1])


if __name__ == '__main__':
    my_router = Router()
    my_router.get_all_edges_from_combine_txt(txt_path=os.path.join('file_op','out.txt'),
                                             txt_encoding='gbk')
