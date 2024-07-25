import time

import pandas as pd
from community import community_louvain
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx

# load the karate club graph
# G = nx.florentine_families_graph()
G = nx.Graph()
for index, row in pd.read_csv("data/user_pair.csv").iterrows():
    G.add_edge(row['user_id'], row['to_user_id'])
    if index % 100 == 0:
        print(index)
    if index > 200:
        break


print("数据准备结束")

# compute the best partition
partition = community_louvain.best_partition(G)

# draw the graph
pos = nx.spring_layout(G)
# color the nodes according to their partition
cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40,
                       cmap=cmap, node_color=list(partition.values()))
nx.draw_networkx_edges(G, pos, alpha=0.5)
plt.show()