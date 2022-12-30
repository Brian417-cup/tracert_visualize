import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


# 邻接矩阵画图
def simple_use():
    G = nx.Graph()
    # 创建邻接矩阵画图
    Matrix = np.array(
        [
            [0, 0, 1, 1, 1, 1],  # a
            [0, 0, 1, 1, 0, 1],  # b
            [1, 1, 0, 0, 1, 1],  # c
            [1, 1, 0, 0, 1, 1],  # d
            [1, 0, 1, 1, 0, 1],  # e
            [1, 1, 1, 1, 1, 0],
        ])

    for i in range(len(Matrix)):
        for j in range(len(Matrix)):
            if Matrix[i, j] != 0:
                G.add_edge(i, j)

    pos = nx.random_layout(G)
    nx.draw(G, pos, node_size=50, node_color='black', edge_color='b', width=2)
    plt.show()


# 邻接矩阵画图，并加上flag
def simple_use_with_flag():
    G = nx.Graph()
    Matrix = np.array(
        [
            [0, 0, 1, 1, 1, 1],  # a
            [0, 0, 1, 1, 0, 1],  # b
            [1, 1, 0, 0, 1, 1],  # c
            [1, 1, 0, 0, 1, 1],  # d
            [1, 0, 1, 1, 0, 1],  # e
            [1, 1, 1, 1, 1, 0],
        ])

    for i in range(len(Matrix)):
        for j in range(len(Matrix)):
            if Matrix[i, j] != 0:
                G.add_edge(i, j)

    pos = nx.random_layout(G)
    nx.draw_networkx_nodes(G, pos, node_shape='*', node_size=500, node_color='orange')  # 1800,100
    nx.draw_networkx_edges(G, pos, edge_color='b', width=2, style='dashed')  # solid|dashed|dotted, dashdot
    plt.show()


# 手动添加有权重边的方式画图
def simple_use_with_number_and_weight():
    G = nx.Graph()
    # 权值边设定
    G.add_edge(5, 1, weight=1)

    G.add_edge(5, 3, weight=2)
    G.add_edge(1, 2, weight=3)
    G.add_edge(1, 3, weight=4)
    G.add_edge(3, 2, weight=5)
    G.add_edge(3, 4, weight=6)
    G.add_edge(2, 4, weight=7)
    G.add_edge(2, 6, weight=8)
    G.add_edge(4, 6, weight=9)

    data = {(u, v): weight['weight'] for (u, v, weight) in G.edges(data=True)}
    pos = {1: [0, 0],
           2: [5, 0],
           3: [0, -5],
           4: [5, -5],
           5: [-2.5, -2.5],
           6: [7.5, -2.5],
           }

    # 对节点的颜色进行标注
    color_map = ["#ffc20e"]  # 5
    color_map.extend(["#ffc20e"])  # 1
    color_map.extend(["#7bbfea"])  # 3
    color_map.extend(["#7bbfea"])  # 2
    color_map.extend(["#7fbfea"])  # 4
    color_map.extend(["#7fbfea"])  # 6

    # 对链路的颜色进行标注
    edge_map = ["#ffc20e"]
    edge_map.extend(['black'] * 8)

    nx.draw_networkx_nodes(G, pos, node_size=500, node_color=color_map)  # 1800,100
    nx.draw_networkx_edges(G, pos, width=3, edge_color=edge_map)  # 1,5
    nx.draw_networkx_labels(G, pos, font_size=20)  # 40
    nx.draw_networkx_edge_labels(G, pos, data, font_size=20)  # 30
    plt.show()


if __name__ == '__main__':
    # simple_use()
    # simple_use_with_flag()
    simple_use_with_number_and_weight()
