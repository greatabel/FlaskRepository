# coding:utf-8
import matplotlib.pyplot as plt
import networkx as nx
import numpy
import numpy as np

file_path = "data/relation_data.csv"
with open(file_path, "r") as f:
    rt_time = []
    for line in f:
        time = line.strip().split(",")[-1]
        # print time
        day = time[1:5] + time[6:8] + time[9:11]
        # print day

        # hms= time[9:17].replace(':', '')
        hm = time[12:17].replace(":", "")
        time = int(day + hm)

        rt_time.append(time)
# 计算转发时间的先后顺序
array = numpy.array(rt_time)
order = array.argsort()
ranks = order.argsort()

G = nx.Graph()
with open(file_path, "r") as f:
    for position, line in enumerate(f):
        uid, rtuid = line.strip().split(",")[:-1]
        G.add_edge(uid, rtuid, time=ranks[position])
edges, colors = zip(*nx.get_edge_attributes(G, "time").items())

print("-" * 10)
# degree=G.degree()#计算节点的出度
# degree=G.degree()#计算节点的出度
degree = G.degree(G)
closenesss = nx.closeness_centrality(G)
betweenness = nx.betweenness_centrality(G)

print(G.number_of_edges())  # 1547
# print g.diameter(G) # 2
path_length = nx.all_pairs_shortest_path_length(G)
pos = nx.spring_layout(G)  # 设置网络的布局
# fig = plt.figure(figsize=(80, 60),facecolor='white')
# pos=nx.spring_layout(G) #设置网络的布局


de = dict(G.degree)
de2 = [de[v] for v in de.keys()]
# print("de2",de2)
nx.draw_networkx(
    G,
    pos,
    node_size=de2,
    with_labels=False,
    node_color="red",
    linewidths=None,
    width=1.0,
    edge_color="blue",
)

plt.savefig("bot.png")
plt.show()
