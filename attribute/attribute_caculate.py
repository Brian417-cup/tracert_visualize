import networkx as nx


# 计算网络直径
def diameter(G: nx.Graph):
    return nx.diameter(G)

# 计算网络的群聚系数
def clustering(G:nx.Graph):
    return nx.clustering(G)

# 计算网络的度分布
def degree_distribution(G: nx.Graph):
    return nx.degree_histogram(G)


# 计算网络的同配性或异配性
def is_assortativity(G: nx.Graph):
    r = nx.degree_assortativity_coefficient(G)
    return True if r > 0 else False, r
