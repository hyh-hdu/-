import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from networkx.algorithms.community import modularity
from sklearn.metrics.cluster import adjusted_rand_score

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['axes.unicode_minus'] = False

G = nx.karate_club_graph()

print(f"节点数量: {G.number_of_nodes()}")
print(f"边数量: {G.number_of_edges()}")

print("\n网络指标")
density = nx.density(G)
avg_clustering = nx.average_clustering(G)
print(f"网络密度: {density:.4f}")
print(f"平均聚类系数: {avg_clustering:.4f}")

centrality_degree = nx.degree_centrality(G)
centrality_betweenness = nx.betweenness_centrality(G, normalized=True)
centrality_closeness = nx.closeness_centrality(G)
centrality_eigenvector = nx.eigenvector_centrality(G, max_iter=1000)
structural_constraint = nx.constraint(G)

df_analysis = pd.DataFrame({
    'Degree': centrality_degree,
    'Betweenness': centrality_betweenness,
    'Closeness': centrality_closeness,
    'Eigenvector': centrality_eigenvector,
    'Constraint': structural_constraint,
})
df_analysis = df_analysis.sort_values(by='Betweenness', ascending=False)

print("\n节点中心性计算")
print(df_analysis.to_string(float_format="%.4f"))

print("\n社区检测")
try:
    from networkx.algorithms.community import louvain_communities
    communities_detected_sets = list(louvain_communities(G, seed=42))
except ImportError:
    communities_detected_sets = list(nx.community.louvain_communities(G, seed=42))

print(f"算法自动识别出 {len(communities_detected_sets)} 个 主要社区。")

modularity_score = modularity(G, communities_detected_sets)
print(f"模块度 (Modularity): {modularity_score:.4f}")

ground_truth_labels = [G.nodes[n]['club'] for n in G.nodes()]
detected_labels_dict = {}
for i, community_set in enumerate(communities_detected_sets):
    for node in community_set:
        detected_labels_dict[node] = i
detected_labels = [detected_labels_dict[n] for n in G.nodes()]

ari_score = adjusted_rand_score(ground_truth_labels, detected_labels)
print(f"调整兰德指数 (ARI Score): {ari_score:.4f}")


plt.figure(figsize=(20, 9), facecolor='white')
pos = nx.spring_layout(G, k=0.6, iterations=50, seed=42)
ColorHi = '#377EB8'
ColorJohn = '#FF9933'

ax1 = plt.subplot(1, 2, 1)
truth_colors = [ColorHi if G.nodes[n]['club'] == 'Mr. Hi' else ColorJohn for n in G.nodes()]
nx.draw_networkx(
    G, pos,
    with_labels=True,
    node_color=truth_colors,
    node_size=800,
    font_color='black',
    edge_color='#AAAAAA',
    width=0.5,
    ax=ax1
)
ax1.set_title('Ground Truth: The Actual Split (2 Factions)', fontsize=16, fontweight='bold')
plt.text(pos[0][0], pos[0][1] + 0.08, 'Mr. Hi (Node 0)', ha='center', color='black', fontweight='bold', fontsize=11)
plt.text(pos[33][0], pos[33][1] + 0.08, 'John A. (Node 33)', ha='center', color='black', fontweight='bold', fontsize=11)
ax1.axis('off')

ax2 = plt.subplot(1, 2, 2)
color_map_list = ['#377EB8', '#FF9933', '#4DAF4A', '#E41A1C']
detected_node_colors = [color_map_list[detected_labels_dict[node] % len(color_map_list)] for node in G.nodes()]
nx.draw_networkx(
    G, pos,
    with_labels=True,
    node_color=detected_node_colors,
    node_size=800,
    font_color='black',
    edge_color='#AAAAAA',
    width=0.5,
    ax=ax2
)
ax2.set_title(f'Algorithm: Louvain Dectection ({len(communities_detected_sets)} Factions)', fontsize=16,
              fontweight='bold')
ax2.axis('off')

output_filename_1 = 'SNA_Example_Karate_Club_Comparison.pdf'
plt.savefig(output_filename_1, format='pdf', bbox_inches='tight', dpi=300)
plt.show()


plt.figure(figsize=(15, 12), facecolor='white')

plot_info = [
    ('Degree Centrality (Activity)', centrality_degree, 'Reds'),
    ('Betweenness Centrality (Brokerage)', centrality_betweenness, 'Greens'),
    ('Closeness Centrality (Efficiency)', centrality_closeness, 'Blues'),
    ('Eigenvector Centrality (Influence)', centrality_eigenvector, 'Purples')
]

def normalize_values(scores_dict):
    scores = list(scores_dict.values())
    min_val, max_val = min(scores), max(scores)
    if max_val == min_val: return [1.0] * len(scores)
    return [(score - min_val) / (max_val - min_val) for score in scores]


for i, (title, data_dict, cmap_name) in enumerate(plot_info):
    ax = plt.subplot(2, 2, i + 1)
    norm_scores = normalize_values(data_dict)
    node_size = [score * 1800 + 200 for score in norm_scores]
    node_color = [plt.get_cmap(cmap_name)(score) for score in norm_scores]

    nx.draw_networkx(G, pos, ax=ax, with_labels=True,
                     node_color=node_color,
                     node_size=node_size,
                     edge_color='#AAAAAA',
                     font_color='black',
                     font_size=8)

    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.axis('off')

output_filename_2 = 'SNA_Example_Karate_Club_Centralities.pdf'
plt.tight_layout()
plt.savefig(output_filename_2, format='pdf', bbox_inches='tight', dpi=300)
plt.show()