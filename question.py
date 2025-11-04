import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['axes.unicode_minus'] = False

G = nx.les_miserables_graph()

print(f"网络已构建 (悲惨世界):")
print(f" - 节点 (角色) 数量: {G.number_of_nodes()}")
print(f" - 边 (共同出现) 数量: {G.number_of_edges()}")

# 计算中心性
c_degree = dict(G.degree(weight='weight'))
c_betweenness = nx.betweenness_centrality(G, weight='weight', normalized=True, k=77, seed=42)
c_closeness = nx.closeness_centrality(G, distance='weight')  # 距离 = 1/权重
c_eigenvector = nx.eigenvector_centrality(G, weight='weight', max_iter=1000)

# louvain社区检测
try:
    communities = list(nx.community.louvain_communities(G, weight='weight', seed=42))
except ImportError:
    from networkx.algorithms.community import louvain_communities

    communities = list(louvain_communities(G, weight='weight', seed=42))
community_map = {}
for i, comm in enumerate(communities):
    for node in comm:
        community_map[node] = i

print(f"Louvain 算法检测到 {len(communities)} 个主要社区。")

df = pd.DataFrame(index=G.nodes())
df['Community'] = df.index.map(community_map)
df['Degree (Weighted)'] = df.index.map(c_degree)
df['Betweenness'] = df.index.map(c_betweenness)
df['Closeness'] = df.index.map(c_closeness)
df['Eigenvector'] = df.index.map(c_eigenvector)
df_sorted = df.sort_values(by='Degree (Weighted)', ascending=False)
print(df_sorted.head(15).to_string(float_format="%.4f"))


plt.figure(figsize=(15, 10), facecolor='white')
pos = nx.spring_layout(G, k=0.3, iterations=50, seed=42, weight='weight')
cmap = plt.get_cmap('tab20')  # 'tab20' 适合多社区
node_colors = [cmap(community_map[node]) for node in G.nodes()]
max_degree = max(c_degree.values())
min_degree = min(c_degree.values())
node_sizes = [((c_degree[node] - min_degree) / (max_degree - min_degree)) * 3000 + 50
              for node in G.nodes()]
nx.draw_networkx(
    G,
    pos,
    with_labels=False,
    node_color=node_colors,
    node_size=node_sizes,
    edge_color='#AAAAAA',
    width=0.2,
    alpha=0.8
)

plt.title('Les Misérables Character Network (Size=Weighted Degree, Color=Community)',
          fontsize=18, fontweight='bold')
plt.axis('off')
output_filename = 'SNA_Exercise_LesMiserables.pdf'
plt.savefig(output_filename, format='pdf', bbox_inches='tight', dpi=300)
plt.show()
