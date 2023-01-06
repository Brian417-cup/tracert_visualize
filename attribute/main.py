import networkx as nx
from attribute import attribute_caculate as ac
import numpy as np

if __name__ == '__main__':
    G = nx.DiGraph()
    Matrix = np.array(
        [
            [0, 0, 1, 1, 1, 1],  # a
            [0, 0, 1, 1, 0, 1],  # b
            [1, 1, 0, 0, 1, 1],  # c
            [1, 1, 0, 0, 1, 1],  # d
            [1, 0, 1, 1, 0, 1],  # e
            [1, 0, 1, 1, 1, 0],
        ])

    for i in range(len(Matrix)):
        for j in range(len(Matrix)):
            if Matrix[i, j] != 0:
                G.add_edge(i, j)

    # 网络直径
    print(f'网络直径:{ac.diameter(G)}')

    # 度分布
    dl = ac.degree_distribution(G)
    print(f'度分布:{ac.degree_distribution(G)}')

    # 如果是有向图，应该这样绘制
    print(G.in_degree)
    print(G.out_degree)

    # 群聚系数
    m = ac.clustering(G)
    print('群聚系数为:')
    for key in m:
        print(f'{key}<-->{m[key]}')

    # 是否为同配网络
    r = ac.is_assortativity(G)
    print('是否为同配网络:', '是' if r[0] else '不是')
    print(f'其中同配系数为: {r[1]}')
